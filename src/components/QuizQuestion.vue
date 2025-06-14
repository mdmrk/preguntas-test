<template>
  <div v-show="question.image !== undefined" class="mb-6">
    <img :src="'/quiz/' + question.image" />
  </div>
  <div class="mb-6">
    <div class="text-base font-semibold text-gray-900 dark:text-white mb-3 flex-1">
      <TextRenderer :text="question.question" />
    </div>
  </div>

  <div class="space-y-3 mb-6">
    <div
      v-for="(option, optionIndex) in question.options"
      :key="optionIndex"
      class="flex items-center p-4 rounded-lg border"
      :class="[
        !answered
          ? 'cursor-pointer hover:bg-blue-50 hover:border-blue-300 hover:shadow-md dark:hover:bg-blue-900/10 dark:hover:border-blue-600'
          : 'cursor-default',
        answered && optionIndex === question.correctAnswer
          ? 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-700'
          : answered && selectedOption === optionIndex && optionIndex !== question.correctAnswer
            ? 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-700'
            : 'bg-gray-50 border-gray-200 dark:bg-gray-700 dark:border-gray-600'
      ]"
      @click="selectAnswer(optionIndex)"
    >
      <div class="flex items-center w-full">
        <div
          class="w-4 h-4 rounded-full border-2 mr-4 flex items-center justify-center"
          :class="[
            answered && optionIndex === question.correctAnswer
              ? 'border-green-500 bg-green-500'
              : answered && selectedOption === optionIndex && optionIndex !== question.correctAnswer
                ? 'border-red-500 bg-red-500'
                : 'border-gray-300 dark:border-gray-600'
          ]"
        >
          <div
            v-if="
              answered && (optionIndex === question.correctAnswer || selectedOption === optionIndex)
            "
            class="w-2 h-2 rounded-full bg-white"
          ></div>
        </div>
        <span
          class="text-base font-medium flex-1"
          :class="[
            answered && optionIndex === question.correctAnswer
              ? 'text-green-800 dark:text-green-300'
              : answered && selectedOption === optionIndex && optionIndex !== question.correctAnswer
                ? 'text-red-800 dark:text-red-300'
                : 'text-gray-700 dark:text-gray-300'
          ]"
        >
          <TextRenderer :text="option" />
        </span>
        <div v-if="answered && optionIndex === question.correctAnswer" class="ml-auto">
          <CheckIcon class="w-5 text-green-600 dark:text-green-400" />
        </div>
        <div
          v-if="
            answered && selectedOption === optionIndex && optionIndex !== question.correctAnswer
          "
          class="ml-auto"
        >
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

  <div v-if="answered" class="flex justify-center items-center">
    <div class="flex space-x-3">
      <button
        @click="$emit('next')"
        class="cursor-pointer px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg"
      >
        Siguiente
      </button>
    </div>
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
}

interface Emits {
  (e: "answered", payload: { questionId: number; selectedOption: number; isCorrect: boolean }): void
  (e: "next"): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const selectedOption = ref<number | null>(null)
const answered = ref(false)

const isCorrect = computed(() => {
  return selectedOption.value === props.question.correctAnswer
})

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

watch(
  () => props.question,
  () => {
    selectedOption.value = null
    answered.value = false
  }
)
</script>
