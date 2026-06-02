# AI Tactical Improvement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add tactical regression coverage for the Gomoku AI and make focused AI fixes where the baseline fails.

**Architecture:** Tactical cases are stored as JSONL fixtures under `tests/fixtures/`. A pytest test parses each 15x15 board and calls `GomokuAI.get_move_analysis()` using an isolated test cache. If failures expose weak tactical handling, fixes stay inside the existing AI modules: `threats.py`, `evaluator.py`, `move_ordering.py`, or `ai_core.py`.

**Tech Stack:** Python 3, pytest, FastAPI backend modules, classical Gomoku AI search.

---

### Task 1: Tactical Fixture And Test

**Files:**
- Create: `tests/fixtures/tactical_cases.jsonl`
- Create: `tests/test_tactical_cases.py`

- [ ] **Step 1: Create tactical fixtures**

Create `tests/fixtures/tactical_cases.jsonl` with these cases:

```jsonl
{"name":"opening_center","player":1,"board":["...............","...............","...............","...............","...............","...............","...............","...............","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,7]],"tags":["opening"]}
{"name":"ai_win_horizontal","player":1,"board":["...............","...............","...............","...............","...............","...............","...............",".....OOOO......","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,4],[7,9]],"tags":["win","five"]}
{"name":"block_human_open_four_horizontal","player":1,"board":["...............","...............","...............","...............","...............","...............","...............",".....XXXX......","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,4],[7,9]],"tags":["block","open_four"]}
{"name":"block_human_broken_four_xx_xx","player":1,"board":["...............","...............","...............","...............","...............","...............","...............",".....XX.XX.....","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,7]],"tags":["block","broken_four"]}
{"name":"block_human_broken_four_x_xxx","player":1,"board":["...............","...............","...............","...............","...............","...............","...............",".....X.XXX.....","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,6]],"tags":["block","broken_four"]}
{"name":"block_human_broken_four_xxx_x","player":1,"board":["...............","...............","...............","...............","...............","...............","...............",".....XXX.X.....","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,8]],"tags":["block","broken_four"]}
{"name":"ai_win_diagonal","player":1,"board":["...............","...............","...............","...............","....O..........",".....O.........","......O........",".......O.......","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[3,3],[8,8]],"tags":["win","diagonal"]}
{"name":"block_human_vertical","player":1,"board":["...............","...............","...............",".......X.......",".......X.......",".......X.......",".......X.......","...............","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[2,7],[7,7]],"tags":["block","vertical"]}
{"name":"prefer_creating_open_four_over_small_attack","player":1,"board":["...............","...............","...............","...............","...............","...............",".....OOO.......",".....XX........","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[6,4],[6,8]],"tags":["attack","open_four"]}
```

- [ ] **Step 2: Create parser and regression test**

Create `tests/test_tactical_cases.py`:

```python
from __future__ import annotations

import json
import sys
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


def test_tactical_cases_choose_expected_moves() -> None:
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

    assert not failures, "\n".join(failures)
```

- [ ] **Step 3: Run baseline tactical test**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m pytest tests\test_tactical_cases.py -v
```

Expected before AI fixes: PASS if current AI already handles all cases, otherwise FAIL listing concrete cases.

---

### Task 2: Focused AI Fixes

**Files:**
- Modify if needed: `backend/threats.py`
- Modify if needed: `backend/evaluator.py`
- Modify if needed: `backend/move_ordering.py`
- Modify if needed: `backend/ai_core.py`
- Test: `tests/test_tactical_cases.py`

- [ ] **Step 1: If broken-four cases fail, improve threat detection**

In `backend/threats.py`, update `ThreatDetector.summarize_line()` so `closed_four` also catches broken-four windows:

```python
    def summarize_line(self, line: str) -> ThreatSummary:
        padded = f"2{line}2"
        five = self._count_windows(line, 5, lambda window: window == "11111")
        open_four = padded.count("011110")
        four_windows = self._count_windows(
            padded,
            5,
            lambda window: window.count("1") == 4 and window.count("0") == 1 and "2" not in window,
        )
        broken_four = self._count_windows(
            padded,
            6,
            lambda window: (
                window.count("1") == 4
                and window.count("0") == 2
                and "2" not in window
                and any(pattern in window for pattern in ("11011", "11101", "10111"))
            ),
        )
        closed_four = max(0, four_windows - open_four * 2) + broken_four
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
```

- [ ] **Step 2: If tests still fail due to priority, tune threat scores**

In `backend/evaluator.py`, adjust only the tactical urgency scores:

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

In `backend/move_ordering.py`, keep move-level tactical ordering strong enough:

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

- [ ] **Step 3: Run tactical test after each AI change**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m pytest tests\test_tactical_cases.py -v
```

Expected after fixes: PASS.

---

### Task 3: Verification And Cleanup

**Files:**
- Verify: `backend/*.py`
- Verify: `arena/*.py`
- Remove if generated: `tests/gomoku_tt_test.pkl`

- [ ] **Step 1: Run backend compile check**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py
```

Expected: no output and exit code 0.

- [ ] **Step 2: Run arena smoke test**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

Expected: command exits successfully and prints a small self-play summary.

- [ ] **Step 3: Remove isolated test cache**

Run:

```powershell
Remove-Item -LiteralPath tests\gomoku_tt_test.pkl -ErrorAction SilentlyContinue
```

Expected: `tests/gomoku_tt_test.pkl` does not remain in the working tree.

- [ ] **Step 4: Check git status**

Run:

```powershell
git status --short
```

Expected: only intentional changes are present. Existing unrelated changes in `IMPLEMENTATION_PLAN.md`, `.codex/`, and `Gomoku_AI_Improvement_Roadmap.md` are not modified by this implementation.
