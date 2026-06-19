import test from 'node:test'
import assert from 'node:assert/strict'
import {
  AI_FIRST,
  HUMAN_FIRST,
  isValidFirstPlayer
} from './playTurn.js'

test('dialog accepts the human and AI opening choices', () => {
  assert.equal(isValidFirstPlayer(HUMAN_FIRST), true)
  assert.equal(isValidFirstPlayer(AI_FIRST), true)
})

test('dialog rejects unknown opening choices', () => {
  assert.equal(isValidFirstPlayer('random'), false)
  assert.equal(isValidFirstPlayer(null), false)
})
