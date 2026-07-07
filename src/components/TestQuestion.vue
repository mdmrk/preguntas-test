<template>
  <div v-if="question.image" class="mb-6">
    <img :src="'/test/' + question.image" :alt="`Imagen para la pregunta: ${question.question}`" />
  </div>

  <div class="mb-6">
    <div class="text-base font-semibold mb-3 flex-1 min-w-0">
      <TextRenderer :text="question.question" />
    </div>
  </div>

  <div class="space-y-2" role="radiogroup" aria-label="Opciones de respuesta">
    <div
      v-for="(option, shuffledIndex) in shuffledOptions"
      :key="shuffledIndex"
      class="flex items-center px-4 py-3 rounded-lg border outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-gray-900"
      :class="getOptionClasses(shuffledIndex)"
      @click="selectAnswer(shuffledIndex, $event)"
      @keydown.enter.prevent="selectAnswer(shuffledIndex, $event)"
      @keydown.space.prevent="selectAnswer(shuffledIndex, $event)"
      role="radio"
      :aria-checked="selectedOption === shuffledIndex"
      :tabindex="answered ? -1 : 0"
    >
      <div class="flex items-center w-full">
        <div class="mr-3 flex items-center justify-center min-w-[1.5rem]">
          <span
            class="w-5 h-5 rounded-md flex items-center justify-center text-xs font-bold shrink-0"
            :class="getLetterClasses(shuffledIndex)"
            aria-hidden="true"
          >
            {{ String.fromCharCode(65 + shuffledIndex) }}
          </span>
        </div>

        <div class="text-base font-medium flex-1 min-w-0" :class="getTextClasses(shuffledIndex)">
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
      @click="toggleExplanation"
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
      class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg cursor-pointer w-full"
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
import confetti from "@hiseb/confetti"
import { computed, ref, watch } from "vue"
import { useConfettiEnabled } from "@/composables/useConfettiEnabled"
import type { Question } from "@/types/test"
import { shuffle } from "@/utils"
import ChevronDownIcon from "./icons/ChevronDownIcon.vue"
import CopiedIcon from "./icons/CopiedIcon.vue"
import CopyIcon from "./icons/CopyIcon.vue"
import FlagIcon from "./icons/FlagIcon.vue"
import ReportModal from "./ReportModal.vue"
import TextRenderer from "./TextRenderer.vue"

interface Props {
  question: Question
  openExplanation: boolean
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

const { confettiEnabled } = useConfettiEnabled()

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
    const mappedIndex = originalToShuffledIndex.value[props.question.answer]
    return mappedIndex !== undefined ? mappedIndex : null
  }
  return null
}

const selectedOption = ref<number | null>(getInitialSelectedOption())
const answered = ref(props.answered || false)
const copied = ref(false)
const reportOpen = ref(false)
const EXPLANATION_PREF_KEY = "explanationOpen"

const getExplanationPref = () => {
  const saved = localStorage.getItem(EXPLANATION_PREF_KEY)
  if (saved === "true") return true
  if (saved === "false") return false
  return props.openExplanation
}

const explanationOpen = ref(getExplanationPref())

const toggleExplanation = () => {
  explanationOpen.value = !explanationOpen.value
  localStorage.setItem(EXPLANATION_PREF_KEY, String(explanationOpen.value))
}

const isCorrect = computed(() => {
  if (selectedOption.value === null) return false
  const originalIndex = shuffledToOriginalIndex.value[selectedOption.value]
  return originalIndex === props.question.answer
})

const isCorrectOption = (shuffledIndex: number) => {
  if (!answered.value) return false
  const originalIndex = shuffledToOriginalIndex.value[shuffledIndex]
  return originalIndex === props.question.answer
}

const isSelectedIncorrectOption = (shuffledIndex: number) =>
  answered.value && selectedOption.value === shuffledIndex && !isCorrectOption(shuffledIndex)

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

const getLetterClasses = (shuffledIndex: number) => {
  if (answered.value && isCorrectOption(shuffledIndex)) {
    return "bg-green-500 text-white"
  }

  if (answered.value && isSelectedIncorrectOption(shuffledIndex)) {
    return "bg-red-500 text-white"
  }

  if (!answered.value && selectedOption.value === shuffledIndex) {
    return "bg-blue-500 text-white"
  }

  return "bg-gray-200 text-gray-700 dark:bg-gray-600 dark:text-gray-200"
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

const selectAnswer = (shuffledIndex: number, event?: Event) => {
  if (answered.value || props.readOnly) return

  selectedOption.value = shuffledIndex
  answered.value = true

  const originalIndex = shuffledToOriginalIndex.value[shuffledIndex]
  if (originalIndex === undefined) return

  if (isCorrect.value && confettiEnabled.value) {
    const target = event?.currentTarget as HTMLElement | undefined
    const rect = target?.getBoundingClientRect()
    confetti(
      rect
        ? { position: { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 }, fade: true }
        : {},
    )
  }

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
  explanationOpen.value = getExplanationPref()
}

watch(() => props.question, resetQuestion)
watch(() => props.answered, resetQuestion)
</script>
