# AI Tactical Improvement Design

## Goal

Improve the Gomoku/Caro 15x15 AI by making tactical behavior measurable first, then adjusting threat detection, evaluation, or move ordering only where tests show a concrete weakness.

The first target is tactical correctness, not deeper search. The AI should reliably choose immediate wins, block immediate losses, respond to open-four and broken-four threats, and avoid obviously disconnected moves in small reproducible boards.

## Scope

This change will add a tactical benchmark suite and use it to guide focused AI fixes.

In scope:

- Add fixed tactical board fixtures under `tests/fixtures/`.
- Add a Python test that parses those fixtures and calls `GomokuAI.get_move_analysis()`.
- Use a test-only transposition table file so benchmark runs do not mutate production cache.
- Fix AI behavior only if tactical tests expose a failure.
- Verify backend syntax, tactical tests, arena smoke behavior, and generated files.

Out of scope:

- Reinforcement learning, neural network training, or heavy dependencies.
- Increasing difficulty depth or candidate limits as the primary fix.
- Claiming tournament-engine strength.
- Large frontend changes.
- Dataset generation unless explicitly requested later.

## Architecture

The tactical suite will live outside the backend package:

- `tests/fixtures/tactical_cases.jsonl`: one JSON object per board case.
- `tests/test_tactical_cases.py`: parser and regression test runner.

Fixtures use a readable board format:

- `.` means empty, value `0`.
- `O` means AI stone, value `1`.
- `X` means human stone, value `-1`.

Each case includes:

- `name`
- `player`
- `board`
- `expected_moves`
- `tags`

The test runner creates a `GomokuAI` instance with a stable `SearchConfig` and a cache file under `tests/`, then checks whether the selected move is in `expected_moves`.

## AI Change Path

If tests fail, fixes will follow the existing module boundaries:

- `backend/threats.py`: pattern recognition such as broken-four or open-four detection.
- `backend/evaluator.py`: threat score balance when recognition is correct but priorities are wrong.
- `backend/move_ordering.py`: candidate scoring when the correct move exists but is searched too late.
- `backend/ai_core.py`: search orchestration only if the failure is caused by timeout, candidate pruning, or immediate tactical checks.

The implementation should preserve `GomokuAI` as the public entry point and keep immediate win/block checks before deep search.

## Error Handling

Fixture parsing will fail loudly if a board is not 15x15 or contains an unknown symbol. Test failures will report the case name, actual move, expected moves, and AI reason.

Generated cache files from tests will be isolated under `tests/` and removed after verification when they are not intended artifacts.

## Testing

Minimum verification after implementation:

- Python compile check for backend and arena modules.
- Tactical regression test.
- Arena smoke test with a small self-play run.
- `git status --short` to confirm no unintended cache or dataset changes.

If frontend files are not changed, frontend build is not required for this AI-only task.
