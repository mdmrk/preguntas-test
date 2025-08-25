<template>
  <button @click="cycleTheme" class="nav-button" :aria-label="`Switch from ${currentTheme} mode`">
    <SunIcon v-if="currentTheme === 'light'" class="w-5 h-5" />
    <MoonIcon v-else-if="currentTheme === 'dark'" class="w-5 h-5" />
    <DeviceIcon v-else class="w-5 h-5" />
  </button>
</template>

<script setup lang="ts">
import DeviceIcon from "@/components/icons/DeviceIcon.vue"
import MoonIcon from "@/components/icons/MoonIcon.vue"
import SunIcon from "@/components/icons/SunIcon.vue"
import { onMounted, ref } from "vue"

const currentTheme = ref<string>("device")
const themes = ["light", "dark", "device"] as const

const getSystemPreference = () => {
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
}

const loadHighlightTheme = (isDark: boolean) => {
  const existingLink = document.querySelector("link[data-highlight-theme]")
  if (existingLink) {
    existingLink.remove()
  }

  const link = document.createElement("link")
  link.rel = "stylesheet"
  link.setAttribute("data-highlight-theme", "true")
  link.href = isDark
    ? "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css"
    : "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/intellij-light.min.css"

  document.head.appendChild(link)
}

const applyTheme = (theme: string) => {
  let actualTheme = theme
  if (theme === "device") {
    actualTheme = getSystemPreference()
  }

  const isDark = actualTheme === "dark"

  if (isDark) {
    document.documentElement.classList.add("dark")
  } else {
    document.documentElement.classList.remove("dark")
  }

  loadHighlightTheme(isDark)

  if (theme === "device") {
    localStorage.removeItem("theme")
  } else {
    localStorage.setItem("theme", theme)
  }
}

const setupTheme = () => {
  const savedTheme = localStorage.getItem("theme")
  if (savedTheme && themes.includes(savedTheme as any)) {
    currentTheme.value = savedTheme
  } else {
    currentTheme.value = "device"
  }
  applyTheme(currentTheme.value)
}

const cycleTheme = () => {
  const currentIndex = themes.indexOf(currentTheme.value as any)
  const nextIndex = (currentIndex + 1) % themes.length
  currentTheme.value = themes[nextIndex]
  applyTheme(currentTheme.value)
}

onMounted(() => {
  setupTheme()

  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)")
  const handleChange = () => {
    if (currentTheme.value === "device") {
      applyTheme("device")
    }
  }
  mediaQuery.addEventListener("change", handleChange)

  return () => mediaQuery.removeEventListener("change", handleChange)
})
</script>
