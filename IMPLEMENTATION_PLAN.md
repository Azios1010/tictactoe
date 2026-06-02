# Gomoku AI Improvement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Nâng cấp và đánh giá AI Gomoku 15x15 theo hướng classical game AI, tập trung vào benchmark, tactical correctness, threat-aware evaluation và search optimization.

**Architecture:** AI vẫn đi theo hướng không dùng reinforcement learning hoặc model training. Core engine nằm trong `backend/`, gồm search orchestration, board rules, threat detection, evaluator và move ordering. Các cải tiến phải giữ `GomokuAI` là public entry point để `backend/main.py` và `arena/engine.py` tiếp tục dùng chung.

**Tech Stack:** Python 3, FastAPI, React/Vite, classical minimax/alpha-beta, iterative deepening, Zobrist hashing, transposition table, JSONL benchmark data.

---

## Trọng Tâm Đóng Góp AI

Dự án cần được trình bày như một hệ thống AI Gomoku classical-search, không phải một sản phẩm web là chính. Các đóng góp chính nên nhấn mạnh:

1. **Candidate move generation**: giảm branching factor bằng cách chỉ xét các ô gần quân đã đánh, đồng thời không loại bỏ tactical moves quan trọng.
2. **Move ordering**: ưu tiên thắng ngay, chặn thắng, tạo/chặn four, tạo/chặn three và double threat để alpha-beta pruning cắt nhánh hiệu quả hơn.
3. **Threat detection**: nhận diện five, open four, closed four, open three, broken three và double threat.
4. **Pattern-based evaluation**: chấm điểm bàn cờ theo công thức `AttackScore - DefenseScore`, kết hợp threat score và contiguous pattern score.
5. **Immediate win/block**: kiểm tra nước thắng hoặc chặn thắng một lượt trước khi search sâu.
6. **Iterative deepening with time limit**: trả nước đi ổn định trong giới hạn thời gian.
7. **Zobrist hash + transposition table**: cache trạng thái search, có phân biệt side-to-move.
8. **Threat extension / quiescence giới hạn**: tiếp tục search một số forcing moves khi leaf node còn threat nguy hiểm.

## Phạm Vi Hiện Tại

### Đã có trong code

- `backend/ai_types.py`: constants, `SearchConfig`, `MoveAnalysis`, `ThreatSummary`.
- `backend/board_rules.py`: winner check, bounds, normalize board, line potential.
- `backend/threats.py`: threat detector theo line pattern.
- `backend/evaluator.py`: board evaluator kết hợp threat score và contiguous pattern score.
- `backend/move_ordering.py`: candidate generation, scoring, tactical candidate, reason classification.
- `backend/ai_core.py`: minimax, alpha-beta, iterative deepening, transposition table, Zobrist hash, immediate win/block, threat extension.
- `arena/engine.py`: self-play và xuất sample JSONL.

### Chưa nên claim là đã hoàn thiện

- Principal Variation Search.
- Killer Move Heuristic.
- History Heuristic.
- Aspiration Window.
- Parallel Search.
- Threat Space Search / VCF solver đầy đủ.
- Benchmark chuẩn hóa với engine ngoài như Rapfi hoặc Yixin.

---

## Task 1: Tạo Tactical Benchmark Suite

**Mục tiêu:** Có bộ test/benchmark chiến thuật để chứng minh AI xử lý đúng các tình huống Gomoku quan trọng.

**Files:**
- Create: `tests/fixtures/tactical_cases.jsonl`
- Create: `tests/test_tactical_cases.py`

- [ ] **Step 1: Tạo thư mục test**

Run:

```powershell
New-Item -ItemType Directory -Force tests
New-Item -ItemType Directory -Force tests\fixtures
```

Expected: thư mục `tests/` và `tests/fixtures/` tồn tại.

- [ ] **Step 2: Thêm fixture tactical cases**

Create `tests/fixtures/tactical_cases.jsonl` with:

```jsonl
{"name":"opening_center","player":1,"board":["...............","...............","...............","...............","...............","...............","...............","...............","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,7]],"tags":["opening"]}
{"name":"ai_win_horizontal","player":1,"board":["...............","...............","...............","...............","...............","...............","...............",".....OOOO......","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,4],[7,9]],"tags":["win","five"]}
{"name":"block_human_open_four_horizontal","player":1,"board":["...............","...............","...............","...............","...............","...............","...............",".....XXXX......","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,4],[7,9]],"tags":["block","open_four"]}
{"name":"block_human_broken_four_xx_xx","player":1,"board":["...............","...............","...............","...............","...............","...............","...............",".....XX.XX.....","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,7]],"tags":["block","broken_four"]}
{"name":"ai_win_diagonal","player":1,"board":["...............","...............","...............","...............","....O..........",".....O.........","......O........",".......O.......","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[3,3],[8,8]],"tags":["win","diagonal"]}
{"name":"block_human_vertical","player":1,"board":["...............","...............","...............",".......X.......",".......X.......",".......X.......",".......X.......","...............","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[2,7],[7,7]],"tags":["block","vertical"]}
```

- [ ] **Step 3: Viết parser và tactical test**

Create `tests/test_tactical_cases.py` with:

```python
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_core import AI_STONE, EMPTY, HUMAN_STONE, GomokuAI, SearchConfig


FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "tactical_cases.jsonl"
SYMBOLS = {
    ".": EMPTY,
    "O": AI_STONE,
    "X": HUMAN_STONE,
}


def parse_board(rows: list[str]) -> list[list[int]]:
    assert len(rows) == 15
    board: list[list[int]] = []
    for row in rows:
        assert len(row) == 15
        board.append([SYMBOLS[cell] for cell in row])
    return board


def load_cases() -> list[dict]:
    return [json.loads(line) for line in FIXTURE_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_tactical_cases_choose_expected_moves() -> None:
    ai = GomokuAI(
        config=SearchConfig(depth=3, candidate_radius=2, candidate_limit=12, time_limit_ms=1500, threat_extension_depth=1),
        memory_filename=ROOT_DIR / "tests" / "gomoku_tt_test.pkl",
    )

    failures: list[str] = []
    for case in load_cases():
        board = parse_board(case["board"])
        analysis = ai.get_move_analysis(board, case["player"])
        expected_moves = {tuple(move) for move in case["expected_moves"]}
        if analysis.move not in expected_moves:
            failures.append(f"{case['name']}: got {analysis.move}, expected one of {sorted(expected_moves)}, reason={analysis.reason}")

    assert not failures, "\n".join(failures)
```

- [ ] **Step 4: Chạy test để kiểm tra baseline hiện tại**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m pytest tests\test_tactical_cases.py -v
```

Expected: PASS nếu đã xử lý đúng các tactical case cơ bản. Nếu chưa cài `pytest`, dùng script benchmark ở Task 2 trước hoặc cài `pytest` trong môi trường dev.

- [ ] **Step 5: Dọn cache test nếu phát sinh**

Run:

```powershell
Remove-Item -LiteralPath tests\gomoku_tt_test.pkl -ErrorAction SilentlyContinue
```

Expected: không còn `tests/gomoku_tt_test.pkl`.

---

## Task 2: Tạo Benchmark Script Cho Báo Cáo

**Mục tiêu:** Có số liệu thực nghiệm để so sánh Easy/Medium/Hard và baseline đơn giản.

**Files:**
- Create: `benchmark_ai.py`
- Output: `benchmark_results.json`

- [ ] **Step 1: Tạo script benchmark**

Create `benchmark_ai.py` with:

```python
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai_core import AI_STONE, BOARD_SIZE, EMPTY, HUMAN_STONE, GomokuAI, SearchConfig
from main import DIFFICULTY_CONFIGS, get_ai


def empty_board() -> list[list[int]]:
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def create_midgame_board() -> list[list[int]]:
    board = empty_board()
    placements = [
        (7, 7, HUMAN_STONE),
        (7, 8, AI_STONE),
        (8, 7, HUMAN_STONE),
        (6, 8, AI_STONE),
        (8, 8, HUMAN_STONE),
        (6, 7, AI_STONE),
    ]
    for row, col, stone in placements:
        board[row][col] = stone
    return board


def create_block_board() -> list[list[int]]:
    board = empty_board()
    for col in range(5, 9):
        board[7][col] = HUMAN_STONE
    board[6][6] = AI_STONE
    board[8][6] = AI_STONE
    return board


def center_first_move(board: list[list[int]]) -> tuple[int, int] | None:
    center = BOARD_SIZE // 2
    if board[center][center] == EMPTY:
        return (center, center)
    for radius in range(1, BOARD_SIZE):
        for row in range(max(0, center - radius), min(BOARD_SIZE, center + radius + 1)):
            for col in range(max(0, center - radius), min(BOARD_SIZE, center + radius + 1)):
                if board[row][col] == EMPTY:
                    return (row, col)
    return None


def run_ai_case(name: str, board: list[list[int]]) -> list[dict]:
    rows: list[dict] = []
    for difficulty in DIFFICULTY_CONFIGS:
        ai = get_ai(difficulty)
        start = time.perf_counter()
        analysis = ai.get_move_analysis([row[:] for row in board], AI_STONE)
        elapsed_ms = (time.perf_counter() - start) * 1000
        rows.append(
            {
                "case": name,
                "agent": f"project_{difficulty}",
                "move": analysis.move,
                "score": analysis.score,
                "reason": analysis.reason,
                "completed_depth": analysis.completed_depth,
                "elapsed_ms": round(elapsed_ms, 2),
            }
        )
    return rows


def run_center_baseline_case(name: str, board: list[list[int]]) -> dict:
    start = time.perf_counter()
    move = center_first_move([row[:] for row in board])
    elapsed_ms = (time.perf_counter() - start) * 1000
    return {
        "case": name,
        "agent": "center_first_baseline",
        "move": move,
        "score": 0,
        "reason": "center_or_nearest_empty",
        "completed_depth": 0,
        "elapsed_ms": round(elapsed_ms, 2),
    }


def main() -> None:
    cases = {
        "opening": empty_board(),
        "midgame": create_midgame_board(),
        "block_open_four": create_block_board(),
    }
    results: list[dict] = []
    for name, board in cases.items():
        results.append(run_center_baseline_case(name, board))
        results.extend(run_ai_case(name, board))

    output_path = ROOT_DIR / "benchmark_results.json"
    output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"Saved benchmark results to {output_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Chạy benchmark**

Run:

```powershell
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

Expected: terminal in ra JSON gồm `center_first_baseline`, `project_easy`, `project_medium`, `project_hard` cho từng case.

- [ ] **Step 3: Ghi số liệu vào báo cáo**

Use `benchmark_results.json` to build a table with:

```text
Case | Agent | Move | Reason | Completed Depth | Time (ms)
```

Expected: báo cáo có số liệu thực nghiệm thay vì chỉ mô tả thuật toán.

- [ ] **Step 4: Dọn cache nếu benchmark làm thay đổi cache tracked**

Run:

```powershell
git status --short
```

Expected: nếu `backend/gomoku_tt.pkl` bị thay đổi do benchmark, restore file đó trước khi commit nếu task không yêu cầu lưu cache:

```powershell
git restore --source=HEAD -- backend\gomoku_tt.pkl
```

---

## Task 3: Cải Thiện Pattern-Based Evaluator

**Mục tiêu:** Giúp AI đánh giá tốt hơn các pattern Gomoku quan trọng như open-four, broken-four và open-three.

**Files:**
- Modify: `backend/threats.py`
- Modify: `backend/evaluator.py`
- Test: `tests/test_tactical_cases.py`

- [ ] **Step 1: Thêm tactical cases cho broken four**

Append to `tests/fixtures/tactical_cases.jsonl`:

```jsonl
{"name":"block_human_broken_four_x_xxx","player":1,"board":["...............","...............","...............","...............","...............","...............","...............",".....X.XXX.....","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,6]],"tags":["block","broken_four"]}
{"name":"block_human_broken_four_xxx_x","player":1,"board":["...............","...............","...............","...............","...............","...............","...............",".....XXX.X.....","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[7,8]],"tags":["block","broken_four"]}
```

- [ ] **Step 2: Chạy test để ghi nhận hành vi hiện tại**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m pytest tests\test_tactical_cases.py -v
```

Expected: nếu FAIL ở broken-four, failure message chỉ rõ case và nước AI chọn.

- [ ] **Step 3: Mở rộng threat pattern nếu test fail**

Update `backend/threats.py` in `ThreatDetector.summarize_line()` so `closed_four` also catches common broken-four windows:

```python
broken_four = self._count_windows(
    padded,
    6,
    lambda window: window.count("1") == 4 and window.count("0") == 2 and "2" not in window and any(
        pattern in window for pattern in ("11011", "11101", "10111")
    ),
)
closed_four = max(0, four_windows - open_four * 2) + broken_four
```

Expected: broken-four threats are scored as urgent defensive or attacking threats.

- [ ] **Step 4: Cân chỉnh score nếu AI vẫn ưu tiên sai**

Update `backend/evaluator.py` only if tactical tests still fail. Keep terminal wins higher than all normal threats:

```python
THREAT_SCORES = {
    "five": 1_000_000,
    "open_four": 160_000,
    "closed_four": 45_000,
    "open_three": 8_000,
    "broken_three": 3_000,
    "double_threat": 55_000,
}
```

Expected: evaluator ưu tiên threat bắt buộc hơn các nước tăng điểm nhỏ.

- [ ] **Step 5: Chạy lại tactical test**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m pytest tests\test_tactical_cases.py -v
```

Expected: PASS.

---

## Task 4: Enhanced Transposition Table Với Best Move

**Mục tiêu:** Lưu `best_move` trong transposition table để cải thiện move ordering ở các lần search sau.

**Files:**
- Modify: `backend/ai_core.py`
- Modify: `backend/ai_types.py` nếu cần dataclass riêng cho TT entry.
- Test: `tests/test_tactical_cases.py`

- [ ] **Step 1: Đổi cấu trúc transposition table**

In `backend/ai_core.py`, replace:

```python
self.transposition_table: dict[int, tuple[int, float, str]] = {}
```

with:

```python
self.transposition_table: dict[int, tuple[int, float, str, tuple[int, int] | None]] = {}
```

- [ ] **Step 2: Update load/save memory**

Update `load_memory()` to accept both old 3-field entries and new 4-field entries:

```python
normalized_entries = {}
for board_hash, entry in entries.items():
    if len(entry) == 3:
        depth, score, flag = entry
        best_move = None
    else:
        depth, score, flag, best_move = entry
        if best_move is not None:
            best_move = (int(best_move[0]), int(best_move[1]))
    normalized_entries[int(board_hash)] = (int(depth), float(score), str(flag), best_move)
self.transposition_table = normalized_entries
```

Expected: cache cũ không làm engine crash.

- [ ] **Step 3: Update cache read sites**

In `_minimax()`, replace:

```python
cached_depth, cached_score, cached_flag = cached
```

with:

```python
cached_depth, cached_score, cached_flag, _cached_best_move = cached
```

Expected: existing alpha/beta logic remains unchanged.

- [ ] **Step 4: Store best move after search**

Track `best_move` in `_minimax()` loops and store:

```python
self.transposition_table[search_hash] = (depth, value, flag, best_move)
```

Expected: each cached non-leaf node can carry the move that produced the cached value.

- [ ] **Step 5: Prioritize cached best move**

Before iterating candidates in `_minimax()`, compute:

```python
cached_best_move = cached[3] if cached is not None else None
if cached_best_move in candidates:
    candidates = self._prioritize_move(candidates, cached_best_move)
```

Expected: principal candidate is searched first when available.

- [ ] **Step 6: Run tactical tests and benchmark**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m pytest tests\test_tactical_cases.py -v
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

Expected: tactical tests pass; benchmark time should stay same or improve.

---

## Task 5: Threat Space Search / VCF Solver Tối Giản

**Mục tiêu:** Thêm search riêng cho forcing line đơn giản, giúp AI tìm chuỗi tạo four và thắng bắt buộc tốt hơn minimax thường.

**Files:**
- Modify: `backend/ai_core.py`
- Modify: `backend/move_ordering.py`
- Test: `tests/test_tactical_cases.py`

- [ ] **Step 1: Thêm case forcing win hai bước**

Append to `tests/fixtures/tactical_cases.jsonl`:

```jsonl
{"name":"prefer_creating_open_four_over_small_attack","player":1,"board":["...............","...............","...............","...............","...............","...............",".....OOO.......",".....XX........","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[6,4],[6,8]],"tags":["attack","open_four"]}
```

- [ ] **Step 2: Chạy test trước khi sửa**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m pytest tests\test_tactical_cases.py -v
```

Expected: nếu FAIL, ghi nhận đây là case chứng minh cần threat-space search.

- [ ] **Step 3: Thêm helper tìm forcing candidates**

In `backend/move_ordering.py`, keep `generate_forcing_candidates()` focused on:

```python
if summary.open_four or summary.closed_four:
    return True
```

Expected: threat-space search chỉ xét nước tạo hoặc chặn four, tránh branching quá rộng.

- [ ] **Step 4: Thêm VCF search tối giản**

In `backend/ai_core.py`, add:

```python
def _find_forcing_win(
    self,
    board: list[list[int]],
    attacker: int,
    defender: int,
    depth: int,
    deadline: float | None,
) -> tuple[int, int] | None:
    if depth <= 0:
        return None

    candidates = self._generate_forcing_candidates(board)
    for row, col in candidates:
        self._check_deadline(deadline)
        if board[row][col] != EMPTY:
            continue
        board[row][col] = attacker
        try:
            if self._has_winner(board, attacker):
                return (row, col)
            defender_block = self._find_winning_move(board, attacker)
            if defender_block is None:
                continue
            block_row, block_col = defender_block
            board[block_row][block_col] = defender
            try:
                reply = self._find_forcing_win(board, attacker, defender, depth - 1, deadline)
                if reply is not None:
                    return (row, col)
            finally:
                board[block_row][block_col] = EMPTY
        finally:
            board[row][col] = EMPTY
    return None
```

Expected: helper thử các forcing moves và kiểm tra chuỗi thắng đơn giản.

- [ ] **Step 5: Gọi forcing search trước minimax thường**

In `_get_move_analysis_for_ai()`, after immediate win/block and before iterative deepening:

```python
forcing_move = self._find_forcing_win(board, AI_STONE, HUMAN_STONE, depth=2, deadline=self._search_deadline())
if forcing_move is not None:
    return MoveAnalysis(
        move=forcing_move,
        score=500_000,
        reason=self._classify_move_reason(board, forcing_move),
        completed_depth=0,
    )
```

Expected: AI chọn nước tạo forcing line rõ ràng trước khi vào search thông thường.

- [ ] **Step 6: Run verification**

Run:

```powershell
.\backend\venv\Scripts\python.exe -m pytest tests\test_tactical_cases.py -v
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

Expected: tactical tests pass; benchmark không timeout bất thường.

---

## Task 6: Viết Phần Benchmark So Sánh Với Model/Engine Khác

**Mục tiêu:** Báo cáo có phần so sánh đúng mức với các engine/model hiện có mà không claim quá đà.

**Files:**
- Create: `REPORT_AI_BENCHMARK_NOTES.md`

- [ ] **Step 1: Tạo bảng so sánh định tính**

Create `REPORT_AI_BENCHMARK_NOTES.md` with:

```markdown
# AI Benchmark and Contribution Notes

## So sánh định tính với các hướng AI Gomoku hiện có

| Hệ thống | Hướng tiếp cận | Điểm mạnh | Khác biệt với dự án |
|---|---|---|---|
| Rapfi | Alpha-beta nâng cao + classical/NNUE evaluation | Engine rất mạnh, tối ưu sâu, có NNUE | Dự án không dùng NNUE/training, tập trung classical search dễ giải thích |
| Yixin | Traditional alpha-beta + tri thức Gomoku/Renju mạnh | Từng là engine mạnh cấp thi đấu | Dự án nhỏ hơn, hướng học thuật, minh họa rõ các thành phần search/evaluator |
| AlphaZero-Gomoku | Self-play RL + neural network + MCTS | Có khả năng học từ self-play | Dự án không training, không cần GPU, dễ kiểm soát heuristic |
| Baseline minimax đơn giản | Minimax/alpha-beta cơ bản | Dễ triển khai | Dự án bổ sung candidate pruning, move ordering, threat detection, TT và time limit |

## Đóng góp AI chính của dự án

1. Giảm branching factor bằng candidate generation quanh quân đã đánh.
2. Nâng hiệu quả alpha-beta bằng move ordering dựa trên tactical score.
3. Nhận diện threat Gomoku: open-four, closed-four, open-three, broken-three, double threat.
4. Dùng pattern-based evaluation theo công thức AttackScore - DefenseScore.
5. Kiểm tra immediate win/block trước search sâu.
6. Dùng iterative deepening và time limit để phản hồi ổn định.
7. Dùng Zobrist hashing và transposition table có side-to-move.
8. Có arena self-play để sinh JSONL phục vụ phân tích hoặc training sau này.

## Benchmark thực nghiệm trong dự án

Sử dụng `benchmark_ai.py` để đo:

- Thời gian trung bình mỗi nước.
- Completed depth.
- Reason trả về.
- Khả năng chọn đúng nước trong tactical cases.
- So sánh Easy/Medium/Hard với center-first baseline.
```

- [ ] **Step 2: Thêm số liệu từ benchmark_results.json**

After running `benchmark_ai.py`, append a table:

```markdown
## Kết quả benchmark local

| Case | Agent | Move | Reason | Completed Depth | Time (ms) |
|---|---|---|---|---:|---:|
```

Fill rows from `benchmark_results.json`.

- [ ] **Step 3: Viết kết luận không claim quá mức**

Append:

```markdown
Kết quả benchmark không nhằm chứng minh dự án mạnh hơn các engine thi đấu như Rapfi hoặc Yixin. Mục tiêu là chứng minh các cải tiến classical AI giúp bot xử lý tốt hơn các tình huống chiến thuật Gomoku so với baseline đơn giản, đồng thời vẫn phản hồi trong thời gian phù hợp cho ứng dụng tương tác.
```

Expected: báo cáo có định vị đúng, không so sánh sai với state-of-the-art.

---

## Verification Checklist

Trước khi coi plan là hoàn thành, chạy các lệnh sau:

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py
```

Expected: không có syntax error.

```powershell
.\backend\venv\Scripts\python.exe -m pytest tests\test_tactical_cases.py -v
```

Expected: tactical tests pass.

```powershell
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

Expected: tạo `benchmark_results.json` và in kết quả benchmark.

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

Expected: arena smoke test chạy xong và in summary JSON.

```powershell
git status --short
```

Expected: chỉ có các file chủ đích bị thay đổi. Không commit cache `.pkl` hoặc dataset mới nếu task không yêu cầu.

---

## Thứ Tự Ưu Tiên Khuyến Nghị

1. Tactical benchmark suite.
2. Benchmark script cho báo cáo.
3. Pattern-based evaluator nâng cao.
4. Enhanced transposition table lưu best move.
5. Threat Space Search / VCF solver tối giản.
6. Báo cáo benchmark và contribution notes.

Nếu thời gian hạn chế, chỉ cần hoàn thành Tasks 1, 2 và 6 là đủ để có báo cáo AI có số liệu và đóng góp rõ ràng. Nếu muốn cải thiện chất lượng bot thật sự, làm tiếp Tasks 3 và 5.
