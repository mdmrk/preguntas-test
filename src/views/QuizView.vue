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

      <div v-if="currentQuestion">
        <div class="mb-6">
          <div class="text-base font-semibold text-gray-900 dark:text-white mb-3 flex-1">
            <TextRenderer :text="currentQuestion.question" />
          </div>
        </div>

        <div class="space-y-3 mb-6">
          <div
            v-for="(option, optionIndex) in currentQuestion.options"
            :key="optionIndex"
            class="flex items-center p-4 rounded-lg border"
            :class="[
              !showAnswer
                ? 'cursor-pointer hover:bg-blue-50 hover:border-blue-300 hover:shadow-md dark:hover:bg-blue-900/10 dark:hover:border-blue-600'
                : 'cursor-default',
              showAnswer && optionIndex === currentQuestion.correctAnswer
                ? 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-700'
                : showAnswer &&
                    selectedOption === optionIndex &&
                    optionIndex !== currentQuestion.correctAnswer
                  ? 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-700'
                  : 'bg-gray-50 border-gray-200 dark:bg-gray-700 dark:border-gray-600'
            ]"
            @click="selectOption(optionIndex)"
          >
            <div class="flex items-center w-full">
              <div
                class="w-4 h-4 rounded-full border-2 mr-4 flex items-center justify-center"
                :class="[
                  showAnswer && optionIndex === currentQuestion.correctAnswer
                    ? 'border-green-500 bg-green-500'
                    : showAnswer &&
                        selectedOption === optionIndex &&
                        optionIndex !== currentQuestion.correctAnswer
                      ? 'border-red-500 bg-red-500'
                      : 'border-gray-300 dark:border-gray-600'
                ]"
              >
                <div
                  v-if="
                    showAnswer &&
                    (optionIndex === currentQuestion.correctAnswer ||
                      selectedOption === optionIndex)
                  "
                  class="w-2 h-2 rounded-full bg-white"
                ></div>
              </div>
              <span
                class="text-base font-medium flex-1"
                :class="[
                  showAnswer && optionIndex === currentQuestion.correctAnswer
                    ? 'text-green-800 dark:text-green-300'
                    : showAnswer &&
                        selectedOption === optionIndex &&
                        optionIndex !== currentQuestion.correctAnswer
                      ? 'text-red-800 dark:text-red-300'
                      : 'text-gray-700 dark:text-gray-300'
                ]"
              >
                <TextRenderer :text="option" />
              </span>
              <div
                v-if="showAnswer && optionIndex === currentQuestion.correctAnswer"
                class="ml-auto"
              >
                <CheckIcon class="w-5 text-green-600 dark:text-green-400" />
              </div>
              <div
                v-if="
                  showAnswer &&
                  selectedOption === optionIndex &&
                  optionIndex !== currentQuestion.correctAnswer
                "
                class="ml-auto"
              >
                <XIcon class="w-5 text-red-600 dark:text-red-400" />
              </div>
            </div>
          </div>
        </div>

        <div class="flex justify-center items-center">
          <div class="flex space-x-3">
            <button
              v-if="showAnswer && currentQuestionIndex < questions.length - 1"
              @click="nextQuestion"
              class="cursor-pointer px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg"
            >
              Siguiente
            </button>

            <button
              v-if="showAnswer && currentQuestionIndex === questions.length - 1"
              @click="finishQuiz"
              class="cursor-pointer px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg"
            >
              Finalizar
            </button>
          </div>
        </div>
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
            Reintentar Quiz
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
import CheckIcon from "@/components/icons/CheckIcon.vue"
import LoadingSpinnerIcon from "@/components/icons/LoadingSpinnerIcon.vue"
import XIcon from "@/components/icons/XIcon.vue"
import TextRenderer from "@/components/TextRenderer.vue"
import { QuizLoader } from "@/composables/useQuizLoader"
import "katex/dist/katex.min.css"
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const quizContent = ref("")
const loading = ref(true)
const currentQuestionIndex = ref(0)
const answers = ref<Array<{ questionId: number; selectedOption: number; isCorrect: boolean }>>([])
const selectedOption = ref<number | null>(null)
const showAnswer = ref(false)
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

const selectOption = (optionIndex: number) => {
  if (!showAnswer.value && currentQuestion.value) {
    selectedOption.value = optionIndex

    const answerData = {
      questionId: currentQuestion.value.id,
      selectedOption: optionIndex,
      isCorrect: optionIndex === currentQuestion.value.correctAnswer
    }

    answers.value.push(answerData)
    showAnswer.value = true
  }
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
    selectedOption.value = null
    showAnswer.value = false
  }
}

const finishQuiz = () => {
  quizFinished.value = true
}

const restartQuiz = () => {
  currentQuestionIndex.value = 0
  answers.value = []
  selectedOption.value = null
  showAnswer.value = false
  quizFinished.value = false
}
</script>
