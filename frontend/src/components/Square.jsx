function Square({ value, onClick, disabled, highlight }) {
  const label = value === 1 ? 'O' : value === -1 ? 'X' : ''
  const className = `square ${highlight ? 'square-highlight' : ''}`

  return (
    <button type="button" className={className} onClick={onClick} disabled={disabled || value !== 0}>
      <span className={`stone ${value === 1 ? 'stone-ai' : value === -1 ? 'stone-human' : ''}`}>
        {label}
      </span>
    </button>
  )
}

export default Square

