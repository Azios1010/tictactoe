from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_core import BOARD_SIZE, EMPTY, HUMAN_STONE, MoveAnalysis
import main


def empty_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


class StubAI:
    def __init__(self) -> None:
        self.recorded_count = 0
        self.saved = False
        self.player = None

    def record_game_outcome(self, ai_moves: list[dict], winner: int, player: int = 1) -> int:
        self.player = player
        self.recorded_count = len(ai_moves) if winner == -player else 0
        return self.recorded_count

    def save_memory(self) -> None:
        self.saved = True


class StubMoveAI:
    def __init__(self) -> None:
        self.evaluated_board = None

    def get_move_analysis(self, board: list[list[int]], player: int) -> MoveAnalysis:
        return MoveAnalysis(move=(7, 7), score=float("inf"), reason="winning_move", completed_depth=0)

    def evaluate_board_for_player(self, board: list[list[int]], player: int) -> int:
        self.evaluated_board = [[cell * player for cell in row] for row in board]
        return 123


class GameResultApiTest(unittest.TestCase):
    def test_get_move_uses_finite_evaluation_for_ai_playing_x(self) -> None:
        stub_ai = StubMoveAI()
        board = empty_board()
        board[6][6] = HUMAN_STONE

        with patch.object(main, "get_ai", return_value=stub_ai):
            request = main.MoveRequest(board=board, player=HUMAN_STONE, difficulty="easy")
            response = main.get_move(request)

        self.assertEqual(response.evaluation, 123)
        self.assertEqual(stub_ai.evaluated_board[6][6], 1)

    def test_report_game_result_records_losing_ai_moves(self) -> None:
        stub_ai = StubAI()
        payload = {
            "difficulty": "medium",
            "winner": HUMAN_STONE,
            "ai_moves": [
                {
                    "board": empty_board(),
                    "row": 7,
                    "col": 8,
                }
            ],
        }

        with patch.object(main, "get_ai", return_value=stub_ai):
            request = main.GameResultRequest(**payload)
            response = main.report_game_result(request)

        self.assertEqual(response.recorded_moves, 1)
        self.assertTrue(stub_ai.saved)

    def test_report_game_result_supports_ai_playing_x(self) -> None:
        stub_ai = StubAI()
        payload = {
            "difficulty": "medium",
            "winner": 1,
            "ai_player": -1,
            "ai_moves": [
                {
                    "board": empty_board(),
                    "row": 7,
                    "col": 7,
                }
            ],
        }

        with patch.object(main, "get_ai", return_value=stub_ai):
            request = main.GameResultRequest(**payload)
            response = main.report_game_result(request)

        self.assertEqual(response.recorded_moves, 1)
        self.assertEqual(stub_ai.player, -1)
        self.assertTrue(stub_ai.saved)
