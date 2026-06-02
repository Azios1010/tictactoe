from __future__ import annotations

from functools import lru_cache
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from ai_core import AI_STONE, BOARD_SIZE, EMPTY, GomokuAI, HUMAN_STONE, SearchConfig


def get_cors_origins() -> list[str]:
    raw_origins = os.getenv("FRONTEND_ORIGINS", "*").strip()
    if not raw_origins or raw_origins == "*":
        return ["*"]
    return [origin.strip().rstrip("/") for origin in raw_origins.split(",") if origin.strip()]


CORS_ORIGINS = get_cors_origins()
app = FastAPI(title="Gomoku Minimax API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials="*" not in CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

BACKEND_DIR = Path(__file__).resolve().parent
DIFFICULTY_CONFIGS = {
    "easy": SearchConfig(depth=2, candidate_radius=2, candidate_limit=8, time_limit_ms=400, threat_extension_depth=0),
    "medium": SearchConfig(depth=3, candidate_radius=2, candidate_limit=10, time_limit_ms=1200, threat_extension_depth=1),
    "hard": SearchConfig(depth=4, candidate_radius=3, candidate_limit=12, time_limit_ms=2200, threat_extension_depth=1),
}


@lru_cache(maxsize=len(DIFFICULTY_CONFIGS))
def get_ai(difficulty: str) -> GomokuAI:
    return GomokuAI(
        config=DIFFICULTY_CONFIGS[difficulty],
        memory_filename=BACKEND_DIR / "gomoku_tt.pkl",
    )


class MoveRequest(BaseModel):
    board: list[list[int]] = Field(..., description="15x15 matrix with 0 empty, -1 human, 1 AI")
    player: int = Field(default=AI_STONE, description="Player controlled by the AI")
    difficulty: str = Field(default="medium", description="AI difficulty: easy, medium, or hard")

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

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, difficulty: str) -> str:
        normalized = difficulty.lower().strip()
        if normalized not in DIFFICULTY_CONFIGS:
            raise ValueError("Difficulty must be one of easy, medium, or hard.")
        return normalized


class MoveResponse(BaseModel):
    row: int | None
    col: int | None
    evaluation: int
    reason: str
    difficulty: str
    completed_depth: int
    message: str


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "Gomoku Minimax API",
        "health": "/api/health",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/get-move", response_model=MoveResponse)
def get_move(payload: MoveRequest) -> MoveResponse:
    board = [row[:] for row in payload.board]
    ai = get_ai(payload.difficulty)
    analysis = ai.get_move_analysis(board=board, player=payload.player)
    move = analysis.move
    evaluation = ai.evaluate_board(board)

    if move is None:
        return MoveResponse(
            row=None,
            col=None,
            evaluation=evaluation,
            reason=analysis.reason,
            difficulty=payload.difficulty,
            completed_depth=analysis.completed_depth,
            message="Game already finished.",
        )

    row, col = move
    if board[row][col] != EMPTY:
        raise HTTPException(status_code=400, detail="AI selected an invalid move.")

    return MoveResponse(
        row=row,
        col=col,
        evaluation=evaluation,
        reason=analysis.reason,
        difficulty=payload.difficulty,
        completed_depth=analysis.completed_depth,
        message="Move generated successfully.",
    )
