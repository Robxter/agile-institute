import type { CSSProperties } from 'react';
import { APP_URL } from '../api/client';
import { views } from '../content/landing';
import styles from './Roles.module.css';

/** Una vista del centro de mando por cada dimensión competencial. */
export function Roles() {
  return (
    <section id="vistas" className={`container ${styles.section}`} aria-labelledby="vistas-title">
      <h2 id="vistas-title" className={styles.title}>
        {views.title}
      </h2>
      <ul className={styles.grid}>
        {views.items.map((view, i) => (
          <li key={view.key} data-reveal style={{ '--reveal-i': i } as CSSProperties}>
            <a href={`${APP_URL}#/${view.key}`} className={styles.card}>
              <h3>{view.title}</h3>
              <p>{view.body}</p>
            </a>
          </li>
        ))}
      </ul>
      <h3 className="visually-hidden">Indicadores del modelo</h3>
      <ul className={styles.chips}>
        {views.indicators.map((tag) => (
          <li key={tag}>{tag}</li>
        ))}
      </ul>
    </section>
  );
}
