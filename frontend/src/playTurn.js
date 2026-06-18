export const HUMAN_FIRST = 'human'
export const AI_FIRST = 'ai'

export function getNextFirstPlayer(currentFirstPlayer) {
  return currentFirstPlayer === HUMAN_FIRST ? AI_FIRST : HUMAN_FIRST
}
