from __future__ import annotations

import atexit
import pickle
import random
from math import inf
from pathlib import Path
from time import perf_counter
from typing import Iterable

from ai_types import (
    AI_STONE,
    BOARD_SIZE,
    DIRECTIONS,
    EMPTY,
    HUMAN_STONE,
    MoveAnalysis,
    SearchConfig,
    SearchTimeout,
)
from board_rules import empty_cells, has_any_stone, has_winner, in_bounds, is_full, is_winning_line, line_potential, normalize_board
from evaluator import BoardEvaluator
from move_ordering import MoveOrdering
from threats import ThreatDetector


class GomokuAI:
    """Search orchestrator for a 15x15 Gomoku board."""

    MEMORY_VERSION = 3
    EXACT = "EXACT"
    LOWERBOUND = "LOWERBOUND"
    UPPERBOUND = "UPPERBOUND"
    _zobrist_table: list[list[list[int]]] | None = None
    _zobrist_side_to_move: dict[int, int] | None = None

    def __init__(
        self,
        board_size: int = BOARD_SIZE,
        config: SearchConfig | None = None,
        memory_filename: str | Path = "gomoku_tt.pkl",
    ) -> None:
        self.board_size = board_size
        self.config = config or SearchConfig()
        self.memory_filename = Path(memory_filename)
        self.threat_detector = ThreatDetector(board_size=self.board_size)
        self.evaluator = BoardEvaluator(threat_detector=self.threat_detector, board_size=self.board_size)
        self.move_ordering = MoveOrdering(
            config=self.config,
            evaluator=self.evaluator,
            threat_detector=self.threat_detector,
            board_size=self.board_size,
        )
        if self.__class__._zobrist_table is None or self.__class__._zobrist_side_to_move is None:
            zobrist_table, side_to_move = self._init_zobrist()
            self.__class__._zobrist_table = zobrist_table
            self.__class__._zobrist_side_to_move = side_to_move
        self.transposition_table: dict[int, tuple[int, float, str, tuple[int, int] | None]] = {}
        self.load_memory(self.memory_filename)
        atexit.register(self.save_memory, self.memory_filename)

    def _init_zobrist(self) -> tuple[list[list[list[int]]], dict[int, int]]:
        rng = random.Random(20260408)
        table = [
            [[rng.getrandbits(64) for _ in range(2)] for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]
        side_to_move = {
            AI_STONE: rng.getrandbits(64),
            HUMAN_STONE: rng.getrandbits(64),
        }
        return table, side_to_move

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

    def compute_search_hash(self, board: list[list[int]], side_to_move: int) -> int:
        side_hashes = self.__class__._zobrist_side_to_move
        if side_hashes is None:
            raise RuntimeError("Zobrist side-to-move hashes have not been initialized.")
        return self.compute_hash(board) ^ side_hashes[side_to_move]

    def load_memory(self, filename: str | Path | None = None) -> None:
        path = Path(filename or self.memory_filename)
        if not path.exists():
            return

        try:
            with path.open("rb") as handle:
                payload = pickle.load(handle)
        except (OSError, pickle.PickleError, EOFError):
            return

        if not isinstance(payload, dict):
            return

        if payload.get("version") == self.MEMORY_VERSION and isinstance(payload.get("entries"), dict):
            entries = payload["entries"]
            normalized_entries: dict[int, tuple[int, float, str, tuple[int, int] | None]] = {}
            for board_hash, entry in entries.items():
                if not isinstance(entry, (tuple, list)) or len(entry) not in {3, 4}:
                    continue
                depth, score, flag = entry[:3]
                best_move = entry[3] if len(entry) == 4 else None
                if best_move is not None:
                    best_move = (int(best_move[0]), int(best_move[1]))
                normalized_entries[int(board_hash)] = (int(depth), float(score), str(flag), best_move)
            self.transposition_table = normalized_entries

    def save_memory(self, filename: str | Path | None = None) -> None:
        path = Path(filename or self.memory_filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("wb") as handle:
                payload = {
                    "version": self.MEMORY_VERSION,
                    "entries": self.transposition_table,
                }
                pickle.dump(payload, handle, protocol=pickle.HIGHEST_PROTOCOL)
        except OSError:
            return

    def get_best_move(self, board: list[list[int]], player: int = AI_STONE) -> tuple[int, int] | None:
        return self.get_move_analysis(board, player).move

    def get_move_analysis(self, board: list[list[int]], player: int = AI_STONE) -> MoveAnalysis:
        if player not in {AI_STONE, HUMAN_STONE}:
            raise ValueError("Player must be either 1 or -1.")

        if player == HUMAN_STONE:
            normalized = normalize_board(board, player)
            return self._get_move_analysis_for_ai(normalized)

        return self._get_move_analysis_for_ai(board)

    def _get_best_move_for_ai(self, board: list[list[int]]) -> tuple[int, int] | None:
        return self._get_move_analysis_for_ai(board).move

    def _get_move_analysis_for_ai(self, board: list[list[int]]) -> MoveAnalysis:
        if self._has_winner(board, AI_STONE) or self._has_winner(board, HUMAN_STONE):
            return MoveAnalysis(move=None, score=float(self.evaluate_board(board)), reason="game_finished", completed_depth=0)

        candidates = self._generate_candidates(board)
        if not candidates or not self._has_any_stone(board):
            center = self.board_size // 2
            return MoveAnalysis(move=(center, center), score=0, reason="opening_center", completed_depth=0)

        winning_move = self._find_winning_move(board, AI_STONE, candidates)
        if winning_move is not None:
            return MoveAnalysis(
                move=winning_move,
                score=float("inf"),
                reason="winning_move",
                completed_depth=0,
            )

        blocking_move = self._find_winning_move(board, HUMAN_STONE, candidates)
        if blocking_move is not None:
            return MoveAnalysis(
                move=blocking_move,
                score=float(self._score_move(board, blocking_move[0], blocking_move[1])),
                reason="blocking_win",
                completed_depth=0,
            )

        blocking_double_threat = self._find_double_open_three_move(board, HUMAN_STONE, candidates)
        if blocking_double_threat is not None:
            return MoveAnalysis(
                move=blocking_double_threat,
                score=float(self._score_move(board, blocking_double_threat[0], blocking_double_threat[1])),
                reason="blocking_double_threat",
                completed_depth=0,
            )

        creating_double_threat = self._find_double_open_three_move(board, AI_STONE, candidates)
        if creating_double_threat is not None:
            return MoveAnalysis(
                move=creating_double_threat,
                score=float(self._score_move(board, creating_double_threat[0], creating_double_threat[1])),
                reason="creating_double_threat",
                completed_depth=0,
            )

        deadline = self._search_deadline()
        try:
            forcing_move = self._find_forcing_win(
                board=board,
                attacker=AI_STONE,
                defender=HUMAN_STONE,
                depth=2,
                deadline=deadline,
            )
        except SearchTimeout:
            forcing_move = None
        if forcing_move is not None:
            return MoveAnalysis(
                move=forcing_move,
                score=500_000,
                reason=self._classify_move_reason(board, forcing_move),
                completed_depth=0,
            )

        best_move: tuple[int, int] | None = candidates[0]
        best_score = float(self._score_move(board, best_move[0], best_move[1]))
        ordered_candidates = candidates
        completed_depth = 0
        timed_out = False

        for depth in range(1, max(1, self.config.depth) + 1):
            try:
                move, score = self._search_root(board, ordered_candidates, depth, deadline)
            except SearchTimeout:
                timed_out = True
                break
            if move is not None:
                best_move = move
                best_score = score
                completed_depth = depth
                ordered_candidates = self._prioritize_move(candidates, best_move)

        reason = "timeout_best_known" if timed_out and completed_depth == 0 else self._classify_move_reason(board, best_move)
        return MoveAnalysis(move=best_move, score=best_score, reason=reason, completed_depth=completed_depth)

    def _search_root(
        self,
        board: list[list[int]],
        candidates: list[tuple[int, int]],
        depth: int,
        deadline: float | None,
    ) -> tuple[tuple[int, int] | None, float]:
        self._check_deadline(deadline)

        best_score = -inf
        best_move: tuple[int, int] | None = None
        alpha = -inf
        beta = inf
        for row, col in candidates:
            self._check_deadline(deadline)
            board[row][col] = AI_STONE
            try:
                score = self._minimax(
                    board,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    maximizing=False,
                    deadline=deadline,
                    extension_depth=0,
                )
            finally:
                board[row][col] = EMPTY

            if score > best_score:
                best_score = score
                best_move = (row, col)
            alpha = max(alpha, best_score)

        return best_move, best_score

    def _minimax(
        self,
        board: list[list[int]],
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        deadline: float | None = None,
        extension_depth: int = 0,
    ) -> float:
        self._check_deadline(deadline)
        alpha_orig = alpha
        beta_orig = beta
        side_to_move = AI_STONE if maximizing else HUMAN_STONE
        search_hash = self.compute_search_hash(board, side_to_move)
        cache_enabled = depth > 0 or extension_depth >= self.config.threat_extension_depth
        cached = self.transposition_table.get(search_hash) if cache_enabled else None
        if cached is not None:
            cached_depth, cached_score, cached_flag, _cached_best_move = cached
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
            if cache_enabled:
                self.transposition_table[search_hash] = (depth, value, self.EXACT, None)
            return value
        if self._has_winner(board, HUMAN_STONE):
            value = -2_000_000 - depth
            if cache_enabled:
                self.transposition_table[search_hash] = (depth, value, self.EXACT, None)
            return value
        if depth <= 0 or self._is_full(board):
            if depth <= 0 and extension_depth < self.config.threat_extension_depth:
                tactical_candidates = self._generate_forcing_candidates(board)
                if tactical_candidates:
                    return self._search_extension(
                        board=board,
                        candidates=tactical_candidates,
                        alpha=alpha,
                        beta=beta,
                        maximizing=maximizing,
                        deadline=deadline,
                        extension_depth=extension_depth,
                    )
            value = float(self.evaluate_board(board))
            if cache_enabled:
                self.transposition_table[search_hash] = (depth, value, self.EXACT, None)
            return value

        candidates = self._generate_candidates(board)
        if not candidates:
            value = float(self.evaluate_board(board))
            if cache_enabled:
                self.transposition_table[search_hash] = (depth, value, self.EXACT, None)
            return value

        cached_best_move = cached[3] if cached is not None else None
        if cached_best_move in candidates:
            candidates = self._prioritize_move(candidates, cached_best_move)

        best_move: tuple[int, int] | None = None
        if maximizing:
            value = -inf
            for row, col in candidates:
                self._check_deadline(deadline)
                board[row][col] = AI_STONE
                try:
                    child_score = self._minimax(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        False,
                        deadline,
                        extension_depth,
                    )
                finally:
                    board[row][col] = EMPTY
                if child_score > value:
                    value = child_score
                    best_move = (row, col)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        else:
            value = inf
            for row, col in candidates:
                self._check_deadline(deadline)
                board[row][col] = HUMAN_STONE
                try:
                    child_score = self._minimax(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        True,
                        deadline,
                        extension_depth,
                    )
                finally:
                    board[row][col] = EMPTY
                if child_score < value:
                    value = child_score
                    best_move = (row, col)
                beta = min(beta, value)
                if beta <= alpha:
                    break

        flag = self.EXACT
        if value <= alpha_orig:
            flag = self.UPPERBOUND
        elif value >= beta_orig:
            flag = self.LOWERBOUND

        if cache_enabled:
            self.transposition_table[search_hash] = (depth, value, flag, best_move)
        return value

    def _search_extension(
        self,
        board: list[list[int]],
        candidates: list[tuple[int, int]],
        alpha: float,
        beta: float,
        maximizing: bool,
        deadline: float | None,
        extension_depth: int,
    ) -> float:
        if maximizing:
            value = -inf
            for row, col in candidates:
                self._check_deadline(deadline)
                board[row][col] = AI_STONE
                try:
                    value = max(
                        value,
                        self._minimax(
                            board,
                            depth=0,
                            alpha=alpha,
                            beta=beta,
                            maximizing=False,
                            deadline=deadline,
                            extension_depth=extension_depth + 1,
                        ),
                    )
                finally:
                    board[row][col] = EMPTY
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value

        value = inf
        for row, col in candidates:
            self._check_deadline(deadline)
            board[row][col] = HUMAN_STONE
            try:
                value = min(
                    value,
                    self._minimax(
                        board,
                        depth=0,
                        alpha=alpha,
                        beta=beta,
                        maximizing=True,
                        deadline=deadline,
                        extension_depth=extension_depth + 1,
                    ),
                )
            finally:
                board[row][col] = EMPTY
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

    def evaluate_board(self, board: list[list[int]]) -> int:
        return self.evaluator.evaluate(board)

    def _find_winning_move(
        self,
        board: list[list[int]],
        player: int,
        candidates: Iterable[tuple[int, int]] | None = None,
    ) -> tuple[int, int] | None:
        search_space = candidates if candidates is not None else self._empty_cells(board)
        for row, col in search_space:
            if board[row][col] != EMPTY:
                continue
            board[row][col] = player
            has_winner_for_player = self._has_winner(board, player)
            board[row][col] = EMPTY
            if has_winner_for_player:
                return (row, col)
        return None

    def _find_double_open_three_move(
        self,
        board: list[list[int]],
        player: int,
        candidates: Iterable[tuple[int, int]] | None = None,
    ) -> tuple[int, int] | None:
        search_space = candidates if candidates is not None else self._empty_cells(board)
        for row, col in search_space:
            if board[row][col] != EMPTY:
                continue
            board[row][col] = player
            try:
                summary = self._move_threat_summary(board, row, col, player)
                if summary.open_three >= 2:
                    return (row, col)
            finally:
                board[row][col] = EMPTY
        return None

    def _find_forcing_win(
        self,
        board: list[list[int]],
        attacker: int,
        defender: int,
        depth: int,
        deadline: float | None,
    ) -> tuple[int, int] | None:
        if depth <= 0:
            return None

        candidates = self._generate_candidates(board)
        for row, col in candidates:
            self._check_deadline(deadline)
            if board[row][col] != EMPTY:
                continue
            if not self.move_ordering.generates_forcing_threat(board, row, col, attacker):
                continue
            board[row][col] = attacker
            try:
                if self._has_winner(board, attacker):
                    return (row, col)
                defender_block = self._find_winning_move(board, attacker)
                if defender_block is None:
                    return (row, col)
                block_row, block_col = defender_block
                board[block_row][block_col] = defender
                try:
                    reply = self._find_forcing_win(board, attacker, defender, depth - 1, deadline)
                    if reply is not None:
                        return (row, col)
                finally:
                    board[block_row][block_col] = EMPTY
            finally:
                board[row][col] = EMPTY
        return None

    def _generate_candidates(self, board: list[list[int]]) -> list[tuple[int, int]]:
        return self.move_ordering.generate_candidates(board)

    def _score_move(self, board: list[list[int]], row: int, col: int) -> int:
        return self.move_ordering.score_move(board, row, col)

    def _score_local_shape(self, board: list[list[int]], row: int, col: int, player: int) -> int:
        return self.move_ordering.score_local_shape(board, row, col, player)

    def _score_move_threats(self, summary) -> int:
        return self.move_ordering.score_move_threats(summary)

    def _classify_move_reason(self, board: list[list[int]], move: tuple[int, int] | None) -> str:
        return self.move_ordering.classify_move_reason(board, move)

    def _is_tactical_candidate(self, board: list[list[int]], row: int, col: int) -> bool:
        return self.move_ordering.is_tactical_candidate(board, row, col)

    def _generate_tactical_candidates(self, board: list[list[int]]) -> list[tuple[int, int]]:
        return self.move_ordering.generate_tactical_candidates(board)

    def _generate_forcing_candidates(self, board: list[list[int]]) -> list[tuple[int, int]]:
        return self.move_ordering.generate_forcing_candidates(board)

    def _is_forcing_candidate(self, board: list[list[int]], row: int, col: int) -> bool:
        return self.move_ordering.is_forcing_candidate(board, row, col)

    def _candidate_radius(self, occupied_count: int) -> int:
        return self.move_ordering.candidate_radius(occupied_count)

    def _threat_summary(self, board: list[list[int]], player: int):
        return self.threat_detector.summary(board, player)

    def _move_threat_summary(self, board: list[list[int]], row: int, col: int, player: int):
        return self.threat_detector.move_summary(board, row, col, player)

    def _summarize_line_threats(self, line: str):
        return self.threat_detector.summarize_line(line)

    def _score_threat_summary(self, summary) -> int:
        return self.evaluator.score_threat_summary(summary)

    def _evaluate_player(self, board: list[list[int]], player: int) -> int:
        return self.evaluator.evaluate_player(board, player)

    def _empty_cells(self, board: list[list[int]]) -> Iterable[tuple[int, int]]:
        return empty_cells(board, self.board_size)

    def _normalize_board(self, board: list[list[int]], player: int) -> list[list[int]]:
        return normalize_board(board, player)

    def _line_potential(
        self,
        board: list[list[int]],
        row: int,
        col: int,
        dr: int,
        dc: int,
        player: int,
    ) -> tuple[int, int]:
        return line_potential(board, row, col, dr, dc, player, self.board_size)

    def _prioritize_move(
        self,
        candidates: list[tuple[int, int]],
        preferred: tuple[int, int],
    ) -> list[tuple[int, int]]:
        return [preferred, *(move for move in candidates if move != preferred)]

    def _search_deadline(self) -> float | None:
        if self.config.time_limit_ms is None:
            return None
        return perf_counter() + max(1, self.config.time_limit_ms) / 1000

    def _check_deadline(self, deadline: float | None) -> None:
        if deadline is not None and perf_counter() >= deadline:
            raise SearchTimeout

    def _has_winner(self, board: list[list[int]], player: int) -> bool:
        return has_winner(board, player, self.board_size)

    def _is_winning_line(
        self,
        board: list[list[int]],
        row: int,
        col: int,
        dr: int,
        dc: int,
        player: int,
    ) -> bool:
        return is_winning_line(board, row, col, dr, dc, player, self.board_size)

    def _is_full(self, board: Iterable[Iterable[int]]) -> bool:
        return is_full(board)

    def _has_any_stone(self, board: Iterable[Iterable[int]]) -> bool:
        return has_any_stone(board)

    def _in_bounds(self, row: int, col: int) -> bool:
        return in_bounds(row, col, self.board_size)
