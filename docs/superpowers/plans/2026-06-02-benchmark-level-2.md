# Benchmark Level 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `benchmark_ai.py` to compare project AI against deterministic internal baselines: random, center-first, greedy 1-ply, and shallow minimax.

**Architecture:** Keep the benchmark as a standalone root script using only Python standard library and existing backend AI modules. Add helper functions with unit tests first, then regenerate `benchmark_results.json` with `benchmark_notes` and `accuracy_by_agent`.

**Tech Stack:** Python 3, `unittest`, existing Gomoku backend modules.

---

### Task 1: Benchmark Helper Tests

**Files:**
- Modify: `tests/test_benchmark_output.py`

- [ ] **Step 1: Add tests for random and greedy helpers**

Add tests for deterministic random baseline, expected-move correctness, and accuracy summaries.

- [ ] **Step 2: Run tests red**

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_benchmark_output -v
```

Expected: FAIL until new helpers exist.

---

### Task 2: Internal Baseline Agents

**Files:**
- Modify: `benchmark_ai.py`

- [ ] **Step 1: Add `random_baseline`**

Use `random.Random(seed)` and legal empty cells.

- [ ] **Step 2: Add `greedy_1ply_baseline`**

Evaluate each candidate after placing `AI_STONE`, then choose the highest evaluation.

- [ ] **Step 3: Add `basic_minimax_baseline`**

Implement a shallow alpha-beta minimax using existing evaluator and candidate generation, without project AI tactical pre-checks or persistent TT.

- [ ] **Step 4: Run helper tests green**

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_benchmark_output -v
```

Expected: PASS.

---

### Task 3: Benchmark Cases And JSON Output

**Files:**
- Modify: `benchmark_ai.py`
- Modify: `benchmark_results.json`

- [ ] **Step 1: Add benchmark cases**

Add `ai_win_horizontal`, `block_broken_four`, and `diagonal_win` in addition to existing cases.

- [ ] **Step 2: Add benchmark notes**

Output JSON should contain:

```json
{
  "results": [],
  "accuracy_by_agent": {},
  "benchmark_notes": {
    "comparison_level": "internal_baselines",
    "not_sota": true,
    "external_engines": "not integrated"
  }
}
```

- [ ] **Step 3: Run benchmark**

```powershell
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

Expected: `benchmark_results.json` includes all baseline and project agents.

---

### Task 4: Verification And Cleanup

**Files:**
- Verify: `benchmark_ai.py`
- Verify: `tests/test_benchmark_output.py`

- [ ] **Step 1: Compile**

```powershell
.\backend\venv\Scripts\python.exe -m py_compile benchmark_ai.py
```

- [ ] **Step 2: Benchmark tests**

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_benchmark_output -v
```

- [ ] **Step 3: Cleanup**

Remove generated benchmark `*.pkl` and `__pycache__`. Keep `benchmark_results.json`.
