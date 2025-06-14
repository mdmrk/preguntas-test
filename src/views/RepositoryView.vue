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

        <div class="mb-6">
          <div class="text-base font-semibold text-gray-900 dark:text-white mb-3">
            <TextRenderer :text="question.question" />
          </div>
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

    <div v-else-if="!loading && questions.length === 0" class="text-center py-12">
      <p class="text-gray-500 dark:text-gray-400">No questions found.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import CheckIcon from "@/components/icons/CheckIcon.vue"
import LoadingSpinnerIcon from "@/components/icons/LoadingSpinnerIcon.vue"
import TextRenderer from "@/components/TextRenderer.vue"
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
