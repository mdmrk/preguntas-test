<template>
  <div class="max-w-2xl mx-auto">
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
      <span class="ml-3 text-gray-300 font-medium">Cargando...</span>
    </div>

    <div v-if="questions.length > 0">
      <div class="bg-gray-800 rounded-lg mb-6 text-gray-50">
        <div class="flex items-center justify-between mb-3">
          <div class="text-blue-400 text-sm">
            {{ currentQuestionIndex + 1 }} / {{ questions.length }}
          </div>

          <div v-show="answeredQuestions > 0" class="flex items-center space-x-3 text-sm">
            <div class="text-green-400">{{ correctAnswers }}</div>
            <div class="text-red-400">{{ failedAnswers }}</div>
            <div class="text-green-400">{{ correctAnswersPercentage.toFixed(0) }}%</div>
          </div>
        </div>

        <div class="w-full bg-gray-700 rounded-full h-2 flex overflow-hidden">
          <div
            v-show="answeredQuestions > 0"
            class="bg-green-400 rounded-l-full"
            :style="{ width: `${correctAnswersPercentage.toFixed(0)}%` }"
          ></div>
          <div v-show="answeredQuestions > 0" class="bg-red-400 flex-1 rounded-r-full"></div>
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
