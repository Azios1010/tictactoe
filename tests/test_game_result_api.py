from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_core import BOARD_SIZE, EMPTY, HUMAN_STONE
import main


def empty_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


class StubAI:
    def __init__(self) -> None:
        self.recorded_count = 0
        self.saved = False

    def record_game_outcome(self, ai_moves: list[dict], winner: int) -> int:
        self.recorded_count = len(ai_moves) if winner == HUMAN_STONE else 0
        return self.recorded_count

    def save_memory(self) -> None:
        self.saved = True


class GameResultApiTest(unittest.TestCase):
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
