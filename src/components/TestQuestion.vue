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
      class="flex items-center p-4 rounded-lg border outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
      :class="getOptionClasses(shuffledIndex)"
      @click="selectAnswer(shuffledIndex)"
      @keydown.enter.prevent="selectAnswer(shuffledIndex)"
      @keydown.space.prevent="selectAnswer(shuffledIndex)"
      role="radio"
      :aria-checked="selectedOption === shuffledIndex"
      :tabindex="answered ? -1 : 0"
    >
      <div class="flex items-center w-full">
        <div
          class="w-4 h-4 rounded-full border-2 mr-4 flex items-center justify-center"
          :class="getRadioClasses(shuffledIndex)"
          aria-hidden="true"
        >
          <div v-if="shouldShowRadioDot(shuffledIndex)" class="w-2 h-2 rounded-full bg-white" />
        </div>

        <div
          class="text-base font-medium flex-1 min-w-0 overflow-x-auto"
          :class="getTextClasses(shuffledIndex)"
        >
          <TextRenderer :text="option" />
        </div>

        <div v-if="isCorrectOption(shuffledIndex)" class="ml-auto">
          <CheckIcon class="w-5 text-green-600 dark:text-green-400" aria-label="Correcta" />
        </div>

        <div v-if="isSelectedIncorrectOption(shuffledIndex)" class="ml-auto">
          <XIcon class="w-5 text-red-600 dark:text-red-400" aria-label="Incorrecta" />
        </div>
      </div>
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

    <button
      v-show="answered && !readOnly"
      @click="$emit('next')"
      class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg cursor-pointer"
    >
      Siguiente
    </button>
  </div>
</template>

<script setup lang="ts">
import type { Question } from "@/types/test"
import { shuffle } from "@/utils"
import { computed, ref, watch } from "vue"
import TextRenderer from "./TextRenderer.vue"
import CheckIcon from "./icons/CheckIcon.vue"
import CopiedIcon from "./icons/CopiedIcon.vue"
import CopyIcon from "./icons/CopyIcon.vue"
import XIcon from "./icons/XIcon.vue"

interface Props {
  question: Question
  readOnly?: boolean
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
  props.shuffleAnswers ? shuffle(optionIndices.value) : optionIndices.value
)

const shuffledOptions = computed(() =>
  shuffledIndices.value.map((originalIndex) => props.question.options[originalIndex])
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

  if (isCorrectOption(shuffledIndex)) {
    return `${baseClasses} bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-700`
  }

  if (isSelectedIncorrectOption(shuffledIndex)) {
    return `${baseClasses} bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-700`
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
    isCorrect: isCorrect.value
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
}

watch(() => props.question, resetQuestion)
watch(() => props.answered, resetQuestion)
</script>
