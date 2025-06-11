<template>
  <div class="max-w-2xl mx-auto">
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
      <span class="sr-only">Loading...</span>
    </div>

    <div v-else-if="questions.length > 0">
      <div
        class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg mb-6 p-4"
      >
        <div class="flex items-center justify-between mb-3">
          <div class="text-blue-600 dark:text-blue-400 text-sm font-medium">
            {{ currentQuestionIndex + 1 }} / {{ questions.length }}
          </div>

          <div
            v-show="answeredQuestions > 0"
            class="flex items-center space-x-3 text-sm font-medium"
          >
            <div class="text-green-600 dark:text-green-400">{{ correctAnswers }}</div>
            <div class="text-red-600 dark:text-red-400">{{ failedAnswers }}</div>
            <div class="text-green-600 dark:text-green-400">
              {{ correctAnswersPercentage.toFixed(0) }}%
            </div>
          </div>
        </div>

        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 flex overflow-hidden">
          <div
            v-show="answeredQuestions > 0"
            class="bg-green-500 dark:bg-green-400 rounded-l-full"
            :style="{ width: `${correctAnswersPercentage.toFixed(0)}%` }"
          ></div>
          <div
            v-show="answeredQuestions > 0"
            class="bg-red-500 dark:bg-red-400 flex-1 rounded-r-full"
          ></div>
        </div>
      </div>

      <QuizQuestion
        v-if="currentQuestion"
        :key="currentQuestion.id"
        :question="currentQuestion"
        @answered="handleAnswered"
        @next="nextQuestion"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import QuizQuestion from "@/components/QuizQuestion.vue"
import { QuizLoader } from "@/composables/useQuizLoader"
import "highlight.js/styles/github-dark-dimmed.css"
import "katex/dist/katex.min.css"
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const quizContent = ref("")
const loading = ref(true)
const currentQuestionIndex = ref(4)
const answers = ref<Array<{ questionId: number; selectedOption: number; isCorrect: boolean }>>([])

const quizId = computed(() => route.params.quizId as string)

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

const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value] || null
})

const correctAnswers = computed(() => {
  return answers.value.filter((answer) => answer.isCorrect).length
})

const answeredQuestions = computed(() => {
  return answers.value.length
})

const failedAnswers = computed(() => {
  return answeredQuestions.value - correctAnswers.value
})

const correctAnswersPercentage = computed(() => {
  if (answeredQuestions.value === 0) return 0
  return (correctAnswers.value / answeredQuestions.value) * 100
})

const handleAnswered = (payload: {
  questionId: number
  selectedOption: number
  isCorrect: boolean
}) => {
  answers.value.push(payload)
}

const nextQuestion = () => {
  currentQuestionIndex.value++
}
</script>
