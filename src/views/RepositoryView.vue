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
        <div class="flex flex-col items-start space-x-4">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">{{ testTitle }}</h2>
          <span class="text-sm font-medium text-gray-600 dark:text-gray-400">
            {{ questionCountText }}
          </span>
        </div>

        <div
          v-if="availableTags.length > 0"
          class="pt-4 border-t border-gray-200 dark:border-gray-700 mt-4"
        >
          <div class="flex flex-wrap gap-2">
            <label v-for="tag in availableTags" :key="tag" class="cursor-pointer">
              <input
                :id="tag"
                type="checkbox"
                :value="tag"
                v-model="selectedTags"
                class="sr-only"
              />
              <span
                :class="[
                  'inline-flex items-center px-3 py-1 rounded-full text-sm font-medium',
                  selectedTags.includes(tag)
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600',
                  'hover:ring-2 hover:ring-blue-500 hover:ring-offset-2 dark:ring-offset-gray-800',
                ]"
              >
                {{ tag }}
              </span>
            </label>
          </div>
        </div>
      </div>

      <div v-if="filterLoading" class="flex items-center justify-center py-12">
        <LoadingSpinnerIcon />
      </div>
      <div v-else class="space-y-6">
        <div
          v-for="question in displayedQuestions"
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
            :openExplanation="false"
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
import { useHead } from "@unhead/vue"
import { computed, markRaw, onMounted, ref, shallowRef, watch } from "vue"
import { useRoute } from "vue-router"
import LoadingSpinnerIcon from "@/components/icons/LoadingSpinnerIcon.vue"
import TestQuestion from "@/components/TestQuestion.vue"
import type { Question } from "@/types/test"
import { formatTestTitle } from "@/utils"

const route = useRoute()
const questions = shallowRef<Question[]>([])
const loading = ref(true)
const filterLoading = ref(false)
const selectedTags = ref<string[]>([])
const displayedQuestions = shallowRef<Question[]>([])
const testId = computed(() => route.params.id as string)

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
  Diciembre: 11,
}

const tagSortKey = (tag: string) => {
  const [month, year] = tag.split(" ")
  if (!month || !year) return null
  const monthIndex = monthMapping[month]
  const yearNumber = parseInt(year, 10)
  if (monthIndex === undefined || Number.isNaN(yearNumber)) return null
  return yearNumber * 12 + monthIndex
}

const availableTags = computed(() => {
  const tags = new Set<string>()
  questions.value.forEach((question) => {
    question.tags?.forEach((tag) => {
      tags.add(tag)
    })
  })

  return Array.from(tags).sort((a, b) => {
    const keyA = tagSortKey(a)
    const keyB = tagSortKey(b)
    if (keyA === null || keyB === null) return a.localeCompare(b)
    return keyB - keyA
  })
})

const filteredQuestions = computed(() => {
  if (selectedTags.value.length === 0) {
    return questions.value
  }
  return questions.value.filter((question) =>
    selectedTags.value.some((tag) => question.tags?.includes(tag)),
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

const questionNumbers = computed(
  () => new Map(questions.value.map((question, index) => [question.id, index + 1])),
)

const getQuestionNumber = (question: Question) => questionNumbers.value.get(question.id) ?? 0

const testTitle = computed(() => formatTestTitle(testId.value))

useHead({
  title: computed(() => `Repositorio - ${testTitle.value}`),
  meta: [
    {
      name: "description",
      content: computed(() => `Explora las preguntas del repositorio de ${testTitle.value}.`),
    },
  ],
})

const loadTestData = async () => {
  try {
    const module = await import(`@/data/${testId.value}.json`)
    questions.value = markRaw(module.default)
    displayedQuestions.value = questions.value
  } catch (error) {
    console.error("Failed to load test:", error)
  } finally {
    loading.value = false
  }
}

watch(selectedTags, (newTags, oldTags) => {
  window.scrollTo({ top: 0, behavior: "instant" })
  const next = filteredQuestions.value
  if (newTags.length === 0 && oldTags.length > 0 && questions.value.length > 200) {
    filterLoading.value = true
    displayedQuestions.value = []
    setTimeout(() => {
      displayedQuestions.value = next
      filterLoading.value = false
    }, 0)
  } else {
    displayedQuestions.value = next
  }
})

onMounted(loadTestData)
</script>
