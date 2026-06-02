# Benchmark Context

The project is a Gomoku/Caro 15x15 classical AI engine with:

- Easy: low depth and short time limit.
- Medium: balanced depth/time.
- Hard: higher depth/time and threat extension.

Useful files:

- `IMPLEMENTATION_PLAN.md`: current AI improvement and benchmark plan.
- `Gomoku_AI_Improvement_Roadmap.md`: candidate future improvements.
- `backend/main.py`: difficulty configs.
- `backend/ai_core.py`: move analysis and completed depth.
- `arena/engine.py`: self-play and JSONL sample generation.

Metrics suitable for a course report:

- Tactical accuracy over fixed board cases.
- Average move latency in milliseconds.
- Completed search depth.
- Reason returned by AI.
- Correct immediate win/block behavior.
- No illegal moves.

Baselines suitable for local comparison:

- Center-first baseline.
- Greedy 1-ply evaluator baseline.
- Basic minimax without threat-aware ordering, if implemented.
- Project Easy, Medium, Hard.

External systems should usually be used for qualitative comparison only unless integrated and run under the same rules:

- Rapfi.
- Yixin.
- AlphaZero-Gomoku style models.
