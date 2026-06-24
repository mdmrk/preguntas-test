<template>
  <button
    @click="toggleConfetti"
    class="nav-button"
    :aria-label="confettiEnabled ? 'Disable confetti' : 'Enable confetti'"
    :aria-pressed="confettiEnabled"
  >
    <ConfettiIcon class="w-5 h-5" :class="{ 'opacity-40': !confettiEnabled }" />
  </button>
</template>

<script setup lang="ts">
import ConfettiIcon from "@/components/icons/ConfettiIcon.vue"
import { useConfettiEnabled } from "@/composables/useConfettiEnabled"

const { confettiEnabled, toggleConfetti } = useConfettiEnabled()
</script>
