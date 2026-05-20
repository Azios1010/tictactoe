from __future__ import annotations

from typing import Callable, Iterable

from ai_types import BOARD_SIZE, DIRECTIONS, EMPTY, ThreatSummary
from board_rules import in_bounds


class ThreatDetector:
    def __init__(self, board_size: int = BOARD_SIZE) -> None:
        self.board_size = board_size

    def summary(self, board: list[list[int]], player: int) -> ThreatSummary:
        five = 0
        open_four = 0
        closed_four = 0
        open_three = 0
        broken_three = 0

        for line in self._iter_line_strings(board, player):
            summary = self.summarize_line(line)
            five += summary.five
            open_four += summary.open_four
            closed_four += summary.closed_four
            open_three += summary.open_three
            broken_three += summary.broken_three

        return ThreatSummary(
            five=five,
            open_four=open_four,
            closed_four=closed_four,
            open_three=open_three,
            broken_three=broken_three,
        )

    def move_summary(self, board: list[list[int]], row: int, col: int, player: int) -> ThreatSummary:
        five = 0
        open_four = 0
        closed_four = 0
        open_three = 0
        broken_three = 0

        for dr, dc in DIRECTIONS:
            line = self._local_line_string(board, row, col, dr, dc, player)
            summary = self.summarize_line(line)
            five += summary.five
            open_four += summary.open_four
            closed_four += summary.closed_four
            open_three += summary.open_three
            broken_three += summary.broken_three

        return ThreatSummary(
            five=five,
            open_four=open_four,
            closed_four=closed_four,
            open_three=open_three,
            broken_three=broken_three,
        )

    def summarize_line(self, line: str) -> ThreatSummary:
        padded = f"2{line}2"
        five = self._count_windows(line, 5, lambda window: window == "11111")
        open_four = padded.count("011110")
        four_windows = self._count_windows(
            padded,
            5,
            lambda window: window.count("1") == 4 and window.count("0") == 1 and "2" not in window,
        )
        closed_four = max(0, four_windows - open_four * 2)
        open_three = sum(padded.count(pattern) for pattern in ("01110", "010110", "011010"))
        broken_three = sum(
            padded.count(pattern)
            for pattern in (
                "01101",
                "01011",
                "11010",
                "10110",
            )
        )
        return ThreatSummary(
            five=five,
            open_four=open_four,
            closed_four=closed_four,
            open_three=open_three,
            broken_three=broken_three,
        )

    def _count_windows(self, line: str, size: int, predicate: Callable[[str], bool]) -> int:
        return sum(1 for index in range(0, len(line) - size + 1) if predicate(line[index : index + size]))

    def _iter_line_strings(self, board: list[list[int]], player: int) -> Iterable[str]:
        for row in range(self.board_size):
            yield self._line_string(board, row, 0, 0, 1, player)
        for col in range(self.board_size):
            yield self._line_string(board, 0, col, 1, 0, player)

        for col in range(self.board_size):
            yield self._line_string(board, 0, col, 1, 1, player)
            yield self._line_string(board, 0, col, 1, -1, player)
        for row in range(1, self.board_size):
            yield self._line_string(board, row, 0, 1, 1, player)
            yield self._line_string(board, row, self.board_size - 1, 1, -1, player)

    def _line_string(
        self,
        board: list[list[int]],
        row: int,
        col: int,
        dr: int,
        dc: int,
        player: int,
    ) -> str:
        cells: list[str] = []
        while in_bounds(row, col, self.board_size):
            cells.append(self._cell_symbol(board[row][col], player))
            row += dr
            col += dc
        return "".join(cells)

    def _local_line_string(
        self,
        board: list[list[int]],
        row: int,
        col: int,
        dr: int,
        dc: int,
        player: int,
    ) -> str:
        cells: list[str] = []
        for offset in range(-5, 6):
            next_row = row + dr * offset
            next_col = col + dc * offset
            if in_bounds(next_row, next_col, self.board_size):
                cells.append(self._cell_symbol(board[next_row][next_col], player))
            else:
                cells.append("2")
        return "".join(cells)

    def _cell_symbol(self, cell: int, player: int) -> str:
        if cell == EMPTY:
            return "0"
        if cell == player:
            return "1"
        return "2"
