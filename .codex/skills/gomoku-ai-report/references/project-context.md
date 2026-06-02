# Report Context

Project identity:

- Repository name: `Tictactoe`.
- Actual game: Gomoku/Caro 15x15.
- Frontend: React/Vite.
- Backend: Python FastAPI.
- AI direction: classical search, no RL or model training.

AI modules:

- `backend/ai_core.py`: search orchestration, minimax, alpha-beta, iterative deepening, Zobrist hashing, TT.
- `backend/threats.py`: threat pattern recognition.
- `backend/evaluator.py`: heuristic evaluation.
- `backend/move_ordering.py`: candidate generation and move ordering.
- `arena/engine.py`: self-play and JSONL generation.

Implemented AI features:

- Minimax and alpha-beta pruning.
- Iterative deepening under time limit.
- Zobrist hash.
- Transposition table with side-to-move.
- Immediate win and block checks.
- Candidate pruning around existing stones.
- Threat-aware move ordering.
- Threat-based and pattern-based evaluation.
- Limited threat extension.

Most important report angle:

The project contributes an explainable classical AI pipeline for Gomoku 15x15. It combines general adversarial search with Gomoku-specific threat knowledge, making the system suitable for an AI course report even without neural training.
