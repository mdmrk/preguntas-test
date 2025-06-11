<template>
  <div class="max-w-4xl mx-auto">
    <div v-if="loading" class="flex items-center justify-center py-12">
      <svg
        aria-hidden="true"
        class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
        viewBox="0 0 100 101"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
          fill="currentColor"
        />
        <path
          d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
          fill="currentFill"
        />
      </svg>
      <span class="sr-only">Cargando...</span>
    </div>

    <div v-else-if="questions.length > 0" class="mb-6">
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <img
            src="@/assets/search.svg"
            class="w-5 h-5 filter-(--svg-gray) transition-transform"
            alt="search"
          />
        </div>
        <input
          v-model="searchInput"
          type="text"
          placeholder="Buscar..."
          class="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
        />
        <div v-if="searchInput" class="absolute inset-y-0 right-0 pr-3 flex items-center">
          <button
            @click="clearSearch"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <img
              src="@/assets/x.svg"
              class="w-5 h-5 filter-(--svg-gray) transition-transform"
              alt="x"
            />
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
              <svg
                class="w-5 h-5 text-green-600 dark:text-green-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clip-rule="evenodd"
                ></path>
              </svg>
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
