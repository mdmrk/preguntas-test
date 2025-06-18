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
      path: "/test/:id",
      name: "test",
      component: () => import("@/views/TestView.vue"),
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
  const baseTitle = to.name === "test" ? "Preguntas" : "Repositorio"

  if (to.name === "test" || to.name === "repository") {
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
