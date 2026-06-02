# Báo Cáo Bài Tập Lớn: Gomoku/Caro 15x15 AI

## 1. Thông Tin Chung

- **Tên dự án:** Gomoku AI Project
- **Tên thư mục mã nguồn:** `Tictactoe`
- **Bài toán thực tế:** xây dựng hệ thống chơi Gomoku/Caro 15x15 giữa người chơi và AI, kèm chế độ AI tự đấu để sinh dữ liệu phân tích.
- **Hướng tiếp cận AI:** classical game AI, không dùng reinforcement learning, không huấn luyện neural network.
- **Frontend:** React + Vite
- **Backend:** Python FastAPI
- **AI core:** minimax, alpha-beta pruning, iterative deepening, Zobrist hashing, transposition table, threat detection, heuristic evaluator.

## 2. Kết Quả Cần Nộp

Theo yêu cầu BTL, kết quả nộp gồm:

1. **Mã nguồn**
   - Đưa toàn bộ source code lên GitHub.
   - Chia sẻ link GitHub trong báo cáo hoặc file hướng dẫn.
   - Ngoài source code, dự án có thể được deploy lên internet để giảng viên chạy thử trực tiếp.
   - Source code gồm các thư mục chính:
     - `backend/`: FastAPI backend và AI engine.
     - `frontend/`: giao diện React/Vite.
     - `arena/`: self-play engine và pipeline sinh dữ liệu JSONL.
     - `tests/`: tactical regression tests cho AI.

2. **File hướng dẫn**
   - File `README.md` hiện mô tả cách cài đặt/chạy backend, frontend và arena.
   - Các lệnh quan trọng:

```powershell
cd backend
.\start_backend.ps1
```

```powershell
cd frontend
npm install
npm.cmd run dev
```

```powershell
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

3. **Tài liệu báo cáo**
   - Có thể dùng file Markdown này làm nội dung gốc.
   - Sau đó chuyển sang PDF để nộp theo yêu cầu.
   - Khi deploy xong, bổ sung các đường dẫn:
     - Link GitHub: `[điền link repository]`
     - Link demo frontend: `[điền link Vercel frontend]`
     - Link backend API health: `[điền link Railway/Render backend]/api/health`

## 3. Giới Thiệu Bài Toán

Gomoku/Caro là trò chơi hai người trên bàn cờ dạng lưới. Trong dự án này, bàn cờ có kích thước 15x15. Hai người chơi lần lượt đặt quân vào ô trống. Người thắng là người tạo được 5 quân liên tiếp theo hàng ngang, hàng dọc hoặc đường chéo.

Bài toán AI cần giải quyết là chọn nước đi tốt cho máy trong không gian trạng thái lớn. Với bàn cờ 15x15, nếu xét toàn bộ ô trống, mỗi lượt có thể có tối đa 225 nước đi. Khi tìm kiếm nhiều lớp bằng minimax, số nhánh tăng rất nhanh. Vì vậy, hệ thống cần kết hợp nhiều kỹ thuật AI cổ điển để giảm branching factor, ưu tiên các nước chiến thuật và trả kết quả trong thời gian phù hợp cho ứng dụng tương tác.

## 4. Phương Pháp Được Sử Dụng

### 4.1. Biểu Diễn Trạng Thái

Board là ma trận 15x15 với quy ước:

- `0`: ô trống.
- `1`: AI/O/black trong internal engine.
- `-1`: người chơi/X/white.

Các module xử lý luật nằm trong `backend/board_rules.py`, gồm kiểm tra biên, kiểm tra thắng, chuẩn hóa board và duyệt ô trống.

### 4.2. Minimax Và Alpha-Beta Pruning

AI sử dụng minimax để mô phỏng các lượt đi luân phiên giữa AI và người chơi. Alpha-beta pruning được dùng để cắt bỏ các nhánh không cần xét, giúp giảm số trạng thái phải đánh giá.

Trong code, phần search chính nằm trong:

- `backend/ai_core.py`
- class `GomokuAI`
- các hàm `_search_root()` và `_minimax()`

### 4.3. Iterative Deepening Và Time Limit

AI không tìm kiếm đến độ sâu cố định một cách mù quáng. Thay vào đó, engine dùng iterative deepening: tìm từ depth thấp đến depth cao hơn, trong giới hạn thời gian.

Lợi ích:

- Luôn có nước đi tốt nhất đã biết nếu hết thời gian.
- Easy/Medium/Hard có thể dùng time limit khác nhau.
- Phù hợp với giao diện tương tác, tránh làm UI chờ quá lâu.

### 4.4. Candidate Move Generation

Thay vì xét mọi ô trống trên bàn cờ, AI chỉ sinh candidate quanh các quân đã có. Cách này giảm mạnh branching factor.

Ví dụ, thay vì xét 225 ô, trong nhiều trạng thái giữa game AI chỉ cần xét khoảng vài chục nước gần khu vực đang tranh chấp.

Module liên quan:

- `backend/move_ordering.py`
- `MoveOrdering.generate_candidates()`

### 4.5. Threat Detection

AI nhận diện các pattern quan trọng của Gomoku:

- Five
- Open four
- Closed four
- Open three
- Broken three
- Double threat

Module liên quan:

- `backend/threats.py`
- `ThreatDetector`

Threat detection giúp AI biết khi nào cần thắng ngay, chặn đối thủ, tạo thế tấn công hoặc giảm nguy cơ bị thua.

### 4.6. Pattern-Based Evaluation

Evaluator chấm điểm board theo hướng:

```text
Score = AttackScore - DefenseScore
```

Trong đó:

- `AttackScore`: điểm các thế có lợi cho AI.
- `DefenseScore`: điểm các thế nguy hiểm của đối thủ.

Module liên quan:

- `backend/evaluator.py`
- `BoardEvaluator`

Evaluator kết hợp threat score và contiguous pattern score để đánh giá thế cờ khi search đến leaf node.

### 4.7. Immediate Win/Block

Trước khi search sâu, AI kiểm tra:

1. AI có nước thắng ngay không.
2. Người chơi có nước thắng ngay cần chặn không.

Điều này giúp tránh các lỗi chiến thuật một bước, ví dụ bỏ qua việc chặn 4 quân liên tiếp của đối thủ.

### 4.8. Zobrist Hashing Và Transposition Table

AI dùng Zobrist hashing để mã hóa board thành hash. Transposition table lưu kết quả search của các trạng thái đã gặp, giúp giảm tính toán lặp lại.

Cải tiến hiện tại:

- Hash có tính đến side-to-move.
- Transposition table lưu thêm `best_move`.
- Khi gặp lại trạng thái, AI ưu tiên cached best move trong move ordering.

### 4.9. Minimal Threat Space Search / VCF-Lite

Dự án đã thêm một phiên bản tối giản của forcing search. Trước khi vào minimax thường, AI thử tìm nước tạo threat bắt buộc, ví dụ tạo open-four.

Đây chưa phải full Threat Space Search hoặc full VCF solver, nhưng giúp AI xử lý tốt hơn một số chuỗi thắng hoặc tạo áp lực ngắn.

Module liên quan:

- `backend/ai_core.py`
- `GomokuAI._find_forcing_win()`
- `backend/move_ordering.py`
- `MoveOrdering.generates_forcing_threat()`

## 5. Chức Năng Chính Của Hệ Thống

### 5.1. Chế Độ Người Chơi Với AI

Luồng hoạt động:

1. Người chơi click vào một ô trên frontend.
2. Frontend cập nhật board local với quân `-1`.
3. Frontend gọi API `POST /api/get-move`.
4. Backend validate board.
5. Backend chọn AI theo difficulty.
6. AI trả về nước đi, evaluation, reason và completed depth.
7. Frontend đặt quân AI `1` và cập nhật trạng thái.

Endpoint chính:

```http
GET /api/health
POST /api/get-move
```

### 5.2. Difficulty

Difficulty được cấu hình trong `backend/main.py`:

- Easy: depth thấp, time limit ngắn.
- Medium: cân bằng giữa độ sâu và thời gian.
- Hard: depth/time limit cao hơn.

### 5.3. Arena Self-Play

Arena cho phép AI tự đấu để sinh dữ liệu JSONL. Dữ liệu có thể dùng cho phân tích hoặc huấn luyện sau này nếu mở rộng theo hướng learning-based.

Các file chính:

- `arena/engine.py`
- `arena/run_arena.py`
- `arena/service.py`

## 6. Phần Mềm, Thư Viện Và Dữ Liệu Sử Dụng

### 6.1. Thư Viện

- Python 3
- FastAPI
- Pydantic
- Uvicorn
- React
- Vite

### 6.2. Dữ Liệu

Dự án không sử dụng dataset bên ngoài để huấn luyện AI. AI hiện tại là classical search engine. Arena có thể sinh dữ liệu JSONL phục vụ phân tích hoặc hướng phát triển sau này.

### 6.3. Phương Pháp Có Sẵn Được Khai Thác

Dự án sử dụng các phương pháp AI cổ điển đã biết:

- Minimax
- Alpha-beta pruning
- Iterative deepening
- Zobrist hashing
- Transposition table
- Pattern-based heuristic evaluation

Các phương pháp này được áp dụng và điều chỉnh cho bài toán Gomoku/Caro 15x15.

## 7. Kết Quả Benchmark

Benchmark được chạy bằng:

```powershell
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

Output được lưu tại:

```text
benchmark_results.json
```

### 7.1. Bảng Kết Quả

| Case | Agent | Move | Reason | Completed Depth | Time (ms) |
|---|---|---|---|---:|---:|
| opening | center_first_baseline | [7, 7] | center_or_nearest_empty | 0 | 0.00 |
| opening | project_easy | [7, 7] | opening_center | 0 | 0.12 |
| opening | project_medium | [7, 7] | opening_center | 0 | 0.07 |
| opening | project_hard | [7, 7] | opening_center | 0 | 0.07 |
| midgame | center_first_baseline | [6, 6] | center_or_nearest_empty | 0 | 0.01 |
| midgame | project_easy | [6, 10] | creating_double_threat | 2 | 171.22 |
| midgame | project_medium | [6, 6] | building_attack | 2 | 1222.49 |
| midgame | project_hard | [6, 6] | building_attack | 2 | 2215.72 |
| block_open_four | center_first_baseline | [6, 7] | center_or_nearest_empty | 0 | 0.02 |
| block_open_four | project_easy | [7, 9] | blocking_win | 0 | 22.48 |
| block_open_four | project_medium | [7, 9] | blocking_win | 0 | 20.12 |
| block_open_four | project_hard | [7, 9] | blocking_win | 0 | 15.92 |
| forcing_open_four | center_first_baseline | [7, 7] | center_or_nearest_empty | 0 | 0.01 |
| forcing_open_four | project_easy | [6, 4] | creating_open_four | 0 | 45.94 |
| forcing_open_four | project_medium | [6, 4] | creating_open_four | 0 | 49.80 |
| forcing_open_four | project_hard | [6, 4] | creating_open_four | 0 | 52.16 |

### 7.2. Nhận Xét Benchmark

Kết quả cho thấy AI xử lý tốt các tình huống chiến thuật ngắn:

- Opening: chọn trung tâm.
- Block open-four: chọn nước chặn thắng ngay.
- Forcing open-four: chọn nước tạo open-four.

Ở case midgame, Medium và Hard hoàn thành depth 2 và mất nhiều thời gian hơn Easy. Điều này phản ánh trade-off giữa độ sâu search và thời gian phản hồi. Dự án phù hợp để minh họa classical AI search, nhưng chưa nên claim là engine Gomoku cấp thi đấu.

## 8. Kiểm Thử

Các kiểm thử đã có:

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_tactical_cases tests.test_forcing_search tests.test_transposition_table -v
```

Nội dung test:

- Tactical cases: opening, thắng ngay, chặn open-four, chặn broken-four, chặn dọc/chéo.
- Forcing search: chọn nước tạo open-four.
- Transposition table: load cache cũ/mới và hỗ trợ cached best move.

Kiểm tra compile:

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py benchmark_ai.py
```

Arena smoke test:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

## 9. Khó Khăn Và Cách Giải Quyết

### 9.1. Branching Factor Lớn

Vấn đề: bàn cờ 15x15 có tối đa 225 ô, khiến minimax tăng số nhánh rất nhanh.

Cách giải quyết:

- Candidate generation quanh các quân đã có.
- Candidate limit theo difficulty.
- Move ordering để alpha-beta pruning hiệu quả hơn.

### 9.2. AI Có Thể Bỏ Qua Threat Ngắn

Vấn đề: nếu chỉ dựa vào evaluator ở leaf node, AI có thể bỏ qua một số threat bắt buộc.

Cách giải quyết:

- Immediate win/block trước search.
- Threat detection cho open-four, closed-four, open-three, broken-three.
- Minimal forcing search trước minimax thường.

### 9.3. Time Limit Ở Midgame

Vấn đề: Medium/Hard có thể chạm time limit và chỉ hoàn thành depth thấp.

Cách giải quyết:

- Iterative deepening để luôn có best move đã biết.
- Transposition table để giảm search lặp.
- Lưu best move trong cache để cải thiện move ordering ở lần search sau.

### 9.4. Báo Cáo Cần Có Bằng Chứng

Vấn đề: nếu chỉ mô tả thuật toán, báo cáo khó chứng minh chất lượng AI.

Cách giải quyết:

- Thêm tactical regression tests.
- Thêm benchmark script xuất JSON.
- So sánh với baseline đơn giản.

## 10. Kết Luận

Dự án xây dựng được một hệ thống Gomoku/Caro 15x15 có AI theo hướng classical search. AI không dùng learning hoặc training, nhưng kết hợp nhiều kỹ thuật quan trọng của game AI:

- Minimax và alpha-beta pruning.
- Candidate move generation.
- Move ordering dựa trên threat.
- Threat detection.
- Pattern-based evaluation.
- Immediate win/block.
- Iterative deepening.
- Zobrist hashing và transposition table.
- Minimal forcing search.

Kết quả benchmark cho thấy AI xử lý tốt các tình huống chiến thuật ngắn và có khả năng giải thích nước đi thông qua `reason`. Tuy nhiên, AI vẫn còn giới hạn ở midgame do branching factor lớn và chưa có full Threat Space Search hoặc solver chuyên sâu.

## 11. Hướng Phát Triển Tương Lai

Các hướng cải tiến hợp lý:

1. Mở rộng tactical benchmark suite.
2. Cải thiện evaluator cho double-threat phức tạp.
3. Phát triển Threat Space Search / VCF solver đầy đủ hơn.
4. Thêm killer move heuristic và history heuristic.
5. Thêm Principal Variation Search và aspiration window.
6. Tối ưu parallel root search.
7. Hiển thị debug board/reason/depth chi tiết hơn trên UI.
8. So sánh định tính hoặc thực nghiệm với các engine như Rapfi/Yixin nếu có điều kiện chạy cùng luật.

## 12. Triển Khai Lên Internet

Thay vì chỉ nộp source code, dự án có thể triển khai online để giảng viên chạy thử trực tiếp. Điều này giúp tăng chất lượng demo và chứng minh hệ thống hoạt động như một ứng dụng hoàn chỉnh.

### 12.1. Mục Tiêu Deploy

Mục tiêu deploy:

- Có một link frontend public để người dùng mở trực tiếp trên trình duyệt.
- Có một backend API public để frontend gọi AI.
- Backend trả lời được endpoint health check.
- Người dùng có thể chơi Gomoku/Caro với AI mà không cần cài đặt local.
- Nếu cần demo arena, có thể deploy thêm arena service hoặc giữ arena ở chế độ chạy local.

### 12.2. Phương Án Khuyến Nghị

Phương án khuyến nghị:

```text
Frontend React/Vite  -> Vercel
Backend FastAPI      -> Railway hoặc Render
Arena service        -> tùy chọn, có thể deploy sau
```

Lý do chọn phương án này:

- Vercel phù hợp cho frontend React/Vite, build ra static files và host qua CDN.
- Railway hoặc Render phù hợp cho FastAPI backend chạy bằng Uvicorn.
- Tách frontend và backend giúp deploy đơn giản hơn so với tự cấu hình VPS.
- Phù hợp với mục tiêu đồ án: có link demo public, dễ trình bày, ít chi phí vận hành.

### 12.3. Deploy Frontend Trên Vercel

Frontend nằm trong thư mục:

```text
frontend/
```

Cấu hình build:

```text
Install command: npm install
Build command: npm run build
Output directory: dist
```

Biến môi trường cần cấu hình trên Vercel:

```text
VITE_API_BASE_URL=https://<backend-domain>
VITE_ARENA_API_BASE_URL=https://<arena-domain>
```

Trong đó:

- `VITE_API_BASE_URL` là URL public của backend FastAPI.
- `VITE_ARENA_API_BASE_URL` chỉ cần nếu deploy arena service.

Theo tài liệu Vercel, các biến môi trường dùng trong Vite cần prefix `VITE_` để frontend có thể đọc tại build time.

Tài liệu tham khảo:

- Vercel Vite: https://vercel.com/docs/frameworks/frontend/vite
- Vercel environment variables: https://vercel.com/docs/projects/environment-variables

### 12.4. Deploy Backend FastAPI Trên Railway Hoặc Render

Backend nằm trong thư mục:

```text
backend/
```

Các dependency backend nằm trong:

```text
backend/requirements.txt
```

Start command đề xuất:

```powershell
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Nếu nền tảng không dùng biến `$PORT`, có thể cấu hình port theo hướng dẫn riêng của nền tảng.

Endpoint kiểm tra sau khi deploy:

```http
GET https://<backend-domain>/api/health
```

Kết quả kỳ vọng:

```json
{"status":"ok"}
```

Tài liệu tham khảo:

- Railway FastAPI guide: https://docs.railway.com/guides/fastapi
- Render FastAPI template: https://render.com/templates/fastapi

### 12.5. CORS Và Kết Nối Frontend - Backend

Backend hiện đã bật CORS trong `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Cấu hình này thuận tiện cho demo vì frontend public có thể gọi backend public. Khi triển khai production nghiêm túc hơn, nên giới hạn `allow_origins` về đúng domain frontend, ví dụ:

```python
allow_origins=["https://<frontend-domain>"]
```

### 12.6. Deploy Arena Service

Arena service nằm ở:

```text
arena/service.py
```

Arena có thể deploy như một service FastAPI riêng nếu muốn demo chế độ AI tự đấu online.

Start command đề xuất:

```powershell
uvicorn arena.service:app --host 0.0.0.0 --port $PORT
```

Tuy nhiên, arena có thể sinh file JSONL và chạy nhiều game nên cần cân nhắc giới hạn tài nguyên. Với mục tiêu demo BTL, có thể:

- Deploy frontend và backend trước.
- Chạy arena local khi trình bày nếu cần.
- Chỉ deploy arena nếu nền tảng có đủ tài nguyên và cần demo self-play online.

### 12.7. Kiểm Tra Sau Deploy

Checklist sau deploy:

1. Mở frontend public URL.
2. Chọn difficulty.
3. Click một ô để người chơi đánh X.
4. Kiểm tra AI trả nước O.
5. Kiểm tra status hiển thị reason/depth/evaluation.
6. Mở backend health URL:

```text
https://<backend-domain>/api/health
```

7. Kiểm tra browser console không có lỗi CORS.

### 12.8. Nội Dung Cần Bổ Sung Khi Nộp

Khi đã deploy xong, thêm vào đầu báo cáo hoặc README:

```text
GitHub source code: <link repository>
Frontend demo: <link Vercel app>
Backend health check: <link backend>/api/health
API docs: <link backend>/docs
```

FastAPI tự cung cấp trang tài liệu API tại:

```text
https://<backend-domain>/docs
```

Đây là điểm thuận lợi khi trình bày vì giảng viên có thể xem và thử endpoint trực tiếp.

## 13. Tiêu Chí Đánh Giá BTL

Theo yêu cầu đánh giá, công việc BTL được xem xét theo các tiêu chí sau.

### 13.1. Mức Độ Phức Tạp / Khó Khăn Của Bài Toán

Gomoku/Caro 15x15 là bài toán có không gian trạng thái lớn. Việc chọn nước đi tốt cần xử lý branching factor cao, đối kháng hai người chơi và các threat chiến thuật đặc thù. So với tic-tac-toe 3x3, bài toán phức tạp hơn nhiều vì số ô và số pattern cần nhận diện lớn hơn.

### 13.2. Chất Lượng Phương Pháp Giải Quyết

Phương pháp được dùng phù hợp với bài toán game đối kháng:

- Minimax cho quyết định đối kháng.
- Alpha-beta pruning để giảm số node.
- Candidate generation để giảm số nước cần xét.
- Threat detection để đưa tri thức Gomoku vào search.
- Pattern evaluator để đánh giá trạng thái chưa kết thúc.
- Iterative deepening và time limit để phù hợp ứng dụng tương tác.
- Benchmark và regression test để kiểm chứng hành vi AI.

### 13.3. Chất Lượng Bài Trình Bày

Bài trình bày nên tập trung vào:

1. Bài toán Gomoku 15x15 và độ khó.
2. Kiến trúc hệ thống.
3. Luồng AI chọn nước đi.
4. Các kỹ thuật AI chính.
5. Demo người chơi với AI.
6. Benchmark so sánh baseline và project AI.
7. Khó khăn, giới hạn và hướng phát triển.

Thời lượng khuyến nghị: khoảng 15 phút.

### 13.4. Chất Lượng Tài Liệu Báo Cáo

Báo cáo cần có:

- Giới thiệu bài toán.
- Mô tả phương pháp.
- Mô tả chức năng hệ thống.
- Cách cài đặt và chạy.
- Thư viện/phương pháp/dữ liệu sử dụng.
- Kết quả benchmark.
- Khó khăn và cách giải quyết.
- Kết luận và hướng phát triển.

### 13.5. Cài Đặt Hệ Thống Thử Nghiệm

Hệ thống có thể chạy thử qua:

- Backend FastAPI tại `http://127.0.0.1:8000`.
- Frontend React/Vite tại `http://127.0.0.1:5173`.
- Arena service tại `http://127.0.0.1:8100`.
- Benchmark backend bằng `benchmark_ai.py`.
- Demo online sau deploy:
  - Frontend demo: `[điền link Vercel app]`
  - Backend health check: `[điền link backend]/api/health`
  - API docs: `[điền link backend]/docs`

Các chức năng chính dễ kiểm thử:

- Chơi người với AI.
- Chọn difficulty.
- Xem reason/evaluation/depth AI trả về.
- Chạy arena self-play.
- Chạy tactical regression tests.
- Chạy benchmark JSON.

## 14. Gợi Ý Dàn Ý Slide 15 Phút

1. **Slide 1:** Tên đề tài, thành viên, mục tiêu.
2. **Slide 2:** Giới thiệu Gomoku/Caro 15x15.
3. **Slide 3:** Vì sao bài toán khó: branching factor và threat.
4. **Slide 4:** Kiến trúc hệ thống frontend/backend/arena.
5. **Slide 5:** Luồng AI chọn nước đi.
6. **Slide 6:** Minimax, alpha-beta, iterative deepening.
7. **Slide 7:** Candidate generation và move ordering.
8. **Slide 8:** Threat detection và evaluator.
9. **Slide 9:** Transposition table và Zobrist hash.
10. **Slide 10:** Minimal forcing search.
11. **Slide 11:** Benchmark results.
12. **Slide 12:** Demo hệ thống online.
13. **Slide 13:** Khó khăn và cách giải quyết.
14. **Slide 14:** Giới hạn hiện tại.
15. **Slide 15:** Kết luận và hướng phát triển.
