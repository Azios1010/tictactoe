export const HUMAN_FIRST = 'human'
export const AI_FIRST = 'ai'

export function isValidFirstPlayer(firstPlayer) {
  return firstPlayer === HUMAN_FIRST || firstPlayer === AI_FIRST
}

export function getPlayerStones(firstPlayer) {
  if (firstPlayer === HUMAN_FIRST) {
    return { humanStone: -1, aiStone: 1 }
  }
  if (firstPlayer === AI_FIRST) {
    return { humanStone: 1, aiStone: -1 }
  }
  return null
}
