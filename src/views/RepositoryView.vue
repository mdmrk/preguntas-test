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
          <div class="flex items-center space-x-4">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Repositorio</h2>
            <span class="text-sm font-medium text-gray-600 dark:text-gray-400">
              {{ questionCountText }}
            </span>
          </div>
        </div>

        <div
          v-if="availableTags.length > 0"
          class="pt-4 border-t border-gray-200 dark:border-gray-700 mt-4"
        >
          <div class="flex flex-wrap gap-2">
            <label v-for="tag in availableTags" :key="tag" class="cursor-pointer">
              <input type="checkbox" :value="tag" v-model="selectedTags" class="sr-only" />
              <span
                :class="[
                  'inline-flex items-center px-3 py-1 rounded-full text-sm font-medium',
                  selectedTags.includes(tag)
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600'
                ]"
              >
                {{ tag }}
              </span>
            </label>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div
          v-for="question in questions"
          v-show="isQuestionVisible(question)"
          :key="question.id"
          class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4"
        >
          <div class="flex items-center justify-between mb-4">
            <span
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
            >
              Pregunta {{ getQuestionNumber(question) }}
            </span>
            <div class="flex flex-wrap gap-1">
              <span
                v-for="tag in question.tags"
                :key="tag"
                class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200"
              >
                {{ tag }}
              </span>
            </div>
          </div>
          <TestQuestion
            :question="question"
            :answered="true"
            :readOnly="true"
            :shuffleAnswers="false"
          />
        </div>
      </div>
    </template>
    <div v-else class="text-center py-12">
      <div
        class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-8"
      >
        <p class="text-gray-500 dark:text-gray-400 text-lg">
          No se encontraron preguntas en este repositorio.
        </p>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import LoadingSpinnerIcon from "@/components/icons/LoadingSpinnerIcon.vue"
import TestQuestion from "@/components/TestQuestion.vue"
import { TestLoader } from "@/composables/useTestLoader"
import type { Question } from "@/types/test"
import "katex/dist/katex.min.css"
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const testContent = ref("")
const loading = ref(true)
const selectedTags = ref<string[]>([])
const testId = computed(() => route.params.id as string)
const loader = new TestLoader()

const questions = computed(() => {
  if (!testContent.value) return []
  return loader.parseTestText(testContent.value, false)
})

const availableTags = computed(() => {
  const tags = new Set<string>()
  questions.value.forEach((question) => {
    question.tags.forEach((tag) => tags.add(tag))
  })

  const monthMapping: Record<string, number> = {
    Enero: 0,
    Febrero: 1,
    Marzo: 2,
    Abril: 3,
    Mayo: 4,
    Junio: 5,
    Julio: 6,
    Agosto: 7,
    Septiembre: 8,
    Octubre: 9,
    Noviembre: 10,
    Diciembre: 11
  }

  return Array.from(tags).sort((a, b) => {
    const [monthA, yearA] = a.split(" ")
    const [monthB, yearB] = b.split(" ")

    const dateA = new Date(parseInt(yearA), monthMapping[monthA] || 0)
    const dateB = new Date(parseInt(yearB), monthMapping[monthB] || 0)

    return dateB.getTime() - dateA.getTime()
  })
})

const isQuestionVisible = (question: Question): boolean => {
  if (selectedTags.value.length === 0) {
    return true
  }
  return selectedTags.value.some((tag) => question.tags.includes(tag))
}

const filteredQuestions = computed(() => {
  if (selectedTags.value.length === 0) {
    return questions.value
  }
  return questions.value.filter((question) =>
    selectedTags.value.some((tag) => question.tags.includes(tag))
  )
})

const questionCountText = computed(() => {
  const totalCount = questions.value.length
  const filteredCount = filteredQuestions.value.length
  if (selectedTags.value.length === 0) {
    return `${totalCount} preguntas únicas en total`
  }
  return `${filteredCount} de ${totalCount} preguntas mostradas`
})

const getQuestionNumber = (question: Question) => {
  return questions.value.findIndex((q) => q.id === question.id) + 1
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
