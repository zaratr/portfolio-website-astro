// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://walkswithgiants.com',
  // Tailwind v4 — single Vite plugin, no config file required.
  vite: {
    plugins: [tailwindcss()],
  },
  // Default output is 'static' — every page is pre-rendered at build time.
  // Role pages get noindex via per-page <meta>, not via route config.
});
