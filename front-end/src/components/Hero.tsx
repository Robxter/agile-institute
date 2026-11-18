import { APP_URL } from '../api/client';
import { dimensions, hero } from '../content/landing';
import { Button } from './Button';
import { Icon } from './Icon';
import { PresenterIllustration } from './illustrations/Illustrations';
import styles from './Hero.module.css';

export function Hero({ onCta }: { onCta: () => void }) {
  return (
    <section id="top" className={`container ${styles.hero}`} aria-labelledby="hero-title">
      <div className={styles.copy}>
        <h1 id="hero-title" className={styles.title}>
          Desarrolla las competencias para trabajar con <mark className={styles.underline}>agilidad</mark> y un uso{' '}
          <span className={styles.accent}>responsable de la&nbsp;IA</span>
        </h1>
        <p className={styles.lead}>{hero.lead}</p>
        <Button arrow onClick={onCta}>
          {hero.cta}
        </Button>
      </div>

      <aside className={styles.panel} aria-labelledby="panel-title">
        <h2 id="panel-title" className={styles.panelTitle}>
          {hero.dashboardTitle}
        </h2>
        <ul className={styles.list}>
          {dimensions.map((d) => (
            <li key={d.key}>
              <a href={`${APP_URL}#/${d.key}`} className={styles.item}>
                <Icon name={d.icon} size={20} />
                <span>{d.title}</span>
                <Icon name="chevron" size={16} className={styles.chevron} />
              </a>
            </li>
          ))}
        </ul>
        <div className={styles.panelFoot}>
          <p className={styles.note}>{hero.dashboardNote}</p>
          <div className={styles.presenter}>
            <PresenterIllustration />
          </div>
        </div>
      </aside>
    </section>
  );
}
