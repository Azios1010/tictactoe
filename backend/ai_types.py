from __future__ import annotations

from dataclasses import dataclass


BOARD_SIZE = 15
EMPTY = 0
AI_STONE = 1
HUMAN_STONE = -1
WIN_LENGTH = 5
DIRECTIONS = ((1, 0), (0, 1), (1, 1), (1, -1))


@dataclass(frozen=True)
class SearchConfig:
    depth: int = 5
    candidate_radius: int = 5
    candidate_limit: int = 14
    time_limit_ms: int | None = 1200
    threat_extension_depth: int = 1


class SearchTimeout(Exception):
    """Raised internally when the configured search deadline is reached."""


@dataclass(frozen=True)
class ThreatSummary:
    five: int = 0
    open_four: int = 0
    closed_four: int = 0
    open_three: int = 0
    broken_three: int = 0

    @property
    def forcing_count(self) -> int:
        return self.open_four + self.closed_four + self.open_three + self.broken_three

    @property
    def double_threat(self) -> int:
        return max(0, self.forcing_count - 1)


@dataclass(frozen=True)
class MoveAnalysis:
    move: tuple[int, int] | None
    score: float
    reason: str
    completed_depth: int
