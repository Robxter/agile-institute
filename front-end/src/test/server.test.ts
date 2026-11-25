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

  it('guarda la solicitud y envía aviso al equipo y acuse al solicitante vía Resend', async () => {
    Object.assign(process.env, { RESEND_API_KEY: 're_test', MAIL_FROM: 'AI <hola@x.es>', MAIL_TEAM_TO: 'equipo@x.es' });
    const realFetch = globalThis.fetch;
    const sent: { headers: Record<string, string>; body: Record<string, unknown> }[] = [];
    const spy = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
      if (String(input) !== 'https://api.resend.com/emails') return realFetch(input, init);
      sent.push({ headers: init!.headers as Record<string, string>, body: JSON.parse(init!.body as string) });
      // El primer envío falla: la respuesta al usuario no debe verse afectada.
      return sent.length === 1 ? new Response('{"message":"boom"}', { status: 500 }) : new Response('{"id":"em_1"}');
    });
    try {
      const res = await fetch(`${base}/api/pilot-requests`, {
        method: 'POST',
        body: JSON.stringify({ name: 'Ana <b>', email: 'ana@empresa.es', organization: 'Empresa', consent: true }),
      });
      expect(res.status).toBe(201);
      await vi.waitFor(() => expect(sent).toHaveLength(2));
      const team = sent.find((s) => (s.body.to as string[])[0] === 'equipo@x.es')!;
      const ack = sent.find((s) => (s.body.to as string[])[0] === 'ana@empresa.es')!;
      expect(team.headers.authorization).toBe('Bearer re_test');
      expect(team.body).toMatchObject({ from: 'AI <hola@x.es>', reply_to: 'ana@empresa.es' });
      expect(team.body.html).toContain('Ana &lt;b&gt;');
      expect(team.body.html).not.toContain('<b>');
      expect(ack.headers['idempotency-key']).toMatch(/^pilot-ack-/);
    } finally {
      spy.mockRestore();
      for (const k of ['RESEND_API_KEY', 'MAIL_FROM', 'MAIL_TEAM_TO']) delete process.env[k];
    }
  });

  it('responde 502 si el centro de mando no está disponible', async () => {
    const res = await fetch(`${base}/api/auth/me`);
    expect(res.status).toBe(502);
  });
});
