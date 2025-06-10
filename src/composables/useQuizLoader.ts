import type { Question } from "@/types/quiz"

export class QuizLoader {
  parseQuizText(text: string): Question[] {
    const chunks = text.split("\n\n")
    const questions: Question[] = []

    let i = 0
    let questionId = 1

    while (i < chunks.length) {
      const lines = chunks[i].split("\n").filter(Boolean)

      const questionText = lines[0]
      const correctAnswerIndex = parseInt(lines[1]) - 1
      const options: string[] = []

      let j = 2
      while (j < lines.length) {
        options.push(lines[j])
        j++
      }

      questions.push({
        id: questionId++,
        question: questionText,
        options,
        correctAnswer: correctAnswerIndex
      })
      i++
    }

    return questions
  }

  private isNumericLine(line: string): boolean {
    return /^\d+$/.test(line.trim())
  }
}
