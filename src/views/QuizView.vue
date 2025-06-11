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
            class="bg-green-500 dark:bg-green-400 rounded-l-full"
            :style="{ width: `${(correctAnswers / questions.length) * 100}%` }"
          ></div>
          <div
            v-if="answeredQuestions > 0"
            class="bg-red-500 dark:bg-red-400"
            :style="{ width: `${(failedAnswers / questions.length) * 100}%` }"
          ></div>
          <div class="bg-gray-300 dark:bg-gray-600 flex-1 rounded-r-full"></div>
        </div>
      </div>

      <div v-if="currentQuestion" class="bg-white dark:bg-gray-800 rounded-lg">
        <div class="mb-6">
          <div class="flex items-start justify-between gap-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex-1">
              <TextRenderer :text="currentQuestion.question" />
            </h3>
            <button
              @click="copyQuestionAndAnswers"
              class="nav-button"
              title="Copiar pregunta y respuestas"
            >
              <img src="@/assets/copy.svg" alt="Copiar" class="w-5 h-5" />
            </button>
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
              <div
                v-if="
                  showAnswer &&
                  selectedOption === optionIndex &&
                  optionIndex !== currentQuestion.correctAnswer
                "
                class="ml-auto"
              >
                <svg
                  class="w-5 h-5 text-red-600 dark:text-red-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div class="flex justify-between items-center">
          <div class="flex space-x-3">
            <button
              v-if="showAnswer && currentQuestionIndex < questions.length - 1"
              @click="nextQuestion"
              class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg"
            >
              Siguiente
            </button>

            <button
              v-if="showAnswer && currentQuestionIndex === questions.length - 1"
              @click="finishQuiz"
              class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg"
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
            class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg"
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

const copyQuestionAndAnswers = async () => {
  if (!currentQuestion.value) return

  let textToCopy = `Pregunta ${currentQuestionIndex.value + 1}:\n${currentQuestion.value.question}\n\n`

  currentQuestion.value.options.forEach((option, index) => {
    const letter = String.fromCharCode(65 + index)
    const isCorrect = index === currentQuestion.value.correctAnswer
    textToCopy += `${letter}) ${option}${isCorrect ? " ✓" : ""}\n`
  })

  try {
    await navigator.clipboard.writeText(textToCopy)
    console.log("Question and answers copied to clipboard")
  } catch (err) {
    console.error("Failed to copy to clipboard:", err)
    const textArea = document.createElement("textarea")
    textArea.value = textToCopy
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand("copy")
    document.body.removeChild(textArea)
  }
}
</script>
