---
name: gomoku-ai-report
description: Write AI-focused report content for this Gomoku 15x15 project. Use when drafting contributions, methodology, benchmark discussion, limitations, future work, or comparisons with Rapfi, Yixin, AlphaZero-Gomoku, minimax baselines, or other Gomoku AI systems for an AI course report.
---

# Gomoku AI Report

## Workflow

1. Read `references/project-context.md`, `IMPLEMENTATION_PLAN.md`, and any benchmark result files the user provides.
2. Keep the report focused on AI, not web app features.
3. Separate implemented contributions from future work.
4. Use cautious wording when comparing with strong external engines.
5. Prefer evidence-backed claims using benchmark tables or code references.

## Main Contribution Claims

Use these as the core AI contributions:

1. Candidate move generation reduces branching factor on a 15x15 board.
2. Move ordering improves alpha-beta pruning by searching tactical moves first.
3. Threat detection models Gomoku-specific patterns.
4. Pattern-based evaluation combines attack and defense scores.
5. Immediate win/block prevents obvious one-ply tactical mistakes.
6. Iterative deepening and time limits make search usable in an interactive setting.
7. Zobrist hashing and transposition table reduce repeated search.
8. Arena self-play can generate JSONL samples for analysis or later training.

## Claims To Avoid

Do not claim these as completed unless code and tests prove them:

- Stronger than Rapfi or Yixin.
- State-of-the-art Gomoku AI.
- Full Threat Space Search.
- Full VCF solver.
- Neural-network training.
- Reinforcement learning.
- Principal Variation Search.
- Killer move or history heuristic.
- Parallel search.

## Comparison Framing

Use this framing:

```text
The goal is not to outperform tournament engines such as Rapfi or Yixin. The project demonstrates how classical AI search techniques can be combined with Gomoku-specific threat knowledge to produce a practical, explainable 15x15 Gomoku agent.
```

Compare systems by method:

- Basic minimax: simple but too slow or tactically weak on 15x15.
- Project AI: minimax plus alpha-beta, candidate pruning, move ordering, threat detection, evaluator, TT, time limit.
- Rapfi/Yixin: advanced tournament engines with deeper engineering and stronger domain optimizations.
- AlphaZero-Gomoku: learning-based approach using self-play, MCTS, and neural networks.

## Benchmark Section Template

Use this table format:

```markdown
| Case | Agent | Move | Reason | Completed Depth | Time (ms) |
|---|---|---|---|---:|---:|
```

Interpretation pattern:

```text
The tactical benchmark shows whether the AI selects moves that satisfy immediate Gomoku constraints such as winning in one move or blocking an opponent four. Latency and completed depth show the trade-off between playing strength and interactive response time.
```

## Future Work

Recommended future work, in order:

1. Tactical benchmark suite.
2. Stronger pattern evaluator for broken-four and double-threat cases.
3. Enhanced transposition table storing best move.
4. Minimal Threat Space Search or VCF solver.
5. Killer move and history heuristic.
6. PVS and aspiration window.
7. Parallel root search.
