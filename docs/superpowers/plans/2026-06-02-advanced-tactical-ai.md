# Advanced Tactical AI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve backend tactical intelligence and benchmark evidence for double-threat, broken-four, and benchmark accuracy.

**Architecture:** Keep changes inside the existing backend AI modules. Add focused `unittest` regression coverage first, then update `ThreatDetector`, `BoardEvaluator`, `MoveOrdering`, and `benchmark_ai.py` only where tests require it. No frontend, deployment, RL, neural training, or broad search refactor.

**Tech Stack:** Python 3 standard library, `unittest`, existing FastAPI/Gomoku backend modules.

---

### Task 1: Advanced Tactical Tests

**Files:**
- Create: `tests/test_advanced_tactics.py`

- [ ] **Step 1: Add failing detector and move tests**

Create tests that assert:

```python
ThreatDetector().summarize_line("0110110").closed_four >= 1
ThreatDetector().summarize_line("0111010").closed_four >= 1
ThreatDetector().summarize_line("0101110").closed_four >= 1
```

Also add board-level AI tests for:

- AI creates a double open-three from a center move.
- AI blocks the same double open-three if the human can create it.

- [ ] **Step 2: Verify red**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_advanced_tactics -v
```

Expected: detector tests fail before `ThreatDetector.summarize_line()` is improved.

---

### Task 2: Threat Detector And Ordering Improvements

**Files:**
- Modify: `backend/threats.py`
- Modify: `backend/move_ordering.py`
- Modify: `backend/evaluator.py`
- Test: `tests/test_advanced_tactics.py`

- [ ] **Step 1: Count broken-four as closed-four**

In `ThreatDetector.summarize_line()`, count windows containing `11011`, `11101`, or `10111` with two open cells as urgent closed-four threats.

- [ ] **Step 2: Keep double-threat urgency high**

If board-level tests need it, tune `BoardEvaluator.THREAT_SCORES` and `MoveOrdering.score_move_threats()` without increasing search depth or candidate limit.

- [ ] **Step 3: Verify green**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_advanced_tactics -v
```

Expected: PASS.

---

### Task 3: Benchmark Accuracy Output

**Files:**
- Modify: `benchmark_ai.py`

- [ ] **Step 1: Add expected moves to benchmark cases**

Represent benchmark cases as objects with:

```python
{
    "name": "forcing_open_four",
    "board": create_forcing_open_four_board(),
    "expected_moves": {(6, 4), (6, 8)},
}
```

- [ ] **Step 2: Emit correctness fields**

Each benchmark row should include:

- `expected_moves`
- `is_correct`

The final JSON should include:

- `results`
- `accuracy_by_agent`

- [ ] **Step 3: Verify benchmark**

Run:

```powershell
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

Expected: `benchmark_results.json` contains `results` and `accuracy_by_agent`.

---

### Task 4: Full Backend Verification

**Files:**
- Verify backend and generated benchmark output.

- [ ] **Step 1: Run regression tests**

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_tactical_cases tests.test_forcing_search tests.test_transposition_table tests.test_advanced_tactics -v
```

- [ ] **Step 2: Run compile check**

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py benchmark_ai.py
```

- [ ] **Step 3: Run arena smoke**

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

- [ ] **Step 4: Cleanup generated cache**

Remove `tests/*.pkl`, `gomoku_tt.pkl`, and `tests/__pycache__` if generated. Keep `benchmark_results.json` because it is report evidence.
