from __future__ import annotations

import unittest

from benchmark_ai import (
    AI_STONE,
    BOARD_SIZE,
    EMPTY,
    create_ai_win_horizontal_board,
    greedy_1ply_move,
    random_legal_move,
    summarize_accuracy,
)


def empty_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


class BenchmarkOutputTest(unittest.TestCase):
    def test_summarize_accuracy_by_agent_ignores_cases_without_expected_moves(self) -> None:
        rows = [
            {"agent": "project_easy", "expected_moves": [[7, 7]], "is_correct": True},
            {"agent": "project_easy", "expected_moves": [[6, 4]], "is_correct": False},
            {"agent": "project_easy", "expected_moves": [], "is_correct": None},
            {"agent": "project_hard", "expected_moves": [[7, 7]], "is_correct": True},
        ]

        self.assertEqual(
            summarize_accuracy(rows),
            {
                "project_easy": {"correct": 1, "total": 2, "accuracy": 0.5},
                "project_hard": {"correct": 1, "total": 1, "accuracy": 1.0},
            },
        )

    def test_random_legal_move_is_deterministic_with_seed(self) -> None:
        board = empty_board()
        board[7][7] = AI_STONE

        self.assertEqual(random_legal_move(board, seed=2026), random_legal_move(board, seed=2026))

    def test_greedy_1ply_finds_immediate_horizontal_win(self) -> None:
        board = create_ai_win_horizontal_board()

        self.assertIn(greedy_1ply_move(board), {(7, 4), (7, 9)})
