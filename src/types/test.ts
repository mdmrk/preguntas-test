export interface Question {
  id: number
  question: string
  options: string[]
  answer: number
  image?: string
  tags?: string[]
  explanation?: string
}
