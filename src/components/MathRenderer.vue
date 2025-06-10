<template>
  <span v-html="renderedText"></span>
</template>

<script setup lang="ts">
import katex from "katex"
import "katex/dist/katex.min.css"
import { computed } from "vue"

interface Props {
  text: string
}

const props = defineProps<Props>()

const renderedText = computed(() => {
  try {
    let result = props.text

    result = result.replace(/\$\$([^$]+)\$\$/g, (match, math) => {
      return katex.renderToString(math, { displayMode: true, throwOnError: false })
    })

    result = result.replace(/\$([^$]+)\$/g, (match, math) => {
      return katex.renderToString(math, { displayMode: false, throwOnError: false })
    })

    return result
  } catch (error) {
    console.warn("Math rendering error:", error)
    return props.text
  }
})
</script>

<style scoped>
:deep(.katex) {
  color: inherit;
}
</style>
