export function formatTestTitle(id: string): string {
  return id
    .split("-")
    .map((word, index) =>
      index === 0 ? word.toUpperCase() : word.charAt(0).toUpperCase() + word.slice(1),
    )
    .join(" ")
}

export function shuffle<T>(array: readonly T[]): T[] {
  const result = [...array]

  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[result[i], result[j]] = [result[j], result[i]]
  }

  return result
}
