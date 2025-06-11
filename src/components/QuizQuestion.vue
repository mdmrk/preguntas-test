<template>

    <div class="mb-6">
      <h3 class="text-lg font-medium">
        <TextRenderer :text="question.question" />
      </h3>
    </div>
    <div class="space-y-3 mb-6">
      <button
        v-for="(option, index) in question.options"
        :key="index"
        @click="selectAnswer(index)"
        :disabled="answered"
        :class="['w-full text-left p-4 rounded-lg border-2 font-medium', getOptionClass(index)]"
      >
        <TextRenderer :text="option" />
      </button>
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
    <div v-if="answered" class="text-center">
      <button
        @click="$emit('next')"
        class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white font-semibold py-3 px-8 rounded-lg"
      >
        Siguiente
      </button>
    </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue"
import TextRenderer from "./TextRenderer.vue"

interface Question {
  id: number
  question: string
  options: string[]
  correctAnswer: number
  explanation?: string
}

interface Props {
  question: Question
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
  if (answered.value) return
  selectedOption.value = index
  answered.value = true
  emit("answered", {
    questionId: props.question.id,
    selectedOption: index,
    isCorrect: isCorrect.value
  })
}

const getOptionClass = (index: number) => {
  if (!answered.value) {
    return "border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/50 cursor-pointer"
  }
  if (index === props.question.correctAnswer) {
    return "border-green-500 bg-green-50 dark:bg-green-900/50 text-green-900 dark:text-green-100"
  }
  if (index === selectedOption.value && !isCorrect.value) {
    return "border-red-500 bg-red-50 dark:bg-red-900/50 text-red-900 dark:text-red-100"
  }
  return "border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900 cursor-not-allowed opacity-60"
}
</script>
