from __future__ import annotations

from functools import lru_cache
import os
from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

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

DIFFICULTY_CONFIGS = {
    "easy": SearchConfig(depth=2, candidate_radius=2, candidate_limit=8, time_limit_ms=400, threat_extension_depth=0),
    "medium": SearchConfig(
        depth=3,
        candidate_radius=2,
        candidate_limit=10,
        time_limit_ms=1200,
        threat_extension_depth=1,
        policy_prior_weight=10_000,
        policy_prior_top_k=24,
    ),
    "hard": SearchConfig(
        depth=4,
        candidate_radius=3,
        candidate_limit=12,
        time_limit_ms=2200,
        threat_extension_depth=1,
        policy_prior_weight=20_000,
        policy_prior_top_k=32,
    ),
}


@lru_cache(maxsize=len(DIFFICULTY_CONFIGS))
def get_ai(difficulty: str) -> GomokuAI:
    return GomokuAI(
        config=DIFFICULTY_CONFIGS[difficulty],
        memory_filename=BACKEND_DIR / "gomoku_tt.pkl",
    )


class MoveRequest(BaseModel):
    board: list[list[int]] = Field(..., description="15x15 matrix with 0 empty, -1 X, 1 O")
    player: int = Field(default=AI_STONE, description="Board stone controlled by the AI")
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


class ReportedAiMove(BaseModel):
    board: list[list[int]] = Field(..., description="Board before the AI selected this move")
    row: int = Field(..., ge=0, lt=BOARD_SIZE)
    col: int = Field(..., ge=0, lt=BOARD_SIZE)

    @field_validator("board")
    @classmethod
    def validate_board(cls, board: list[list[int]]) -> list[list[int]]:
        return MoveRequest.validate_board(board)


class GameResultRequest(BaseModel):
    difficulty: str = Field(default="medium", description="AI difficulty used during the game")
    winner: int = Field(..., description="Winning board stone: -1 X, 1 O, or 0 draw")
    ai_player: int = Field(default=AI_STONE, description="Board stone controlled by the AI")
    ai_moves: list[ReportedAiMove] = Field(default_factory=list)

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, difficulty: str) -> str:
        return MoveRequest.validate_difficulty(difficulty)

    @field_validator("winner")
    @classmethod
    def validate_winner(cls, winner: int) -> int:
        if winner not in {EMPTY, AI_STONE, HUMAN_STONE}:
            raise ValueError("Winner must be one of -1, 0, or 1.")
        return winner

    @field_validator("ai_player")
    @classmethod
    def validate_ai_player(cls, player: int) -> int:
        return MoveRequest.validate_player(player)


class GameResultResponse(BaseModel):
    recorded_moves: int
    message: str


class ConsultationRequest(BaseModel):
    board: list[list[int]] = Field(..., description="15x15 matrix with 0 empty, -1 X, 1 O")
    player: int = Field(default=AI_STONE, description="Active player side to move")
    top_k: int = Field(default=3, description="Number of top moves to recommend")

    @field_validator("board")
    @classmethod
    def validate_board(cls, board: list[list[int]]) -> list[list[int]]:
        return MoveRequest.validate_board(board)

    @field_validator("player")
    @classmethod
    def validate_player(cls, player: int) -> int:
        return MoveRequest.validate_player(player)

    @field_validator("top_k")
    @classmethod
    def validate_top_k(cls, top_k: int) -> int:
        if top_k < 1 or top_k > BOARD_SIZE * BOARD_SIZE:
            raise ValueError("top_k must be at least 1.")
        return top_k


class ConsultantMove(BaseModel):
    row: int
    col: int
    probability: float
    rank: int


class ConsultationResponse(BaseModel):
    moves: list[ConsultantMove]
    value: float
    model_available: bool
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


@app.on_event("startup")
def warm_consultant_model() -> None:
    if not any(config.policy_prior_weight > 0 for config in DIFFICULTY_CONFIGS.values()):
        return
    try:
        from dl.predict_policy import ConsultantPredictor

        ConsultantPredictor()
    except Exception as exc:
        print(f"Warning: consultant model warm-up skipped: {exc}")


@app.post("/api/get-move", response_model=MoveResponse)
def get_move(payload: MoveRequest) -> MoveResponse:
    board = [row[:] for row in payload.board]
    ai = get_ai(payload.difficulty)
    analysis = ai.get_move_analysis(board=board, player=payload.player)
    move = analysis.move
    evaluation = ai.evaluate_board_for_player(board, payload.player)

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


@app.post("/api/report-game-result", response_model=GameResultResponse)
def report_game_result(payload: GameResultRequest) -> GameResultResponse:
    ai = get_ai(payload.difficulty)
    ai_move_records = [
        {
            "board": move.board,
            "move": {"row": move.row, "col": move.col},
        }
        for move in payload.ai_moves
    ]
    recorded_moves = ai.record_game_outcome(
        ai_move_records,
        winner=payload.winner,
        player=payload.ai_player,
    )
    if recorded_moves:
        ai.save_memory()

    return GameResultResponse(
        recorded_moves=recorded_moves,
        message="Game result recorded." if recorded_moves else "No losing AI moves recorded.",
    )


@app.post("/api/get-consultation", response_model=ConsultationResponse)
def get_consultation(payload: ConsultationRequest) -> ConsultationResponse:
    try:
        from dl.predict_policy import predict_top_moves
        result = predict_top_moves(payload.board, payload.player, payload.top_k)
        if not result.get("model_available", False):
            return ConsultationResponse(
                moves=[],
                value=0.0,
                model_available=False,
                message="Consultant model is not available.",
            )

        moves = [
            ConsultantMove(
                row=m["row"],
                col=m["col"],
                probability=m["probability"],
                rank=m["rank"],
            )
            for m in result.get("moves", [])
        ]
        return ConsultationResponse(
            moves=moves,
            value=result.get("value", 0.0),
            model_available=True,
            message="Consultation generated successfully.",
        )
    except Exception as e:
        return ConsultationResponse(
            moves=[],
            value=0.0,
            model_available=False,
            message=f"Error running consultant model: {e}",
        )
