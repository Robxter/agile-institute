import type { CSSProperties } from 'react';
import { roles } from '../content/landing';
import styles from './Roles.module.css';

export function Roles() {
  return (
    <section id="roles" className={`container ${styles.section}`} aria-labelledby="roles-title">
      <h2 id="roles-title" className={styles.title}>
        {roles.title}
      </h2>
      <ul className={styles.grid}>
        {roles.items.map((role, i) => (
          <li key={role.title} className={styles.card} data-reveal style={{ '--reveal-i': i } as CSSProperties}>
            <h3>{role.title}</h3>
            <p>{role.body}</p>
          </li>
        ))}
      </ul>
      <h3 className="visually-hidden">Indicadores del modelo</h3>
      <ul className={styles.chips}>
        {roles.indicators.map((tag) => (
          <li key={tag}>{tag}</li>
        ))}
      </ul>
    </section>
  );
}
