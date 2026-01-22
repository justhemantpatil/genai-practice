import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import uiTracePlugin from "../babel-plugins/ui-trace-plugin.js";

export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: [
          // Enable tracing: Always enable for now to test
          uiTracePlugin
        ]
      }
    })
  ]
});
