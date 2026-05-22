<template>
  <Teleport to="body">
    <div
      v-if="open"
      class="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="report-title"
    >
      <div class="absolute inset-0 bg-black/50" @click="close" />

      <div
        class="relative bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-md p-6 flex flex-col gap-4"
      >
        <div class="flex items-center justify-between">
          <h2 id="report-title" class="text-base font-semibold text-gray-900 dark:text-gray-50">
            Reportar problema
          </h2>
          <button @click="close" class="nav-button" aria-label="Cerrar">
            <XIcon class="w-4 h-4" />
          </button>
        </div>

        <p class="text-sm text-gray-500 dark:text-gray-400">
          Describe el problema con esta pregunta. El reporte es anónimo.
        </p>

        <textarea
          v-model="message"
          :disabled="status === 'sending' || status === 'sent'"
          placeholder="Ej: La respuesta correcta marcada es incorrecta, hay una errata en el enunciado…"
          rows="4"
          class="w-full rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-50 text-sm p-3 resize-none outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        />

        <div v-if="status === 'error'" class="text-sm text-red-600 dark:text-red-400">
          Error al enviar el reporte. Intenta de nuevo.
        </div>

        <div v-if="status === 'sent'" class="text-sm text-green-600 dark:text-green-400">
          Reporte enviado. ¡Gracias!
        </div>

        <div class="flex justify-end gap-2">
          <button
            @click="close"
            class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer"
          >
            Cancelar
          </button>
          <button
            @click="submit"
            :disabled="!message.trim() || status === 'sending' || status === 'sent'"
            class="px-4 py-2 bg-red-600 hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg cursor-pointer"
          >
            {{ status === "sending" ? "Enviando…" : "Enviar reporte" }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from "vue"
import XIcon from "./icons/XIcon.vue"

const EMAILJS_SERVICE_ID = "service_525gx29"
const EMAILJS_TEMPLATE_ID = "template_2zgiy5q"
const EMAILJS_PUBLIC_KEY = "y35aevnCKYA_LrWu5"

interface Props {
  open: boolean
  questionId: number
  questionText: string
  options: string[]
}

type Emits = (e: "close") => void

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const message = ref("")
const status = ref<"idle" | "sending" | "sent" | "error">("idle")

const close = () => {
  if (status.value === "sending") return
  emit("close")
}

const submit = async () => {
  if (!message.value.trim() || status.value === "sending") return

  status.value = "sending"
  try {
    const res = await fetch("https://api.emailjs.com/api/v1.0/email/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        service_id: EMAILJS_SERVICE_ID,
        template_id: EMAILJS_TEMPLATE_ID,
        user_id: EMAILJS_PUBLIC_KEY,
        template_params: {
          pregunta_id: props.questionId,
          pregunta: props.questionText,
          opciones: props.options
            .map((opt, i) => `${String.fromCharCode(65 + i)}. ${opt}`)
            .join("\n"),
          reporte: message.value.trim(),
        },
      }),
    })

    if (res.ok) {
      status.value = "sent"
      setTimeout(close, 1500)
    } else {
      status.value = "error"
    }
  } catch {
    status.value = "error"
  }
}

watch(
  () => props.open,
  (val) => {
    if (val) {
      message.value = ""
      status.value = "idle"
    }
  },
)
</script>
