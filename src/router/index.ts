import HomeView from "@/views/HomeView.vue"
import { createRouter, createWebHistory } from "vue-router"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: {
        title: "Preguntas"
      }
    },
    {
      path: "/quiz/:id",
      name: "quiz",
      component: () => import("@/views/QuizView.vue"),
      props: true,
      meta: {
        title: "Preguntas"
      }
    },
    {
      path: "/repository/:id",
      name: "repository",
      component: () => import("@/views/RepositoryView.vue"),
      props: true,
      meta: {
        title: "Repositorio"
      }
    }
  ]
})

router.beforeEach((to, _, next) => {
  const baseTitle = to.name === "quiz" ? "Preguntas" : "Repositorio"

  if (to.name === "quiz" || to.name === "repository") {
    const id = to.params.id as string
    const formattedTitle = id
      .split(/[-_]/)
      .map((word, index) => {
        if (index === 0) {
          return word.toUpperCase()
        }
        return word.charAt(0).toUpperCase() + word.slice(1)
      })
      .join(" ")
    document.title = `${baseTitle} - ${formattedTitle}`
  } else {
    document.title = "Preguntas Test"
  }

  next()
})

export default router
