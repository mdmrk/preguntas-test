<script setup lang="ts">
import MainButton from "@/components/MainButton.vue"
</script>

<template>
  <main>
    <nav class="flex flex-col items-center w-full space-y-3">
      <MainButton id="redes" bg="gradient-orange" text="REDES" />
      <MainButton bg="gradient-red" class="relative" text="ADA">
        <MainButton id="ada-parcial-1" bg="gradient-red" text="parcial 1" />
        <MainButton id="ada-parcial-2" bg="gradient-red" text="parcial 2" />
        <MainButton
          id="ada-final"
          years="2025;2024;2023;2022;2021"
          bg="gradient-red"
          text="final"
        />
      </MainButton>
      <MainButton bg="gradient-blue" class="relative" text="PPSS">
        <MainButton id="ppss-parcial-1" bg="gradient-blue" text="parcial 1" />
        <MainButton id="ppss-parcial-2" bg="gradient-blue" text="parcial 2" />
      </MainButton>
      <MainButton id="gpi" bg="gradient-green" text="GPI" />
      <MainButton id="hada" bg="gradient-indigo" text="HADA" />
      <MainButton id="dca" bg="gradient-teal" text="DCA" />
    </nav>
  </main>
</template>
