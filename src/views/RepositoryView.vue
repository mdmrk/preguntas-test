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
          v-for="question in displayedQuestions"
          :key="question.id"
          class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4"
          style="content-visibility: auto; contain-intrinsic-size: 1px 100px"
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
import type { Question } from "@/types/test"
import { useHead } from "@unhead/vue"
import { computed, markRaw, onMounted, ref, shallowRef, watch } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const questions = shallowRef<Question[]>([])
const loading = ref(true)
const selectedTags = ref<string[]>([])
const testId = computed(() => route.params.id as string)

const displayedLimit = ref(20)

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
    const partsA = a.split(" ")
    const partsB = b.split(" ")

    if (
      partsA.length < 2 ||
      partsB.length < 2 ||
      !partsA[0] ||
      !partsA[1] ||
      !partsB[0] ||
      !partsB[1]
    ) {
      return a.localeCompare(b)
    }

    const monthA = partsA[0]
    const yearA = partsA[1]
    const monthB = partsB[0]
    const yearB = partsB[1]

    const monthIndexA = monthMapping[monthA]
    const monthIndexB = monthMapping[monthB]

    if (monthIndexA === undefined || monthIndexB === undefined) {
      return a.localeCompare(b)
    }

    const dateA = new Date(parseInt(yearA), monthIndexA)
    const dateB = new Date(parseInt(yearB), monthIndexB)

    return dateB.getTime() - dateA.getTime()
  })
})

const filteredQuestions = computed(() => {
  if (selectedTags.value.length === 0) {
    return questions.value
  }
  return questions.value.filter((question) =>
    selectedTags.value.some((tag) => question.tags.includes(tag))
  )
})

const displayedQuestions = computed(() => {
  return filteredQuestions.value.slice(0, displayedLimit.value)
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

const testTitle = computed(() => {
  const base = testId.value
    .split("-")
    .map((word, index) => {
      if (index === 0) {
        return word.toUpperCase()
      }
      return word.charAt(0).toUpperCase() + word.slice(1)
    })
    .join(" ")
  return base
})

useHead({
  title: computed(() => `Repositorio - ${testTitle.value}`),
  meta: [
    {
      name: "description",
      content: computed(() => `Explora las preguntas del repositorio de ${testTitle.value}.`)
    }
  ]
})

const loadTestData = async () => {
  try {
    const module = await import(`@/data/${testId.value}.json`)
    questions.value = markRaw(module.default)
    startProgressiveRendering()
  } catch (error) {
    console.error("Failed to load test:", error)
  } finally {
    loading.value = false
  }
}

const startProgressiveRendering = () => {
  displayedLimit.value = 20

  const renderNextChunk = () => {
    if (displayedLimit.value < filteredQuestions.value.length) {
      displayedLimit.value += 50
      requestAnimationFrame(renderNextChunk)
    }
  }

  requestAnimationFrame(renderNextChunk)
}

watch(selectedTags, () => {
  displayedLimit.value = 20
  window.scrollTo({ top: 0, behavior: "instant" })
  startProgressiveRendering()
})

onMounted(loadTestData)
</script>
