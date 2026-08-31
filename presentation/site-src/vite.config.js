import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { viteSingleFile } from 'vite-plugin-singlefile';

// Everything (JS + CSS) is inlined into a single index.html so the site can be
// opened straight off disk or from a USB stick — no server, no build step, and no
// CORS problems from ES modules over file://. Images stay as sibling folders.
export default defineConfig({
  base: './',
  plugins: [react(), viteSingleFile()],
  build: { chunkSizeWarningLimit: 3000, assetsInlineLimit: 0 },
});
