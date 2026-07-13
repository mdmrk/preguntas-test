<template>
  <button @click="cycleTheme" class="nav-button" :aria-label="`Switch from ${currentTheme} mode`">
    <SunIcon v-if="currentTheme === 'light'" class="w-5 h-5" />
    <MoonIcon v-else-if="currentTheme === 'dark'" class="w-5 h-5" />
    <DeviceIcon v-else class="w-5 h-5" />
  </button>
</template>

<script setup lang="ts">
import darkThemeUrl from "highlight.js/styles/github-dark.min.css?url"
import lightThemeUrl from "highlight.js/styles/intellij-light.min.css?url"
import { onMounted, onUnmounted, ref } from "vue"
import DeviceIcon from "@/components/icons/DeviceIcon.vue"
import MoonIcon from "@/components/icons/MoonIcon.vue"
import SunIcon from "@/components/icons/SunIcon.vue"

const themes = ["light", "dark", "device"] as const
type Theme = (typeof themes)[number]

const currentTheme = ref<Theme>("device")

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
  link.href = isDark ? darkThemeUrl : lightThemeUrl

  document.head.appendChild(link)
}

const applyTheme = (theme: Theme) => {
  let actualTheme = theme
  if (theme === "device") {
    actualTheme = getSystemPreference()
  }

  const isDark = actualTheme === "dark"

  document.documentElement.classList.toggle("dark", isDark)

  loadHighlightTheme(isDark)

  if (theme === "device") {
    localStorage.removeItem("theme")
  } else {
    localStorage.setItem("theme", theme)
  }
}

const isValidTheme = (theme: string): theme is Theme => {
  return themes.includes(theme as Theme)
}

const setupTheme = () => {
  const savedTheme = localStorage.getItem("theme")
  if (savedTheme && isValidTheme(savedTheme)) {
    currentTheme.value = savedTheme
  } else {
    currentTheme.value = "device"
  }
  applyTheme(currentTheme.value)
}

const cycleTheme = () => {
  const currentIndex = themes.indexOf(currentTheme.value)
  const nextIndex = (currentIndex + 1) % themes.length
  const nextTheme = themes[nextIndex]
  if (nextTheme) {
    currentTheme.value = nextTheme
    applyTheme(currentTheme.value)
  }
}

const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)")
const handleSystemPreferenceChange = () => {
  if (currentTheme.value === "device") {
    applyTheme("device")
  }
}

onMounted(() => {
  setupTheme()
  mediaQuery.addEventListener("change", handleSystemPreferenceChange)
})

onUnmounted(() => {
  mediaQuery.removeEventListener("change", handleSystemPreferenceChange)
})
</script>
