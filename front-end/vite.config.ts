/// <reference types="vitest" />
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const bffPort = env.BFF_PORT ?? '5174';

  return {
    plugins: [react()],
    server: {
      port: 5173,
      // Todo /api pasa por el BFF, que a su vez delega en el centro de mando (FastAPI).
      proxy: { '/api': `http://127.0.0.1:${bffPort}` },
    },
    build: { outDir: 'dist', sourcemap: true },
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: './src/test/setup.ts',
    },
  };
});
