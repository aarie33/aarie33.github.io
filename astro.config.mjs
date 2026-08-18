// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://aarie33.github.io',
  base: '/',
  image: {
    responsiveStyles: true,
  },
  integrations: [sitemap()],
});
