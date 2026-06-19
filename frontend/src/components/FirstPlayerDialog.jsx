import { AI_FIRST, HUMAN_FIRST } from '../playTurn'

function FirstPlayerDialog({ open, onSelect }) {
  if (!open) {
    return null
  }

  return (
    <div className="first-player-backdrop">
      <section
        className="first-player-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="first-player-title"
        aria-describedby="first-player-description"
      >
        <p className="eyebrow">New game</p>
        <h2 id="first-player-title">Who moves first?</h2>
        <p id="first-player-description">The first mover plays X. The second mover plays O.</p>

        <div className="first-player-actions">
          <button
            type="button"
            className="primary-button"
            onClick={() => onSelect(HUMAN_FIRST)}
            autoFocus
          >
            You move first
          </button>
          <button
            type="button"
            className="ghost-button"
            onClick={() => onSelect(AI_FIRST)}
          >
            AI moves first
          </button>
        </div>
      </section>
    </div>
  )
}

export default FirstPlayerDialog
