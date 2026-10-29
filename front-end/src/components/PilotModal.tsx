import { useEffect, useRef, useState, type FormEvent } from 'react';
import { ApiError, submitPilotRequest, type FieldErrors, type PilotRequest } from '../api/client';
import { organizationSizes } from '../content/landing';
import { Button } from './Button';
import { Icon } from './Icon';
import styles from './PilotModal.module.css';

const EMPTY: PilotRequest = { name: '', email: '', organization: '', size: '', message: '', consent: false, website: '' };

type Status = 'idle' | 'sending' | 'sent' | 'error';

export function PilotModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const [form, setForm] = useState<PilotRequest>(EMPTY);
  const [errors, setErrors] = useState<FieldErrors>({});
  const [status, setStatus] = useState<Status>('idle');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open && !dialog.open) {
      // jsdom y navegadores antiguos no implementan showModal
      if (typeof dialog.showModal === 'function') dialog.showModal();
      else dialog.setAttribute('open', '');
    } else if (!open && dialog.open) {
      if (typeof dialog.close === 'function') dialog.close();
      else dialog.removeAttribute('open');
    }
  }, [open]);

  useEffect(() => {
    if (open) return;
    // Reinicia el formulario al cerrar tras un envío correcto
    if (status === 'sent') {
      setForm(EMPTY);
      setStatus('idle');
    }
  }, [open, status]);

  const update = <K extends keyof PilotRequest>(key: K, value: PilotRequest[K]) => {
    setForm((f) => ({ ...f, [key]: value }));
    setErrors((e) => ({ ...e, [key]: undefined }));
  };

  const validate = (): FieldErrors => {
    const e: FieldErrors = {};
    if (form.name.trim().length < 2) e.name = 'Indica tu nombre.';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())) e.email = 'Introduce un correo válido.';
    if (form.organization.trim().length < 2) e.organization = 'Indica tu organización.';
    if (!form.consent) e.consent = 'Necesitamos tu consentimiento para contactarte.';
    return e;
  };

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    const local = validate();
    if (Object.keys(local).length) {
      setErrors(local);
      const first = Object.keys(local)[0];
      dialogRef.current?.querySelector<HTMLElement>(`[name="${first}"]`)?.focus();
      return;
    }
    setStatus('sending');
    setMessage('');
    try {
      await submitPilotRequest(form);
      setStatus('sent');
    } catch (err) {
      const apiErr = err instanceof ApiError ? err : new ApiError('Algo ha fallado. Inténtalo de nuevo.', 0);
      setErrors(apiErr.fields);
      setMessage(apiErr.message);
      setStatus('error');
    }
  }

  const field = (key: 'name' | 'email' | 'organization', label: string, type = 'text', autoComplete?: string) => (
    <div className={styles.field}>
      <label htmlFor={`pilot-${key}`}>{label}</label>
      <input
        id={`pilot-${key}`}
        name={key}
        type={type}
        autoComplete={autoComplete}
        value={form[key]}
        onChange={(e) => update(key, e.target.value)}
        aria-invalid={Boolean(errors[key])}
        aria-describedby={errors[key] ? `pilot-${key}-error` : undefined}
        required
      />
      {errors[key] && (
        <span id={`pilot-${key}-error`} className={styles.error}>
          {errors[key]}
        </span>
      )}
    </div>
  );

  return (
    <dialog
      ref={dialogRef}
      className={styles.dialog}
      aria-labelledby="pilot-title"
      onClose={onClose}
      onCancel={onClose}
      onClick={(e) => e.target === dialogRef.current && onClose()}
    >
      <div className={styles.inner}>
        <button type="button" className={styles.close} onClick={onClose}>
          <Icon name="close" size={22} />
          <span className="visually-hidden">Cerrar</span>
        </button>

        {status === 'sent' ? (
          <div className={styles.success} role="status">
            <span className={styles.successIcon}>
              <Icon name="check" size={30} />
            </span>
            <h2 id="pilot-title">¡Gracias! Hemos recibido tu solicitud</h2>
            <p>Nuestro equipo te escribirá en los próximos días para preparar el piloto con tu organización.</p>
            <Button onClick={onClose}>Cerrar</Button>
          </div>
        ) : (
          <form onSubmit={onSubmit} noValidate>
            <h2 id="pilot-title" className={styles.title}>
              Hablemos de un piloto
            </h2>
            <p className={styles.intro}>
              Cuéntanos sobre tu organización y te proponemos cómo medir competencias, experiencia y uso de la IA con tus equipos.
            </p>

            <div className={styles.grid}>
              {field('name', 'Nombre', 'text', 'name')}
              {field('email', 'Correo de trabajo', 'email', 'email')}
              {field('organization', 'Organización', 'text', 'organization')}
              <div className={styles.field}>
                <label htmlFor="pilot-size">Tamaño</label>
                <select id="pilot-size" name="size" value={form.size} onChange={(e) => update('size', e.target.value)}>
                  <option value="">Selecciona…</option>
                  {organizationSizes.map((s) => (
                    <option key={s.value} value={s.value}>
                      {s.label}
                    </option>
                  ))}
                </select>
              </div>
              <div className={`${styles.field} ${styles.full}`}>
                <label htmlFor="pilot-message">¿Qué te gustaría conseguir? (opcional)</label>
                <textarea
                  id="pilot-message"
                  name="message"
                  rows={3}
                  maxLength={1000}
                  value={form.message}
                  onChange={(e) => update('message', e.target.value)}
                />
              </div>
            </div>

            {/* Campo trampa: oculto para personas */}
            <input
              className={styles.honeypot}
              type="text"
              name="website"
              tabIndex={-1}
              autoComplete="off"
              aria-hidden="true"
              value={form.website}
              onChange={(e) => update('website', e.target.value)}
            />

            <label className={styles.consent}>
              <input
                type="checkbox"
                name="consent"
                checked={form.consent}
                onChange={(e) => update('consent', e.target.checked)}
                aria-invalid={Boolean(errors.consent)}
              />
              <span>Acepto que Agile Institute use estos datos solo para contactarme sobre el piloto.</span>
            </label>
            {errors.consent && <span className={styles.error}>{errors.consent}</span>}

            {status === 'error' && message && (
              <p className={styles.formError} role="alert">
                {message}
              </p>
            )}

            <div className={styles.actions}>
              <Button type="submit" arrow disabled={status === 'sending'}>
                {status === 'sending' ? 'Enviando…' : 'Enviar solicitud'}
              </Button>
            </div>
          </form>
        )}
      </div>
    </dialog>
  );
}
