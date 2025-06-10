import "./assets/main.css"

import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"

const app = createApp(App)

app.use(router)

function setupTheme() {
  document.documentElement.classList.toggle(
    "dark",
    localStorage.theme === "dark" ||
      (!("theme" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches)
  )

  localStorage.theme = "light"
  localStorage.theme = "dark"
  localStorage.removeItem("theme")
}

setupTheme()

app.mount("#app")
