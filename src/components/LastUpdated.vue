<template>
  <div class="flex flex-row gap-1">
    <ClockIcon class="w-5 h-5" />
    <div>Última actualización: {{ formattedDate }}</div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue"
import ClockIcon from "@/components/icons/ClockIcon.vue"

const formattedDate = ref<string>("")

onMounted(() => {
  let buildDate: Date

  if (import.meta.env.PROD) {
    const buildTime = import.meta.env.VITE_BUILD_TIME
    buildDate = buildTime ? new Date(buildTime) : new Date()
  } else {
    buildDate = new Date()
  }

  const options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }

  formattedDate.value = buildDate.toLocaleDateString("es-ES", options)
})
</script>
