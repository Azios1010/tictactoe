# Benchmark Level 2 Design

## Goal

Improve the project benchmark from a simple center-first comparison to a stronger internal baseline comparison suitable for the AI course report.

This benchmark is still not a SOTA comparison. It should not claim the project AI is stronger than Rapfi, Yixin, AlphaZero-Gomoku, or other external engines. Its purpose is to show that the project AI outperforms simple internal baselines on reproducible tactical Gomoku cases.

## Scope

In scope:

- Add internal baseline agents to `benchmark_ai.py`.
- Keep benchmark deterministic and reproducible.
- Add expected move metadata and accuracy reporting for all tactical cases.
- Add tests for benchmark helper functions.
- Regenerate `benchmark_results.json`.

Out of scope:

- Integrating external engines.
- Downloading third-party Gomoku agents.
- Changing frontend or backend API behavior.
- Changing production AI search logic.
- Running large self-play experiments.

## Agents

The benchmark should compare:

1. `random_baseline`
   - Picks a legal empty cell using a fixed random seed.
   - Used as a lower-bound baseline.

2. `center_first_baseline`
   - Picks center if available, otherwise nearest empty cell.
   - Already exists and remains as a simple positional baseline.

3. `greedy_1ply_baseline`
   - Scores candidate moves by placing AI once and evaluating the resulting board.
   - No minimax, alpha-beta, forcing search, or opponent reply.

4. `basic_minimax_baseline`
   - Uses shallow minimax/alpha-beta with the existing evaluator.
   - Does not use the full project AI pipeline such as immediate tactical pre-checks, forcing search, transposition table best-move ordering, or difficulty presets.

5. `project_easy`, `project_medium`, `project_hard`
   - Existing project AI configurations.

## Benchmark Cases

The benchmark should include:

- `opening`
- `ai_win_horizontal`
- `block_open_four`
- `block_broken_four`
- `forcing_open_four`
- `create_double_three`
- `block_double_three`
- `diagonal_win`
- `midgame`

All tactical cases except `midgame` should include `expected_moves`. `midgame` can remain a qualitative speed/depth case with no correctness score.

## Output Format

`benchmark_results.json` should contain:

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

Each row in `results` should include:

- `case`
- `agent`
- `move`
- `expected_moves`
- `is_correct`
- `score`
- `reason`
- `completed_depth`
- `elapsed_ms`

## Reporting Guidance

The report should describe this as a Level 2 internal benchmark:

```text
The benchmark compares the project AI against deterministic internal baselines: random move, center-first, greedy 1-ply, and shallow minimax. It does not compare against tournament Gomoku engines or SOTA systems.
```

This gives stronger evidence than center-first alone while staying practical for a BTL.

## Verification

Minimum verification:

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_benchmark_output -v
```

```powershell
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

```powershell
.\backend\venv\Scripts\python.exe -m py_compile benchmark_ai.py
```

Before finishing, remove generated `*.pkl` and `__pycache__` files. Keep `benchmark_results.json` as report evidence.
