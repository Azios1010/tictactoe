# Gomoku AI Project

Dự án Gomoku/Caro 15x15 full-stack với frontend React, backend FastAPI và AI classical search.

Tên repo hiện là `Tictactoe`, nhưng game đang triển khai là Gomoku/Caro 15x15, không phải tic-tac-toe 3x3.

## Tính năng chính

- Chơi người - máy trên board 15x15.
- AI dùng minimax/alpha-beta pruning.
- Iterative deepening theo time limit.
- Transposition table với Zobrist hash.
- Threat detection: open-four, closed-four, open-three, broken-three, double-threat.
- Difficulty: Easy, Medium, Hard.
- Backend trả `reason` để giải thích nước đi của AI.
- Arena mode cho AI tự đấu và sinh dữ liệu JSONL.

## Công nghệ

- Backend: Python, FastAPI, Pydantic, Uvicorn.
- Frontend: React, Vite.
- Arena: Python CLI và FastAPI service riêng.

## Cấu trúc thư mục

```text
.
├── backend/
│   ├── ai_core.py
│   ├── main.py
│   ├── requirements.txt
│   └── start_backend.ps1
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── components/
│   │       ├── Board.jsx
│   │       └── Square.jsx
│   ├── package.json
│   └── vite.config.js
├── arena/
│   ├── engine.py
│   ├── service.py
│   ├── run_arena.py
│   ├── generate_data.py
│   └── data/
├── AGENTS.md
├── PIPELINE.md
├── IMPLEMENTATION_PLAN.md
└── README.md
```

## Quy ước board

Board là ma trận 15x15.

```text
0  = ô trống
1  = AI / O
-1 = người chơi / X
```

Frontend hiển thị:

- `X`: người chơi.
- `O`: AI.

## Chạy backend

Cách khuyến nghị trên Windows:

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

Backend mặc định:

```text
http://127.0.0.1:8000
```

Health check:

```text
GET http://127.0.0.1:8000/api/health
```

## Chạy frontend

```powershell
cd frontend
npm install
npm.cmd run dev
```

Frontend mặc định:

```text
http://127.0.0.1:5173
```

Nếu PowerShell chặn `npm`, dùng `npm.cmd`.

Build frontend:

```powershell
cd frontend
npm.cmd run build
```

## Chạy arena

Arena API:

```powershell
.\arena\start_arena.ps1
```

Arena mặc định:

```text
http://127.0.0.1:8100
```

Batch self-play:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 10
```

Ví dụ cấu hình nhẹ:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

## API người - máy

Endpoint:

```http
POST /api/get-move
```

Request:

```json
{
  "board": [[0, 0, 0]],
  "player": 1,
  "difficulty": "medium"
}
```

`difficulty` có thể là:

```text
easy
medium
hard
```

Response:

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

File chính:

```text
backend/ai_core.py
```

Sau refactor, AI được tách thành nhiều module nhỏ:

```text
backend/ai_types.py       # Constants, SearchConfig, MoveAnalysis, ThreatSummary
backend/board_rules.py    # Luật board cơ bản: bounds, winner, normalize, line potential
backend/threats.py        # ThreatDetector: open-four, closed-four, open-three, broken-three
backend/evaluator.py      # BoardEvaluator: chấm điểm board từ threat + pattern liên tục
backend/move_ordering.py  # Candidate generation, move scoring, reason classification
backend/ai_core.py        # GomokuAI: orchestration, minimax, alpha-beta, cache, time limit
```

`ai_core.py` vẫn là entry point public để `backend/main.py` và `arena/*` import không đổi.

Luồng chọn nước:

1. Validate player.
2. Normalize board nếu cần.
3. Nếu board trống, đánh trung tâm.
4. Nếu AI thắng ngay, đánh nước thắng.
5. Nếu người chơi thắng ngay, chặn.
6. Sinh candidate moves.
7. Sắp xếp candidate bằng local shape score và threat score.
8. Chạy iterative deepening với alpha-beta pruning.
9. Dùng evaluator để chấm leaf node.
10. Trả `MoveAnalysis` gồm move, score, reason và completed depth.

Các reason thường gặp:

- `opening_center`
- `winning_move`
- `blocking_win`
- `creating_open_four`
- `blocking_open_four`
- `building_attack`
- `reducing_threat`
- `best_search_score`
- `timeout_best_known`

## Kiểm tra nhanh

Python compile:

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
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

## Tài liệu cho team

- `AGENTS.md`: tổng quan cho người/agent mới vào dự án.
- `PIPELINE.md`: quy trình phát triển, test, benchmark và review.
- `IMPLEMENTATION_PLAN.md`: kế hoạch nâng cấp AI theo phase.
- `DEPLOYMENT.md`: hướng dẫn deploy frontend lên Vercel và backend/arena lên Render.

## Deploy internet

Dự án đã có cấu hình `render.yaml` cho Render Blueprint:

- `gomoku-ai-backend`: FastAPI người - máy.
- `gomoku-ai-arena`: FastAPI arena tự đấu.

Frontend deploy bằng Vercel với root directory `frontend`. Cần cấu hình:

```text
VITE_API_BASE_URL=https://<render-backend-url>
VITE_ARENA_API_BASE_URL=https://<render-arena-url>
```

Xem chi tiết trong `DEPLOYMENT.md`.

## Lưu ý khi phát triển

- Không commit cache `.pkl` nếu chỉ sinh ra do chạy test.
- Không commit dataset mới trong `arena/data/` nếu task không yêu cầu.
- Khi AI đánh sai, ưu tiên tạo tactical case tái hiện lỗi.
- Không tăng depth trước khi kiểm tra evaluator/candidate pruning.
- Sau khi sửa backend đang chạy, restart server để load AI instance mới.
