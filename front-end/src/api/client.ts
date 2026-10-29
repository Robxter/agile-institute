export interface PilotRequest {
  name: string;
  email: string;
  organization: string;
  size: string;
  message: string;
  consent: boolean;
  /** Campo trampa anti-spam; debe ir vacío. */
  website?: string;
}

export type FieldErrors = Partial<Record<keyof PilotRequest, string>>;

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly fields: FieldErrors = {},
  ) {
    super(message);
  }
}

/** URL del centro de mando (FastAPI) para "Acceder" y los accesos a cada cuadro. */
export const APP_URL: string = import.meta.env.VITE_APP_URL ?? '/';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(path, {
      ...init,
      headers: { 'content-type': 'application/json', ...init?.headers },
      credentials: 'same-origin',
    });
  } catch {
    throw new ApiError('No hemos podido conectar. Revisa tu conexión e inténtalo de nuevo.', 0);
  }
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new ApiError(body.error ?? 'Algo ha fallado. Inténtalo de nuevo.', res.status, body.fields);
  return body as T;
}

export function submitPilotRequest(data: PilotRequest) {
  return request<{ id: string }>('/api/pilot-requests', { method: 'POST', body: JSON.stringify(data) });
}
