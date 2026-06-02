from __future__ import annotations

from ai_types import AI_STONE, BOARD_SIZE, DIRECTIONS, EMPTY, HUMAN_STONE, SearchConfig, ThreatSummary, WIN_LENGTH
from board_rules import has_winner, in_bounds, line_potential
from evaluator import BoardEvaluator
from threats import ThreatDetector


class MoveOrdering:
    def __init__(
        self,
        config: SearchConfig,
        evaluator: BoardEvaluator,
        threat_detector: ThreatDetector,
        board_size: int = BOARD_SIZE,
    ) -> None:
        self.config = config
        self.evaluator = evaluator
        self.threat_detector = threat_detector
        self.board_size = board_size

    def generate_candidates(self, board: list[list[int]]) -> list[tuple[int, int]]:
        occupied = [
            (row, col)
            for row in range(self.board_size)
            for col in range(self.board_size)
            if board[row][col] != EMPTY
        ]
        if not occupied:
            center = self.board_size // 2
            return [(center, center)]

        candidates: set[tuple[int, int]] = set()
        radius = self.candidate_radius(len(occupied))
        for row, col in occupied:
            for d_row in range(-radius, radius + 1):
                for d_col in range(-radius, radius + 1):
                    next_row = row + d_row
                    next_col = col + d_col
                    if in_bounds(next_row, next_col, self.board_size) and board[next_row][next_col] == EMPTY:
                        candidates.add((next_row, next_col))

        ranked = sorted(candidates, key=lambda move: self.score_move(board, move[0], move[1]), reverse=True)
        forcing = [move for move in ranked if self.is_forcing_candidate(board, move[0], move[1])]
        selected_limit = max(self.config.candidate_limit, len(forcing), 1)

        selected: list[tuple[int, int]] = []
        seen: set[tuple[int, int]] = set()
        for move in [*forcing, *ranked]:
            if move not in seen:
                selected.append(move)
                seen.add(move)
            if len(selected) >= selected_limit:
                break

        return selected

    def score_move(self, board: list[list[int]], row: int, col: int) -> int:
        board[row][col] = AI_STONE
        ai_wins = has_winner(board, AI_STONE, self.board_size)
        ai_threats = self.threat_detector.move_summary(board, row, col, AI_STONE)
        board[row][col] = HUMAN_STONE
        human_wins = has_winner(board, HUMAN_STONE, self.board_size)
        human_threats = self.threat_detector.move_summary(board, row, col, HUMAN_STONE)
        board[row][col] = EMPTY

        center = self.board_size // 2
        center_bias = self.board_size - (abs(center - row) + abs(center - col))
        tactical_bias = 0
        if ai_wins:
            tactical_bias += 10_000_000
        if human_wins:
            tactical_bias += 9_000_000
        tactical_bias += self.score_move_threats(ai_threats)
        tactical_bias += self.score_move_threats(human_threats) // 2
        local_shape_score = self.score_local_shape(board, row, col, AI_STONE)
        local_block_score = self.score_local_shape(board, row, col, HUMAN_STONE) // 2
        return tactical_bias + local_shape_score + local_block_score + center_bias

    def score_local_shape(self, board: list[list[int]], row: int, col: int, player: int) -> int:
        score = 0
        board[row][col] = player
        try:
            for dr, dc in DIRECTIONS:
                count, open_ends = line_potential(board, row, col, dr, dc, player, self.board_size)
                if count >= WIN_LENGTH:
                    score += 1_000_000
                elif count == 4:
                    score += 100_000 if open_ends == 2 else 20_000
                elif count == 3:
                    score += 8_000 if open_ends == 2 else 1_200
                elif count == 2:
                    score += 500 if open_ends == 2 else 100
        finally:
            board[row][col] = EMPTY
        return score

    def score_move_threats(self, summary: ThreatSummary) -> int:
        return (
            summary.open_four * 900_000
            + summary.closed_four * 180_000
            + summary.open_three * 30_000
            + summary.broken_three * 10_000
            + summary.double_threat * 300_000
        )

    def classify_move_reason(self, board: list[list[int]], move: tuple[int, int] | None) -> str:
        if move is None:
            return "no_legal_move"

        row, col = move
        board[row][col] = AI_STONE
        ai_summary = self.threat_detector.move_summary(board, row, col, AI_STONE)
        board[row][col] = HUMAN_STONE
        human_summary = self.threat_detector.move_summary(board, row, col, HUMAN_STONE)
        board[row][col] = EMPTY

        if ai_summary.double_threat:
            return "creating_double_threat"
        if ai_summary.open_four:
            return "creating_open_four"
        if ai_summary.closed_four:
            return "creating_closed_four"
        if human_summary.double_threat:
            return "blocking_double_threat"
        if human_summary.open_four:
            return "blocking_open_four"
        if human_summary.closed_four:
            return "blocking_closed_four"
        if ai_summary.open_three or ai_summary.broken_three:
            return "building_attack"
        if human_summary.open_three or human_summary.broken_three:
            return "reducing_threat"
        return "best_search_score"

    def generate_tactical_candidates(self, board: list[list[int]]) -> list[tuple[int, int]]:
        candidates = self.generate_candidates(board)
        return [move for move in candidates if self.is_tactical_candidate(board, move[0], move[1])]

    def is_tactical_candidate(self, board: list[list[int]], row: int, col: int) -> bool:
        for player in (AI_STONE, HUMAN_STONE):
            board[row][col] = player
            try:
                if has_winner(board, player, self.board_size):
                    return True
                summary = self.threat_detector.move_summary(board, row, col, player)
                if summary.open_four or summary.closed_four or summary.open_three or summary.broken_three:
                    return True
            finally:
                board[row][col] = EMPTY
        return False

    def generate_forcing_candidates(self, board: list[list[int]]) -> list[tuple[int, int]]:
        candidates = self.generate_candidates(board)
        return [move for move in candidates if self.is_forcing_candidate(board, move[0], move[1])]

    def generates_forcing_threat(self, board: list[list[int]], row: int, col: int, player: int) -> bool:
        board[row][col] = player
        try:
            if has_winner(board, player, self.board_size):
                return True
            summary = self.threat_detector.move_summary(board, row, col, player)
            return bool(summary.open_four or summary.closed_four)
        finally:
            board[row][col] = EMPTY

    def is_forcing_candidate(self, board: list[list[int]], row: int, col: int) -> bool:
        for player in (AI_STONE, HUMAN_STONE):
            board[row][col] = player
            try:
                if has_winner(board, player, self.board_size):
                    return True
                summary = self.threat_detector.move_summary(board, row, col, player)
                if summary.open_four or summary.closed_four:
                    return True
            finally:
                board[row][col] = EMPTY
        return False

    def candidate_radius(self, occupied_count: int) -> int:
        if occupied_count <= 2:
            return min(self.config.candidate_radius, 2)
        if occupied_count <= 10:
            return min(self.config.candidate_radius, 2)
        return min(self.config.candidate_radius, 3)
