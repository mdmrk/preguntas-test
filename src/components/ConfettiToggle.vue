<template>
  <button
    @click="toggleConfetti"
    class="nav-button"
    :aria-label="confettiEnabled ? 'Disable confetti' : 'Enable confetti'"
    :aria-pressed="confettiEnabled"
  >
    <ConfettiIcon v-if="confettiEnabled" class="w-5 h-5" />
    <ConfettiOffIcon v-else class="w-5 h-5 opacity-40" />
  </button>
</template>

<script setup lang="ts">
import ConfettiIcon from "@/components/icons/ConfettiIcon.vue"
import ConfettiOffIcon from "@/components/icons/ConfettiOffIcon.vue"
import { useConfettiEnabled } from "@/composables/useConfettiEnabled"

const { confettiEnabled, toggleConfetti } = useConfettiEnabled()
</script>
