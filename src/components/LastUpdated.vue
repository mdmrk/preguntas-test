<template>
  <div class="last-updated">Última actualización: {{ formattedDate }}</div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue"

const formattedDate = ref("")

onMounted(() => {
  const buildDate = import.meta.env.PROD
    ? new Date(import.meta.env.VITE_BUILD_TIME || Date.now())
    : new Date()

  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  }

  formattedDate.value = buildDate.toLocaleDateString("es-ES", options)
})
</script>

<style scoped>
.last-updated {
  font-size: 0.9rem;
  color: #666;
  margin: 1rem 0;
}
</style>
