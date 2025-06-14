<template>
  <div class="max-w-4xl mx-auto">
    <div v-if="loading" class="flex items-center justify-center py-12">
      <LoadingSpinnerIcon />
      <span class="sr-only">Cargando...</span>
    </div>

    <template v-else-if="questions.length > 0">
      <div
        class="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg"
      >
        <h2 class="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">Repositorio</h2>
        <p class="text-sm text-blue-700 dark:text-blue-300">{{ questionCountText }}</p>
      </div>

      <div class="space-y-6">
        <div
          v-for="(question, index) in questions"
          :key="question.id"
          class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6"
        >
          <div class="flex items-center justify-between mb-4">
            <span
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
            >
              Pregunta {{ index + 1 }}
            </span>
          </div>

          <QuizQuestion :question="question" mode="repository" :answered="true" :readOnly="true" />
        </div>
      </div>
    </template>

    <div v-else class="text-center py-12">
      <div
        class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-8"
      >
        <p class="text-gray-500 dark:text-gray-400 text-lg">
          No se encontraron preguntas en este repositorio.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import LoadingSpinnerIcon from "@/components/icons/LoadingSpinnerIcon.vue"
import QuizQuestion from "@/components/QuizQuestion.vue"
import { QuizLoader } from "@/composables/useQuizLoader"
import "katex/dist/katex.min.css"
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const quizContent = ref("")
const loading = ref(true)

const quizId = computed(() => route.params.id as string)
const loader = new QuizLoader()

const questions = computed(() => {
  if (!quizContent.value) return []
  return loader.parseQuizText(quizContent.value)
})

const questionCountText = computed(() => {
  const count = questions.value.length
  return `${count} pregunta${count === 1 ? "" : "s"} en total`
})

const loadQuizData = async () => {
  try {
    const module = await import(`@/data/${quizId.value}.txt?raw`)
    quizContent.value = module.default
  } catch (error) {
    console.error("Failed to load quiz:", error)
  } finally {
    loading.value = false
  }
}

onMounted(loadQuizData)
</script>
