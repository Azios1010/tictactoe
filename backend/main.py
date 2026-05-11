from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from ai_core import AI_STONE, BOARD_SIZE, EMPTY, GomokuAI, HUMAN_STONE


app = FastAPI(title="Gomoku Minimax API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai = GomokuAI()


class MoveRequest(BaseModel):
    board: list[list[int]] = Field(..., description="15x15 matrix with 0 empty, -1 human, 1 AI")
    player: int = Field(default=AI_STONE, description="Player controlled by the AI")

    @field_validator("board")
    @classmethod
    def validate_board(cls, board: list[list[int]]) -> list[list[int]]:
        if len(board) != BOARD_SIZE:
            raise ValueError(f"Board must contain {BOARD_SIZE} rows.")
        for row in board:
            if len(row) != BOARD_SIZE:
                raise ValueError(f"Each row must contain {BOARD_SIZE} columns.")
            for cell in row:
                if cell not in {EMPTY, AI_STONE, HUMAN_STONE}:
                    raise ValueError("Board cells must be one of -1, 0, or 1.")
        return board

    @field_validator("player")
    @classmethod
    def validate_player(cls, player: int) -> int:
        if player not in {AI_STONE, HUMAN_STONE}:
            raise ValueError("Player must be either 1 or -1.")
        return player


class MoveResponse(BaseModel):
    row: int | None
    col: int | None
    evaluation: int
    message: str


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/get-move", response_model=MoveResponse)
def get_move(payload: MoveRequest) -> MoveResponse:
    board = [row[:] for row in payload.board]
    move = ai.get_best_move(board=board, player=payload.player)
    evaluation = ai.evaluate_board(board)

    if move is None:
        return MoveResponse(row=None, col=None, evaluation=evaluation, message="Game already finished.")

    row, col = move
    if board[row][col] != EMPTY:
        raise HTTPException(status_code=400, detail="AI selected an invalid move.")

    return MoveResponse(
        row=row,
        col=col,
        evaluation=evaluation,
        message="Move generated successfully.",
    )

