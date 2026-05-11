from __future__ import annotations

import argparse
import json

from arena.engine import ArenaConfig, generate_self_play_games, persist_dataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Gomoku self-play arena and export training data.")
    parser.add_argument("--games", type=int, default=10, help="Number of self-play games to run.")
    parser.add_argument("--depth", type=int, default=2, help="Minimax search depth.")
    parser.add_argument("--candidate-radius", type=int, default=2, help="Candidate search radius.")
    parser.add_argument("--candidate-limit", type=int, default=14, help="Candidate move cap.")
    parser.add_argument("--max-moves", type=int, default=225, help="Maximum moves per game.")
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not write JSONL samples to disk; print summary only.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = ArenaConfig(
        depth=args.depth,
        candidate_radius=args.candidate_radius,
        candidate_limit=args.candidate_limit,
        max_moves=args.max_moves,
    )
    result = generate_self_play_games(game_count=args.games, config=config)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))

    if not args.no_save:
        output_path = persist_dataset(result["games"])
        print(f"Saved dataset to: {output_path}")


if __name__ == "__main__":
    main()
