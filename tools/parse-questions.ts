import { readdir, readFile, writeFile } from "node:fs/promises"
import { join, parse } from "node:path"

const DATA_DIR = join(process.cwd(), "src", "data")

interface Question {
  id: number
  question: string
  options: string[]
  correctAnswer: number
  image?: string
  tags: string[]
}

function parseTestText(text: string): Question[] {
  const chunks = text.split(/^,$/m)
  const questions: Question[] = []
  let questionId = 1

  for (let i = 0; i < chunks.length; i++) {
    const lines = chunks[i]!.split("\n").filter(Boolean)

    let questionText = ""
    let correctAnswerIndex = -1
    let image: string | undefined = undefined
    const options: string[] = []
    let parsingQuestion = false
    let parsingOption = false
    let currentOptionIndex = -1
    let tags: string[] = []

    for (let j = 0; j < lines.length; j++) {
      const line = lines[j]!

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
      } else if (line.startsWith("C:")) {
        tags = line.substring(2).trim().split(";")
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
        tags,
        image
      })
    }
  }

  return questions
}

async function main() {
  console.log("Starting question parsing...")
  try {
    const files = await readdir(DATA_DIR)
    const txtFiles = files.filter((f) => f.endsWith(".txt"))

    if (txtFiles.length === 0) {
      console.log("No .txt files found in data directory.")
      return
    }

    console.log(`Found ${txtFiles.length} files to parse.`)

    for (const file of txtFiles) {
      const filePath = join(DATA_DIR, file)
      const content = await readFile(filePath, "utf-8")
      const questions = parseTestText(content)
      const outputName = parse(file).name + ".json"
      const outputPath = join(DATA_DIR, outputName)

      await writeFile(outputPath, JSON.stringify(questions))
      console.log(`Generated ${outputName} (${questions.length} questions)`)
    }

    console.log("Parsing complete!")
  } catch (error) {
    console.error("Error parsing questions:", error)
    process.exit(1)
  }
}

main()
