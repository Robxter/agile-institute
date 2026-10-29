// @vitest-environment node
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

  it('responde 502 si el centro de mando no está disponible', async () => {
    const res = await fetch(`${base}/api/auth/me`);
    expect(res.status).toBe(502);
  });
});
