from __future__ import annotations

from ai_types import AI_STONE, BOARD_SIZE, DIRECTIONS, EMPTY, HUMAN_STONE, ThreatSummary, WIN_LENGTH
from board_rules import in_bounds
from threats import ThreatDetector


class BoardEvaluator:
    PATTERN_SCORES = {
        (5, 0): 1_000_000,
        (4, 2): 100_000,
        (4, 1): 10_000,
        (3, 2): 4_000,
        (3, 1): 500,
        (2, 2): 200,
        (2, 1): 50,
        (1, 2): 10,
    }
    THREAT_SCORES = {
        "five": 1_000_000,
        "open_four": 160_000,
        "closed_four": 45_000,
        "open_three": 8_000,
        "broken_three": 3_000,
        "double_threat": 55_000,
    }

    def __init__(self, threat_detector: ThreatDetector, board_size: int = BOARD_SIZE) -> None:
        self.threat_detector = threat_detector
        self.board_size = board_size

    def evaluate(self, board: list[list[int]]) -> int:
        ai_score = self.evaluate_player(board, AI_STONE)
        human_score = self.evaluate_player(board, HUMAN_STONE)
        return ai_score - human_score

    def evaluate_player(self, board: list[list[int]], player: int) -> int:
        threat_score = self.score_threat_summary(self.threat_detector.summary(board, player))
        contiguous_score = self._evaluate_contiguous_player(board, player)
        return threat_score + contiguous_score

    def score_threat_summary(self, summary: ThreatSummary) -> int:
        return (
            summary.five * self.THREAT_SCORES["five"]
            + summary.open_four * self.THREAT_SCORES["open_four"]
            + summary.closed_four * self.THREAT_SCORES["closed_four"]
            + summary.open_three * self.THREAT_SCORES["open_three"]
            + summary.broken_three * self.THREAT_SCORES["broken_three"]
            + summary.double_threat * self.THREAT_SCORES["double_threat"]
        )

    def _evaluate_contiguous_player(self, board: list[list[int]], player: int) -> int:
        total = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] != player:
                    continue
                for dr, dc in DIRECTIONS:
                    prev_r = row - dr
                    prev_c = col - dc
                    if in_bounds(prev_r, prev_c, self.board_size) and board[prev_r][prev_c] == player:
                        continue
                    count, open_ends = self._count_pattern(board, row, col, dr, dc, player)
                    if count >= WIN_LENGTH:
                        total += self.PATTERN_SCORES[(5, 0)]
                    else:
                        total += self.PATTERN_SCORES.get((count, open_ends), 0)
        return total

    def _count_pattern(
        self,
        board: list[list[int]],
        row: int,
        col: int,
        dr: int,
        dc: int,
        player: int,
    ) -> tuple[int, int]:
        count = 0
        r, c = row, col
        while in_bounds(r, c, self.board_size) and board[r][c] == player:
            count += 1
            r += dr
            c += dc

        open_ends = 0
        if in_bounds(r, c, self.board_size) and board[r][c] == EMPTY:
            open_ends += 1

        prev_r = row - dr
        prev_c = col - dc
        if in_bounds(prev_r, prev_c, self.board_size) and board[prev_r][prev_c] == EMPTY:
            open_ends += 1

        return count, open_ends
