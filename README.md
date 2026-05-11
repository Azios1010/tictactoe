# Gomoku AI Project

Ứng dụng cờ caro full-stack với:

- Backend Python `FastAPI`
- AI dùng `Minimax + Alpha-Beta Pruning`
- Hàm đánh giá `heuristic` để lượng giá thế cờ
- Frontend `React + Vite`

Kiến trúc đã tách lớp để sau này có thể thay phần heuristic bằng mô hình deep learning.

## Cấu trúc dự án

```text
.
├── backend/
│   ├── ai_core.py
│   ├── main.py
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Board.jsx
│   │   │   └── Square.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

## Thuật toán

### 1. Minimax với Alpha-Beta Pruning

- AI giả lập các nước đi ứng viên.
- Người chơi được coi là nút minimizing.
- AI được coi là nút maximizing.
- Alpha-beta pruning giúp cắt bớt nhánh không cần thiết.

### 2. Heuristic đánh giá bàn cờ

Hàm lượng giá tính điểm dựa trên các mẫu thế cờ:

- 5 quân liên tiếp: thắng tuyệt đối
- 4 mở hai đầu: ưu tiên rất cao
- 4 mở một đầu
- 3 mở hai đầu
- 2 mở hai đầu

Để giảm không gian tìm kiếm trên bàn 15x15, AI chỉ xét các ô trống nằm gần các quân đã có trên bàn.

### 3. Hướng mở rộng với deep learning

Thiết kế hiện tại cho phép:

- Giữ `GomokuAI` là lớp điều phối tìm kiếm
- Thay `evaluate_board()` bằng model inference
- Hoặc kết hợp heuristic + neural evaluation

## API backend

### `GET /api/health`

Kiểm tra server đang chạy.

### `POST /api/get-move`

Body:

```json
{
  "board": [[0, 0, 0], "... ma trận 15x15 ..."],
  "player": 1
}
```

Quy ước:

- `0`: ô trống
- `-1`: người chơi
- `1`: AI

Response:

```json
{
  "row": 7,
  "col": 7,
  "evaluation": 120,
  "message": "Move generated successfully."
}
```

## Chạy backend

Cách ổn định nhất trên Windows là dùng script có sẵn:

```powershell
cd backend
.\start_backend.ps1
```

Script sẽ:

- tạo `venv` nếu chưa có
- tự cài `fastapi`, `uvicorn`, `pydantic` nếu đang thiếu
- chạy server bằng đúng Python trong `venv`

Nếu bạn muốn chạy thủ công:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

Server mặc định chạy tại `http://127.0.0.1:8000`.

## Chạy frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend mặc định chạy tại `http://127.0.0.1:5173`.

Nếu backend không chạy ở cổng mặc định, tạo file `.env` trong `frontend/`:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Khi chạy bằng Vite dev server, frontend mặc định sẽ proxy `/api` sang `http://127.0.0.1:8000`, nên thường không cần cấu hình thêm.

## Luồng hoạt động

1. Người chơi đặt quân `X`.
2. Frontend gửi bàn cờ hiện tại tới backend.
3. Backend dùng minimax + heuristic để chọn nước đi tối ưu cho `O`.
4. Frontend cập nhật bàn cờ và hiển thị kết quả.

## Gợi ý phát triển tiếp

- Tăng độ sâu tìm kiếm động theo giai đoạn trận đấu
- Thêm luật chặn đầu, cấm nước tùy biến
- Ghi lịch sử nước đi và undo
- Thêm chế độ AI vs AI
- Thêm evaluator bằng deep learning

## Arena mode cho self-play

Arena mode được tách riêng khỏi `backend/` hiện tại. Phần mới nằm trong thư mục `arena/` và chỉ import lại `backend/ai_core.py`, không sửa file backend sẵn có.

### Thành phần mới

- `arena/service.py`: FastAPI service cho self-play
- `arena/engine.py`: engine cho 2 AI tự đấu và ghi sample training
- `arena/run_arena.py`: CLI để chạy batch self-play không cần UI
- `arena/start_arena.ps1`: script chạy arena API ở cổng `8100`

### Chạy arena API

```powershell
.\arena\start_arena.ps1
```

Sau đó mở frontend và chuyển sang tab `Arena`.

Frontend sẽ gọi:

- `POST http://127.0.0.1:8100/arena/api/self-play`

Nếu cần đổi host/port, tạo `frontend/.env`:

```bash
VITE_ARENA_API_BASE_URL=http://127.0.0.1:8100
```

### Chạy batch bằng CLI

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 100
```

Ví dụ:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 500 --depth 2 --candidate-radius 2 --candidate-limit 14
```

Mặc định, dữ liệu sẽ được ghi vào:

```text
arena/data/arena_<timestamp>.jsonl
```

### Định dạng dữ liệu training

Mỗi dòng trong file `jsonl` là một trạng thái trước nước đi:

```json
{
  "game_id": "b8e1...",
  "turn_index": 12,
  "player": 1,
  "board": [[0, 0], "..."],
  "normalized_board": [[0, 0], "..."],
  "move": { "row": 7, "col": 8 },
  "evaluation": 350,
  "winner": 1,
  "outcome": 1
}
```

Ý nghĩa:

- `board`: bàn cờ gốc tại thời điểm trước khi đánh
- `normalized_board`: bàn cờ đã đổi perspective để người sắp đi luôn là `1`
- `move`: nước đi được chọn
- `evaluation`: heuristic hiện tại của AI tại trạng thái đó
- `winner`: kết quả cuối cùng của ván (`1`, `-1`, hoặc `0`)
- `outcome`: kết quả nhìn từ phía người đánh ở sample đó (`1` thắng, `0` hòa, `-1` thua)
