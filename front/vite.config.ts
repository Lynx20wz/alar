import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";
import devtoolsJson from 'vite-plugin-devtools-json';

export default defineConfig({
  plugins: [sveltekit(), devtoolsJson()],
  server: {
    port: 5050,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        rewrite: (path) => path.replace(/^\/api/, ""),
        changeOrigin: true,
      },
    },
  },
});
