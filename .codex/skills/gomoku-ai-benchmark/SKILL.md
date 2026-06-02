---
name: gomoku-ai-benchmark
description: Create, run, or interpret benchmarks for this Gomoku 15x15 AI project. Use when building tactical cases, comparing Easy Medium Hard difficulty, measuring response time or completed depth, creating benchmark scripts, generating JSON results, or preparing benchmark tables for the AI course report.
---

# Gomoku AI Benchmark

## Workflow

1. Read `references/project-context.md` and `IMPLEMENTATION_PLAN.md`.
2. Decide whether the benchmark is tactical correctness, speed, or self-play.
3. Keep benchmark boards small and reproducible.
4. Compare against simple baselines before discussing external engines.
5. Save generated data only when the user asks; otherwise avoid committing cache or datasets.

## Benchmark Types

### Tactical correctness

Use fixed board cases for:

- Opening center.
- AI immediate win.
- Human immediate win block.
- Open-four block.
- Closed-four block.
- Broken-four block: `XX.XX`, `XXX.X`, `X.XXX`.
- Diagonal threats.
- Double threat.

Recommended fixture format:

```json
{"name":"block_open_four_horizontal","player":1,"board":["..............."],"expected_moves":[[7,4],[7,9]],"tags":["block","open_four"]}
```

Board symbols:

- `.` empty
- `O` AI stone, value `1`
- `X` human stone, value `-1`

### Speed and depth

Measure:

- Move selected.
- Reason.
- Evaluation score.
- Completed depth.
- Elapsed milliseconds.

Compare:

- `center_first_baseline`
- `project_easy`
- `project_medium`
- `project_hard`

### Arena smoke benchmark

Use arena only for basic stability unless the user asks for dataset generation:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

## Required Commands

Python compile:

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py
```

Tactical tests, if present:

```powershell
.\backend\venv\Scripts\python.exe -m pytest tests\test_tactical_cases.py -v
```

Check generated files:

```powershell
git status --short
```

## Reporting Rules

- Do not claim the project beats Rapfi, Yixin, or AlphaZero-style systems without direct controlled matches.
- Report local benchmark conditions: machine, difficulty, depth, time limit, candidate limit.
- Prefer tables with `Case | Agent | Move | Reason | Completed Depth | Time ms`.
- If benchmark data is missing, state that the section is a proposed benchmark plan, not measured evidence.
