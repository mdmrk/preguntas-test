<template>
  <div class="max-w-4xl mx-auto">
    <div v-if="loading" class="flex items-center justify-center py-12">
      <LoadingSpinnerIcon />
      <span class="sr-only">Cargando...</span>
    </div>

    <template v-else-if="questions.length > 0">
      <div
        class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 mb-6"
      >
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-4">
            <span
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
            >
              {{ currentQuestionIndex + 1 }} / {{ questions.length }}
            </span>

            <div v-if="stats.answered > 0" class="flex items-center space-x-4 text-sm font-medium">
              <div class="flex items-center space-x-1">
                <div class="w-3 h-3 rounded-full bg-green-500" />
                <span class="text-green-600 dark:text-green-400">{{ stats.correct }}</span>
              </div>
              <div class="flex items-center space-x-1">
                <div class="w-3 h-3 rounded-full bg-red-500" />
                <span class="text-red-600 dark:text-red-400">{{ stats.incorrect }}</span>
              </div>
              <span class="text-blue-600 dark:text-blue-400">{{ stats.percentageRounded }}%</span>
            </div>
          </div>
          <div>
            <h1 class="text-lg font-semibold text-gray-900 dark:text-white">
              {{ testTitle }}
            </h1>
          </div>
        </div>

        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 flex overflow-hidden">
          <div
            v-if="stats.answered > 0"
            class="bg-green-500 dark:bg-green-400 transition-all duration-300"
            :class="progressBarClasses"
            :style="{ width: `${stats.percentage}%` }"
          />
          <div
            v-if="stats.incorrect > 0"
            class="bg-red-500 dark:bg-red-400 transition-all duration-300 rounded-r-full"
            :style="{ width: `${stats.incorrectPercentage}%` }"
          />
          <div
            v-if="stats.answered === 0"
            class="bg-gray-300 dark:bg-gray-600 flex-1 rounded-full"
          />
        </div>
      </div>

      <TestQuestion
        v-if="currentQuestion && !testFinished"
        :question="currentQuestion"
        @answered="handleAnswer"
        @next="nextQuestion"
      />

      <div
        v-if="testFinished"
        class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6"
      >
        <div class="text-center">
          <div class="mb-4">
            <div class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ finalPercentage }}%
            </div>
            <div class="text-gray-600 dark:text-gray-400">
              {{ stats.correct }} de {{ questions.length }} respuestas correctas
            </div>
          </div>

          <div class="flex justify-center space-x-8 mb-6">
            <div class="text-center">
              <div class="text-2xl font-bold text-green-600 dark:text-green-400">
                {{ stats.correct }}
              </div>
              <div class="text-sm text-gray-600 dark:text-gray-400">Correctas</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-red-600 dark:text-red-400">
                {{ stats.incorrect }}
              </div>
              <div class="text-sm text-gray-600 dark:text-gray-400">Incorrectas</div>
            </div>
          </div>

          <button
            @click="restartTest"
            class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg cursor-pointer"
          >
            Reintentar
          </button>
        </div>
      </div>
    </template>

    <div v-else class="text-center py-12">
      <p class="text-gray-500 dark:text-gray-400">No se encontraron preguntas.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import LoadingSpinnerIcon from "@/components/icons/LoadingSpinnerIcon.vue"
import TestQuestion from "@/components/TestQuestion.vue"
import { TestLoader } from "@/composables/useTestLoader"
import "katex/dist/katex.min.css"
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"

interface Answer {
  questionId: number
  selectedOption: number
  isCorrect: boolean
}

const route = useRoute()
const testContent = ref("")
const loading = ref(true)
const currentQuestionIndex = ref(0)
const answers = ref<Answer[]>([])
const testFinished = ref(false)

const testId = computed(() => route.params.id as string)
const year = computed(() => route.params.year as string | undefined)

const loader = new TestLoader()

const questions = computed(() => {
  if (!testContent.value) return []
  const allQuestions = loader.parseTestText(testContent.value)
  if (year.value !== undefined) {
    return allQuestions.filter((q) => q.tags && q.tags.some((tag) => tag.includes(year.value!)))
  }
  return allQuestions
})

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value] || null)

const testTitle = computed(() => {
  let base = testId.value
    .split("-")
    .map((word, index) => {
      if (index === 0) {
        return word.toUpperCase()
      }
      return word.charAt(0).toUpperCase() + word.slice(1)
    })
    .join(" ")
  if (year.value !== undefined) {
    base += ` ${year.value}`
  }
  return base
})

const stats = computed(() => {
  const answered = answers.value.length
  const correct = answers.value.filter((answer) => answer.isCorrect).length
  const incorrect = answered - correct
  const percentage = answered > 0 ? (correct / answered) * 100 : 0
  const incorrectPercentage = answered > 0 ? (incorrect / answered) * 100 : 0
  const percentageRounded = Math.round(percentage)

  return {
    answered,
    correct,
    incorrect,
    percentage,
    incorrectPercentage,
    percentageRounded
  }
})

const progressBarClasses = computed(() => ({
  "rounded-l-full": true,
  "rounded-r-full": stats.value.incorrect === 0
}))

const finalPercentage = computed(() => Math.round(stats.value.percentage * 10) / 10)

const handleAnswer = (answer: Answer) => {
  answers.value.push(answer)
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
  } else {
    testFinished.value = true
  }
}

const restartTest = () => {
  currentQuestionIndex.value = 0
  answers.value = []
  testFinished.value = false
}

const loadTestData = async () => {
  try {
    const module = await import(`@/data/${testId.value}.txt?raw`)
    testContent.value = module.default
  } catch (error) {
    console.error("Failed to load test:", error)
  } finally {
    loading.value = false
  }
}

onMounted(loadTestData)
</script>
