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


def create_ai_double_three_board() -> list[list[int]]:
    board = empty_board()
    board[7][6] = AI_STONE
    board[7][8] = AI_STONE
    board[6][7] = AI_STONE
    board[8][7] = AI_STONE
    board[5][5] = HUMAN_STONE
    board[9][9] = HUMAN_STONE
    return board


def create_human_double_three_board() -> list[list[int]]:
    board = empty_board()
    board[7][6] = HUMAN_STONE
    board[7][8] = HUMAN_STONE
    board[6][7] = HUMAN_STONE
    board[8][7] = HUMAN_STONE
    board[5][5] = AI_STONE
    board[9][9] = AI_STONE
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


def normalize_expected_moves(expected_moves: list[tuple[int, int]]) -> list[list[int]]:
    return [[row, col] for row, col in expected_moves]


def is_correct_move(move: tuple[int, int] | None, expected_moves: list[tuple[int, int]]) -> bool | None:
    if not expected_moves:
        return None
    return move in set(expected_moves)


def summarize_accuracy(rows: list[dict]) -> dict[str, dict[str, float | int]]:
    summary: dict[str, dict[str, float | int]] = {}
    for row in rows:
        if not row["expected_moves"]:
            continue
        agent = row["agent"]
        if agent not in summary:
            summary[agent] = {"correct": 0, "total": 0, "accuracy": 0.0}
        summary[agent]["total"] += 1
        if row["is_correct"]:
            summary[agent]["correct"] += 1

    for row in summary.values():
        total = int(row["total"])
        correct = int(row["correct"])
        row["accuracy"] = round(correct / total, 3) if total else 0.0
    return summary


def run_center_baseline(case_name: str, board: list[list[int]], expected_moves: list[tuple[int, int]]) -> dict:
    start = time.perf_counter()
    move = center_first_move([row[:] for row in board])
    elapsed_ms = (time.perf_counter() - start) * 1000
    return {
        "case": case_name,
        "agent": "center_first_baseline",
        "move": move,
        "expected_moves": normalize_expected_moves(expected_moves),
        "is_correct": is_correct_move(move, expected_moves),
        "score": 0,
        "reason": "center_or_nearest_empty",
        "completed_depth": 0,
        "elapsed_ms": round(elapsed_ms, 2),
    }


def run_project_ai(case_name: str, board: list[list[int]], expected_moves: list[tuple[int, int]]) -> list[dict]:
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
                "expected_moves": normalize_expected_moves(expected_moves),
                "is_correct": is_correct_move(analysis.move, expected_moves),
                "score": analysis.score,
                "reason": analysis.reason,
                "completed_depth": analysis.completed_depth,
                "elapsed_ms": round(elapsed_ms, 2),
            }
        )
    return rows


def main() -> None:
    cases = [
        {"name": "opening", "board": empty_board(), "expected_moves": [(7, 7)]},
        {"name": "midgame", "board": create_midgame_board(), "expected_moves": []},
        {"name": "block_open_four", "board": create_block_open_four_board(), "expected_moves": [(7, 4), (7, 9)]},
        {"name": "forcing_open_four", "board": create_forcing_open_four_board(), "expected_moves": [(6, 4), (6, 8)]},
        {"name": "create_double_three", "board": create_ai_double_three_board(), "expected_moves": [(7, 7)]},
        {"name": "block_double_three", "board": create_human_double_three_board(), "expected_moves": [(7, 7)]},
    ]

    results: list[dict] = []
    for case in cases:
        case_name = case["name"]
        board = case["board"]
        expected_moves = case["expected_moves"]
        results.append(run_center_baseline(case_name, board, expected_moves))
        results.extend(run_project_ai(case_name, board, expected_moves))

    output = {
        "results": results,
        "accuracy_by_agent": summarize_accuracy(results),
    }

    output_path = ROOT_DIR / "benchmark_results.json"
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Case | Agent | Move | Correct | Reason | Depth | Time ms")
    print("--- | --- | --- | --- | --- | ---: | ---:")
    for row in results:
        print(
            f"{row['case']} | {row['agent']} | {row['move']} | {row['is_correct']} | {row['reason']} | "
            f"{row['completed_depth']} | {row['elapsed_ms']}"
        )
    print("Accuracy by agent:")
    for agent, summary in output["accuracy_by_agent"].items():
        print(f"{agent}: {summary['correct']}/{summary['total']} ({summary['accuracy']})")
    print(f"Saved benchmark results to {output_path}")


if __name__ == "__main__":
    main()
