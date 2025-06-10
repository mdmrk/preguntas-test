<template>
  <button
    class="w-full h-22 font-black text-8xl text-left overflow-clip pl-4 rounded-4xl cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-2xl gradient-blue text-white"
  >
    <div class="translate-y-5"><slot /></div>
  </button>
</template>

<script setup lang="ts"></script>

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
