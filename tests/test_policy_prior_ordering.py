from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_types import AI_STONE, BOARD_SIZE, EMPTY, SearchConfig
from ai_core import GomokuAI
from evaluator import BoardEvaluator
from move_ordering import MoveOrdering
from threats import ThreatDetector


def empty_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


class PolicyPriorOrderingTest(unittest.TestCase):
    def test_policy_prior_can_promote_root_candidate(self) -> None:
        board = empty_board()
        board[7][7] = AI_STONE
        preferred = (6, 6)
        calls = 0

        def provider(_board: list[list[int]], candidates: list[tuple[int, int]]) -> dict[tuple[int, int], float]:
            nonlocal calls
            calls += 1
            self.assertIn(preferred, candidates)
            return {preferred: 1.0}

        threat_detector = ThreatDetector()
        ordering = MoveOrdering(
            config=SearchConfig(
                candidate_radius=1,
                candidate_limit=4,
                policy_prior_weight=100_000,
                policy_prior_top_k=4,
            ),
            evaluator=BoardEvaluator(threat_detector=threat_detector),
            threat_detector=threat_detector,
            policy_prior_provider=provider,
        )

        candidates = ordering.generate_candidates(board, use_policy_prior=True)

        self.assertEqual(candidates[0], preferred)
        self.assertEqual(calls, 1)

    def test_policy_prior_is_not_used_unless_requested(self) -> None:
        board = empty_board()
        board[7][7] = AI_STONE

        def provider(_board: list[list[int]], _candidates: list[tuple[int, int]]) -> dict[tuple[int, int], float]:
            raise AssertionError("policy prior should not be called below root")

        threat_detector = ThreatDetector()
        ordering = MoveOrdering(
            config=SearchConfig(
                candidate_radius=1,
                candidate_limit=4,
                policy_prior_weight=100_000,
            ),
            evaluator=BoardEvaluator(threat_detector=threat_detector),
            threat_detector=threat_detector,
            policy_prior_provider=provider,
        )

        candidates = ordering.generate_candidates(board, use_policy_prior=False)

        self.assertGreater(len(candidates), 0)

    def test_policy_prior_is_not_called_for_immediate_win(self) -> None:
        board = empty_board()
        board[7][4] = AI_STONE
        board[7][5] = AI_STONE
        board[7][6] = AI_STONE
        board[7][7] = AI_STONE

        ai = GomokuAI(
            config=SearchConfig(
                depth=2,
                candidate_radius=2,
                candidate_limit=8,
                policy_prior_weight=100_000,
            ),
            memory_filename=ROOT_DIR / "tests" / "gomoku_tt_test.pkl",
        )

        def provider(_board: list[list[int]], _candidates: list[tuple[int, int]]) -> dict[tuple[int, int], float]:
            raise AssertionError("policy prior should not run before immediate win checks")

        ai.move_ordering.policy_prior_provider = provider

        analysis = ai.get_move_analysis(board, AI_STONE)

        self.assertEqual(analysis.reason, "winning_move")
        self.assertIn(analysis.move, {(7, 3), (7, 8)})


if __name__ == "__main__":
    unittest.main()
