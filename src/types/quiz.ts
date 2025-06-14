export interface Question {
  id: number
  question: string
  options: string[]
  correctAnswer: number
  image?: string
  explanation?: string
}
