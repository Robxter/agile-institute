import type { CSSProperties } from 'react';
import { process } from '../content/landing';
import styles from './Process.module.css';

export function Process() {
  return (
    <section id="como-funciona" className={`container ${styles.section}`} aria-labelledby="process-title">
      <h2 id="process-title" className={styles.title}>
        {process.title}
      </h2>
      <ol className={styles.steps}>
        {process.steps.map((step, i) => (
          <li key={step.title} className={styles.step} data-reveal style={{ '--reveal-i': i } as CSSProperties}>
            <span className={styles.num} aria-hidden="true">
              {i + 1}
            </span>
            <div>
              <h3>{step.title}</h3>
              <p>{step.body}</p>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
