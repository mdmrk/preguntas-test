export function shuffle<T>(array: T[]): T[] {
  let currentIndex = array.length,
    randomIndex

  while (currentIndex != 0) {
    randomIndex = Math.floor(Math.random() * currentIndex)
    currentIndex--
    const tempValue = array[currentIndex]!
    array[currentIndex] = array[randomIndex]!
    array[randomIndex] = tempValue
  }

  return array
}
