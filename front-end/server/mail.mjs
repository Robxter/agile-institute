// Envío de correo con Resend (API REST, sin SDK) para el BFF de Agile Institute.
//
//   RESEND_API_KEY  clave de Resend (secreto: solo en .env local o en Render)
//   MAIL_FROM       remitente de un dominio verificado en Resend, p. ej. "Agile Institute™ <hola@agileinstitute.es>"
//   MAIL_TEAM_TO    destinatarios internos separados por comas (avisos de nuevas solicitudes de piloto)
//
// Sin RESEND_API_KEY o MAIL_FROM no se envía nada (desarrollo/pruebas): se registra y se devuelve { skipped: true }.
// Un fallo de correo nunca rompe la petición: la solicitud ya está guardada antes de enviar.

const RESEND_URL = 'https://api.resend.com/emails';

export const escapeHtml = (s) =>
  String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

/** Envía un correo. `idempotencyKey` evita duplicados si se reintenta la misma operación. */
export async function sendEmail({ to, subject, html, text, replyTo, idempotencyKey }) {
  const key = process.env.RESEND_API_KEY;
  const from = process.env.MAIL_FROM;
  const recipients = (Array.isArray(to) ? to : [to]).filter(Boolean);
  if (!key || !from || recipients.length === 0) {
    const why = !key ? 'sin RESEND_API_KEY' : !from ? 'sin MAIL_FROM' : 'sin destinatarios';
    console.log(`[mail] omitido (${why}): ${subject}`);
    return { skipped: true };
  }
  const res = await fetch(RESEND_URL, {
    method: 'POST',
    headers: {
      authorization: `Bearer ${key}`,
      'content-type': 'application/json',
      ...(idempotencyKey ? { 'idempotency-key': idempotencyKey } : {}),
    },
    body: JSON.stringify({ from, to: recipients, subject, html, text, ...(replyTo ? { reply_to: replyTo } : {}) }),
    signal: AbortSignal.timeout(8000),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`Resend ${res.status}: ${body?.message ?? 'error'}`);
  return { id: body.id };
}

const teamList = () =>
  (process.env.MAIL_TEAM_TO ?? '')
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);

/** Correos de una solicitud de piloto: aviso al equipo y acuse al solicitante. Nunca lanza. */
export async function notifyPilotRequest(record) {
  const rows = [
    ['Nombre', record.name],
    ['Correo', record.email],
    ['Organización', record.organization],
    ['Tamaño', record.size || '—'],
    ['Mensaje', record.message || '—'],
    ['Recibida', record.receivedAt],
    ['ID', record.id],
  ];
  const name = escapeHtml(record.name);
  const org = escapeHtml(record.organization);
  const results = await Promise.allSettled([
    sendEmail({
      to: teamList(),
      subject: `Nueva solicitud de piloto · ${record.organization}`,
      replyTo: record.email,
      idempotencyKey: `pilot-team-${record.id}`,
      html: `<h2>Nueva solicitud de piloto</h2><table>${rows
        .map(([k, v]) => `<tr><th align="left">${k}</th><td>${escapeHtml(v)}</td></tr>`)
        .join('')}</table>`,
      text: rows.map(([k, v]) => `${k}: ${v}`).join('\n'),
    }),
    sendEmail({
      to: record.email,
      subject: 'Hemos recibido tu solicitud de piloto · Agile Institute™',
      replyTo: teamList()[0],
      idempotencyKey: `pilot-ack-${record.id}`,
      html: `<p>Hola ${name},</p><p>Gracias por tu interés en el piloto de Agile Institute™ para ${org}. Te contactaremos en breve.</p><p>— Equipo Agile Institute™</p>`,
      text: `Hola ${record.name},\n\nGracias por tu interés en el piloto de Agile Institute™ para ${record.organization}. Te contactaremos en breve.\n\n— Equipo Agile Institute™`,
    }),
  ]);
  for (const r of results) if (r.status === 'rejected') console.error('[mail]', r.reason?.message ?? r.reason);
  return results;
}
