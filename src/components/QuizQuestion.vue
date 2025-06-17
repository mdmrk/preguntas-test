<template>
  <div v-show="question.image !== undefined" class="mb-6">
    <img :src="'/quiz/' + question.image" />
  </div>

  <div class="mb-6">
    <div class="text-base font-semibold mb-3 flex-1">
      <TextRenderer :text="question.question" />
    </div>
  </div>

  <div class="space-y-3">
    <div
      v-for="(option, optionIndex) in question.options"
      :key="optionIndex"
      class="flex items-center p-4 rounded-lg border"
      :class="getOptionClasses(optionIndex)"
      @click="selectAnswer(optionIndex)"
    >
      <div class="flex items-center w-full">
        <div
          class="w-4 h-4 rounded-full border-2 mr-4 flex items-center justify-center"
          :class="getRadioClasses(optionIndex)"
        >
          <div v-if="shouldShowRadioDot(optionIndex)" class="w-2 h-2 rounded-full bg-white" />
        </div>

        <span class="text-base font-medium flex-1" :class="getTextClasses(optionIndex)">
          <TextRenderer :text="option" />
        </span>

        <div v-if="isCorrectOption(optionIndex)" class="ml-auto">
          <CheckIcon class="w-5 text-green-600 dark:text-green-400" />
        </div>

        <div v-if="isSelectedIncorrectOption(optionIndex)" class="ml-auto">
          <XIcon class="w-5 text-red-600 dark:text-red-400" />
        </div>
      </div>
    </div>
  </div>

  <div v-if="answered && question.explanation" class="mb-6">
    <div
      class="p-4 bg-blue-50 dark:bg-blue-900/50 border border-blue-200 dark:border-blue-700 rounded-lg"
    >
      <h4 class="font-semibold mb-2 text-blue-900 dark:text-blue-100">Explicación</h4>
      <div class="text-blue-800 dark:text-blue-200">
        <TextRenderer :text="question.explanation" />
      </div>
    </div>
  </div>

  <div v-if="answered && !readOnly" class="flex justify-center items-center mt-6">
    <button
      @click="$emit('next')"
      class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg cursor-pointer"
    >
      Siguiente
    </button>
  </div>
</template>

<script setup lang="ts">
import type { Question } from "@/types/quiz"
import { computed, ref, watch } from "vue"
import TextRenderer from "./TextRenderer.vue"
import CheckIcon from "./icons/CheckIcon.vue"
import XIcon from "./icons/XIcon.vue"

interface Props {
  question: Question
  readOnly?: boolean
  answered?: boolean
}

interface Emits {
  (e: "answered", payload: { questionId: number; selectedOption: number; isCorrect: boolean }): void
  (e: "next"): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const selectedOption = ref<number | null>(props.answered ? props.question.correctAnswer : null)
const answered = ref(props.answered || false)

const isCorrect = computed(() => selectedOption.value === props.question.correctAnswer)

const isCorrectOption = (optionIndex: number) =>
  answered.value && optionIndex === props.question.correctAnswer

const isSelectedIncorrectOption = (optionIndex: number) =>
  answered.value &&
  selectedOption.value === optionIndex &&
  optionIndex !== props.question.correctAnswer

const shouldShowRadioDot = (optionIndex: number) =>
  answered.value &&
  (optionIndex === props.question.correctAnswer || selectedOption.value === optionIndex)

const getOptionClasses = (optionIndex: number) => {
  const baseClasses = answered.value
    ? "cursor-default"
    : "cursor-pointer hover:bg-blue-50 hover:border-blue-300 hover:shadow-md dark:hover:bg-blue-900/10 dark:hover:border-blue-600"

  if (isCorrectOption(optionIndex)) {
    return `${baseClasses} bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-700`
  }

  if (isSelectedIncorrectOption(optionIndex)) {
    return `${baseClasses} bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-700`
  }

  return `${baseClasses} bg-gray-50 border-gray-200 dark:bg-gray-700 dark:border-gray-600`
}

const getRadioClasses = (optionIndex: number) => {
  if (isCorrectOption(optionIndex)) {
    return "border-green-500 bg-green-500"
  }

  if (isSelectedIncorrectOption(optionIndex)) {
    return "border-red-500 bg-red-500"
  }

  return "border-gray-300 dark:border-gray-600"
}

const getTextClasses = (optionIndex: number) => {
  if (isCorrectOption(optionIndex)) {
    return "text-green-800 dark:text-green-300"
  }

  if (isSelectedIncorrectOption(optionIndex)) {
    return "text-red-800 dark:text-red-300"
  }

  return "text-gray-900 dark:text-gray-50"
}

const selectAnswer = (index: number) => {
  if (answered.value || props.readOnly) return

  selectedOption.value = index
  answered.value = true

  emit("answered", {
    questionId: props.question.id,
    selectedOption: index,
    isCorrect: isCorrect.value
  })
}

const resetQuestion = () => {
  selectedOption.value = props.answered ? props.question.correctAnswer : null
  answered.value = props.answered || false
}

watch(() => props.question, resetQuestion)
</script>
