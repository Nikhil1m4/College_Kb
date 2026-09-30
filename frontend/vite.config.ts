import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // Build output goes to the project-root `public/` directory so Vercel
  // picks it up as static CDN content alongside the FastAPI function.
  build: {
    outDir: '../public',
    emptyOutDir: true,
  },
  server: {
    // Forward /api/* to uvicorn during local dev (no CORS needed in prod
    // because frontend and API share the same Vercel domain).
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
