# Kaggle Consultant Training Notebook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Kaggle-ready notebook that trains and evaluates a supervised Gomoku policy-value consultant model from JSONL self-play data.

**Architecture:** The notebook is self-contained and does not import the local backend. It discovers Kaggle input JSONL files, performs file-level train/validation/test split, streams samples into PyTorch, trains a compact CNN, evaluates report-grade top-K metrics with legal move masking, and exports checkpoint plus metrics.

**Tech Stack:** Kaggle Notebook, Python, PyTorch, NumPy, JSONL.

---

### Task 1: Create Kaggle Notebook

**Files:**
- Create: `notebooks/kaggle_gomoku_consultant_training.ipynb`

- [x] **Step 1: Add notebook sections**

Create markdown/code cells for goal, config, data discovery, schema inspection, split, dataset, model, metrics, training, final evaluation, tactical diagnostics, inference demo, and export.

- [x] **Step 2: Keep notebook self-contained**

Do not import project backend modules. Define board encoding, dataset parsing, CNN, metrics, and export logic inside the notebook.

- [x] **Step 3: Optimize for report metrics**

Compute top-1, top-3, top-5 agreement, illegal top-1 rate, value MAE/MSE, and inference latency. Include random-legal and center-first baselines.

- [x] **Step 4: Support Kaggle constraints**

Use streaming JSONL reading, configurable `MAX_TRAIN_SAMPLES`, `MAX_EVAL_SAMPLES`, `BATCH_SIZE`, `EPOCHS`, and Kaggle paths under `/kaggle/input` and `/kaggle/working`.

- [x] **Step 5: Verify JSON structure**

Run a local JSON parse of the `.ipynb` file to ensure the notebook is valid.
