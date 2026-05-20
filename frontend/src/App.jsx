import { useEffect, useRef, useState } from 'react'
import Board from './components/Board'

const BOARD_SIZE = 15
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''
const ARENA_API_BASE_URL = import.meta.env.VITE_ARENA_API_BASE_URL ?? 'http://127.0.0.1:8100'
const difficultyOptions = ['easy', 'medium', 'hard']

const directions = [
  [1, 0],
  [0, 1],
  [1, 1],
  [1, -1]
]

function cloneBoard(board) {
  return board.map((row) => [...row])
}

function createEmptyBoard() {
  return Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(0))
}

function isBoardFull(board) {
  return board.every((row) => row.every((cell) => cell !== 0))
}

function hasWinner(board, player) {
  for (let row = 0; row < BOARD_SIZE; row += 1) {
    for (let col = 0; col < BOARD_SIZE; col += 1) {
      if (board[row][col] !== player) {
        continue
      }

      for (const [dr, dc] of directions) {
        let count = 0
        for (let step = 0; step < 5; step += 1) {
          const nextRow = row + dr * step
          const nextCol = col + dc * step
          if (
            nextRow < 0 ||
            nextRow >= BOARD_SIZE ||
            nextCol < 0 ||
            nextCol >= BOARD_SIZE ||
            board[nextRow][nextCol] !== player
          ) {
            break
          }
          count += 1
        }

        if (count === 5) {
          return true
        }
      }
    }
  }
  return false
}

function formatWinner(value) {
  if (value === 1) {
    return 'Black AI wins'
  }
  if (value === -1) {
    return 'White AI wins'
  }
  return 'Draw'
}

function formatDifficulty(value) {
  return value.charAt(0).toUpperCase() + value.slice(1)
}

function formatReason(value) {
  return value.replaceAll('_', ' ')
}

function App() {
  const [mode, setMode] = useState('play')
  const [board, setBoard] = useState(createEmptyBoard)
  const [status, setStatus] = useState('You move first as X.')
  const [isThinking, setIsThinking] = useState(false)
  const [gameOver, setGameOver] = useState(false)
  const [lastMove, setLastMove] = useState(null)
  const [aiEvaluation, setAiEvaluation] = useState(0)
  const [aiReason, setAiReason] = useState('ready')
  const [aiCompletedDepth, setAiCompletedDepth] = useState(0)
  const [difficulty, setDifficulty] = useState('medium')
  const [arenaBatchSize, setArenaBatchSize] = useState(10)
  const [arenaSummary, setArenaSummary] = useState(null)
  const [arenaPlayback, setArenaPlayback] = useState([])
  const [isArenaRunning, setIsArenaRunning] = useState(false)
  const playbackTimersRef = useRef([])

  useEffect(() => {
    if (mode !== 'play') {
      return
    }

    if (hasWinner(board, -1)) {
      setStatus('Player wins.')
      setGameOver(true)
      return
    }

    if (hasWinner(board, 1)) {
      setStatus('AI wins.')
      setGameOver(true)
      return
    }

    if (isBoardFull(board)) {
      setStatus('Draw.')
      setGameOver(true)
    }
  }, [board, mode])

  useEffect(() => {
    return () => {
      playbackTimersRef.current.forEach((timerId) => window.clearTimeout(timerId))
    }
  }, [])

  function clearArenaPlaybackTimers() {
    playbackTimersRef.current.forEach((timerId) => window.clearTimeout(timerId))
    playbackTimersRef.current = []
  }

  function resetPlayMode() {
    clearArenaPlaybackTimers()
    setBoard(createEmptyBoard())
    setStatus('You move first as X.')
    setIsThinking(false)
    setGameOver(false)
    setLastMove(null)
    setAiEvaluation(0)
    setAiReason('ready')
    setAiCompletedDepth(0)
  }

  function resetArenaBoard(message = 'Arena ready. Run self-play to collect new samples.') {
    clearArenaPlaybackTimers()
    setBoard(createEmptyBoard())
    setStatus(message)
    setGameOver(false)
    setLastMove(null)
    setAiEvaluation(0)
    setAiReason('ready')
    setAiCompletedDepth(0)
    setArenaPlayback([])
  }

  function switchMode(nextMode) {
    setMode(nextMode)
    if (nextMode === 'play') {
      resetPlayMode()
      return
    }
    resetArenaBoard()
  }

  async function requestAiMove(nextBoard) {
    setIsThinking(true)
    setStatus('AI is thinking...')

    try {
      const response = await fetch(`${API_BASE_URL}/api/get-move`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          board: nextBoard,
          player: 1,
          difficulty
        })
      })

      if (!response.ok) {
        throw new Error('Unable to fetch a move from the backend AI.')
      }

      const data = await response.json()
      setAiEvaluation(data.evaluation)
      setAiReason(data.reason ?? 'best_search_score')
      setAiCompletedDepth(data.completed_depth ?? 0)

      if (data.row == null || data.col == null) {
        setStatus('The game is already finished.')
        setGameOver(true)
        return
      }

      setBoard((currentBoard) => {
        const updatedBoard = cloneBoard(currentBoard)
        updatedBoard[data.row][data.col] = 1
        return updatedBoard
      })
      setLastMove({ row: data.row, col: data.col })
      setStatus(`AI played row ${data.row + 1}, col ${data.col + 1}. ${formatReason(data.reason ?? 'best_search_score')}.`)
    } catch (error) {
      if (error instanceof TypeError) {
        setStatus('Backend is unreachable. Start FastAPI on port 8000.')
      } else {
        setStatus(error.message || 'Backend request failed.')
      }
    } finally {
      setIsThinking(false)
    }
  }

  function handleSquareClick(row, col) {
    if (mode !== 'play' || board[row][col] !== 0 || isThinking || gameOver) {
      return
    }

    const nextBoard = cloneBoard(board)
    nextBoard[row][col] = -1
    setBoard(nextBoard)
    setLastMove({ row, col })

    if (hasWinner(nextBoard, -1) || isBoardFull(nextBoard)) {
      return
    }

    void requestAiMove(nextBoard)
  }

  function playArenaReplay(game) {
    clearArenaPlaybackTimers()
    setArenaPlayback(game.moves)
    setBoard(createEmptyBoard())
    setLastMove(null)
    setGameOver(false)
    setAiEvaluation(0)

    if (game.moves.length === 0) {
      setStatus(`Arena complete. ${formatWinner(game.winner)}.`)
      setGameOver(true)
      return
    }

    setStatus(`Arena replay started with ${game.moves.length} moves.`)

    game.moves.forEach((move, index) => {
      const timerId = window.setTimeout(() => {
        setBoard((currentBoard) => {
          const updatedBoard = cloneBoard(currentBoard)
          updatedBoard[move.row][move.col] = move.player
          return updatedBoard
        })
        setLastMove({ row: move.row, col: move.col })
        const actor = move.player === 1 ? 'Black AI' : 'White AI'
        setStatus(`${actor} played row ${move.row + 1}, col ${move.col + 1}.`)

        if (index === game.moves.length - 1) {
          const completionTimer = window.setTimeout(() => {
            setStatus(`Arena complete. ${formatWinner(game.winner)}.`)
            setGameOver(true)
          }, 240)
          playbackTimersRef.current.push(completionTimer)
        }
      }, index * 180)

      playbackTimersRef.current.push(timerId)
    })
  }

  async function runArena() {
    clearArenaPlaybackTimers()
    resetArenaBoard('Arena is generating self-play games...')
    setIsArenaRunning(true)

    try {
      const response = await fetch(`${ARENA_API_BASE_URL}/arena/api/self-play`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          games: arenaBatchSize,
          save_to_disk: true
        })
      })

      if (!response.ok) {
        throw new Error('Arena service rejected the self-play request.')
      }

      const data = await response.json()
      setArenaSummary(data)
      playArenaReplay(data.latest_game)
    } catch (error) {
      setArenaSummary(null)
      if (error instanceof TypeError) {
        setStatus('Arena service is unreachable. Start arena/start_arena.ps1 on port 8100.')
      } else {
        setStatus(error.message || 'Arena request failed.')
      }
    } finally {
      setIsArenaRunning(false)
    }
  }

  function handleReset() {
    if (mode === 'play') {
      resetPlayMode()
      return
    }
    resetArenaBoard()
  }

  const secondaryMetric = mode === 'play' ? aiEvaluation : arenaSummary?.samples ?? 0
  const secondaryLabel = mode === 'play' ? 'Heuristic' : 'Samples'
  const detailMetric = mode === 'play' ? `${formatReason(aiReason)} / d${aiCompletedDepth}` : formatWinner(arenaSummary?.latest_game?.winner ?? 0)
  const detailLabel = mode === 'play' ? `${formatDifficulty(difficulty)} reason` : 'Latest result'
  const disabledBoard = mode === 'arena' || isThinking || gameOver

  return (
    <main className="app-shell">
      <section className="hero-panel">
        <p className="eyebrow">Gomoku Lab</p>
        <h1>{mode === 'play' ? 'Play Vs AI' : 'Arena Self-Play'}</h1>
        <p className="hero-copy">
          {mode === 'play'
            ? 'Interactive mode uses the existing FastAPI backend and minimax evaluator.'
            : 'Arena mode runs two AIs against each other, replays the latest game, and saves JSONL samples for downstream deep learning training.'}
        </p>

        <div className="mode-switch" role="tablist" aria-label="Game mode">
          <button
            type="button"
            className={`mode-button ${mode === 'play' ? 'mode-button-active' : ''}`}
            onClick={() => switchMode('play')}
          >
            Play
          </button>
          <button
            type="button"
            className={`mode-button ${mode === 'arena' ? 'mode-button-active' : ''}`}
            onClick={() => switchMode('arena')}
          >
            Arena
          </button>
        </div>

        <div className="info-grid">
          <div className="info-card">
            <span className="info-label">Status</span>
            <strong>{status}</strong>
          </div>
          <div className="info-card">
            <span className="info-label">{secondaryLabel}</span>
            <strong>{secondaryMetric}</strong>
          </div>
          <div className="info-card">
            <span className="info-label">{detailLabel}</span>
            <strong>{detailMetric}</strong>
          </div>
        </div>

        {mode === 'arena' ? (
          <div className="arena-panel">
            <label className="field-label" htmlFor="arena-games">
              Self-play games per batch
            </label>
            <input
              id="arena-games"
              className="number-input"
              type="number"
              min="1"
              max="200"
              value={arenaBatchSize}
              onChange={(event) => setArenaBatchSize(Number(event.target.value) || 1)}
            />

            <div className="action-row">
              <button type="button" className="primary-button" onClick={runArena} disabled={isArenaRunning}>
                {isArenaRunning ? 'Running...' : 'Run arena'}
              </button>
              <button type="button" className="ghost-button" onClick={handleReset} disabled={isArenaRunning}>
                Clear board
              </button>
            </div>

            <div className="arena-summary">
              <div className="summary-item">
                <span className="info-label">Wins</span>
                <strong>
                  B {arenaSummary?.black_wins ?? 0} / W {arenaSummary?.white_wins ?? 0} / D {arenaSummary?.draws ?? 0}
                </strong>
              </div>
              <div className="summary-item">
                <span className="info-label">Latest replay moves</span>
                <strong>{arenaPlayback.length}</strong>
              </div>
              <div className="summary-item">
                <span className="info-label">Dataset path</span>
                <strong className="path-text">{arenaSummary?.output_path ?? 'Not generated yet'}</strong>
              </div>
            </div>
          </div>
        ) : (
          <div className="play-controls">
            <label className="field-label" htmlFor="difficulty">
              Difficulty
            </label>
            <div className="action-row">
              <select
                id="difficulty"
                className="select-input"
                value={difficulty}
                onChange={(event) => setDifficulty(event.target.value)}
                disabled={isThinking}
              >
                {difficultyOptions.map((option) => (
                  <option key={option} value={option}>
                    {formatDifficulty(option)}
                  </option>
                ))}
              </select>
              <button type="button" className="primary-button" onClick={handleReset}>
                New game
              </button>
            </div>
            <span className="hint-text">X is the player, O is the backend AI, board size is 15x15.</span>
          </div>
        )}
      </section>

      <section className="board-panel">
        <Board board={board} onSquareClick={handleSquareClick} disabled={disabledBoard} lastMove={lastMove} />
      </section>
    </main>
  )
}

export default App
