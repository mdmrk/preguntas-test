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
        <div
          v-if="availableTags.length > 0"
          class="mt-4 pt-3 border-t border-blue-200 dark:border-blue-700"
        >
          <div class="flex flex-wrap gap-2">
            <label v-for="tag in availableTags" :key="tag" class="cursor-pointer">
              <input type="checkbox" :value="tag" v-model="selectedTags" class="sr-only" />
              <span
                :class="[
                  'inline-flex items-center px-3 py-1 rounded-full text-sm font-medium transition-colors',
                  selectedTags.includes(tag)
                    ? 'bg-blue-600 text-white'
                    : 'bg-blue-100 text-blue-700 hover:bg-blue-200 dark:bg-blue-800 dark:text-blue-200 dark:hover:bg-blue-700'
                ]"
              >
                {{ tag }}
              </span>
            </label>
          </div>
        </div>
      </div>
      <div class="space-y-6">
        <div
          v-for="question in filteredQuestions"
          :key="question.id"
          class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6"
        >
          <div class="flex items-center justify-between mb-4">
            <span
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
            >
              Pregunta {{ getQuestionNumber(question) }}
            </span>
            <div class="flex flex-wrap gap-1">
              <span
                v-for="tag in question.tags"
                :key="tag"
                class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200"
              >
                {{ tag }}
              </span>
            </div>
          </div>
          <QuizQuestion :question="question" :answered="true" :readOnly="true" />
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
import type { Question } from "@/types/quiz"
import "katex/dist/katex.min.css"
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const quizContent = ref("")
const loading = ref(true)
const selectedTags = ref<string[]>([])

const quizId = computed(() => route.params.id as string)
const loader = new QuizLoader()

const questions = computed(() => {
  if (!quizContent.value) return []
  return loader.parseQuizText(quizContent.value, false)
})

const availableTags = computed(() => {
  const tags = new Set<string>()
  questions.value.forEach((question) => {
    question.tags.forEach((tag) => tags.add(tag))
  })
  return Array.from(tags).sort().reverse()
})

const filteredQuestions = computed(() => {
  if (selectedTags.value.length === 0) {
    return questions.value
  }
  return questions.value.filter((question) =>
    selectedTags.value.some((tag) => question.tags.includes(tag))
  )
})

const questionCountText = computed(() => {
  const totalCount = questions.value.length
  const filteredCount = filteredQuestions.value.length
  if (selectedTags.value.length === 0) {
    return `${totalCount} preguntas únicas en total`
  }
  return `${filteredCount} de ${totalCount} preguntas mostradas`
})

const getQuestionNumber = (question: Question) => {
  return questions.value.findIndex((q) => q.id === question.id) + 1
}

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
