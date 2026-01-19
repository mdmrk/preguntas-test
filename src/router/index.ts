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
      path: "/test/:id/:year?",
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

export default router
