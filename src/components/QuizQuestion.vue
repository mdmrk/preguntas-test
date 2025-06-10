<template>
  <div
    class="quiz-question bg-gradient-to-br from-gray-800 to-gray-900 rounded-3xl shadow-2xl p-8 text-gray-50"
  >
    <div class="mb-8">
      <h3 class="text-lg font mb-6 leading-relaxed">
        {{ question.question }}
      </h3>
    </div>

    <div class="space-y-4 mb-8">
      <button
        v-for="(option, index) in question.options"
        :key="index"
        @click="selectAnswer(index)"
        :disabled="answered"
        :class="[
          'w-full text-left p-2 rounded-2xl border-2 transition-all duration-300 transform hover:scale-[1.02]',
          getOptionClass(index)
        ]"
      >
        <div class="flex items-center">
          <span
            class="flex-shrink-0 w-6 h-6 rounded-full bg-gray-100 bg-opacity-20 text-gray-800 flex items-center justify-center font-bold text-sm mr-4"
          >
            {{ String.fromCharCode(65 + index) }}
          </span>
          <span class="font-medium">{{ option }}</span>
        </div>
      </button>
    </div>

    <div v-if="answered" class="mb-8">
      <div
        v-if="question.explanation"
        class="mt-6 p-6 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl shadow-lg"
      >
        <div class="flex items-start text-white">
          <div
            class="flex-shrink-0 w-8 h-8 rounded-full bg-white bg-opacity-20 flex items-center justify-center mr-4 mt-0.5"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div>
            <h4 class="font-bold mb-2">Explanation</h4>
            <p class="text-white text-opacity-90 leading-relaxed">{{ question.explanation }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="answered" class="text-center">
      <button
        @click="$emit('next')"
        class="relative overflow-hidden bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 font-bold py-4 px-10 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
      >
        <span class="relative z-10">Siguiente</span>
        <div
          class="absolute inset-0 bg-white opacity-0 hover:opacity-10 transition-opacity duration-300"
        ></div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue"

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
    return "border-gray-600 bg-gray-700 bg-opacity-50 hover:border-blue-400 hover:bg-blue-600 hover:bg-opacity-20 cursor-pointer text-gray-50 hover:text-white backdrop-blur-sm"
  }

  if (index === props.question.correctAnswer) {
    return "border-green-400 bg-gradient-to-r from-green-600 to-emerald-600 text-white shadow-lg"
  }

  if (index === selectedOption.value && !isCorrect.value) {
    return "border-red-400 bg-gradient-to-r from-red-600 to-rose-600 text-white shadow-lg"
  }

  return "border-gray-600 bg-gray-800 bg-opacity-60 cursor-not-allowed opacity-50 text-gray-400"
}
</script>
