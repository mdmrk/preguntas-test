import type { Question } from "@/types/quiz"
import { shuffle } from "@/utils"

export class QuizLoader {
  parseQuizText(text: string): Question[] {
    const chunks = text.split("\n\n")
    const questions: Question[] = []
    let questionId = 1

    for (let i = 0; i < chunks.length; i++) {
      const lines = chunks[i].split("\n").filter(Boolean)

      let questionText = ""
      let correctAnswerIndex = -1
      let image: string | undefined = undefined
      const options: string[] = []
      let parsingQuestion = false
      let parsingOption = false
      let currentOptionIndex = -1

      for (let j = 0; j < lines.length; j++) {
        const line = lines[j]

        if (line.startsWith("O:")) {
          options.push(line.substring(2))
          currentOptionIndex = options.length - 1
          parsingQuestion = false
          parsingOption = true
        } else if (line.startsWith("Q:")) {
          questionText = line.substring(2)
          parsingQuestion = true
          parsingOption = false
        } else if (line.startsWith("A:")) {
          correctAnswerIndex = parseInt(line.substring(2))
          parsingQuestion = false
          parsingOption = false
        } else if (line.startsWith("I:")) {
          image = line.substring(2).trim()
          parsingQuestion = false
          parsingOption = false
        } else if (parsingQuestion) {
          questionText += line + "\n"
        } else if (parsingOption && currentOptionIndex >= 0) {
          options[currentOptionIndex] += "\n" + line
        }
      }

      if (questionText && correctAnswerIndex >= 0 && options.length > 0) {
        questions.push({
          id: questionId++,
          question: questionText.trim(),
          options: options.map((option) => option.trim()),
          correctAnswer: correctAnswerIndex,
          image: image
        })
      }
    }

    return shuffle(questions)
  }
}
