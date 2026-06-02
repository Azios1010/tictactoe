# Backend AI Forcing And Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve backend AI evidence and tactical strength by adding a minimal forcing-search path, stronger threat scoring, and an automatic benchmark JSON script.

**Architecture:** Keep `GomokuAI` as the public AI entry point. Add a bounded forcing search before normal iterative deepening, keep candidate generation delegated to `MoveOrdering`, and keep evaluation changes limited to threat urgency constants. Add backend-only tests and a standalone `benchmark_ai.py` script that writes `benchmark_results.json`.

**Tech Stack:** Python 3 standard library, existing Gomoku backend modules, `unittest`.

---

### Task 1: Forcing Search Regression

**Files:**
- Create: `tests/test_forcing_search.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_forcing_search.py` with a board where AI has an open-three and should find a forcing move that creates an open-four:

```python
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


def empty_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


class ForcingSearchTest(unittest.TestCase):
    def test_find_forcing_win_prefers_open_four_creation(self) -> None:
        board = empty_board()
        board[6][5] = AI_STONE
        board[6][6] = AI_STONE
        board[6][7] = AI_STONE
        board[7][5] = HUMAN_STONE
        board[7][6] = HUMAN_STONE

        with tempfile.TemporaryDirectory() as temp_dir:
            ai = GomokuAI(
                config=SearchConfig(depth=2, candidate_radius=2, candidate_limit=8, time_limit_ms=800),
                memory_filename=Path(temp_dir) / "tt.pkl",
            )

            move = ai._find_forcing_win(
                board=board,
                attacker=AI_STONE,
                defender=HUMAN_STONE,
                depth=2,
                deadline=None,
            )

        self.assertIn(move, {(6, 4), (6, 8)})
```

- [ ] **Step 2: Run test to verify red**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_forcing_search -v
```

Expected: FAIL with `AttributeError: 'GomokuAI' object has no attribute '_find_forcing_win'`.

---

### Task 2: Minimal Forcing Search

**Files:**
- Modify: `backend/ai_core.py`
- Modify: `backend/move_ordering.py`
- Test: `tests/test_forcing_search.py`

- [ ] **Step 1: Add direct forcing candidate helper**

In `backend/move_ordering.py`, add `generates_forcing_threat()` that returns true when a move creates an open-four or closed-four for a specific player:

```python
    def generates_forcing_threat(self, board: list[list[int]], row: int, col: int, player: int) -> bool:
        board[row][col] = player
        try:
            if has_winner(board, player, self.board_size):
                return True
            summary = self.threat_detector.move_summary(board, row, col, player)
            return bool(summary.open_four or summary.closed_four)
        finally:
            board[row][col] = EMPTY
```

- [ ] **Step 2: Add `GomokuAI._find_forcing_win()`**

In `backend/ai_core.py`, add a bounded helper that searches only forcing moves:

```python
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
                defender_win = self._find_winning_move(board, attacker)
                if defender_win is None:
                    return (row, col)
                block_row, block_col = defender_win
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
```

- [ ] **Step 3: Call forcing search before normal deep search**

In `_get_move_analysis_for_ai()`, after immediate win/block and before `deadline = self._search_deadline()`, add:

```python
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
```

Then keep the existing iterative deepening code, but remove its duplicate later `deadline = self._search_deadline()` assignment.

- [ ] **Step 4: Run forcing test**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_forcing_search -v
```

Expected: PASS.

---

### Task 3: Threat Score Tuning

**Files:**
- Modify: `backend/evaluator.py`
- Modify: `backend/move_ordering.py`
- Test: `tests/test_tactical_cases.py`

- [ ] **Step 1: Tune evaluator threat scores**

In `backend/evaluator.py`, set:

```python
    THREAT_SCORES = {
        "five": 1_000_000,
        "open_four": 160_000,
        "closed_four": 45_000,
        "open_three": 8_000,
        "broken_three": 3_000,
        "double_threat": 55_000,
    }
```

- [ ] **Step 2: Tune move ordering threat scores**

In `backend/move_ordering.py`, set:

```python
    def score_move_threats(self, summary: ThreatSummary) -> int:
        return (
            summary.open_four * 900_000
            + summary.closed_four * 180_000
            + summary.open_three * 30_000
            + summary.broken_three * 10_000
            + summary.double_threat * 300_000
        )
```

- [ ] **Step 3: Run tactical tests**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_tactical_cases tests.test_forcing_search tests.test_transposition_table -v
```

Expected: PASS.

---

### Task 4: Benchmark Script

**Files:**
- Create: `benchmark_ai.py`

- [ ] **Step 1: Add benchmark script**

Create `benchmark_ai.py` that runs opening, midgame, block-open-four, and forcing-open-four cases for Easy/Medium/Hard and writes `benchmark_results.json`.

- [ ] **Step 2: Run benchmark**

Run:

```powershell
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

Expected: stdout table and `benchmark_results.json`.

---

### Task 5: Verification And Cleanup

**Files:**
- Verify: backend modules and tests
- Remove generated caches if not intended

- [ ] **Step 1: Python compile**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py benchmark_ai.py
```

- [ ] **Step 2: Backend regression**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_tactical_cases tests.test_forcing_search tests.test_transposition_table -v
```

- [ ] **Step 3: Arena smoke**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

- [ ] **Step 4: Cleanup generated cache**

Remove test/benchmark `*.pkl`, `__pycache__`, and root `gomoku_tt.pkl` if generated.
