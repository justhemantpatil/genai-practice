import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import autoTracePlugin from './auto-trace-plugin.js'
import saveTracePlugin from './save-trace-plugin.js'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: [autoTracePlugin],
      },
    }),
    saveTracePlugin()
  ],
})
