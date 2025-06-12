<template>
  <div class="max-w-4xl mx-auto">
    <div v-if="loading" class="flex items-center justify-center py-12">
      <LoadingSpinnerIcon />
      <span class="sr-only">Cargando...</span>
    </div>

    <div v-else-if="questions.length > 0" class="mb-6">
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <SearchIcon class="w-5 h-5 icon" />
        </div>
        <input
          v-model="searchInput"
          type="text"
          placeholder="Buscar..."
          class="w-full pl-10 pr-4 py-3 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
        />
        <div v-if="searchInput" class="absolute inset-y-0 right-0 pr-3 flex items-center">
          <button
            @click="clearSearch"
            class="text-gray-icon hover:text-gray-600 dark:hover:text-gray-300 cursor-pointer"
          >
            <XIcon class="w-5 h-5" />
          </button>
        </div>
      </div>

      <div class="mt-3 text-sm text-gray-600 dark:text-gray-400">
        <span v-if="searchQuery">
          {{ filteredQuestions.length }} de {{ questions.length }} preguntas encontradas
        </span>
        <span v-else> {{ questions.length }} preguntas en total </span>
      </div>
    </div>

    <div v-if="!loading && filteredQuestions.length > 0" class="space-y-6">
      <div
        v-for="question in filteredQuestions"
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

        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">
            <TextRenderer :text="question.question" />
          </h3>
        </div>

        <div class="space-y-3 mb-4">
          <div
            v-for="(option, optionIndex) in question.options"
            :key="optionIndex"
            class="flex items-center p-3 rounded-lg border transition-colors"
            :class="[
              optionIndex === question.correctAnswer
                ? 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-700'
                : 'bg-gray-50 border-gray-200 dark:bg-gray-700 dark:border-gray-600'
            ]"
          >
            <div class="flex items-center flex-1 min-w-0">
              <div
                class="flex-shrink-0 w-4 h-4 rounded-full border-2 mr-3 flex items-center justify-center"
                :class="[
                  optionIndex === question.correctAnswer
                    ? 'border-green-500 bg-green-500'
                    : 'border-gray-300 dark:border-gray-600'
                ]"
              >
                <div
                  v-if="optionIndex === question.correctAnswer"
                  class="w-2 h-2 rounded-full bg-white"
                ></div>
              </div>
              <span
                class="text-sm font-medium truncate"
                :class="[
                  optionIndex === question.correctAnswer
                    ? 'text-green-800 dark:text-green-300'
                    : 'text-gray-700 dark:text-gray-300'
                ]"
              >
                <TextRenderer :text="option" />
              </span>
            </div>
            <div v-if="optionIndex === question.correctAnswer" class="ml-2 flex-shrink-0">
              <CheckIcon class="text-green-600 dark:text-green-400 w-4" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-else-if="!loading && questions.length > 0 && filteredQuestions.length === 0"
      class="text-center py-12"
    >
      <p class="text-gray-500 dark:text-gray-400">No se encontraron resultados para tu búsqueda.</p>
    </div>

    <div v-else-if="!loading" class="text-center py-12">
      <p class="text-gray-500 dark:text-gray-400">No questions found.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import CheckIcon from "@/components/icons/CheckIcon.vue"
import LoadingSpinnerIcon from "@/components/icons/LoadingSpinnerIcon.vue"
import SearchIcon from "@/components/icons/SearchIcon.vue"
import XIcon from "@/components/icons/XIcon.vue"
import TextRenderer from "@/components/TextRenderer.vue"
import { QuizLoader } from "@/composables/useQuizLoader"
import type { Question } from "@/types/quiz"
import "katex/dist/katex.min.css"
import { computed, onMounted, ref, watch } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const quizContent = ref("")
const loading = ref(true)
const searchInput = ref("")
const searchQuery = ref("")
const DEBOUNCE_DELAY = 600

const quizId = computed(() => route.params.id as string)

const debounce = <T extends unknown[]>(func: (...args: T) => void, delay: number) => {
  let timeoutId: ReturnType<typeof setTimeout>
  return (...args: T) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func(...args), delay)
  }
}

const debouncedSearch = debounce((value: string) => {
  searchQuery.value = value
}, DEBOUNCE_DELAY)

watch(searchInput, (newValue) => {
  debouncedSearch(newValue)
})

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

const filteredQuestions = computed(() => {
  if (!searchQuery.value.trim()) {
    return questions.value
  }

  const query = searchQuery.value.toLowerCase().trim()

  return questions.value.filter((question) => {
    const titleMatch = question.question.toLowerCase().includes(query)

    const optionsMatch = question.options.some((option) => option.toLowerCase().includes(query))

    return titleMatch || optionsMatch
  })
})

const clearSearch = () => {
  searchInput.value = ""
  searchQuery.value = ""
}

const getOriginalQuestionNumber = (question: Question) => {
  return questions.value.findIndex((q) => q.id === question.id) + 1
}
</script>
