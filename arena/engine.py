from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_core import AI_STONE, BOARD_SIZE, EMPTY, GomokuAI, HUMAN_STONE, SearchConfig


DIRECTIONS = ((1, 0), (0, 1), (1, 1), (1, -1))
DEFAULT_DATA_DIR = ROOT_DIR / "arena" / "data"


@dataclass(frozen=True)
class ArenaConfig:
    depth: int = 2
    candidate_radius: int = 2
    candidate_limit: int = 14
    max_moves: int = BOARD_SIZE * BOARD_SIZE
    alternate_opening: bool = True


def create_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def clone_board(board: list[list[int]]) -> list[list[int]]:
    return [row[:] for row in board]


def has_winner(board: list[list[int]], player: int) -> bool:
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] != player:
                continue
            for dr, dc in DIRECTIONS:
                if is_winning_line(board, row, col, dr, dc, player):
                    return True
    return False


def is_winning_line(board: list[list[int]], row: int, col: int, dr: int, dc: int, player: int) -> bool:
    for step in range(5):
        next_row = row + dr * step
        next_col = col + dc * step
        if not (0 <= next_row < BOARD_SIZE and 0 <= next_col < BOARD_SIZE):
            return False
        if board[next_row][next_col] != player:
            return False
    return True


def is_board_full(board: list[list[int]]) -> bool:
    return all(cell != EMPTY for row in board for cell in row)


def normalize_board(board: list[list[int]], current_player: int) -> list[list[int]]:
    return [[cell * current_player for cell in row] for row in board]


def resolve_winner(board: list[list[int]]) -> int:
    if has_winner(board, AI_STONE):
        return AI_STONE
    if has_winner(board, HUMAN_STONE):
        return HUMAN_STONE
    return EMPTY


def outcome_for_player(winner: int, player: int) -> int:
    if winner == EMPTY:
        return 0
    return 1 if winner == player else -1


def build_ai(config: ArenaConfig) -> GomokuAI:
    return GomokuAI(
        board_size=BOARD_SIZE,
        config=SearchConfig(
            depth=config.depth,
            candidate_radius=config.candidate_radius,
            candidate_limit=config.candidate_limit,
        ),
    )


def choose_move(ai: GomokuAI, board: list[list[int]], current_player: int) -> tuple[int, int] | None:
    normalized = normalize_board(board, current_player)
    return ai.get_best_move(normalized, player=AI_STONE)


def simulate_game(
    ai: GomokuAI,
    game_index: int,
    config: ArenaConfig,
) -> dict[str, Any]:
    board = create_board()
    current_player = AI_STONE if not config.alternate_opening or game_index % 2 == 0 else HUMAN_STONE
    samples: list[dict[str, Any]] = []
    moves: list[dict[str, int]] = []
    winner = EMPTY

    for turn_index in range(config.max_moves):
        if has_winner(board, AI_STONE) or has_winner(board, HUMAN_STONE) or is_board_full(board):
            break

        board_before_move = clone_board(board)
        normalized_board = normalize_board(board_before_move, current_player)
        move = ai.get_best_move(normalized_board, player=AI_STONE)
        if move is None:
            break

        row, col = move
        if board[row][col] != EMPTY:
            raise ValueError(f"AI selected occupied cell {(row, col)} on turn {turn_index}.")

        perspective_eval = ai.evaluate_board(normalized_board)
        board[row][col] = current_player
        winner = resolve_winner(board)

        move_record = {"turn": turn_index, "player": current_player, "row": row, "col": col}
        moves.append(move_record)
        samples.append(
            {
                "game_id": "",
                "turn_index": turn_index,
                "player": current_player,
                "board": board_before_move,
                "normalized_board": normalized_board,
                "move": {"row": row, "col": col},
                "evaluation": perspective_eval,
                "winner": EMPTY,
                "outcome": 0,
            }
        )

        if winner != EMPTY or is_board_full(board):
            break

        current_player *= -1

    winner = resolve_winner(board)
    game_id = uuid4().hex
    for sample in samples:
        sample["game_id"] = game_id
        sample["winner"] = winner
        sample["outcome"] = outcome_for_player(winner, sample["player"])

    return {
        "game_id": game_id,
        "winner": winner,
        "result": "draw" if winner == EMPTY else ("black" if winner == AI_STONE else "white"),
        "total_moves": len(moves),
        "moves": moves,
        "final_board": board,
        "samples": samples,
    }


def generate_self_play_games(game_count: int, config: ArenaConfig) -> dict[str, Any]:
    ai = build_ai(config)
    games = [simulate_game(ai=ai, game_index=index, config=config) for index in range(game_count)]
    total_samples = sum(len(game["samples"]) for game in games)

    return {
        "games": games,
        "summary": {
            "games": game_count,
            "samples": total_samples,
            "black_wins": sum(1 for game in games if game["winner"] == AI_STONE),
            "white_wins": sum(1 for game in games if game["winner"] == HUMAN_STONE),
            "draws": sum(1 for game in games if game["winner"] == EMPTY),
            "config": asdict(config),
        },
    }


def persist_dataset(games: list[dict[str, Any]], output_dir: Path | None = None) -> Path:
    destination_dir = output_dir or DEFAULT_DATA_DIR
    destination_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = destination_dir / f"arena_{timestamp}.jsonl"

    with output_path.open("w", encoding="utf-8") as handle:
        for game in games:
            for sample in game["samples"]:
                handle.write(json.dumps(sample, ensure_ascii=True) + "\n")

    return output_path
