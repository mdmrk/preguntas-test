<template>
  <div class="text-sm text-gray-600 mb-4">
    <span v-show="!loading">Visitas: {{ visitCount }}</span>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue"

const visitCount = ref<string>("")
const loading = ref<boolean>(true)

onMounted(async () => {
  try {
    const response = await fetch(
      "https://visit-counter.vercel.app/counter?page=preguntastest.vercel.app"
    )
    const count = await response.text()

    const numericCount = parseInt(count.trim(), 10)

    if (isNaN(numericCount)) {
      visitCount.value = count
      return
    }

    const formatter = new Intl.NumberFormat("es-ES", {
      useGrouping: true,
      minimumIntegerDigits: 1
    })

    visitCount.value = formatter.format(numericCount)
  } catch (error) {
    console.error("Error fetching visit count:", error)
  } finally {
    loading.value = false
  }
})
</script>
