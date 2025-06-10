export interface Question {
  id: number
  question: string
  options: string[]
  correctAnswer: number
  explanation?: string
}

export interface QuizData {
  title: string
  description: string
  questions: Question[]
}
