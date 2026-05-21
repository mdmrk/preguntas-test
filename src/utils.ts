export function shuffle<T>(array: T[]): T[] {
  let currentIndex = array.length
  let randomIndex: number

  while (currentIndex !== 0) {
    randomIndex = Math.floor(Math.random() * currentIndex)
    currentIndex--
    // biome-ignore lint/style/noNonNullAssertion: indices are always in bounds within the loop
    const tempValue = array[currentIndex]!
    // biome-ignore lint/style/noNonNullAssertion: indices are always in bounds within the loop
    array[currentIndex] = array[randomIndex]!
    array[randomIndex] = tempValue
  }

  return array
}
