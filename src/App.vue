<script setup lang="ts">
import HomeButton from "@/components/HomeButton.vue"
import LastUpdated from "@/components/LastUpdated.vue"
import ThemeManager from "@/components/ThemeManager.vue"
import { RouterView } from "vue-router"
</script>

<template>
  <header class="flex justify-end space-x-3 mb-4">
    <HomeButton />
    <ThemeManager />
  </header>
  <RouterView />
  <footer><LastUpdated /></footer>
</template>
