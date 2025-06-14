<template>
  <div class="max-w-4xl mx-auto">
    <div v-if="loading" class="flex items-center justify-center py-12">
      <LoadingSpinnerIcon />
      <span class="sr-only">Cargando...</span>
    </div>

    <div v-else-if="questions.length > 0" class="space-y-6">
      <div
        class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6"
      >
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-4">
            <span
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
            >
              {{ currentQuestionIndex + 1 }} / {{ questions.length }}
            </span>

            <div
              v-show="answeredQuestions > 0"
              class="flex items-center space-x-4 text-sm font-medium"
            >
              <div class="flex items-center space-x-1">
                <div class="w-3 h-3 rounded-full bg-green-500"></div>
                <span class="text-green-600 dark:text-green-400">{{ correctAnswers }}</span>
              </div>
              <div class="flex items-center space-x-1">
                <div class="w-3 h-3 rounded-full bg-red-500"></div>
                <span class="text-red-600 dark:text-red-400">{{ failedAnswers }}</span>
              </div>
              <span class="text-blue-600 dark:text-blue-400">
                {{ correctAnswersPercentage.toFixed(0) }}%
              </span>
            </div>
          </div>
        </div>

        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 flex overflow-hidden">
          <div
            v-if="answeredQuestions > 0"
            class="bg-green-500 dark:bg-green-400 transition-all duration-300"
            :class="{ 'rounded-l-full': true, 'rounded-r-full': failedAnswers === 0 }"
            :style="{ width: `${correctAnswersPercentage}%` }"
          ></div>
          <div
            v-if="answeredQuestions > 0 && failedAnswers > 0"
            class="bg-red-500 dark:bg-red-400 transition-all duration-300"
            :class="{ 'rounded-r-full': true }"
            :style="{ width: `${failedAnswersPercentage}%` }"
          ></div>
          <div
            v-if="answeredQuestions === 0"
            class="bg-gray-300 dark:bg-gray-600 flex-1 rounded-full"
          ></div>
        </div>
      </div>

      <div v-if="currentQuestion && !quizFinished">
        <QuizQuestion :question="currentQuestion" @answered="handleAnswer" @next="nextQuestion" />
      </div>

      <div
        v-if="quizFinished"
        class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6"
      >
        <div class="text-center">
          <div class="mb-4">
            <div class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ correctAnswersPercentage.toFixed(1) }}%
            </div>
            <div class="text-gray-600 dark:text-gray-400">
              {{ correctAnswers }} de {{ questions.length }} respuestas correctas
            </div>
          </div>

          <div class="flex justify-center space-x-4 mb-6">
            <div class="text-center">
              <div class="text-2xl font-bold text-green-600 dark:text-green-400">
                {{ correctAnswers }}
              </div>
              <div class="text-sm text-gray-600 dark:text-gray-400">Correctas</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-red-600 dark:text-red-400">
                {{ failedAnswers }}
              </div>
              <div class="text-sm text-gray-600 dark:text-gray-400">Incorrectas</div>
            </div>
          </div>

          <button
            @click="restartQuiz"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg"
          >
            Reintentar
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <p class="text-gray-500 dark:text-gray-400">No se encontraron preguntas.</p>
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
const currentQuestionIndex = ref(0)
const answers = ref<Array<{ questionId: number; selectedOption: number; isCorrect: boolean }>>([])
const quizFinished = ref(false)

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

const failedAnswersPercentage = computed(() => {
  if (answeredQuestions.value === 0) return 0
  return (failedAnswers.value / answeredQuestions.value) * 100
})

const handleAnswer = (answer: {
  questionId: number
  selectedOption: number
  isCorrect: boolean
}) => {
  answers.value.push(answer)
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
  } else {
    quizFinished.value = true
  }
}

const restartQuiz = () => {
  currentQuestionIndex.value = 0
  answers.value = []
  quizFinished.value = false
}
</script>
