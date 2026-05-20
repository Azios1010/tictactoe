# AGENTS.md

## Giới thiệu dự án

Đây là dự án Gomoku/Caro 15x15 dạng full-stack:

- Frontend: React + Vite.
- Backend: Python FastAPI.
- AI core: classical game engine, không dùng reinforcement learning hoặc model training.
- Thuật toán chính: minimax/alpha-beta pruning, iterative deepening, transposition table, Zobrist hash, threat detection và heuristic pattern evaluator.
- Arena: chế độ AI tự đấu để sinh dữ liệu JSONL phục vụ phân tích hoặc huấn luyện sau này.

Quy ước quân cờ:

- `0`: ô trống.
- `1`: AI/O/black trong internal engine.
- `-1`: người chơi/X/white.

Lưu ý: tên thư mục repo là `Tictactoe`, nhưng game hiện tại là Gomoku/Caro 15x15, không phải tic-tac-toe 3x3.

## Tổng quan kiến trúc

```text
.
├── backend/
│   ├── ai_core.py          # Lõi AI: search, heuristic, threat detection, cache
│   ├── main.py             # FastAPI API cho chế độ người - máy
│   ├── requirements.txt
│   └── start_backend.ps1
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # UI chính, play mode, arena mode
│   │   ├── App.css
│   │   └── components/
│   │       ├── Board.jsx
│   │       └── Square.jsx
│   ├── package.json
│   └── vite.config.js
├── arena/
│   ├── engine.py           # Self-play engine
│   ├── service.py          # FastAPI service cho arena
│   ├── run_arena.py        # CLI batch self-play
│   ├── generate_data.py    # Pipeline sinh dữ liệu cũ/mở rộng
│   └── data/
├── IMPLEMENTATION_PLAN.md  # Kế hoạch nâng cấp AI theo phase
└── README.md
```

## Luồng người - máy

1. Người chơi click một ô trên frontend.
2. Frontend cập nhật board local với quân `-1`.
3. Frontend gọi `POST /api/get-move`, gửi board, player và difficulty.
4. Backend validate board bằng Pydantic.
5. Backend chọn AI instance theo difficulty.
6. `GomokuAI.get_move_analysis()` trả về nước đi, evaluation, reason và completed depth.
7. Frontend đặt quân AI `1`, cập nhật trạng thái và lý do nước đi.

Endpoint chính:

```http
GET /api/health
POST /api/get-move
```

Request mẫu:

```json
{
  "board": [[0, 0, 0]],
  "player": 1,
  "difficulty": "medium"
}
```

Response mẫu:

```json
{
  "row": 7,
  "col": 8,
  "evaluation": 120,
  "reason": "creating_open_four",
  "difficulty": "medium",
  "completed_depth": 2,
  "message": "Move generated successfully."
}
```

## AI core

File chính: `backend/ai_core.py`.

AI hiện đã được tách thành các module nhỏ trong `backend/`:

- `ai_types.py`: constants, config và dataclass dùng chung.
- `board_rules.py`: luật board cơ bản như winner, bounds, normalize.
- `threats.py`: nhận diện threat pattern.
- `evaluator.py`: chấm điểm board.
- `move_ordering.py`: sinh candidate, score nước đi, phân loại reason.
- `ai_core.py`: orchestration/search, transposition table, minimax/alpha-beta.

Giữ import public qua `ai_core.py` để các file cũ như `backend/main.py` và `arena/engine.py` không cần đổi.

Các thành phần quan trọng:

- `SearchConfig`: cấu hình depth, candidate radius, candidate limit, time limit và threat extension.
- `MoveAnalysis`: kết quả search gồm move, score, reason và completed depth.
- `ThreatSummary`: thống kê threat như open-four, closed-four, open-three, broken-three.
- `GomokuAI`: engine chính.

AI hiện dùng:

- Alpha-beta pruning.
- Iterative deepening theo time limit.
- Zobrist hashing.
- Transposition table có side-to-move trong hash.
- Immediate win/block trước khi search sâu.
- Candidate pruning quanh các quân đã có.
- Move ordering bằng local shape score và threat score.
- Threat extension giới hạn cho forcing moves.

Reason có thể trả về:

- `opening_center`
- `winning_move`
- `blocking_win`
- `creating_double_threat`
- `creating_open_four`
- `creating_closed_four`
- `blocking_double_threat`
- `blocking_open_four`
- `blocking_closed_four`
- `building_attack`
- `reducing_threat`
- `best_search_score`
- `timeout_best_known`
- `game_finished`

## Difficulty

Difficulty được cấu hình trong `backend/main.py`.

```python
DIFFICULTY_CONFIGS = {
    "easy": SearchConfig(...),
    "medium": SearchConfig(...),
    "hard": SearchConfig(...),
}
```

Khi chỉnh difficulty, ưu tiên đảm bảo:

- Easy trả nhanh.
- Medium ít timeout và hoàn thành depth tối thiểu ổn định.
- Hard được phép lâu hơn nhưng không làm UI treo quá lâu.

Không tăng depth/candidate limit nếu chưa benchmark. Với Gomoku 15x15, branching factor tăng rất nhanh.

## Arena mode

Arena nằm trong `arena/`.

Vai trò:

- Tự đấu AI vs AI.
- Normalize board để người đang đi luôn nhìn mình là `1`.
- Ghi sample JSONL gồm board, normalized board, move, evaluation, winner và outcome.

API arena:

```http
GET /arena/api/health
POST /arena/api/self-play
```

CLI:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 10
```

## Cài đặt backend

Trên Windows, cách ổn định nhất:

```powershell
cd backend
.\start_backend.ps1
```

Hoặc chạy thủ công:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

Backend mặc định chạy tại:

```text
http://127.0.0.1:8000
```

## Cài đặt frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend mặc định chạy tại:

```text
http://127.0.0.1:5173
```

Trên Windows PowerShell, nếu `npm` bị chặn bởi execution policy, dùng:

```powershell
npm.cmd run dev
npm.cmd run build
```

## Chạy arena service

```powershell
.\arena\start_arena.ps1
```

Arena API mặc định chạy tại:

```text
http://127.0.0.1:8100
```

Frontend gọi arena qua:

```text
VITE_ARENA_API_BASE_URL=http://127.0.0.1:8100
```

## Kiểm tra và build

Backend syntax check:

```powershell
python -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py
```

Nếu dùng virtualenv backend:

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py
```

Frontend build:

```powershell
cd frontend
npm.cmd run build
```

Arena smoke test:

```powershell
python -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

## Coding convention

### Python

- Dùng type hints cho function public và helper quan trọng.
- Giữ logic AI core deterministic khi có thể.
- Không mutate board của caller. Nếu thử nước trong search, luôn reset bằng `finally`.
- Không thêm dependency nặng nếu chưa cần.
- Không ghi file cache/dataset vào diff nếu chỉ chạy test.
- Không dùng model training/RL trong AI core hiện tại.
- Khi chỉnh evaluator, phải thêm hoặc chạy regression board nhỏ để tránh AI đánh nước vô lý.

### React

- State chính nằm trong `App.jsx`.
- Board là ma trận 15x15.
- Không mutate board trực tiếp; dùng `cloneBoard()`.
- Không cho click khi AI đang suy nghĩ hoặc game đã kết thúc.
- UI play mode và arena mode dùng chung board component.

### CSS

- Giữ style đơn giản, dễ đọc.
- Không làm board bị resize bất ngờ.
- Các control phải usable trên màn hình nhỏ.

## Quy tắc khi chỉnh AI

Khi thay đổi search/evaluator:

1. Kiểm tra immediate win.
2. Kiểm tra immediate block.
3. Kiểm tra case AI không đánh nước rời rạc vô nghĩa.
4. Benchmark một board giữa game ở Easy/Medium/Hard.
5. Đảm bảo `completed_depth` không thường xuyên là `0`.
6. Dọn cache sinh ra bởi test.

Ví dụ benchmark nhanh:

```powershell
@'
from pathlib import Path
import sys, time
sys.path.insert(0, str(Path("backend").resolve()))
from ai_core import BOARD_SIZE, EMPTY, HUMAN_STONE, AI_STONE
from main import DIFFICULTY_CONFIGS, get_ai

board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
board[7][7] = HUMAN_STONE
board[7][8] = AI_STONE

for name in DIFFICULTY_CONFIGS:
    ai = get_ai(name)
    t0 = time.perf_counter()
    analysis = ai.get_move_analysis([row[:] for row in board], AI_STONE)
    dt = (time.perf_counter() - t0) * 1000
    print(name, round(dt, 1), analysis)
'@ | .\backend\venv\Scripts\python.exe -
```

## Cache và file sinh ra

AI có thể ghi transposition table ra:

```text
backend/gomoku_tt.pkl
gomoku_tt.pkl
```

Nếu các file này thay đổi chỉ do chạy test/benchmark, không commit chúng. Khôi phục hoặc xóa trước khi kết thúc task.

Dataset arena nằm trong:

```text
arena/data/
```

Chỉ commit dataset khi task yêu cầu rõ ràng.

## Lưu ý chất lượng hiện tại

AI hiện đã mạnh hơn minimax heuristic ban đầu, nhưng chưa phải engine Gomoku hoàn chỉnh. Các điểm cần thận trọng:

- Threat detection vẫn là pattern-based đơn giản.
- Một số thế kép phức tạp có thể đánh giá chưa chuẩn.
- Search bị giới hạn bởi time limit và candidate pruning.
- Nếu AI đánh nước vô lý, ưu tiên kiểm tra evaluator/pattern scoring trước khi tăng depth.

Hướng cải tiến tiếp theo:

- Viết unit tests chính thức cho các board tactical.
- Mở rộng test/benchmark cho từng module AI riêng.
- Thêm benchmark script riêng.
- Hiển thị debug board/reason trong UI chỉ ở dev mode.
