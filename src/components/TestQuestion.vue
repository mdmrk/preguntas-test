<template>
  <div v-if="question.image" class="mb-6">
    <img :src="'/test/' + question.image" :alt="`Imagen para la pregunta: ${question.question}`" />
  </div>

  <div class="mb-6">
    <div class="text-base font-semibold mb-3 flex-1 overflow-x-auto">
      <TextRenderer :text="question.question" />
    </div>
  </div>

  <div class="space-y-3" role="radiogroup" aria-label="Opciones de respuesta">
    <div
      v-for="(option, shuffledIndex) in shuffledOptions"
      :key="shuffledIndex"
      class="flex items-center p-4 rounded-lg border outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-gray-900"
      :class="getOptionClasses(shuffledIndex)"
      @click="selectAnswer(shuffledIndex)"
      @keydown.enter.prevent="selectAnswer(shuffledIndex)"
      @keydown.space.prevent="selectAnswer(shuffledIndex)"
      role="radio"
      :aria-checked="selectedOption === shuffledIndex"
      :tabindex="answered ? -1 : 0"
    >
      <div class="flex items-center w-full">
        <div class="mr-4 flex items-center justify-center min-w-[1.25rem]">
          <div
            v-if="!answered"
            class="w-4 h-4 rounded-full border-2 flex items-center justify-center"
            :class="getRadioClasses(shuffledIndex)"
            aria-hidden="true"
          >
            <div v-if="shouldShowRadioDot(shuffledIndex)" class="w-2 h-2 rounded-full bg-white" />
          </div>

          <template v-else>
            <CheckIcon
              v-if="isCorrectOption(shuffledIndex)"
              class="w-5 text-green-600 dark:text-green-400"
              aria-label="Correcta"
            />
            <XIcon
              v-else-if="isSelectedIncorrectOption(shuffledIndex)"
              class="w-5 text-red-600 dark:text-red-400"
              aria-label="Incorrecta"
            />
            <div v-else class="w-5" aria-hidden="true"></div>
          </template>
        </div>

        <div
          class="text-base font-medium flex-1 min-w-0 overflow-x-auto"
          :class="getTextClasses(shuffledIndex)"
        >
          <TextRenderer :text="option" />
        </div>
      </div>
    </div>
  </div>

  <div
    v-if="answered && question.explanation"
    class="mt-4 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
  >
    <button
      type="button"
      class="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-left bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"
      @click="explanationOpen = !explanationOpen"
      :aria-expanded="explanationOpen"
    >
      <span>Explicación</span>
      <ChevronDownIcon
        class="w-5 h-5 text-gray-500 transition-transform duration-200"
        :class="{ 'rotate-180': explanationOpen }"
        aria-hidden="true"
      />
    </button>
    <div
      v-show="explanationOpen"
      class="px-4 py-3 text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800"
    >
      <TextRenderer :text="question.explanation!" />
    </div>
  </div>

  <div class="flex justify-center items-center mt-6 space-x-3">
    <button
      @click="copyQuestion"
      class="nav-button"
      :aria-label="copied ? 'Pregunta copiada' : 'Copiar pregunta'"
    >
      <CopiedIcon v-if="copied" class="w-5 h-5 text-green-600 dark:text-green-400" />
      <CopyIcon v-else class="w-5 h-5" />
    </button>

    <button @click="reportOpen = true" class="nav-button" aria-label="Reportar problema">
      <FlagIcon class="w-5 h-5" />
    </button>

    <button
      v-show="answered && !readOnly"
      @click="$emit('next')"
      class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg cursor-pointer"
    >
      Siguiente
    </button>
  </div>

  <ReportModal
    :open="reportOpen"
    :question-id="question.id"
    :question-text="question.question"
    :options="shuffledOptions"
    @close="reportOpen = false"
  />
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue"
import type { Question } from "@/types/test"
import { shuffle } from "@/utils"
import CheckIcon from "./icons/CheckIcon.vue"
import ChevronDownIcon from "./icons/ChevronDownIcon.vue"
import CopiedIcon from "./icons/CopiedIcon.vue"
import CopyIcon from "./icons/CopyIcon.vue"
import FlagIcon from "./icons/FlagIcon.vue"
import XIcon from "./icons/XIcon.vue"
import ReportModal from "./ReportModal.vue"
import TextRenderer from "./TextRenderer.vue"

interface Props {
  question: Question
  readOnly?: boolean
  // biome-ignore lint/correctness/noVueDuplicateKeys: false positive, shadows local ref
  answered?: boolean
  shuffleAnswers?: boolean
}

interface Emits {
  (e: "answered", payload: { questionId: number; selectedOption: number; isCorrect: boolean }): void
  (e: "next"): void
}

const props = defineProps<Props>()

const emit = defineEmits<Emits>()

const optionIndices = computed(() => props.question.options.map((_, index) => index))

const shuffledIndices = computed(() =>
  props.shuffleAnswers ? shuffle(optionIndices.value) : optionIndices.value,
)

const shuffledOptions = computed(() =>
  shuffledIndices.value.map((originalIndex) => props.question.options[originalIndex]),
)

const originalToShuffledIndex = computed(() => {
  const mapping: Record<number, number> = {}
  shuffledIndices.value.forEach((originalIndex, shuffledIndex) => {
    mapping[originalIndex] = shuffledIndex
  })
  return mapping
})

const shuffledToOriginalIndex = computed(() => {
  const mapping: Record<number, number> = {}
  shuffledIndices.value.forEach((originalIndex, shuffledIndex) => {
    mapping[shuffledIndex] = originalIndex
  })
  return mapping
})

const getInitialSelectedOption = () => {
  if (props.answered) {
    const mappedIndex = originalToShuffledIndex.value[props.question.correctAnswer]
    return mappedIndex !== undefined ? mappedIndex : null
  }
  return null
}

const selectedOption = ref<number | null>(getInitialSelectedOption())
const answered = ref(props.answered || false)
const copied = ref(false)
const reportOpen = ref(false)
const explanationOpen = ref(false)

const isCorrect = computed(() => {
  if (selectedOption.value === null) return false
  const originalIndex = shuffledToOriginalIndex.value[selectedOption.value]
  return originalIndex === props.question.correctAnswer
})

const isCorrectOption = (shuffledIndex: number) => {
  if (!answered.value) return false
  const originalIndex = shuffledToOriginalIndex.value[shuffledIndex]
  return originalIndex === props.question.correctAnswer
}

const isSelectedIncorrectOption = (shuffledIndex: number) =>
  answered.value && selectedOption.value === shuffledIndex && !isCorrectOption(shuffledIndex)

const shouldShowRadioDot = (shuffledIndex: number) =>
  answered.value && (isCorrectOption(shuffledIndex) || selectedOption.value === shuffledIndex)

const getOptionClasses = (shuffledIndex: number) => {
  const baseClasses = answered.value
    ? "cursor-default"
    : "cursor-pointer hover:bg-blue-50 hover:border-blue-300 hover:shadow-md dark:hover:bg-blue-900/10 dark:hover:border-blue-600"

  const isSelected = selectedOption.value === shuffledIndex
  const ringClass = answered.value && isSelected ? "ring-2" : ""

  if (isCorrectOption(shuffledIndex)) {
    return `${baseClasses} ${ringClass} ring-green-500 bg-green-100 border-green-500 dark:bg-green-900/30 dark:border-green-500 dark:ring-green-400`
  }

  if (isSelectedIncorrectOption(shuffledIndex)) {
    return `${baseClasses} ${ringClass} ring-red-500 bg-red-100 border-red-500 dark:bg-red-900/30 dark:border-red-500 dark:ring-red-400`
  }

  return `${baseClasses} bg-gray-50 border-gray-200 dark:bg-gray-700 dark:border-gray-600`
}

const getRadioClasses = (shuffledIndex: number) => {
  if (isCorrectOption(shuffledIndex)) {
    return "border-green-500 bg-green-500"
  }

  if (isSelectedIncorrectOption(shuffledIndex)) {
    return "border-red-500 bg-red-500"
  }

  return "border-gray-300 dark:border-gray-600"
}

const getTextClasses = (shuffledIndex: number) => {
  if (isCorrectOption(shuffledIndex)) {
    return "text-green-800 dark:text-green-300"
  }

  if (isSelectedIncorrectOption(shuffledIndex)) {
    return "text-red-800 dark:text-red-300"
  }

  return "text-gray-900 dark:text-gray-50"
}

const selectAnswer = (shuffledIndex: number) => {
  if (answered.value || props.readOnly) return

  selectedOption.value = shuffledIndex
  answered.value = true

  const originalIndex = shuffledToOriginalIndex.value[shuffledIndex]
  if (originalIndex === undefined) return

  emit("answered", {
    questionId: props.question.id,
    selectedOption: originalIndex,
    isCorrect: isCorrect.value,
  })
}

const copyQuestion = async () => {
  try {
    let textToCopy = `${props.question.question}\n\n`

    shuffledOptions.value.forEach((option, index) => {
      textToCopy += `${String.fromCharCode(65 + index)}. ${option}\n`
    })

    await navigator.clipboard.writeText(textToCopy)
    copied.value = true

    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error("Failed to copy question:", err)
  }
}

const resetQuestion = () => {
  selectedOption.value = getInitialSelectedOption()
  answered.value = props.answered || false
  explanationOpen.value = false
}

watch(() => props.question, resetQuestion)
watch(() => props.answered, resetQuestion)
</script>
