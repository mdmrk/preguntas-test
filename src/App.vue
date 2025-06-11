<script setup lang="ts">
import ThemeManager from "@/components/ThemeManager.vue"
import { Analytics } from "@vercel/analytics/vue"
import { RouterView } from "vue-router"
</script>

<template>
  <Analytics mode="production" />
  <header><ThemeManager /></header>
  <RouterView />
</template>
