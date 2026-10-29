import type { ButtonHTMLAttributes } from 'react';
import { Icon } from './Icon';
import styles from './Button.module.css';

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  size?: 'md' | 'lg';
  arrow?: boolean;
}

export function Button({ size = 'md', arrow = false, className = '', children, ...rest }: Props) {
  return (
    <button type="button" className={`${styles.button} ${styles[size]} ${className}`} {...rest}>
      <span>{children}</span>
      {arrow && <Icon name="arrow" size={20} className={styles.arrow} />}
    </button>
  );
}
