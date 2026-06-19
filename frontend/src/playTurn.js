export const HUMAN_FIRST = 'human'
export const AI_FIRST = 'ai'

export function isValidFirstPlayer(firstPlayer) {
  return firstPlayer === HUMAN_FIRST || firstPlayer === AI_FIRST
}
