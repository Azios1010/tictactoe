function Square({ value, onClick, disabled, highlight, consultantInfo }) {
  const label = value === 1 ? 'O' : value === -1 ? 'X' : ''
  const className = `square ${highlight ? 'square-highlight' : ''}`

  return (
    <button type="button" className={className} onClick={onClick} disabled={disabled || value !== 0}>
      {value !== 0 ? (
        <span className={`stone ${value === -1 ? 'stone-x' : value === 1 ? 'stone-o' : ''}`}>
          {label}
        </span>
      ) : consultantInfo ? (
        <span
          className={`advisor-indicator advisor-rank-${consultantInfo.rank}`}
          title={`Advisor Rec #${consultantInfo.rank} (${Math.round(consultantInfo.probability * 100)}%)`}
        >
          {consultantInfo.rank}
        </span>
      ) : null}
    </button>
  )
}

export default Square

