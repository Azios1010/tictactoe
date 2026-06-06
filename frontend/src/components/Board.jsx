import Square from './Square'

function Board({ board, onSquareClick, disabled, lastMove, consultantMoves = [] }) {
  const getConsultantInfo = (row, col) => {
    return consultantMoves.find((m) => m.row === row && m.col === col)
  }


  return (
    <div className="board" role="grid" aria-label="Gomoku board">
      {board.map((row, rowIndex) =>
        row.map((cell, colIndex) => (
          <Square
            key={`${rowIndex}-${colIndex}`}
            value={cell}
            onClick={() => onSquareClick(rowIndex, colIndex)}
            disabled={disabled}
            highlight={lastMove?.row === rowIndex && lastMove?.col === colIndex}
            consultantInfo={getConsultantInfo(rowIndex, colIndex)}
          />
        ))
      )}
    </div>
  )
}

export default Board


