// BFF (backend-for-frontend) sin dependencias para la landing de Agile Institute.
//
//  - POST /api/pilot-requests  → valida y guarda solicitudes de piloto (data/pilot-requests.jsonl)
//  - GET  /api/health          → estado del BFF y del centro de mando
//  - /api/*                    → se delega en el centro de mando FastAPI (CDM_API_URL)
//  - /app y /static/*          → interfaz del centro de mando (/ y /static/* de FastAPI), en el mismo origen
//                                que la landing para que su cookie de sesión (SameSite=strict) funcione
//  - resto                     → sirve dist/ (SPA) en producción
import { createServer } from 'node:http';
import { readFile, appendFile, mkdir, stat } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';
import { dirname, extname, join, normalize, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const DIST = join(ROOT, 'dist');
const DATA_DIR = join(ROOT, 'data');
const PORT = Number(process.env.BFF_PORT ?? 5174);
// Se lee en cada petición para poder reconfigurarlo en pruebas.
const cdmUrl = () => (process.env.CDM_API_URL ?? 'http://127.0.0.1:8765').replace(/\/$/, '');
const MAX_BODY = 16 * 1024;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
  '.json': 'application/json',
  '.woff2': 'font/woff2',
  '.map': 'application/json',
};

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const SIZES = new Set(['<50', '50-250', '250-1000', '>1000']);

function sendJson(res, status, body) {
  res.writeHead(status, { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' });
  res.end(JSON.stringify(body));
}

async function readBody(req) {
  const chunks = [];
  let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > MAX_BODY) throw Object.assign(new Error('Cuerpo demasiado grande'), { status: 413 });
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}

export function validatePilotRequest(input) {
  const errors = {};
  const str = (v) => (typeof v === 'string' ? v.trim() : '');
  const data = {
    name: str(input?.name),
    email: str(input?.email).toLowerCase(),
    organization: str(input?.organization),
    size: str(input?.size),
    message: str(input?.message),
    consent: input?.consent === true,
  };
  if (data.name.length < 2) errors.name = 'Indica tu nombre.';
  if (!EMAIL_RE.test(data.email)) errors.email = 'Introduce un correo válido.';
  if (data.organization.length < 2) errors.organization = 'Indica tu organización.';
  if (data.size && !SIZES.has(data.size)) errors.size = 'Tamaño no válido.';
  if (data.message.length > 1000) errors.message = 'Máximo 1000 caracteres.';
  if (!data.consent) errors.consent = 'Necesitamos tu consentimiento para contactarte.';
  return { data, errors, ok: Object.keys(errors).length === 0 };
}

async function handlePilotRequest(req, res) {
  let payload;
  try {
    payload = JSON.parse((await readBody(req)).toString('utf8') || '{}');
  } catch (err) {
    return sendJson(res, err.status ?? 400, { error: 'JSON no válido' });
  }
  // Campo trampa anti-spam: los humanos no lo ven, los bots lo rellenan.
  if (payload?.website) return sendJson(res, 201, { id: randomUUID() });

  const { data, errors, ok } = validatePilotRequest(payload);
  if (!ok) return sendJson(res, 422, { error: 'Revisa los campos marcados', fields: errors });

  const record = { id: randomUUID(), receivedAt: new Date().toISOString(), ...data };
  await mkdir(DATA_DIR, { recursive: true });
  await appendFile(join(DATA_DIR, 'pilot-requests.jsonl'), JSON.stringify(record) + '\n', 'utf8');
  console.log(`[bff] solicitud de piloto ${record.id} · ${record.organization}`);
  return sendJson(res, 201, { id: record.id });
}

async function handleHealth(res) {
  let cdm = 'down';
  try {
    const r = await fetch(`${cdmUrl()}/api/auth/demo-accounts`, { signal: AbortSignal.timeout(1500) });
    cdm = r.ok ? 'up' : `http ${r.status}`;
  } catch {
    /* centro de mando no disponible */
  }
  sendJson(res, 200, { status: 'ok', cdm });
}

async function proxyToCdm(req, res, upstreamPath = req.url) {
  const headers = { ...req.headers };
  delete headers.host;
  delete headers.connection;
  try {
    const hasBody = !['GET', 'HEAD'].includes(req.method ?? 'GET');
    const upstream = await fetch(cdmUrl() + upstreamPath, {
      method: req.method,
      headers,
      body: hasBody ? await readBody(req) : undefined,
      redirect: 'manual',
    });
    const outHeaders = {};
    upstream.headers.forEach((value, key) => {
      if (!['content-encoding', 'content-length', 'transfer-encoding', 'connection'].includes(key)) outHeaders[key] = value;
    });
    const setCookie = upstream.headers.getSetCookie?.();
    if (setCookie?.length) outHeaders['set-cookie'] = setCookie;
    res.writeHead(upstream.status, outHeaders);
    res.end(Buffer.from(await upstream.arrayBuffer()));
  } catch {
    sendJson(res, 502, { error: 'El centro de mando no está disponible' });
  }
}

async function serveStatic(req, res) {
  const urlPath = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  const filePath = normalize(join(DIST, urlPath));
  if (!filePath.startsWith(DIST)) return sendJson(res, 403, { error: 'Prohibido' });

  let target = filePath;
  try {
    if (!(await stat(target)).isFile()) target = join(DIST, 'index.html');
  } catch {
    target = join(DIST, 'index.html');
  }
  try {
    const body = await readFile(target);
    const ext = extname(target);
    const immutable = target.includes(`${join('dist', 'assets')}`);
    res.writeHead(200, {
      'content-type': MIME[ext] ?? 'application/octet-stream',
      'cache-control': immutable ? 'public, max-age=31536000, immutable' : 'no-cache',
    });
    res.end(body);
  } catch {
    res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
    res.end('Compila primero la aplicación con "npm run build".');
  }
}

export const server = createServer(async (req, res) => {
  try {
    const { pathname: path, search } = new URL(req.url ?? '/', 'http://x');
    if (path === '/api/pilot-requests' && req.method === 'POST') return await handlePilotRequest(req, res);
    if (path === '/api/health') return await handleHealth(res);
    if (path.startsWith('/api/') || path.startsWith('/static/')) return await proxyToCdm(req, res);
    if (path === '/app' || path === '/app/') return await proxyToCdm(req, res, '/' + search);
    return await serveStatic(req, res);
  } catch (err) {
    console.error('[bff]', err);
    if (!res.headersSent) sendJson(res, 500, { error: 'Error interno' });
  }
});

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  server.listen(PORT, () => {
    console.log(`[bff] http://127.0.0.1:${PORT}  →  centro de mando ${cdmUrl()}`);
  });
}
