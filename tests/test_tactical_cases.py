from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_core import AI_STONE, EMPTY, HUMAN_STONE, GomokuAI, SearchConfig


FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "tactical_cases.jsonl"
SYMBOLS = {
    ".": EMPTY,
    "O": AI_STONE,
    "X": HUMAN_STONE,
}


def parse_board(rows: list[str]) -> list[list[int]]:
    assert len(rows) == 15
    board: list[list[int]] = []
    for row in rows:
        assert len(row) == 15
        board.append([SYMBOLS[cell] for cell in row])
    return board


def load_cases() -> list[dict]:
    return [
        json.loads(line)
        for line in FIXTURE_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class TacticalCasesTest(unittest.TestCase):
    def test_choose_expected_moves(self) -> None:
        ai = GomokuAI(
            config=SearchConfig(
                depth=3,
                candidate_radius=2,
                candidate_limit=12,
                time_limit_ms=1500,
                threat_extension_depth=1,
            ),
            memory_filename=ROOT_DIR / "tests" / "gomoku_tt_test.pkl",
        )

        failures: list[str] = []
        for case in load_cases():
            board = parse_board(case["board"])
            analysis = ai.get_move_analysis(board, case["player"])
            expected_moves = {tuple(move) for move in case["expected_moves"]}
            if analysis.move not in expected_moves:
                failures.append(
                    f"{case['name']}: got {analysis.move}, expected one of "
                    f"{sorted(expected_moves)}, reason={analysis.reason}, depth={analysis.completed_depth}"
                )

        self.assertFalse(failures, "\n".join(failures))
