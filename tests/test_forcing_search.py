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


class ForcingSearchTest(unittest.TestCase):
    def test_find_forcing_win_prefers_open_four_creation(self) -> None:
        board = empty_board()
        board[6][5] = AI_STONE
        board[6][6] = AI_STONE
        board[6][7] = AI_STONE
        board[7][5] = HUMAN_STONE
        board[7][6] = HUMAN_STONE

        with tempfile.TemporaryDirectory() as temp_dir:
            ai = GomokuAI(
                config=SearchConfig(depth=2, candidate_radius=2, candidate_limit=8, time_limit_ms=800),
                memory_filename=Path(temp_dir) / "tt.pkl",
            )

            move = ai._find_forcing_win(
                board=board,
                attacker=AI_STONE,
                defender=HUMAN_STONE,
                depth=2,
                deadline=None,
            )

        self.assertIn(move, {(6, 4), (6, 8)})
