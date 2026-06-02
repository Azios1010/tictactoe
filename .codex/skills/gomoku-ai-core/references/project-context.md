# Project Context

This repository is a Gomoku/Caro 15x15 project despite the `Tictactoe` folder name.

Core AI files:

- `backend/ai_types.py`: constants, `SearchConfig`, `MoveAnalysis`, `ThreatSummary`.
- `backend/board_rules.py`: bounds, winner checks, normalization, line potential.
- `backend/threats.py`: pattern-based threat detection.
- `backend/evaluator.py`: heuristic evaluator, `AttackScore - DefenseScore`.
- `backend/move_ordering.py`: candidates, tactical scoring, reason classification.
- `backend/ai_core.py`: `GomokuAI`, minimax, alpha-beta, iterative deepening, Zobrist hash, transposition table.

Important implemented concepts:

- Candidate generation around existing stones.
- Immediate AI win and human-win block.
- Move ordering using local shape and threat score.
- Threat detection for five, open four, closed four, open three, broken three, double threat.
- Iterative deepening with time limits.
- Threat extension for forcing candidates.
- Transposition table keyed with side-to-move.

Do not claim these are complete unless implemented in code:

- Principal Variation Search.
- Killer move heuristic.
- History heuristic.
- Aspiration window.
- Parallel search.
- Full Threat Space Search or full VCF solver.
