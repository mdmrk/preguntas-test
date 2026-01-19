<script setup lang="ts">
import MainButton from "@/components/MainButton.vue"
import { useHead } from "@unhead/vue"

useHead({
  title: "Inicio",
  meta: [
    {
      name: "description",
      content:
        "Selecciona una asignatura para practicar preguntas de examen: Redes, ADA, PPSS, PED, GPI, HADA, MADS, DCA."
    }
  ]
})
</script>

<template>
  <main>
    <h1 class="text-3xl font-bold text-center mb-6 text-gray-800 dark:text-gray-100">
      Preguntas Test
    </h1>
    <nav class="flex flex-col items-center w-full space-y-3">
      <MainButton id="redes" bg="gradient-orange" text="REDES" years="2025" />
      <MainButton bg="gradient-red" class="relative" text="ADA">
        <MainButton id="ada-parcial-1" bg="gradient-red" text="parcial 1" />
        <MainButton id="ada-parcial-2" bg="gradient-red" text="parcial 2" />
        <MainButton id="ada-final" years="2025;2024;2023;2022" bg="gradient-red" text="final" />
      </MainButton>
      <MainButton bg="gradient-blue" class="relative" text="PPSS">
        <MainButton id="ppss-parcial-1" bg="gradient-blue" text="parcial 1" />
        <MainButton id="ppss-parcial-2" bg="gradient-blue" text="parcial 2" />
      </MainButton>
      <MainButton id="ped" bg="gradient-amber" text="PED" />
      <MainButton id="gpi" bg="gradient-green" text="GPI" />
      <MainButton id="hada" bg="gradient-indigo" text="HADA" />
      <MainButton bg="gradient-lime" class="relative" text="MADS">
        <MainButton id="mads-parcial-1" bg="gradient-lime" text="parcial 1" />
        <MainButton id="mads-parcial-2" bg="gradient-lime" text="parcial 2" />
      </MainButton>
      <MainButton id="dca" bg="gradient-teal" text="DCA" />
    </nav>
  </main>
</template>
