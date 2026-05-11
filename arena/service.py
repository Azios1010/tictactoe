from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from arena.engine import ArenaConfig, generate_self_play_games, persist_dataset


class ArenaRequest(BaseModel):
    games: int = Field(default=1, ge=1, le=200)
    depth: int = Field(default=2, ge=1, le=4)
    candidate_radius: int = Field(default=2, ge=1, le=4)
    candidate_limit: int = Field(default=14, ge=4, le=32)
    max_moves: int = Field(default=225, ge=10, le=225)
    save_to_disk: bool = True


class ArenaResponse(BaseModel):
    games: int
    samples: int
    black_wins: int
    white_wins: int
    draws: int
    output_path: str | None
    latest_game: dict
    config: dict


app = FastAPI(title="Gomoku Arena API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/arena/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/arena/api/self-play", response_model=ArenaResponse)
def self_play(payload: ArenaRequest) -> ArenaResponse:
    config = ArenaConfig(
        depth=payload.depth,
        candidate_radius=payload.candidate_radius,
        candidate_limit=payload.candidate_limit,
        max_moves=payload.max_moves,
    )
    result = generate_self_play_games(game_count=payload.games, config=config)

    output_path: str | None = None
    if payload.save_to_disk:
        dataset_path = persist_dataset(result["games"])
        output_path = str(Path(dataset_path).resolve())

    summary = result["summary"]
    return ArenaResponse(
        games=summary["games"],
        samples=summary["samples"],
        black_wins=summary["black_wins"],
        white_wins=summary["white_wins"],
        draws=summary["draws"],
        output_path=output_path,
        latest_game=result["games"][-1],
        config=summary["config"],
    )
