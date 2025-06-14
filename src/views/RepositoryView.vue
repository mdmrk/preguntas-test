<template>
  <div class="max-w-4xl mx-auto">
    <div v-if="loading" class="flex items-center justify-center py-12">
      <LoadingSpinnerIcon />
      <span class="sr-only">Cargando...</span>
    </div>

    <div v-else-if="questions.length > 0" class="mb-6">
      <div class="mt-3 text-sm text-gray-600 dark:text-gray-400">
        <span> {{ questions.length }} preguntas en total </span>
      </div>
    </div>

    <div v-if="!loading && questions.length > 0" class="space-y-6">
      <div
        v-for="question in questions"
        :key="question.id"
        class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6"
      >
        <div class="flex items-center justify-between mb-4">
          <span
            class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
          >
            Pregunta {{ getOriginalQuestionNumber(question) }}
          </span>
        </div>

        <QuizQuestion :question="question" :read-only="true" />
      </div>
    </div>

    <div v-else-if="!loading && questions.length === 0" class="text-center py-12">
      <p class="text-gray-500 dark:text-gray-400">No questions found.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import LoadingSpinnerIcon from "@/components/icons/LoadingSpinnerIcon.vue"
import QuizQuestion from "@/components/QuizQuestion.vue"
import { QuizLoader } from "@/composables/useQuizLoader"
import type { Question } from "@/types/quiz"
import "katex/dist/katex.min.css"
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const quizContent = ref("")
const loading = ref(true)

const quizId = computed(() => route.params.id as string)

onMounted(async () => {
  try {
    const module = await import(`@/data/${quizId.value}.txt?raw`)
    quizContent.value = module.default
  } catch (error) {
    console.error("Failed to load quiz:", error)
  } finally {
    loading.value = false
  }
})

const loader = new QuizLoader()

const questions = computed(() => {
  if (!quizContent.value) return []
  return loader.parseQuizText(quizContent.value)
})

const getOriginalQuestionNumber = (question: Question) => {
  return questions.value.findIndex((q) => q.id === question.id) + 1
}
</script>
