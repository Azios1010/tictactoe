from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_core import AI_STONE, BOARD_SIZE, EMPTY, HUMAN_STONE, GomokuAI, SearchConfig


def empty_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


class LossMemoryTest(unittest.TestCase):
    def test_recorded_losing_move_is_avoided_on_same_board(self) -> None:
        board = empty_board()
        board[7][7] = HUMAN_STONE
        board[7][8] = AI_STONE

        with tempfile.TemporaryDirectory() as temp_dir:
            ai = GomokuAI(
                config=SearchConfig(depth=1, candidate_radius=1, candidate_limit=8, time_limit_ms=500),
                memory_filename=Path(temp_dir) / "tt.pkl",
            )
            first_move = ai.get_move_analysis([row[:] for row in board], AI_STONE).move
            self.assertIsNotNone(first_move)

            ai.record_losing_move(board, first_move)
            second_move = ai.get_move_analysis([row[:] for row in board], AI_STONE).move

            self.assertIsNotNone(second_move)
            self.assertNotEqual(second_move, first_move)

    def test_loss_memory_is_saved_and_loaded(self) -> None:
        board = empty_board()
        board[7][7] = HUMAN_STONE
        losing_move = (7, 8)

        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "tt.pkl"
            ai = GomokuAI(memory_filename=cache_path)
            ai.record_losing_move(board, losing_move)
            board_key = ai.compute_search_hash(board, AI_STONE)
            ai.save_memory(cache_path)

            loaded = GomokuAI(memory_filename=cache_path)

            self.assertEqual(loaded.loss_memory[board_key][losing_move], 1)

    def test_game_outcome_records_ai_moves_only_when_human_wins(self) -> None:
        first_board = empty_board()
        first_board[7][7] = HUMAN_STONE
        second_board = [row[:] for row in first_board]
        second_board[7][8] = AI_STONE
        second_board[8][8] = HUMAN_STONE

        history = [
            {"board": first_board, "move": {"row": 7, "col": 8}},
            {"board": second_board, "move": {"row": 6, "col": 8}},
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            ai = GomokuAI(memory_filename=Path(temp_dir) / "tt.pkl")

            recorded = ai.record_game_outcome(history, winner=HUMAN_STONE)

            self.assertEqual(recorded, 2)
            self.assertEqual(ai.loss_memory[ai.compute_search_hash(first_board, AI_STONE)][(7, 8)], 1)
            self.assertEqual(ai.loss_memory[ai.compute_search_hash(second_board, AI_STONE)][(6, 8)], 1)

            not_recorded = ai.record_game_outcome(history, winner=AI_STONE)

            self.assertEqual(not_recorded, 0)
            self.assertEqual(ai.loss_memory[ai.compute_search_hash(first_board, AI_STONE)][(7, 8)], 1)
