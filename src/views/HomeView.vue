<script setup lang="ts">
import MainButton from '@/components/MainButton.vue'
</script>

<template>
  <main class="flex flex-col items-center w-full space-y-2">
    <MainButton class="gradient-red"> First Button </MainButton>
    <MainButton class="gradient-blue"> Second Button </MainButton>
    <MainButton class="gradient-green"> Third Button </MainButton>
  </main>
</template>
