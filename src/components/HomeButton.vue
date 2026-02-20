<template>
  <RouterLink to="/" class="nav-button" aria-label="Go to home">
    <HouseIcon class="w-5 h-5" />
  </RouterLink>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router"
import HouseIcon from "@/components/icons/HouseIcon.vue"
</script>
