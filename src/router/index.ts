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
      path: "/quiz/:quizId",
      name: "quiz",
      component: () => import("@/views/QuizView.vue"),
      props: true,
      meta: {
        title: "Preguntas"
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const baseTitle = "Preguntas"

  if (to.name === "quiz") {
    const quizId = to.params.quizId as string
    const formattedTitle = quizId
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
    document.title = baseTitle
  }

  next()
})

export default router
