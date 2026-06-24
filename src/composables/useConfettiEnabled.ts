import { ref } from "vue"

const STORAGE_KEY = "confettiEnabled"

const stored = localStorage.getItem(STORAGE_KEY)
const confettiEnabled = ref(stored === null ? true : stored === "true")

export const useConfettiEnabled = () => {
  const toggleConfetti = () => {
    confettiEnabled.value = !confettiEnabled.value
    localStorage.setItem(STORAGE_KEY, String(confettiEnabled.value))
  }

  return { confettiEnabled, toggleConfetti }
}
