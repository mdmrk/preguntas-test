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
        <div class="flex items-center justify-between">
          <h1 class="text-lg font-semibold">{{ testTitle }}</h1>

          <div class="flex items-center space-x-4">
            <span
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
            >
              {{ currentQuestionIndex + 1 }} / {{ questions.length }}
            </span>

            <div class="flex items-center space-x-4 text-sm font-medium">
              <div class="flex items-center space-x-1">
                <div class="w-2.5 h-2.5 rounded-full bg-green-500" />
                <span class="text-green-600 dark:text-green-400">{{ stats.correct }}</span>
              </div>
              <div class="flex items-center space-x-1">
                <div class="w-2.5 h-2.5 rounded-full bg-red-500" />
                <span class="text-red-600 dark:text-red-400">{{ stats.incorrect }}</span>
              </div>
              <span class="text-blue-600 dark:text-blue-400">{{
                stats.answered > 0 ? `${stats.percentageRounded}%` : "-%"
              }}</span>
            </div>
          </div>
        </div>
      </div>

      <TestQuestion
        v-if="currentQuestion && !testFinished"
        :question="currentQuestion"
        :openExplanation="true"
        @answered="handleAnswer"
        @next="nextQuestion"
        :shuffle-answers="shouldShuffleAnswers"
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
import { useHead } from "@unhead/vue"
import LoadingSpinnerIcon from "@/components/icons/LoadingSpinnerIcon.vue"
import TestQuestion from "@/components/TestQuestion.vue"
import type { Question } from "@/types/test"
import { formatTestTitle, shuffle } from "@/utils"
import "katex/dist/katex.min.css"
import { computed, markRaw, onMounted, ref, shallowRef } from "vue"
import { useRoute } from "vue-router"

interface Answer {
  questionId: number
  selectedOption: number
  isCorrect: boolean
}

const doNotShuffle: string[] = ["ped"]
const route = useRoute()
const rawQuestions = shallowRef<Question[]>([])
const loading = ref(true)
const currentQuestionIndex = ref(0)
const answers = ref<Answer[]>([])
const testFinished = ref(false)
const testId = computed(() => route.params.id as string)
const year = computed(() => route.params.year as string | undefined)

const shouldShuffleAnswers = computed(
  () => !doNotShuffle.some((str) => testTitle.value.toLowerCase().includes(str.toLowerCase())),
)

const questions = computed(() => {
  if (rawQuestions.value.length === 0) return []

  const q = shouldShuffleAnswers.value ? shuffle(rawQuestions.value) : [...rawQuestions.value]

  if (year.value && year.value.trim() !== "") {
    return q.filter((question) =>
      question.tags?.some((tag: string) => tag.includes(year.value ?? "")),
    )
  }
  return q
})

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value] || null)

const testTitle = computed(() => {
  let base = formatTestTitle(testId.value)
  if (year.value && year.value.trim() !== "") {
    base += ` ${year.value}`
  }
  return base
})

useHead({
  title: computed(() => testTitle.value),
  meta: [
    {
      name: "description",
      content: computed(() => `Practica preguntas de examen de ${testTitle.value}.`),
    },
  ],
})

const stats = computed(() => {
  const answered = answers.value.length
  const correct = answers.value.filter((answer) => answer.isCorrect).length
  const incorrect = answered - correct
  const percentage = answered > 0 ? (correct / answered) * 100 : 0
  const percentageRounded =
    percentage === 0
      ? 0
      : percentage === 100
        ? 100
        : Math.max(1, Math.min(99, Math.round(percentage)))

  return {
    answered,
    correct,
    incorrect,
    percentage,
    percentageRounded,
  }
})

const finalPercentage = computed(() => {
  const p = stats.value.percentage
  if (p === 0) return 0
  if (p === 100) return 100
  return Math.max(0.1, Math.min(99.9, Math.round(p * 10) / 10))
})

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
    const module = await import(`@/data/${testId.value}.json`)
    rawQuestions.value = markRaw(module.default)
  } catch (error) {
    console.error("Failed to load test:", error)
  } finally {
    loading.value = false
  }
}

onMounted(loadTestData)
</script>
