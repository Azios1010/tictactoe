from __future__ import annotations

import atexit
import pickle
import random
from dataclasses import dataclass
from math import inf
from pathlib import Path
from typing import Iterable


BOARD_SIZE = 15
EMPTY = 0
AI_STONE = 1
HUMAN_STONE = -1
WIN_LENGTH = 5


@dataclass(frozen=True)
class SearchConfig:
    depth: int = 5
    candidate_radius: int = 5
    candidate_limit: int = 14


class GomokuAI:
    """Minimax + alpha-beta pruning AI for a 15x15 Gomoku board."""

    EXACT = "EXACT"
    LOWERBOUND = "LOWERBOUND"
    UPPERBOUND = "UPPERBOUND"
    DIRECTIONS = ((1, 0), (0, 1), (1, 1), (1, -1))
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
    _zobrist_table: list[list[list[int]]] | None = None

    def __init__(
        self,
        board_size: int = BOARD_SIZE,
        config: SearchConfig | None = None,
        memory_filename: str | Path = "gomoku_tt.pkl",
    ) -> None:
        self.board_size = board_size
        self.config = config or SearchConfig()
        self.memory_filename = Path(memory_filename)
        if self.__class__._zobrist_table is None:
            self.__class__._zobrist_table = self._init_zobrist()
        self.transposition_table: dict[int, tuple[int, float, str]] = {}
        self.load_memory(self.memory_filename)
        atexit.register(self.save_memory, self.memory_filename)

    def _init_zobrist(self) -> list[list[list[int]]]:
        rng = random.Random(20260408)
        return [
            [[rng.getrandbits(64) for _ in range(2)] for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]

    def compute_hash(self, board: list[list[int]]) -> int:
        zobrist = self.__class__._zobrist_table
        if zobrist is None:
            raise RuntimeError("Zobrist table has not been initialized.")

        board_hash = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                stone = board[row][col]
                if stone == EMPTY:
                    continue
                stone_index = 0 if stone == AI_STONE else 1
                board_hash ^= zobrist[row][col][stone_index]
        return board_hash

    def load_memory(self, filename: str | Path | None = None) -> None:
        path = Path(filename or self.memory_filename)
        if not path.exists():
            return

        try:
            with path.open("rb") as handle:
                payload = pickle.load(handle)
        except (OSError, pickle.PickleError, EOFError):
            return

        if isinstance(payload, dict):
            self.transposition_table = {
                int(board_hash): (int(depth), float(score), str(flag))
                for board_hash, (depth, score, flag) in payload.items()
            }

    def save_memory(self, filename: str | Path | None = None) -> None:
        path = Path(filename or self.memory_filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("wb") as handle:
                pickle.dump(self.transposition_table, handle, protocol=pickle.HIGHEST_PROTOCOL)
        except OSError:
            return

    def get_best_move(self, board: list[list[int]], player: int = AI_STONE) -> tuple[int, int] | None:
        if self._has_winner(board, AI_STONE) or self._has_winner(board, HUMAN_STONE):
            return None

        candidates = self._generate_candidates(board)
        if not candidates:
            center = self.board_size // 2
            return (center, center)

        best_score = -inf
        best_move: tuple[int, int] | None = None
        alpha = -inf
        beta = inf

        for row, col in candidates:
            board[row][col] = player
            score = self._minimax(
                board,
                depth=self.config.depth - 1,
                alpha=alpha,
                beta=beta,
                maximizing=False,
            )
            board[row][col] = EMPTY

            if score > best_score:
                best_score = score
                best_move = (row, col)
            alpha = max(alpha, best_score)

        return best_move

    def _minimax(
        self,
        board: list[list[int]],
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
    ) -> float:
        alpha_orig = alpha
        beta_orig = beta
        board_hash = self.compute_hash(board)
        cached = self.transposition_table.get(board_hash)
        if cached is not None:
            cached_depth, cached_score, cached_flag = cached
            if cached_depth >= depth:
                if cached_flag == self.EXACT:
                    return cached_score
                if cached_flag == self.LOWERBOUND:
                    alpha = max(alpha, cached_score)
                elif cached_flag == self.UPPERBOUND:
                    beta = min(beta, cached_score)
                if alpha >= beta:
                    return cached_score

        if self._has_winner(board, AI_STONE):
            value = 2_000_000 + depth
            self.transposition_table[board_hash] = (depth, value, self.EXACT)
            return value
        if self._has_winner(board, HUMAN_STONE):
            value = -2_000_000 - depth
            self.transposition_table[board_hash] = (depth, value, self.EXACT)
            return value
        if depth <= 0 or self._is_full(board):
            value = float(self.evaluate_board(board))
            self.transposition_table[board_hash] = (depth, value, self.EXACT)
            return value

        candidates = self._generate_candidates(board)
        if not candidates:
            value = float(self.evaluate_board(board))
            self.transposition_table[board_hash] = (depth, value, self.EXACT)
            return value

        if maximizing:
            value = -inf
            for row, col in candidates:
                board[row][col] = AI_STONE
                value = max(value, self._minimax(board, depth - 1, alpha, beta, False))
                board[row][col] = EMPTY
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        else:
            value = inf
            for row, col in candidates:
                board[row][col] = HUMAN_STONE
                value = min(value, self._minimax(board, depth - 1, alpha, beta, True))
                board[row][col] = EMPTY
                beta = min(beta, value)
                if beta <= alpha:
                    break

        flag = self.EXACT
        if value <= alpha_orig:
            flag = self.UPPERBOUND
        elif value >= beta_orig:
            flag = self.LOWERBOUND

        self.transposition_table[board_hash] = (depth, value, flag)
        return value

    def evaluate_board(self, board: list[list[int]]) -> int:
        ai_score = self._evaluate_player(board, AI_STONE)
        human_score = self._evaluate_player(board, HUMAN_STONE)
        return ai_score - human_score

    def _evaluate_player(self, board: list[list[int]], player: int) -> int:
        total = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] != player:
                    continue
                for dr, dc in self.DIRECTIONS:
                    prev_r = row - dr
                    prev_c = col - dc
                    if self._in_bounds(prev_r, prev_c) and board[prev_r][prev_c] == player:
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
        while self._in_bounds(r, c) and board[r][c] == player:
            count += 1
            r += dr
            c += dc

        open_ends = 0
        if self._in_bounds(r, c) and board[r][c] == EMPTY:
            open_ends += 1

        prev_r = row - dr
        prev_c = col - dc
        if self._in_bounds(prev_r, prev_c) and board[prev_r][prev_c] == EMPTY:
            open_ends += 1

        return count, open_ends

    def _generate_candidates(self, board: list[list[int]]) -> list[tuple[int, int]]:
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
        radius = self.config.candidate_radius
        for row, col in occupied:
            for d_row in range(-radius, radius + 1):
                for d_col in range(-radius, radius + 1):
                    next_row = row + d_row
                    next_col = col + d_col
                    if self._in_bounds(next_row, next_col) and board[next_row][next_col] == EMPTY:
                        candidates.add((next_row, next_col))

        ranked = sorted(candidates, key=lambda move: self._score_move(board, move[0], move[1]), reverse=True)
        return ranked[: self.config.candidate_limit]

    def _score_move(self, board: list[list[int]], row: int, col: int) -> int:
        board[row][col] = AI_STONE
        ai_value = self.evaluate_board(board)
        board[row][col] = HUMAN_STONE
        block_value = -self.evaluate_board(board)
        board[row][col] = EMPTY

        center = self.board_size // 2
        center_bias = self.board_size - (abs(center - row) + abs(center - col))
        return ai_value + block_value + center_bias

    def _has_winner(self, board: list[list[int]], player: int) -> bool:
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] != player:
                    continue
                for dr, dc in self.DIRECTIONS:
                    if self._is_winning_line(board, row, col, dr, dc, player):
                        return True
        return False

    def _is_winning_line(
        self,
        board: list[list[int]],
        row: int,
        col: int,
        dr: int,
        dc: int,
        player: int,
    ) -> bool:
        for step in range(WIN_LENGTH):
            next_row = row + dr * step
            next_col = col + dc * step
            if not self._in_bounds(next_row, next_col) or board[next_row][next_col] != player:
                return False
        return True

    def _is_full(self, board: Iterable[Iterable[int]]) -> bool:
        return all(cell != EMPTY for row in board for cell in row)

    def _in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.board_size and 0 <= col < self.board_size
