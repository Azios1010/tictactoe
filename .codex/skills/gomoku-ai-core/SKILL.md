---
name: gomoku-ai-core
description: Work on this Gomoku 15x15 project's classical AI engine. Use when modifying or debugging backend AI files, including minimax, alpha-beta pruning, iterative deepening, Zobrist hashing, transposition table, candidate move generation, move ordering, threat detection, heuristic evaluation, immediate win/block, or threat extension.
---

# Gomoku AI Core

## Workflow

1. Read `AGENTS.md` and `references/project-context.md` before changing AI behavior.
2. Identify the AI layer being touched:
   - Search orchestration: `backend/ai_core.py`
   - Shared types/config: `backend/ai_types.py`
   - Board rules: `backend/board_rules.py`
   - Threat detection: `backend/threats.py`
   - Evaluation: `backend/evaluator.py`
   - Candidate generation and move ordering: `backend/move_ordering.py`
3. Reproduce the behavior with a small board before changing logic.
4. Prefer tactical correctness over increasing depth.
5. Keep `GomokuAI` as the public entry point for `backend/main.py` and `arena/engine.py`.

## AI Rules

- Do not use reinforcement learning, neural-network training, or heavyweight dependencies unless the user explicitly changes the project direction.
- Do not mutate the caller's board. If a move is tested in-place, reset it in `finally`.
- Preserve these stone conventions: `0` empty, `1` AI/O/black, `-1` human/X/white.
- For `player == HUMAN_STONE`, normalize perspective through the existing board normalization path.
- Keep immediate win/block before deep search.
- Keep tactical candidates from being removed by `candidate_limit`.
- Treat `completed_depth == 0` as a signal to inspect timeout, candidate generation, or immediate tactical checks.

## Change Strategy

For search bugs:

1. Check whether the correct move is in `_generate_candidates()`.
2. Inspect `_score_move()` for the correct move and competing moves.
3. Inspect `_threat_summary()` and `evaluate_board()`.
4. Only then adjust depth, candidate limit, or time limit.

For evaluator/threat bugs:

1. Add or run a tactical board case.
2. Test `ThreatDetector.move_summary()` on the key move.
3. Adjust pattern recognition before changing broad score constants.
4. Keep terminal win/loss scores higher than normal heuristic scores.

## Verification

Run Python compile after AI changes:

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py
```

Run arena smoke test after search/evaluator changes:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

Check generated cache before finishing:

```powershell
git status --short
```

If `backend/gomoku_tt.pkl` changed only because of testing, restore it unless the user asked to update cache.
