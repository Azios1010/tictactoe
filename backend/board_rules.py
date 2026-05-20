from __future__ import annotations

from typing import Iterable

from ai_types import BOARD_SIZE, DIRECTIONS, EMPTY, WIN_LENGTH


def in_bounds(row: int, col: int, board_size: int = BOARD_SIZE) -> bool:
    return 0 <= row < board_size and 0 <= col < board_size


def is_winning_line(
    board: list[list[int]],
    row: int,
    col: int,
    dr: int,
    dc: int,
    player: int,
    board_size: int = BOARD_SIZE,
) -> bool:
    for step in range(WIN_LENGTH):
        next_row = row + dr * step
        next_col = col + dc * step
        if not in_bounds(next_row, next_col, board_size) or board[next_row][next_col] != player:
            return False
    return True


def has_winner(board: list[list[int]], player: int, board_size: int = BOARD_SIZE) -> bool:
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] != player:
                continue
            for dr, dc in DIRECTIONS:
                if is_winning_line(board, row, col, dr, dc, player, board_size):
                    return True
    return False


def is_full(board: Iterable[Iterable[int]]) -> bool:
    return all(cell != EMPTY for row in board for cell in row)


def has_any_stone(board: Iterable[Iterable[int]]) -> bool:
    return any(cell != EMPTY for row in board for cell in row)


def empty_cells(board: list[list[int]], board_size: int = BOARD_SIZE) -> Iterable[tuple[int, int]]:
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == EMPTY:
                yield (row, col)


def normalize_board(board: list[list[int]], player: int) -> list[list[int]]:
    return [[cell * player for cell in row] for row in board]


def line_potential(
    board: list[list[int]],
    row: int,
    col: int,
    dr: int,
    dc: int,
    player: int,
    board_size: int = BOARD_SIZE,
) -> tuple[int, int]:
    count = 1
    open_ends = 0

    r = row + dr
    c = col + dc
    while in_bounds(r, c, board_size) and board[r][c] == player:
        count += 1
        r += dr
        c += dc
    if in_bounds(r, c, board_size) and board[r][c] == EMPTY:
        open_ends += 1

    r = row - dr
    c = col - dc
    while in_bounds(r, c, board_size) and board[r][c] == player:
        count += 1
        r -= dr
        c -= dc
    if in_bounds(r, c, board_size) and board[r][c] == EMPTY:
        open_ends += 1

    return count, open_ends
