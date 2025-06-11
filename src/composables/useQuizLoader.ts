import type { Question } from "@/types/quiz"

export class QuizLoader {
  parseQuizText(text: string): Question[] {
    const chunks = text.split("\n\n")
    const questions: Question[] = []
    let questionId = 1

    for (let i = 0; i < chunks.length; i++) {
      const lines = chunks[i].split("\n").filter(Boolean)

      let questionText = ""
      let correctAnswerIndex = -1
      const options: string[] = []
      let parsingQuestion = false

      for (let j = 0; j < lines.length; j++) {
        const line = lines[j].trim()

        if (line.startsWith("Q:")) {
          questionText = line.substring(2).trim()
          parsingQuestion = true
        } else if (line.startsWith("A:")) {
          correctAnswerIndex = parseInt(line.substring(2)) - 1
          parsingQuestion = false
        } else if (parsingQuestion) {
          questionText += " " + line
        } else if (line.length > 0) {
          options.push(line)
        }
      }

      if (questionText && correctAnswerIndex >= 0 && options.length > 0) {
        questions.push({
          id: questionId++,
          question: questionText.trim(),
          options,
          correctAnswer: correctAnswerIndex
        })
      }
    }

    return questions
  }
}
