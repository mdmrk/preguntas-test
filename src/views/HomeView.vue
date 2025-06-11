<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
const router = useRouter()

import MainButton from "@/components/MainButton.vue"
const ada = ref(false)
const ppss = ref(false)

const navigateToQuiz = (quizId: string) => {
  router.push(`/quiz/${quizId}`)
}
</script>

<template>
  <main>
    <nav class="flex flex-col items-center w-full space-y-3">
      <div class="relative w-full flex flex-col items-center">
        <MainButton @click="ada = !ada" class="gradient-red relative z-10">ADA</MainButton>
        <div
          v-show="ada"
          class="flex flex-col items-center w-full px-2 pb-4 space-y-3 bg-red-900 dark:bg-red-950 rounded-b-3xl -mt-8 pt-12"
        >
          <MainButton @click="navigateToQuiz('ada-parcial-1')" class="gradient-red"
            >parcial 1</MainButton
          >
          <MainButton @click="navigateToQuiz('ada-parcial-2')" class="gradient-red"
            >parcial 2</MainButton
          >
          <MainButton @click="navigateToQuiz('ada-completo')" class="gradient-red"
            >completo</MainButton
          >
        </div>
      </div>
      <div class="relative w-full flex flex-col items-center">
        <MainButton @click="ppss = !ppss" class="gradient-blue relative z-10">PPSS</MainButton>
        <div
          v-show="ppss"
          class="flex flex-col items-center w-full px-2 pb-4 space-y-3 bg-blue-900 dark:bg-blue-950 rounded-b-3xl -mt-8 pt-12"
        >
          <MainButton @click="navigateToQuiz('ppss-parcial-1')" class="gradient-blue"
            >parcial 1</MainButton
          >
          <MainButton @click="navigateToQuiz('ppss-parcial-2')" class="gradient-blue"
            >parcial 2</MainButton
          >
        </div>
      </div>
      <MainButton @click="navigateToQuiz('gpi')" class="gradient-green">GPI</MainButton>
    </nav>
  </main>
</template>
