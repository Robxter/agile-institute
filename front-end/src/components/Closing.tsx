import { footer, hero, pilotNotice } from '../content/landing';
import { Button } from './Button';
import { Icon } from './Icon';
import styles from './Closing.module.css';

/** Aviso de fase piloto, llamada final a la acción y pie de página. */
export function Closing({ onCta }: { onCta: () => void }) {
  return (
    <>
      <section className={`container ${styles.noticeWrap}`} aria-label="Aviso">
        <p className={styles.notice} role="note">
          <Icon name="info" size={22} className={styles.icon} />
          <span>
            <strong>{pilotNotice.title}</strong> {pilotNotice.body}
          </span>
        </p>
      </section>

      <section className={`container ${styles.cta}`} aria-label="Contacto">
        <Button size="lg" arrow onClick={onCta}>
          {hero.cta}
        </Button>
      </section>

      <footer className={`container ${styles.footer}`}>
        <p>
          {footer} · {new Date().getFullYear()}
        </p>
      </footer>
    </>
  );
}
