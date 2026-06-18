import test from 'node:test'
import assert from 'node:assert/strict'
import {
  AI_FIRST,
  HUMAN_FIRST,
  getNextFirstPlayer
} from './playTurn.js'

test('new games alternate human, AI, then human again', () => {
  const secondGame = getNextFirstPlayer(HUMAN_FIRST)
  const thirdGame = getNextFirstPlayer(secondGame)

  assert.equal(secondGame, AI_FIRST)
  assert.equal(thirdGame, HUMAN_FIRST)
})
