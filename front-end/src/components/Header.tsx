import { useEffect, useState } from 'react';
import { APP_URL } from '../api/client';
import { nav } from '../content/landing';
import { Icon } from './Icon';
import { Logo } from './Logo';
import styles from './Header.module.css';

export function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(false);
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open]);

  return (
    <header className={`${styles.header} ${scrolled ? styles.scrolled : ''}`}>
      <div className={`container ${styles.bar}`}>
        <a href="#top" className={styles.brand} aria-label="Agile Institute, inicio">
          <Logo />
        </a>

        <nav id="main-nav" className={`${styles.nav} ${open ? styles.navOpen : ''}`} aria-label="Principal">
          <ul>
            {nav.map((item) => (
              <li key={item.href}>
                <a href={item.href} onClick={() => setOpen(false)}>
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
          <a className={`${styles.access} ${styles.accessMobile}`} href={APP_URL}>
            Acceder
          </a>
        </nav>

        <a className={styles.access} href={APP_URL}>
          Acceder
        </a>

        <button
          type="button"
          className={styles.toggle}
          aria-expanded={open}
          aria-controls="main-nav"
          onClick={() => setOpen((v) => !v)}
        >
          <Icon name={open ? 'close' : 'menu'} size={24} />
          <span className="visually-hidden">{open ? 'Cerrar menú' : 'Abrir menú'}</span>
        </button>
      </div>
    </header>
  );
}
