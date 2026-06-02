# Advanced Tactical AI Design

## Goal

Improve the Gomoku/Caro 15x15 AI in ways that are visible in benchmark results and useful for the AI course report. The focus is tactical correctness: double-threat handling, broken-four priority, forcing-line awareness, and benchmark accuracy reporting.

This is a backend-only change. The frontend and arena UI are out of scope.

## Scope

In scope:

- Add advanced tactical regression tests for double-threat and forcing situations.
- Improve threat/evaluator behavior only where tests expose weak priorities.
- Keep immediate win/block checks before deep search.
- Keep `GomokuAI` as the public AI entry point.
- Extend benchmark output with correctness fields and per-agent accuracy.
- Verify tactical tests, compile checks, arena smoke behavior, and generated files.

Out of scope:

- Reinforcement learning or neural network training.
- Full Threat Space Search or full VCF solver.
- Negamax refactor.
- Parallel search.
- Frontend debug UI.
- Deployment changes.

## Architecture

The implementation will stay within existing backend boundaries:

- `backend/threats.py`: pattern recognition if a double-threat or broken-four pattern is not detected.
- `backend/evaluator.py`: global threat scoring if recognition is correct but priority is too weak.
- `backend/move_ordering.py`: move-level tactical score and forcing candidate helpers.
- `backend/ai_core.py`: bounded forcing search only if candidate/evaluator changes are insufficient.
- `tests/test_advanced_tactics.py`: focused tests for the new tactical behavior.
- `benchmark_ai.py`: benchmark cases with expected moves and accuracy summaries.

Existing tests remain part of the safety net:

- `tests/test_tactical_cases.py`
- `tests/test_forcing_search.py`
- `tests/test_transposition_table.py`

## Tactical Cases

The new tests should cover:

1. AI creates a double-threat when no immediate block is required.
2. AI blocks a human double-threat when it is more urgent than a small attack.
3. AI prioritizes blocking broken-four patterns over low-value attacks.
4. AI selects a forcing open-four move in a two-step tactical board.

Cases should use deterministic boards and accept a small set of equivalent expected moves when symmetry allows.

## Benchmark Changes

`benchmark_ai.py` should add expected move metadata for tactical benchmark cases and emit:

- `expected_moves`
- `is_correct`
- `elapsed_ms`
- `completed_depth`
- `reason`
- `accuracy_by_agent`

The JSON output should remain easy to paste into the BTL report.

## Quality Constraints

- Do not increase difficulty depth or candidate limit as the first fix.
- Do not mutate caller boards permanently; temporary moves must be reset in `finally`.
- Do not write production cache into the diff.
- Keep benchmark data small and reproducible.
- Avoid claiming the AI is state-of-the-art or stronger than tournament engines.

## Verification

Minimum verification:

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_tactical_cases tests.test_forcing_search tests.test_transposition_table tests.test_advanced_tactics -v
```

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py benchmark_ai.py
```

```powershell
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

Before finishing, remove generated `*.pkl`, `__pycache__`, and unintended dataset/cache files.
