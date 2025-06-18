import tailwindcss from "@tailwindcss/vite"
import vue from "@vitejs/plugin-vue"
import { fileURLToPath, URL } from "node:url"
import { visualizer } from "rollup-plugin-visualizer"
import { defineConfig } from "vite"
import vueDevTools from "vite-plugin-vue-devtools"

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          hoistStatic: true,
          cacheHandlers: true
        }
      }
    }),
    vueDevTools(),
    tailwindcss(),
    visualizer({
      filename: "dist/stats.html",
      gzipSize: true,
      brotliSize: true,
      open: false
    })
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url))
    }
  },
  esbuild: {
    drop: process.env.NODE_ENV === "production" ? ["console", "debugger"] : []
  },
  build: {
    target: "esnext",
    minify: "esbuild",
    cssMinify: "esbuild",
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("src/data/") && id.includes(".txt")) {
            const fileName = id.split("/").pop()?.replace(".txt", "")
            return `test-${fileName}`
          }

          if (id.includes("src/components/icons/")) {
            return "icons"
          }

          if (id.includes("src/views/")) {
            return "views"
          }

          if (id.includes("src/composables/")) {
            return "composables"
          }

          if (id.includes("node_modules")) {
            if (id.includes("vue") && !id.includes("vue-router")) {
              return "vue-core"
            }
            if (id.includes("vue-router")) {
              return "vue-router"
            }
            if (id.includes("katex")) {
              return "katex-vendor"
            }
            if (id.includes("highlight.js")) {
              return "highlight-vendor"
            }
            if (id.includes("@tailwindcss") || id.includes("tailwindcss")) {
              return "tailwind-vendor"
            }
            return "vendor"
          }
        },
        chunkFileNames: (chunkInfo) => {
          const facadeModuleId = chunkInfo.facadeModuleId
          if (facadeModuleId?.includes("src/data/")) {
            return "assets/test-data/[name]-[hash].js"
          }
          if (facadeModuleId?.includes("src/components/icons/")) {
            return "assets/icons/[name]-[hash].js"
          }
          if (facadeModuleId?.includes("src/views/")) {
            return "assets/views/[name]-[hash].js"
          }
          return "assets/js/[name]-[hash].js"
        },
        assetFileNames: (assetInfo) => {
          const name = assetInfo.name || ""
          if (/\.(png|jpe?g|svg|gif|webp)$/i.test(name)) {
            if (name.includes("gpi")) {
              return "assets/test-images/[name]-[hash].[ext]"
            }
            return "assets/img/[name]-[hash].[ext]"
          }
          if (/\.(woff2?|eot|ttf|otf)$/i.test(name)) {
            return "assets/fonts/[name]-[hash].[ext]"
          }
          if (name.endsWith(".css")) {
            return "assets/css/[name]-[hash].[ext]"
          }
          return "assets/[name]-[hash].[ext]"
        }
      },
      treeshake: {
        moduleSideEffects: false,
        propertyReadSideEffects: false,
        unknownGlobalSideEffects: false
      }
    },
    sourcemap: false,
    reportCompressedSize: false,
    chunkSizeWarningLimit: 1000
  },
  server: {
    host: true,
    port: 5173,
    strictPort: false,
    fs: {
      strict: false
    }
  },
  preview: {
    host: true,
    port: 4173,
    strictPort: false
  },
  optimizeDeps: {
    include: ["vue", "vue-router", "katex", "highlight.js"],
    exclude: ["vue-demi"],
    force: false
  },
  assetsInclude: ["**/*.txt"],
  define: {
    __VUE_PROD_DEVTOOLS__: false,
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false
  }
})
