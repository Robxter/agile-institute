import { assessment } from '../content/landing';
import styles from './Assessment.module.css';

export function Assessment() {
  return (
    <section id="que-evaluamos" className="container" aria-labelledby="assessment-title">
      <div className={styles.band} data-reveal>
        <h2 id="assessment-title" className={styles.title}>
          {assessment.title}
        </h2>
        <ul className={styles.items}>
          {assessment.items.map((item) => (
            <li key={item.title} className={styles.item}>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
