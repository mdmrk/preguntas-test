<template>
  <div class="bg-gray-800 rounded-lg text-gray-50">
    <div class="mb-6">
      <h3 class="text-md text-gray-100">
        <MathRenderer :text="question.question" />
      </h3>
    </div>
    <div class="space-y-3 mb-6">
      <button
        v-for="(option, index) in question.options"
        :key="index"
        @click="selectAnswer(index)"
        :disabled="answered"
        :class="['w-full text-left p-3 rounded-lg border-2', getOptionClass(index)]"
      >
        <MathRenderer :text="option" />
      </button>
    </div>
    <div v-if="answered && question.explanation" class="mb-6">
      <div class="p-4 bg-blue-600 rounded-lg border border-blue-500">
        <h4 class="font-semibold mb-2 text-blue-100">Explicación</h4>
        <div class="text-blue-50">
          <MathRenderer :text="question.explanation" />
        </div>
      </div>
    </div>
    <div v-if="answered" class="text-center">
      <button
        @click="$emit('next')"
        class="bg-blue-600 hover:bg-blue-700 font-semibold py-3 px-8 rounded-lg"
      >
        Siguiente
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue"
import MathRenderer from "./MathRenderer.vue"

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
    return "border-gray-600 bg-gray-900 hover:border-blue-400 hover:bg-blue-600 hover:bg-opacity-20 cursor-pointer"
  }
  if (index === props.question.correctAnswer) {
    return "border-green-600 bg-green-900"
  }
  if (index === selectedOption.value && !isCorrect.value) {
    return "border-red-600 bg-red-900"
  }
  return "border-gray-600 bg-gray-900 cursor-not-allowed opacity-75"
}
</script>
