# Development Pipeline

Tài liệu này mô tả pipeline làm việc cho team khi phát triển dự án Gomoku/Caro AI.

## 1. Mục tiêu pipeline

Pipeline cần đảm bảo:

- Code chạy được trên máy local của mọi thành viên.
- Backend, frontend và arena không bị vỡ khi thay đổi AI core.
- Mỗi thay đổi AI có benchmark hoặc tactical case đi kèm.
- File cache/dataset sinh ra khi test không bị commit nhầm.

## 2. Quy trình làm việc khuyến nghị

```text
1. Pull code mới nhất
2. Tạo branch riêng
3. Chạy backend/frontend local
4. Thực hiện thay đổi nhỏ, có mục tiêu rõ
5. Chạy check tối thiểu
6. Test thủ công trên UI nếu thay đổi gameplay
7. Dọn cache/dataset sinh ra
8. Commit với message rõ ràng
9. Mở pull request hoặc gửi review
```

Ví dụ branch:

```text
feature/difficulty-ui
fix/ai-broken-three-eval
test/tactical-cases
docs/team-readme
```

## 3. Setup local

### Backend

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

Backend chạy tại:

```text
http://127.0.0.1:8000
```

### Frontend

```powershell
cd frontend
npm install
npm.cmd run dev
```

Frontend chạy tại:

```text
http://127.0.0.1:5173
```

### Arena

```powershell
.\arena\start_arena.ps1
```

Arena API chạy tại:

```text
http://127.0.0.1:8100
```

## 4. Check tối thiểu trước khi commit

### Python compile check

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py
```

Nếu chưa dùng venv:

```powershell
python -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py
```

### Frontend build

```powershell
cd frontend
npm.cmd run build
```

### Arena smoke test

```powershell
python -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

Nếu dùng backend venv:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

## 5. Pipeline khi chỉnh AI core

AI core nằm ở:

```text
backend/ai_core.py
```

Các module AI hiện tại:

```text
backend/ai_types.py
backend/board_rules.py
backend/threats.py
backend/evaluator.py
backend/move_ordering.py
backend/ai_core.py
```

Chỉnh evaluator thì ưu tiên vào `evaluator.py` hoặc `threats.py`.
Chỉnh candidate/move ordering thì ưu tiên vào `move_ordering.py`.
Chỉnh search/minimax/cache thì ưu tiên vào `ai_core.py`.

Khi chỉnh AI, làm theo thứ tự:

1. Tái tạo board mà AI đánh sai.
2. Kiểm tra nước đúng có nằm trong candidate list không.
3. Kiểm tra `_score_move()` đang chấm các nước ra sao.
4. Kiểm tra `evaluate_board()` có overvalue pattern sai không.
5. Kiểm tra `completed_depth` có bị `0` hoặc timeout liên tục không.
6. Chỉ sau đó mới tăng depth, candidate limit hoặc time limit.

Không tăng search depth để che lỗi evaluator. Nếu evaluator sai, search sâu hơn vẫn có thể chọn sai.

## 6. Tactical case pipeline

Team nên chuẩn bị file tactical cases:

```text
tests/fixtures/tactical_cases.jsonl
```

Format đề xuất:

```json
{"name":"block_open_four_horizontal","player":1,"board":["...............","...............","...............","...XXXX........","...............","...............","...............","...............","...............","...............","...............","...............","...............","...............","..............."],"expected_moves":[[3,2],[3,7]],"tags":["block","open_four"]}
```

Quy ước:

- `.`: ô trống.
- `X`: người chơi, giá trị `-1`.
- `O`: AI, giá trị `1`.

Mỗi case nên có:

- `name`: tên dễ hiểu.
- `player`: bên cần đi.
- `board`: 15 dòng, mỗi dòng 15 ký tự.
- `expected_moves`: danh sách nước đúng chấp nhận được.
- `tags`: nhóm lỗi hoặc chiến thuật.

Nhóm case cần có:

- AI thắng ngay.
- AI chặn thắng ngay.
- Chặn open-four.
- Chặn closed-four.
- Broken four: `XX.XX`, `XXX.X`, `X.XXX`.
- Open-three.
- Double-three.
- Double-four.
- Diagonal block.
- Không đánh nước rời rạc vô nghĩa.
- Ưu tiên phòng thủ khi threat của đối thủ lớn hơn attack nhỏ.

## 7. Benchmark AI

Benchmark nhanh một board:

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

Kỳ vọng:

- Easy trả nhanh.
- Medium không thường xuyên `completed_depth=0`.
- Hard có thể lâu hơn nhưng không timeout vô nghĩa.

## 8. Dọn file sinh ra

Các file sau có thể bị sinh hoặc cập nhật khi chạy benchmark:

```text
gomoku_tt.pkl
backend/gomoku_tt.pkl
arena/data/*.jsonl
frontend/dist/
```

Quy tắc:

- Không commit cache `.pkl` nếu chỉ do chạy test.
- Không commit dataset mới nếu task không yêu cầu.
- `frontend/dist/` đã nằm trong `.gitignore`.

Khôi phục cache nếu bị thay đổi:

```powershell
git restore --source=HEAD -- backend\gomoku_tt.pkl
```

Xóa cache root nếu bị tạo:

```powershell
Remove-Item -LiteralPath gomoku_tt.pkl
```

## 9. Review checklist

Trước khi review/merge:

- Backend compile pass.
- Frontend build pass nếu có đổi UI.
- Arena smoke test pass nếu có đổi AI core.
- Không có cache/dataset ngoài ý muốn trong `git status`.
- Nếu sửa AI, có board tái tạo lỗi hoặc tactical case.
- Nếu sửa evaluator, kiểm tra không làm hỏng immediate win/block.

## 10. Khi AI đánh tệ

Debug theo thứ tự:

1. Xem `reason` trên UI.
2. Xem `completed_depth`.
3. Tái tạo board trong script nhỏ.
4. In `_generate_candidates()`.
5. In `_score_move()` cho vài nước nghi ngờ.
6. Kiểm tra `_threat_summary()` và `evaluate_board()`.
7. Sửa pattern/evaluator.
8. Chạy lại regression.

Không bắt đầu bằng tăng `depth`; đó thường là cách làm chậm bot mà chưa chắc làm bot thông minh hơn.
