import { defineConfig } from 'vite';
import { resolve } from 'path';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  root: 'src',
  base: '/static/dist/',
  build: {
    outDir: resolve(__dirname, 'static/dist'),
    emptyOutDir: true,
    rollupOptions: {
      input: resolve(__dirname, 'src/main.js'),
      output: {
        entryFileNames: 'main.js',
        assetFileNames: (info) => {
          if (info.name?.endsWith('.css')) return 'main.css';
          return '[name][extname]';
        },
      },
    },
  },
  server: {
    port: 5173,
    origin: 'http://localhost:5173',
  },
});
