from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_core import AI_STONE, BOARD_SIZE, EMPTY, HUMAN_STONE, GomokuAI
from main import DIFFICULTY_CONFIGS


def empty_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def create_midgame_board() -> list[list[int]]:
    board = empty_board()
    placements = [
        (7, 7, HUMAN_STONE),
        (7, 8, AI_STONE),
        (8, 7, HUMAN_STONE),
        (6, 8, AI_STONE),
        (8, 8, HUMAN_STONE),
        (6, 7, AI_STONE),
    ]
    for row, col, stone in placements:
        board[row][col] = stone
    return board


def create_block_open_four_board() -> list[list[int]]:
    board = empty_board()
    for col in range(5, 9):
        board[7][col] = HUMAN_STONE
    board[6][6] = AI_STONE
    board[8][6] = AI_STONE
    return board


def create_forcing_open_four_board() -> list[list[int]]:
    board = empty_board()
    board[6][5] = AI_STONE
    board[6][6] = AI_STONE
    board[6][7] = AI_STONE
    board[7][5] = HUMAN_STONE
    board[7][6] = HUMAN_STONE
    return board


def center_first_move(board: list[list[int]]) -> tuple[int, int] | None:
    center = BOARD_SIZE // 2
    if board[center][center] == EMPTY:
        return (center, center)
    for radius in range(1, BOARD_SIZE):
        for row in range(max(0, center - radius), min(BOARD_SIZE, center + radius + 1)):
            for col in range(max(0, center - radius), min(BOARD_SIZE, center + radius + 1)):
                if board[row][col] == EMPTY:
                    return (row, col)
    return None


def run_center_baseline(case_name: str, board: list[list[int]]) -> dict:
    start = time.perf_counter()
    move = center_first_move([row[:] for row in board])
    elapsed_ms = (time.perf_counter() - start) * 1000
    return {
        "case": case_name,
        "agent": "center_first_baseline",
        "move": move,
        "score": 0,
        "reason": "center_or_nearest_empty",
        "completed_depth": 0,
        "elapsed_ms": round(elapsed_ms, 2),
    }


def run_project_ai(case_name: str, board: list[list[int]]) -> list[dict]:
    rows: list[dict] = []
    for difficulty, config in DIFFICULTY_CONFIGS.items():
        ai = GomokuAI(
            config=config,
            memory_filename=ROOT_DIR / "tests" / f"benchmark_tt_{difficulty}.pkl",
        )
        start = time.perf_counter()
        analysis = ai.get_move_analysis([row[:] for row in board], AI_STONE)
        elapsed_ms = (time.perf_counter() - start) * 1000
        rows.append(
            {
                "case": case_name,
                "agent": f"project_{difficulty}",
                "move": analysis.move,
                "score": analysis.score,
                "reason": analysis.reason,
                "completed_depth": analysis.completed_depth,
                "elapsed_ms": round(elapsed_ms, 2),
            }
        )
    return rows


def main() -> None:
    cases = {
        "opening": empty_board(),
        "midgame": create_midgame_board(),
        "block_open_four": create_block_open_four_board(),
        "forcing_open_four": create_forcing_open_four_board(),
    }

    results: list[dict] = []
    for case_name, board in cases.items():
        results.append(run_center_baseline(case_name, board))
        results.extend(run_project_ai(case_name, board))

    output_path = ROOT_DIR / "benchmark_results.json"
    output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Case | Agent | Move | Reason | Depth | Time ms")
    print("--- | --- | --- | --- | ---: | ---:")
    for row in results:
        print(
            f"{row['case']} | {row['agent']} | {row['move']} | {row['reason']} | "
            f"{row['completed_depth']} | {row['elapsed_ms']}"
        )
    print(f"Saved benchmark results to {output_path}")


if __name__ == "__main__":
    main()
