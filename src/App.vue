<script setup lang="ts">
import HomeButton from "@/components/HomeButton.vue"
import ThemeManager from "@/components/ThemeManager.vue"
import { RouterView } from "vue-router"
</script>

<template>
  <header class="flex items-center justify-between">
    <HomeButton />
    <ThemeManager />
  </header>
  <RouterView />
</template>
