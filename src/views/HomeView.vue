<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

import MainButton from '@/components/MainButton.vue'
const ada = ref(false)

const navigateToQuiz = (quizId: string) => {
  router.push(`/quiz/${quizId}`)
}
</script>

<template>
  <main>
    <nav class="flex flex-col items-center w-full space-y-2">
      <div class="relative w-full flex flex-col items-center">
        <MainButton @click="ada = !ada" class="gradient-red relative z-10">ADA</MainButton>
        <div
          v-show="ada"
          class="flex flex-col items-center w-full px-2 pb-4 space-y-2 bg-red-900 rounded-b-3xl -mt-8 pt-12"
        >
          <MainButton @click="ada = !ada" class="gradient-red">parcial 1</MainButton>
          <MainButton @click="ada = !ada" class="gradient-red">parcial 2</MainButton>
          <MainButton @click="navigateToQuiz('ada-completo')" class="gradient-red"
            >completo</MainButton
          >
        </div>
      </div>
      <MainButton class="gradient-blue">PPSS</MainButton>
      <MainButton class="gradient-green">GPI</MainButton>
    </nav>
  </main>
</template>
