import type { CSSProperties } from 'react';
import { dimensions } from '../content/landing';
import { DimensionIllustration } from './illustrations/Illustrations';
import styles from './Dimensions.module.css';

export function Dimensions() {
  return (
    <section className={`container ${styles.section}`} aria-labelledby="dimensions-title">
      <h2 id="dimensions-title" className="visually-hidden">
        Cinco dimensiones
      </h2>
      <ul className={styles.grid}>
        {dimensions.map((d, i) => (
          <li
            key={d.key}
            id={`dim-${d.key}`}
            tabIndex={-1}
            className={`${styles.card} ${d.key === 'ia' ? styles.ia : ''}`}
            data-reveal
            style={{ '--reveal-i': i } as CSSProperties}
          >
            <div className={styles.text}>
              <h3>{d.title}</h3>
              <p>{d.question}</p>
            </div>
            <div className={styles.art}>
              <DimensionIllustration dimension={d.key} />
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
