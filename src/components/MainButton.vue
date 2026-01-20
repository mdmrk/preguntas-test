<template>
  <div class="w-full">
    <div
      :class="[
        'w-full md:h-26 h-18 text-left overflow-clip pl-4 rounded-3xl md:rounded-4xl relative group duration-100 ease-in hover:scale-105 hover:shadow-2xl',
        props.bg
      ]"
    >
      <button
        @click="handleClick"
        class="absolute inset-0 w-full h-full text-left cursor-pointer focus:outline-none focus:ring-4 focus:ring-white/50 rounded-3xl md:rounded-4xl z-0"
        :aria-label="props.text"
      >
        <span
          class="block md:translate-y-7 translate-y-5 truncate text-shadow-strong font-black text-gray-50 md:text-7xl text-5xl w-full pl-4"
        >
          {{ props.text }}
        </span>
      </button>

      <div v-if="props.id">
        <button
          @click.stop="navigateToRepository"
          class="absolute right-0 top-0 h-full w-16 flex items-center justify-center cursor-pointer rounded-r-3xl md:rounded-r-4xl bg-white/10 hover:bg-white/25 border-l border-white/20 z-10 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
          aria-label="Ir al repositorio"
        >
          <ListCheckIcon class="w-5 text-gray-50" />
        </button>
        <button
          v-show="props.years"
          @click.stop="toggleYears = !toggleYears"
          class="absolute right-16 top-0 h-full w-16 flex items-center justify-center cursor-pointer bg-white/10 hover:bg-white/25 border-l border-white/20 z-10 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
          :aria-expanded="toggleYears"
          aria-label="Mostrar años anteriores"
        >
          <CalendarIcon class="w-5 text-gray-50" />
        </button>
      </div>
      <div
        v-else-if="hasSlot"
        class="absolute right-0 top-0 h-full w-16 flex items-center justify-center pointer-events-none rounded-r-3xl md:rounded-r-4xl z-10"
      >
        <CaretUpDownIcon class="w-5 text-gray-50" />
      </div>
    </div>

    <div class="flex flex-col items-center w-full space-y-3 mt-3" v-if="hasSlot && toggle">
      <slot />
    </div>
    <div v-if="props.years && toggleYears" class="grid grid-cols-3 md:grid-cols-4 gap-3 mt-3">
      <button
        v-for="year in props.years.split(';')"
        :key="year"
        @click="navigateToYear(year)"
        :class="[
          'w-full md:h-20 h-12 font-black text-gray-50 md:text-5xl text-3xl text-left overflow-clip px-4 rounded-2xl md:rounded-3xl cursor-pointer hover:scale-105 hover:shadow-2xl relative group duration-100 ease-in focus:outline-none focus:ring-4 focus:ring-offset-2',
          props.bg
        ]"
      >
        <div class="md:translate-y-6 translate-y-3.5 text-shadow-strong">{{ year }}</div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import CaretUpDownIcon from "@/components/icons/CaretUpDownIcon.vue"
import ListCheckIcon from "@/components/icons/ListCheckIcon.vue"
import { ref, useSlots } from "vue"
import { useRouter } from "vue-router"
import CalendarIcon from "./icons/CalendarIcon.vue"

const router = useRouter()
const toggle = ref(false)
const toggleYears = ref(false)
const slots = useSlots()
const hasSlot = !!slots.default && slots.default().length > 0

interface Props {
  id?: string
  years?: string
  bg: string
  text: string
}

const props = defineProps<Props>()

const handleClick = () => {
  if (hasSlot) {
    toggle.value = !toggle.value
  } else if (props.id) {
    navigateToTest()
  }
}

const navigateToTest = () => {
  if (props.id) {
    router.push(`/test/${props.id}`)
  }
}

const navigateToRepository = () => {
  if (props.id) {
    router.push(`/repository/${props.id}`)
  }
}

const navigateToYear = (year: string) => {
  if (props.id) {
    router.push(`/test/${props.id}/${year}`)
  }
}
</script>

<style scoped>
.gradient-blue {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}
.gradient-purple {
  background: linear-gradient(135deg, #a855f7, #7c3aed);
}
.gradient-pink {
  background: linear-gradient(135deg, #ec4899, #e11d48);
}
.gradient-green {
  background: linear-gradient(135deg, #22c55e, #059669);
}
.gradient-orange {
  background: linear-gradient(135deg, #f97316, #dc2626);
}
.gradient-indigo {
  background: linear-gradient(135deg, #6366f1, #9333ea);
}
.gradient-teal {
  background: linear-gradient(135deg, #14b8a6, #0891b2);
}
.gradient-red {
  background: linear-gradient(135deg, #ef4444, #ec4899);
}
.gradient-yellow {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
}
.gradient-cyan {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}
.gradient-lime {
  background: linear-gradient(135deg, #84cc16, #65a30d);
}
.gradient-amber {
  background: linear-gradient(135deg, #fbbf24, #d97706);
}
.gradient-emerald {
  background: linear-gradient(135deg, #10b981, #059669);
}
.gradient-sky {
  background: linear-gradient(135deg, #0ea5e9, #0284c7);
}
.gradient-violet {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}
.gradient-rose {
  background: linear-gradient(135deg, #f43f5e, #e11d48);
}

.text-shadow-strong {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}
</style>
