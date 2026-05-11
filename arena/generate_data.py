from __future__ import annotations

import argparse
import json
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4


ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_core import AI_STONE, BOARD_SIZE, EMPTY, GomokuAI, HUMAN_STONE, SearchConfig


@dataclass(frozen=True)
class GenerationConfig:
    games: int = 100
    depth: int = 2
    top_k: int = 3
    exploratory_moves: int = 4
    candidate_radius: int = 2
    candidate_limit: int = 14
    max_moves: int = BOARD_SIZE * BOARD_SIZE
    seed: int | None = None


def create_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def clone_board(board: list[list[int]]) -> list[list[int]]:
    return [row[:] for row in board]


def normalize_board(board: list[list[int]], current_player: int) -> list[list[int]]:
    return [[cell * current_player for cell in row] for row in board]


def get_top_k_moves(ai: GomokuAI, board: list[list[int]], k: int) -> list[tuple[int, int]]:
    if hasattr(ai, "get_top_k_moves"):
        moves = ai.get_top_k_moves(board, k)  # type: ignore[attr-defined]
        return [tuple(move) for move in moves if move is not None]

    if hasattr(ai, "_generate_candidates"):
        candidates = ai._generate_candidates(board)  # type: ignore[attr-defined]
        return list(candidates[:k])

    best_move = ai.get_best_move(board)
    return [] if best_move is None else [best_move]


def check_win(ai: GomokuAI, board: list[list[int]], player: int) -> bool:
    if hasattr(ai, "check_win"):
        return bool(ai.check_win(board, player))  # type: ignore[attr-defined]

    if hasattr(ai, "_has_winner"):
        return bool(ai._has_winner(board, player))  # type: ignore[attr-defined]

    raise AttributeError("GomokuAI must expose check_win(board, player) or _has_winner(board, player).")


def is_full(board: list[list[int]]) -> bool:
    return all(cell != EMPTY for row in board for cell in row)


def resolve_winner(ai: GomokuAI, board: list[list[int]]) -> int:
    if check_win(ai, board, AI_STONE):
        return AI_STONE
    if check_win(ai, board, HUMAN_STONE):
        return HUMAN_STONE
    return EMPTY


def outcome_for_player(winner: int, player: int) -> int:
    if winner == EMPTY:
        return 0
    return 1 if winner == player else -1


def choose_move(
    ai: GomokuAI,
    normalized_board: list[list[int]],
    turn_index: int,
    config: GenerationConfig,
    rng: random.Random,
) -> tuple[int, int] | None:
    if turn_index < config.exploratory_moves:
        candidates = get_top_k_moves(ai, normalized_board, config.top_k)
        if candidates:
            return rng.choice(candidates)
    return ai.get_best_move(normalized_board)


def play_self_play_game(
    black_ai: GomokuAI,
    white_ai: GomokuAI,
    game_index: int,
    config: GenerationConfig,
    rng: random.Random,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    board = create_board()
    game_id = uuid4().hex
    current_player = AI_STONE if game_index % 2 == 0 else HUMAN_STONE
    records: list[dict[str, Any]] = []
    winner = EMPTY

    for turn_index in range(config.max_moves):
        if resolve_winner(black_ai, board) != EMPTY or is_full(board):
            break

        acting_ai = black_ai if current_player == AI_STONE else white_ai
        board_before_move = clone_board(board)
        normalized = normalize_board(board_before_move, current_player)
        move = choose_move(acting_ai, normalized, turn_index, config, rng)
        if move is None:
            break

        row, col = move
        if board[row][col] != EMPTY:
            raise ValueError(f"Invalid move {(row, col)} selected on game {game_index}, turn {turn_index}.")

        board[row][col] = current_player
        winner = resolve_winner(black_ai, board)

        records.append(
            {
                "game_id": game_id,
                "turn_index": turn_index,
                "player": current_player,
                "normalized_board": normalized,
                "move": {"row": row, "col": col},
                "winner": EMPTY,
                "outcome": 0,
            }
        )

        if winner != EMPTY or is_full(board):
            break

        current_player *= -1

    winner = resolve_winner(black_ai, board)
    for record in records:
        record["winner"] = winner
        record["outcome"] = outcome_for_player(winner, record["player"])

    summary = {
        "game_id": game_id,
        "winner": winner,
        "moves": len(records),
        "starting_player": AI_STONE if game_index % 2 == 0 else HUMAN_STONE,
    }
    return records, summary


def append_game_records(output_path: Path, records: list[dict[str, Any]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")


def build_ai(config: GenerationConfig) -> GomokuAI:
    return GomokuAI(
        board_size=BOARD_SIZE,
        config=SearchConfig(
            depth=config.depth,
            candidate_radius=config.candidate_radius,
            candidate_limit=config.candidate_limit,
        ),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate diverse Gomoku self-play data and append to JSONL.")
    parser.add_argument("--games", type=int, default=100, help="Number of self-play games to generate.")
    parser.add_argument("--depth", type=int, default=2, help="Shared minimax depth for both agents.")
    parser.add_argument("--top-k", type=int, default=3, help="Randomly sample from the top K moves during exploration.")
    parser.add_argument("--exploratory-moves", type=int, default=4, help="Number of opening moves that use exploration.")
    parser.add_argument("--candidate-radius", type=int, default=2, help="Candidate search radius passed to GomokuAI.")
    parser.add_argument("--candidate-limit", type=int, default=14, help="Candidate move cap passed to GomokuAI.")
    parser.add_argument("--max-moves", type=int, default=BOARD_SIZE * BOARD_SIZE, help="Maximum moves per game.")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed for reproducible generation.")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT_DIR / "arena" / "data" / "training_data.jsonl",
        help="Destination JSONL file. Data is appended after each completed game.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = GenerationConfig(
        games=args.games,
        depth=args.depth,
        top_k=args.top_k,
        exploratory_moves=args.exploratory_moves,
        candidate_radius=args.candidate_radius,
        candidate_limit=args.candidate_limit,
        max_moves=args.max_moves,
        seed=args.seed,
    )
    rng = random.Random(config.seed)

    black_ai = build_ai(config)
    white_ai = build_ai(config)

    black_wins = 0
    white_wins = 0
    draws = 0

    for game_index in range(config.games):
        records, summary = play_self_play_game(
            black_ai=black_ai,
            white_ai=white_ai,
            game_index=game_index,
            config=config,
            rng=rng,
        )
        append_game_records(args.output, records)

        if summary["winner"] == AI_STONE:
            black_wins += 1
        elif summary["winner"] == HUMAN_STONE:
            white_wins += 1
        else:
            draws += 1

        print(
            f"game={game_index + 1}/{config.games} "
            f"winner={summary['winner']} moves={summary['moves']} "
            f"score(B/W/D)={black_wins}/{white_wins}/{draws}"
        )

    print(
        json.dumps(
            {
                "games": config.games,
                "black_wins": black_wins,
                "white_wins": white_wins,
                "draws": draws,
                "output": str(args.output.resolve()),
                "seed": config.seed,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
