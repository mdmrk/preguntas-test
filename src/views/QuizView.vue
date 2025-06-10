<template>
  <div class="py-8">
    <div class="max-w-2xl mx-auto px-4">
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
        <span class="ml-3 text-gray-300 font-medium">Cargando...</span>
      </div>

      <div v-else-if="!quizContent && !loading" class="text-center py-12">
        <div
          class="bg-gradient-to-br from-gray-800 to-gray-900 rounded-3xl shadow-2xl p-8 text-gray-50"
        >
          <div
            class="w-16 h-16 bg-red-600 bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-4"
          >
            <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-50 mb-2">Quiz Not Found</h2>
          <p class="text-gray-300 mb-6">The quiz "{{ quizId }}" could not be loaded.</p>
          <router-link
            to="/"
            class="inline-block bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-3 px-8 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            Back to Home
          </router-link>
        </div>
      </div>

      <div v-else-if="questions.length > 0">
        <div
          class="bg-gradient-to-br from-gray-800 to-gray-900 rounded-3xl shadow-2xl p-8 mb-6 text-gray-50"
        >
          <div class="flex items-center justify-between mb-6">
            <h1 class="text-3xl font-bold text-gray-50">{{ quizTitle }}</h1>
            <div class="text-right">
              <div class="text-sm text-gray-400 uppercase tracking-wide">Question</div>
              <div
                class="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent"
              >
                {{ currentQuestionIndex + 1 }} / {{ questions.length }}
              </div>
            </div>
          </div>

          <div class="relative">
            <div class="w-full bg-gray-700 rounded-full h-3 shadow-inner">
              <div
                class="bg-gradient-to-r from-blue-500 to-indigo-500 h-3 rounded-full transition-all duration-500 ease-out shadow-lg"
                :style="{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }"
              ></div>
            </div>
            <div
              class="absolute inset-0 bg-gradient-to-r from-blue-400 to-indigo-400 rounded-full opacity-30 blur-sm h-3"
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

        <div
          v-if="quizCompleted"
          class="bg-gradient-to-br from-gray-800 to-gray-900 rounded-3xl shadow-2xl p-8 mt-6 text-gray-50"
        >
          <div class="text-center">
            <div
              class="w-20 h-20 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <svg class="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <h2 class="text-3xl font-bold text-gray-50 mb-4">Quiz Complete!</h2>
            <div class="mb-8">
              <p class="text-xl text-gray-300 mb-2">
                You scored {{ correctAnswers }} out of {{ questions.length }}
              </p>
              <div
                class="text-4xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent"
              >
                {{ Math.round(scorePercentage) }}%
              </div>
            </div>
            <div class="flex justify-center space-x-4">
              <button
                @click="restartQuiz"
                class="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-3 px-8 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                Restart Quiz
              </button>
              <router-link
                to="/"
                class="bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white font-bold py-3 px-8 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                Back to Home
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import QuizQuestion from "@/components/QuizQuestion.vue"
import { QuizLoader } from "@/composables/useQuizLoader"
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const quizContent = ref("")
const loading = ref(true)
const currentQuestionIndex = ref(0)
const answers = ref<Array<{ questionId: number; selectedOption: number; isCorrect: boolean }>>([])

const quizId = computed(() => route.params.quizId as string)
const quizTitle = computed(() => {
  return quizId.value
    .split("-")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ")
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

const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value] || null
})

const quizCompleted = computed(() => {
  return currentQuestionIndex.value >= questions.value.length
})

const correctAnswers = computed(() => {
  return answers.value.filter((answer) => answer.isCorrect).length
})

const scorePercentage = computed(() => {
  if (questions.value.length === 0) return 0
  return (correctAnswers.value / questions.value.length) * 100
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

const restartQuiz = () => {
  currentQuestionIndex.value = 0
  answers.value = []
}
</script>
