// @vitest-environment node
import { createServer } from 'node:http';
import type { AddressInfo } from 'node:net';
// @ts-expect-error módulo JS sin tipos
import { server, validatePilotRequest } from '../../server/index.mjs';

describe('BFF', () => {
  let base = '';

  beforeAll(async () => {
    process.env.CDM_API_URL = 'http://127.0.0.1:9';
    await new Promise<void>((r) => server.listen(0, '127.0.0.1', r));
    base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  });
  afterAll(() => new Promise<void>((r) => server.close(() => r())));

  it('valida los campos obligatorios', () => {
    const { ok, errors } = validatePilotRequest({ name: 'A', email: 'x', organization: '', consent: false });
    expect(ok).toBe(false);
    expect(Object.keys(errors).sort()).toEqual(['consent', 'email', 'name', 'organization']);
  });

  it('rechaza solicitudes inválidas con 422', async () => {
    const res = await fetch(`${base}/api/pilot-requests`, { method: 'POST', body: '{"name":"x"}' });
    expect(res.status).toBe(422);
    expect((await res.json()).fields.email).toBeDefined();
  });

  it('sirve el centro de mando en /app y reenvía /static y su cookie de sesión', async () => {
    const seen: string[] = [];
    const upstream = createServer((req, res) => {
      seen.push(req.url ?? '');
      res.writeHead(200, { 'content-type': 'text/html', 'set-cookie': 'cdm_session=t; HttpOnly; SameSite=strict; Path=/' });
      res.end('ok');
    });
    await new Promise<void>((r) => upstream.listen(0, '127.0.0.1', r));
    const previous = process.env.CDM_API_URL;
    // Forma "host:puerto" sin esquema, como la entrega render.yaml (fromService … hostport).
    process.env.CDM_API_URL = `127.0.0.1:${(upstream.address() as AddressInfo).port}`;
    try {
      const page = await fetch(`${base}/app`);
      expect(await page.text()).toBe('ok');
      expect(page.headers.get('set-cookie')).toContain('cdm_session=t');
      await fetch(`${base}/static/app.js`);
      expect(seen).toEqual(['/', '/static/app.js']);
    } finally {
      process.env.CDM_API_URL = previous;
      await new Promise<void>((r) => upstream.close(() => r()));
    }
  });

  it('responde 502 si el centro de mando no está disponible', async () => {
    const res = await fetch(`${base}/api/auth/me`);
    expect(res.status).toBe(502);
  });
});
