<template>
  <div class="text-sm text-gray-600 my-4">Última actualización: {{ formattedDate }}</div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue"

const formattedDate = ref<string>("")

onMounted(() => {
  const buildDate = import.meta.env.PROD
    ? new Date(import.meta.env.VITE_BUILD_TIME || Date.now())
    : new Date()

  const options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  }

  formattedDate.value = buildDate.toLocaleDateString("es-ES", options)
})
</script>
