<template>
  <span v-html="renderedText"></span>
</template>

<script setup lang="ts">
import katex from "katex"
import "katex/dist/katex.min.css"
import "prismjs/themes/prism.css"
import { computed } from "vue"

interface Props {
  text: string
}

const props = defineProps<Props>()

const renderedText = computed(() => {
  try {
    let result = props.text

    // Escape HTML first
    result = escapeHtml(result)

    // Handle display math ($...$)
    result = result.replace(/\$\$([^$]+)\$\$/g, (match, math) => {
      return katex.renderToString(math, { displayMode: true, throwOnError: false })
    })

    // Handle inline math ($...$)
    result = result.replace(/\$([^$]+)\$/g, (match, math) => {
      return katex.renderToString(math, { displayMode: false, throwOnError: false })
    })

    // Handle code blocks (```...```)
    result = result.replace(/```(?:\w+)?\s*([\s\S]*?)\s*```/g, (match, code) => {
      return `<pre><code>${code}</code></pre>`
    })

    // Handle inline code (`...`)
    result = result.replace(/`([^`]+)`/g, (match, code) => {
      return `<code>${code}</code>`
    })

    return result
  } catch (error) {
    console.warn("Rendering error:", error)
    return escapeHtml(props.text)
  }
})

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;")
}
</script>

<style scoped>
:deep(.katex) {
  color: inherit;
}

:deep(pre) {
  background: light-dark(#f5f5f5, #1f2937);
  color: light-dark(#1f2937, #f9fafb);
  border-radius: 4px;
  padding: 1rem;
  overflow-x: auto;
  margin: 0.5rem 0;
  white-space: pre-wrap;
}

:deep(code) {
  background: light-dark(#f5f5f5, #374151);
  color: light-dark(#1f2937, #f9fafb);
  border-radius: 3px;
  padding: 0.2rem 0.4rem;
  font-family: "Courier New", monospace;
}

:deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}
</style>
