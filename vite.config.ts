import tailwindcss from "@tailwindcss/vite"
import vue from "@vitejs/plugin-vue"
import { fileURLToPath, URL } from "node:url"
import { visualizer } from "rollup-plugin-visualizer"
import { defineConfig } from "vite"
import vueDevTools from "vite-plugin-vue-devtools"

export default defineConfig({
  plugins: [vue(), vueDevTools(), tailwindcss(), visualizer()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url))
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("src/data/") && id.includes(".txt")) {
            const fileName = id.split("/").pop()?.replace(".txt", "")
            return `quiz-${fileName}`
          }

          if (id.includes("node_modules")) {
            if (id.includes("vue")) {
              return "vue-vendor"
            }
            return "vendor"
          }
        }
      }
    }
  }
})
