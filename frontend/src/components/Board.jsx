import Square from './Square'

function Board({ board, onSquareClick, disabled, lastMove }) {
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
          />
        ))
      )}
    </div>
  )
}

export default Board

