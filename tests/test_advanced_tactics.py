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
from threats import ThreatDetector


def empty_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


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


class AdvancedTacticsTest(unittest.TestCase):
    def test_broken_four_windows_are_closed_four_threats(self) -> None:
        detector = ThreatDetector()

        for line in ("0110110", "0111010", "0101110"):
            with self.subTest(line=line):
                self.assertGreaterEqual(detector.summarize_line(line).closed_four, 1)

    def test_blocked_three_shapes_are_not_forcing_threats(self) -> None:
        detector = ThreatDetector()

        for line in ("2011102", "2110102", "2011012", "2101102"):
            with self.subTest(line=line):
                summary = detector.summarize_line(line)
                self.assertEqual(summary.open_three, 0)
                self.assertEqual(summary.broken_three, 0)
                self.assertEqual(summary.double_threat, 0)

    def test_single_jump_open_three_is_not_double_counted(self) -> None:
        detector = ThreatDetector()

        for line in ("011010", "010110"):
            with self.subTest(line=line):
                summary = detector.summarize_line(line)
                self.assertEqual(summary.open_three, 1)
                self.assertEqual(summary.broken_three, 0)
                self.assertEqual(summary.double_threat, 0)

    def test_ai_creates_double_open_three(self) -> None:
        board = create_ai_double_three_board()

        with tempfile.TemporaryDirectory() as temp_dir:
            ai = GomokuAI(
                config=SearchConfig(depth=2, candidate_radius=2, candidate_limit=10, time_limit_ms=800),
                memory_filename=Path(temp_dir) / "tt.pkl",
            )
            analysis = ai.get_move_analysis(board, AI_STONE)

        self.assertEqual(analysis.move, (7, 7))
        self.assertEqual(analysis.reason, "creating_double_threat")

    def test_ai_blocks_human_double_open_three(self) -> None:
        board = create_human_double_three_board()

        with tempfile.TemporaryDirectory() as temp_dir:
            ai = GomokuAI(
                config=SearchConfig(depth=2, candidate_radius=2, candidate_limit=10, time_limit_ms=800),
                memory_filename=Path(temp_dir) / "tt.pkl",
            )
            analysis = ai.get_move_analysis(board, AI_STONE)

        self.assertEqual(analysis.move, (7, 7))
        self.assertEqual(analysis.reason, "blocking_double_threat")
