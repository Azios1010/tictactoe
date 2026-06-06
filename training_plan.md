# Report-Optimized Training Plan for a Gomoku Consultant Model

This plan trains a lightweight supervised **Policy-Value Consultant/Advisor**
model from self-play data. The model is not intended to replace the current
classical Gomoku engine. Its purpose is to provide fast move recommendations
and measurable experimental results for the AI course report.

The main report claim should be:

```text
The consultant model learns to imitate the project engine's self-play move
choices and can provide real-time top-K move advice on a 15x15 Gomoku board.
```

Do not describe the metric as absolute "best move accuracy" unless the labels
come from a stronger verified oracle. In this project, the safest and clearest
wording is **top-1 agreement with the self-play engine**.

---

## Objectives

1. Train a small CNN that predicts the next move and board value from a
   normalized 15x15 board.
2. Report top-1, top-3, and top-5 policy agreement on a held-out test set.
3. Report value prediction quality with MAE/MSE.
4. Verify the model does not recommend illegal occupied squares.
5. Compare against simple baselines so the report has meaningful context.
6. Integrate the model as an optional frontend advisor overlay, not as the main
   game-playing engine.

---

## User Review Required

> [!IMPORTANT]
> PyTorch is a heavy dependency. Keep ML dependencies separate from the normal
> backend runtime unless the advisor feature is enabled.

Recommended dependency layout:

- `backend/requirements.txt`: keep the current lightweight FastAPI/classical AI
  dependencies.
- `dl/requirements.txt`: add `torch` and `numpy` for training/evaluation.
- Backend inference may import PyTorch lazily and fail gracefully when
  `backend/consultant_model.pt` or `torch` is unavailable.

> [!IMPORTANT]
> The dataset may contain around 1.7-1.8 million board states. Training scripts
> must support limits such as `--max-samples`, `--max-files`, and
> `--epochs` so the pipeline can run on a local CPU for demonstration.

---

## Dataset Contract

The current arena/self-play data should be treated as the source of supervised
training labels. Before implementing training, inspect the JSONL schema and
normalize it into a consistent internal sample format:

```json
{
  "board": [[0, 0, 0]],
  "player": 1,
  "move": [7, 8],
  "policy": null,
  "value": 0.35,
  "game_id": "optional",
  "source_file": "optional"
}
```

Supported label modes:

- If the sample has a single `move`, train policy with hard-label
  `CrossEntropyLoss` over 225 board positions.
- If the sample has a probability vector such as `prob` or `policy`, train with
  soft-label cross entropy or KL divergence.
- If the sample has `reward`, `outcome`, `winner`, or `evaluation`, convert it
  into a scalar value target in `[-1, 1]`.

Board normalization:

- The side to move is always represented as the current player.
- Channel 0: current player's stones.
- Channel 1: opponent's stones.
- Channel 2: empty squares.
- Input tensor shape: `(3, 15, 15)`.

Legal move handling:

- Occupied positions must never be valid prediction targets.
- During inference and evaluation, mask occupied squares by setting their logits
  to negative infinity before sorting top-K moves.
- Report `illegal_top1_rate`; the expected target is `0%` after masking.

---

## Train/Validation/Test Split

Split by game or source file, not by individual board rows, to reduce data
leakage from near-identical positions in the same game.

Recommended split:

- Train: 80%
- Validation: 10%
- Test: 10%

Rules:

- All augmented versions of the same position stay in the same split.
- Validation is used for early stopping and model selection.
- Test is used only once for final report numbers.
- Save the split manifest to `dl/splits/*.json` for reproducibility.

---

## Model

### [NEW] `dl/model.py`

Define `PolicyValueNet`, a compact CNN:

- Input: `(batch, 3, 15, 15)`.
- Shared trunk: 4 convolution blocks with BatchNorm and ReLU.
- Policy head: logits over 225 board positions.
- Value head: one scalar in `[-1, 1]` using `tanh`.

Keep the model small enough for CPU inference:

- Target model size: under 5 MB if practical.
- Target inference latency: below 50 ms per board on a typical local CPU.

---

## Training Pipeline

### [NEW] `dl/dataset.py`

Responsibilities:

- Stream JSONL samples from `data/`, `data/additional/`, or `arena/data/`.
- Normalize board perspective.
- Convert move labels to flat indices in `[0, 224]`.
- Convert value labels to `[-1, 1]`.
- Apply optional data augmentation.

Augmentations:

- Rotations: 90, 180, 270 degrees.
- Horizontal and vertical flips.
- Apply the same transform to board and move/policy label.

### [NEW] `dl/train_policy.py`

Training configuration:

- Optimizer: AdamW.
- Policy loss: hard or soft cross entropy depending on label mode.
- Value loss: MSE.
- Total loss: `policy_loss + value_weight * value_loss`.
- Default `value_weight`: `0.25`.
- Early stopping on validation top-1 or validation loss.

CLI options:

```powershell
python -m dl.train_policy --data data --max-samples 50000 --epochs 5 --batch-size 128
```

Outputs:

- `backend/consultant_model.pt`: model weights.
- `dl/runs/<run_id>/metrics.json`: train/validation metrics.
- `dl/runs/<run_id>/config.json`: exact configuration.

Do not commit large run artifacts unless the task explicitly asks for them.

---

## Evaluation for the Report

### [NEW] `dl/evaluate_policy.py`

Evaluate the selected checkpoint on the held-out test split.

Required metrics:

| Metric | Meaning |
|---|---|
| `top1_accuracy` | Predicted best legal move equals the engine/self-play label |
| `top3_accuracy` | Label appears in the top 3 legal predictions |
| `top5_accuracy` | Label appears in the top 5 legal predictions |
| `illegal_top1_rate` | Top-1 prediction is occupied before/after masking |
| `value_mae` | Mean absolute error of value head |
| `value_mse` | Mean squared error of value head |
| `latency_ms_mean` | Average single-board inference time |
| `latency_ms_p95` | 95th percentile inference time |

Baseline comparisons:

| Baseline | Purpose |
|---|---|
| Random legal move | Lower-bound policy baseline |
| Center-first heuristic | Simple Gomoku prior |
| Current classical AI, easy config | Lightweight symbolic baseline |
| Consultant CNN | Learned advisor result |

Recommended report table:

```markdown
| Model | Top-1 | Top-3 | Top-5 | Illegal Top-1 | Value MAE | Mean Latency ms |
|---|---:|---:|---:|---:|---:|---:|
```

Interpretation:

```text
Top-1 measures exact agreement with the move selected in the self-play dataset.
Top-3 and top-5 are also important because many Gomoku positions have multiple
reasonable moves. Latency shows whether the advisor is practical for real-time
frontend hints.
```

---

## Tactical Evaluation Set

Top-1 agreement on self-play data is not enough for a convincing Gomoku report.
Add a small hand-written tactical suite to test whether the advisor understands
obvious local threats.

### [NEW] `dl/tactical_cases.json`

Include cases such as:

- Opening center preference.
- AI immediate win.
- Human immediate win block.
- Open-four block.
- Closed-four block.
- Broken-four block: `XX.XX`, `XXX.X`, `X.XXX`.
- Diagonal four.
- Double-threat creation.

Fixture format:

```json
{
  "name": "block_open_four_horizontal",
  "player": 1,
  "board": [
    "...............",
    "..............."
  ],
  "expected_moves": [[7, 4], [7, 9]],
  "tags": ["block", "open_four"]
}
```

Report metrics:

- `tactical_top1_accuracy`
- `tactical_top3_accuracy`
- Accuracy by tag: `win`, `block`, `open_four`, `broken_four`, `diagonal`,
  `double_threat`

This section should be framed as diagnostic evaluation, not proof that the CNN
is stronger than the classical engine.

---

## Inference Wrapper

### [NEW] `dl/predict_policy.py`

Provide:

```python
def predict_top_moves(board: list[list[int]], player: int, top_k: int = 3) -> dict:
    ...
```

Return:

```json
{
  "moves": [
    {"row": 7, "col": 8, "probability": 0.42, "rank": 1}
  ],
  "value": 0.35,
  "model_available": true
}
```

Requirements:

- Normalize board perspective.
- Mask illegal occupied squares.
- Softmax only over legal squares.
- Sort by probability descending.
- Fail gracefully if PyTorch or the checkpoint is unavailable.

---

## Backend Integration

### [MODIFY] `backend/main.py`

Add a new endpoint:

```http
POST /api/get-consultation
```

Request:

```json
{
  "board": [[0, 0, 0]],
  "player": 1,
  "top_k": 3
}
```

Response:

```json
{
  "moves": [
    {"row": 7, "col": 8, "probability": 0.42, "rank": 1}
  ],
  "value": 0.35,
  "model_available": true,
  "message": "Consultation generated successfully."
}
```

Integration rules:

- Import the PyTorch predictor lazily.
- If the model is missing, return `model_available: false` instead of crashing.
- Keep `/api/get-move` fully classical and independent.
- Do not block normal gameplay if advisor inference fails.

---

## Frontend Integration

### [MODIFY] `frontend/src/App.jsx`

Add an optional **Consultant Advisor** toggle in play mode.

Behavior:

- When enabled, call `POST /api/get-consultation` after each board update.
- Display top-3 recommendations on legal empty squares.
- Use rank badges or a subtle heatmap overlay.
- Show value/win-rate estimate in the existing stats area.
- Hide advisor marks when the game ends or when the model is unavailable.

Report-friendly UI note:

- The UI should make it clear that the advisor is a recommendation overlay.
- It should not imply the CNN is the main AI opponent.

---

## Verification Plan

### Static and Unit Checks

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py
```

Add tests for:

- Board normalization.
- Move index transforms under rotation/flip.
- Illegal move masking.
- Model save/load.
- `/api/get-consultation` missing-model fallback.

### Small Training Smoke Test

```powershell
python -m dl.train_policy --data arena/data --max-samples 1000 --epochs 1 --batch-size 32
```

Expected:

- Training loop completes.
- A checkpoint can be saved.
- Evaluation script runs on a tiny split.
- No dataset/cache artifacts are committed unless requested.

### Final Report Run

Use a reproducible command such as:

```powershell
python -m dl.train_policy --data data --max-samples 50000 --epochs 5 --batch-size 128 --seed 42
python -m dl.evaluate_policy --checkpoint backend/consultant_model.pt --split test
python -m dl.evaluate_tactical --checkpoint backend/consultant_model.pt
```

Record:

- Dataset size used.
- Number of train/validation/test samples.
- Hardware environment.
- Training time.
- Final top-1/top-3/top-5.
- Tactical results.
- Inference latency.

---

## Report Framing

Use cautious language:

```text
The learned advisor is evaluated by agreement with the project's self-play
engine labels. This does not prove optimal Gomoku play, but it measures whether
the neural model can compress the classical engine's local decision patterns
into a fast inference model suitable for interactive hints.
```

Avoid claims such as:

- Stronger than Rapfi or Yixin.
- State-of-the-art Gomoku AI.
- Reinforcement learning.
- AlphaZero-style training.
- The CNN finds objectively optimal moves.

Good contribution wording:

```text
In addition to the explainable classical search engine, the project explores a
supervised learning advisor trained from self-play traces. The advisor provides
top-K move suggestions and value estimates, while the report evaluates exact
top-1 agreement, broader top-K agreement, tactical behavior, and real-time
latency.
```

---

## Recommended Implementation Order

1. Inspect JSONL schema and write a dataset adapter.
2. Implement normalization, legal masking, and augmentation tests.
3. Implement `PolicyValueNet`.
4. Train on a tiny sample to validate the pipeline.
5. Add evaluation scripts and baseline metrics.
6. Create tactical evaluation fixtures.
7. Train a report-scale run with a fixed seed.
8. Integrate backend consultation endpoint.
9. Add frontend advisor overlay.
10. Write final report tables from saved metrics.

---

## Success Criteria

The plan is successful when:

- The training pipeline runs on a limited local dataset.
- The report includes top-1/top-3/top-5 agreement, value error, tactical
  accuracy, and latency.
- The advisor never recommends occupied squares after legal masking.
- The frontend can show top-3 recommendations without replacing the classical
  AI opponent.
- Claims remain evidence-backed and do not overstate the learned model.
