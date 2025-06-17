<script setup lang="ts">
import { ref } from "vue"

import MainButton from "@/components/MainButton.vue"
const ada = ref(false)
const ppss = ref(false)
</script>

<template>
  <main>
    <nav class="flex flex-col items-center w-full space-y-3">
      <MainButton id="redes" class="gradient-orange">REDES</MainButton>
      <div class="relative w-full flex flex-col items-center">
        <MainButton @click="ada = !ada" class="gradient-red relative z-10">ADA</MainButton>
        <div
          v-show="ada"
          class="flex flex-col items-center w-full space-y-3 rounded-b-3xl -mt-8 pt-11"
        >
          <MainButton id="ada-parcial-1" class="gradient-red">parcial 1</MainButton>
          <MainButton id="ada-parcial-2" class="gradient-red">parcial 2</MainButton>
          <MainButton id="ada-final" class="gradient-red">final</MainButton>
          <MainButton id="ada-final-24" class="gradient-red">final '24</MainButton>
          <MainButton id="ada-final-25" class="gradient-red">final '25</MainButton>
        </div>
      </div>
      <div class="relative w-full flex flex-col items-center">
        <MainButton @click="ppss = !ppss" class="gradient-blue relative z-10">PPSS</MainButton>
        <div
          v-show="ppss"
          class="flex flex-col items-center w-full space-y-3 rounded-b-3xl -mt-8 pt-11"
        >
          <MainButton id="ppss-parcial-1" class="gradient-blue">parcial 1</MainButton>
          <MainButton id="ppss-parcial-2" class="gradient-blue">parcial 2</MainButton>
        </div>
      </div>
      <MainButton id="gpi" class="gradient-green">GPI</MainButton>
    </nav>
  </main>
</template>
