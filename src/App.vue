<script setup lang="ts">
import HomeButton from "@/components/HomeButton.vue"
import LastUpdated from "@/components/LastUpdated.vue"
import ThemeManager from "@/components/ThemeManager.vue"
import { useHead } from "@unhead/vue"

useHead({
  title: "Preguntas Test",
  titleTemplate: (title) => (title ? `${title} - Preguntas Test` : "Preguntas Test")
})
</script>

<template>
  <header class="flex justify-end space-x-3 mb-4">
    <HomeButton />
    <ThemeManager />
  </header>
  <RouterView />
  <footer class="flex flex-col"><LastUpdated /></footer>
</template>
