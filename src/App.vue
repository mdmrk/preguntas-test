<script setup lang="ts">
import { Analytics } from "@vercel/analytics/vue"
import { RouterView } from "vue-router"
</script>

<template>
  <Analytics mode="production" />
  <header></header>
  <RouterView />
</template>
