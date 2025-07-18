import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
const dotenv = require('dotenv');
const envPath = resolve(__dirname, '..', '.env');
dotenv.config({ path: envPath });
const FLASK_PORT = process.env.FLASK_PORT || 5008;
const FLASK_HOST = process.env.FLASK_HOST || 'localhost';
const FLASK_URL = `http://${FLASK_HOST}:${FLASK_PORT}`;
const VITE_PORT = process.env.VITE_PORT || 5173;

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './', // This ensures assets are loaded correctly in Electron
  server: {
    port: VITE_PORT,
    proxy: {
      '/api': {
        target: `${FLASK_URL}`, // Flask backend port
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
      },
    },
    // Ensure sourcemaps are generated for easier debugging
    sourcemap: true
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  // Prevent Vite from handling process.env
  define: {
    'process.env': {}
  },
  // Optimize dependencies
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      'axios',
      'bootstrap',
      'react-bootstrap',
      'react-icons',
      'react-markdown'
    ]
  }
})