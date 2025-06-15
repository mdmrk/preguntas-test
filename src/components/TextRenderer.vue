<template>
  <span v-html="renderedText"></span>
</template>

<script setup lang="ts">
import hljs from "highlight.js/lib/common"
import katex from "katex"

import { computed } from "vue"

interface Props {
  text: string
}

const props = defineProps<Props>()

const renderedText = computed(() => {
  try {
    let result = props.text

    result = escapeHtml(result)

    result = result.replace(/\$\$([^$]+)\$\$/g, (_, math) => {
      return katex.renderToString(deescapeHtml(math), { displayMode: true, throwOnError: false })
    })

    result = result.replace(/\$([^$]+)\$/g, (_, math) => {
      return katex.renderToString(deescapeHtml(math), { displayMode: false, throwOnError: false })
    })

    result = result.replace(/```cpp(?:\w+)?\s*([\s\S]*?)\s*```/g, (_, code) => {
      return `<pre><code>${hljs.highlight(deescapeHtml(code), { language: "cpp" }).value}</code></pre>`
    })

    result = result.replace(/`([^`]+)`/g, (_, code) => {
      return `<code>${code}</code>`
    })

    return result
  } catch (error) {
    console.warn("Rendering error:", error)
    return escapeHtml(props.text)
  }
})

function deescapeHtml(text: string): string {
  return text
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;")
}
</script>
