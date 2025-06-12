<template>
  <button
    @click="navigateToQuiz"
    class="w-full h-26 font-black text-gray-50 text-7xl text-left overflow-clip pl-4 rounded-4xl cursor-pointer hover:scale-105 hover:shadow-2xl gradient-blue relative group"
  >
    <div
      v-show="id !== undefined"
      @click.prevent.stop="navigateToRepository"
      class="absolute right-0 top-0 h-full w-16 flex items-center justify-center cursor-pointer transition-all rounded-r-4xl bg-white/10 hover:bg-white/25 border-l border-white/20 z-10"
    >
      <ListCheckIcon class="w-5" />
    </div>
    <div class="translate-y-7"><slot /></div>
  </button>
</template>
<script setup lang="ts">
import ListCheckIcon from "@/components/icons/ListCheckIcon.vue"
import { useRouter } from "vue-router"
const router = useRouter()
interface Props {
  id?: string
}
const props = defineProps<Props>()
const navigateToQuiz = () => {
  if (props.id) {
    router.push(`/quiz/${props.id}`)
  }
}
const navigateToRepository = () => {
  if (props.id) {
    router.push(`/repository/${props.id}`)
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
</style>
