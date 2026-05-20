# Implementation Plan: Người - Máy Gomoku AI

Mục tiêu: nâng cấp chế độ người - máy để bot đánh thông minh hơn nhưng vẫn kiểm soát được thời gian phản hồi. Không dùng reinforcement learning hoặc model training; hướng triển khai là classical game engine: search tốt hơn, cache đúng hơn, heuristic/threat evaluator mạnh hơn.

## Nguyên tắc triển khai

- Ưu tiên sửa tính đúng trước khi tăng độ sâu search.
- Mỗi lượt người chơi xong, backend phải search lại từ board mới.
- Bot phải có time limit để không làm UI/API bị treo.
- Các nước chiến thuật bắt buộc như thắng ngay hoặc chặn thắng ngay không được bị loại bởi `candidate_limit`.
- Thay đổi nên giữ `GomokuAI` là core engine dùng chung cho backend và arena.

## Module AI hiện tại

AI core đã được tách khỏi một file lớn thành các module:

- `backend/ai_types.py`: constants, config, dataclass kết quả.
- `backend/board_rules.py`: luật board cơ bản.
- `backend/threats.py`: threat detector.
- `backend/evaluator.py`: heuristic evaluator.
- `backend/move_ordering.py`: candidate generation và move ordering.
- `backend/ai_core.py`: search orchestration, minimax, alpha-beta, transposition table.

Khi triển khai các phase mới, ưu tiên sửa đúng module thay vì nhồi thêm logic vào `ai_core.py`.

## Phase 1: Sửa nền tảng core AI

### 1. Sửa độ đúng của core AI

**Mục tiêu**

Đảm bảo AI search đúng perspective, không dùng nhầm cache giữa các lượt hoặc giữa các người chơi.

**Việc cần làm**

- Thêm side-to-move vào transposition table key.
- Làm rõ contract của `get_best_move()`:
  - hoặc chỉ hỗ trợ `player=AI_STONE`;
  - hoặc chuyển sang perspective-based search/negamax để hỗ trợ cả `1` và `-1`.
- Validate API không nhận mode mà core chưa hỗ trợ đúng.
- Kiểm tra lại arena vì arena đang dùng `normalize_board()`.

**File chính**

- `backend/ai_core.py`
- `backend/main.py`
- `arena/engine.py`

**Done khi**

- Cùng một board nhưng khác lượt đi không dùng chung cache sai.
- API người - máy vẫn trả nước hợp lệ.
- Arena self-play không bị vỡ do thay đổi perspective.

### 2. Chống nước thắng ngay

**Mục tiêu**

Bot không bỏ lỡ nước thắng trong 1 ply và không quên chặn người chơi thắng ngay.

**Việc cần làm**

- Thêm helper tìm nước thắng tức thì cho một player.
- Trong `get_best_move()`:
  - nếu AI có nước thắng ngay, đánh ngay;
  - nếu người chơi có nước thắng ngay, chặn ngay;
  - sau đó mới vào search thường.

**File chính**

- `backend/ai_core.py`

**Done khi**

- Test board AI có 4 quân liên tiếp, bot chọn nước thứ 5.
- Test board người chơi có 4 quân liên tiếp, bot chọn nước chặn.

## Phase 2: Tăng hiệu quả search

### 3. Nâng move ordering

**Mục tiêu**

Giúp alpha-beta pruning cắt nhiều nhánh hơn bằng cách xét nước mạnh trước.

**Việc cần làm**

- Tách scoring nước đi thành tactical score rõ ràng.
- Ưu tiên:
  - thắng ngay;
  - chặn thắng ngay;
  - tạo open four;
  - chặn open four;
  - tạo/chặn open three;
  - gần trung tâm;
  - heuristic score hiện tại.
- Lưu best move từ transposition table để đưa lên đầu danh sách ở lần search sau.

**File chính**

- `backend/ai_core.py`

**Done khi**

- Candidate list luôn đưa tactical moves lên đầu.
- Search cùng depth nhanh hơn hoặc ít nhất không chậm đáng kể.

### 4. Iterative deepening + time limit

**Mục tiêu**

Bot luôn trả nước trong thời gian cấu hình, đồng thời tận dụng thời gian còn lại để search sâu hơn.

**Việc cần làm**

- Thêm config:
  - `time_limit_ms`;
  - `max_depth`;
  - `difficulty`.
- Search depth 1, 2, 3... cho đến hết giờ.
- Nếu timeout trong depth hiện tại, trả best move hoàn chỉnh từ depth trước.
- Không để timeout làm board bị mutate dở.

**File chính**

- `backend/ai_core.py`
- `backend/main.py`
- `frontend/src/App.jsx`

**Done khi**

- Easy/Medium/Hard trả nước ổn định trong giới hạn thời gian.
- Nếu hết giờ, bot vẫn trả một nước hợp lệ.

### 5. Candidate generation thông minh hơn

**Mục tiêu**

Giảm branching factor nhưng không bỏ sót nước chiến thuật bắt buộc.

**Việc cần làm**

- Giữ candidate theo vùng gần quân hiện có.
- Luôn thêm tactical candidates dù vượt `candidate_limit`.
- Điều chỉnh radius theo giai đoạn:
  - đầu game nhỏ;
  - giữa/cuối game hoặc có threat thì mở rộng.
- Loại candidate trùng và sort ổn định.

**File chính**

- `backend/ai_core.py`

**Done khi**

- Nước chặn/thắng không bị loại bởi giới hạn candidate.
- Empty board vẫn chọn trung tâm.

## Phase 3: Nâng chất lượng đánh cờ

### 6. Threat detection

**Mục tiêu**

Nhận diện các thế caro quan trọng thay vì chỉ đếm chuỗi liên tục.

**Việc cần làm**

- Viết module/helper phát hiện:
  - five;
  - open four;
  - closed four;
  - open three;
  - broken three;
  - double threat.
- Trả về threat summary cho từng move hoặc từng board.
- Dùng threat summary trong move ordering và evaluation.

**File chính**

- `backend/ai_core.py`
- Có thể tách `backend/threats.py` nếu file core bắt đầu quá lớn.

**Done khi**

- Bot nhận ra open four và broken three.
- Double threat được chấm cao hơn threat đơn.

### 7. Cải thiện heuristic

**Mục tiêu**

Đánh giá board sát thực tế Gomoku hơn.

**Việc cần làm**

- Thay hoặc bổ sung evaluator pattern-based.
- Nhận diện các mẫu như:
  - `_XXXX_`
  - `_XXXXO`
  - `XX_XX`
  - `X_XXX`
  - `_XXX_`
  - `_XX_X_`
- Tách điểm attack và defense nếu cần.
- Giữ score terminal thắng/thua cao hơn mọi heuristic thường.

**File chính**

- `backend/ai_core.py`
- Có thể tách `backend/evaluator.py`.

**Done khi**

- Bot không đánh giá thấp chuỗi bị hở ở giữa.
- Bot ưu tiên thế tạo thắng bắt buộc hơn nước chỉ tăng điểm nhỏ.

### 8. Threat extension / quiescence có giới hạn

**Mục tiêu**

Không dừng search ở trạng thái đang có threat nguy hiểm.

**Việc cần làm**

- Ở depth 0, nếu board có open four/open three quan trọng, search tiếp một số forcing moves.
- Giới hạn extension bằng:
  - max extension depth;
  - chỉ xét tactical candidates;
  - vẫn tôn trọng time limit.

**File chính**

- `backend/ai_core.py`

**Done khi**

- Bot ít bị horizon effect ở tình huống sắp thắng/sắp thua.
- Không làm thời gian phản hồi vượt quá cấu hình.

## Phase 4: API và UI người - máy

### 9. API/UI cho độ khó

**Mục tiêu**

Cho người chơi chọn độ khó và kiểm soát thời gian suy nghĩ của bot.

**Việc cần làm**

- Backend nhận thêm `difficulty` hoặc search config trong request.
- Map difficulty:
  - Easy: depth thấp, time limit ngắn;
  - Medium: cân bằng;
  - Hard: depth/time limit cao hơn, bật threat extension.
- Frontend thêm control chọn độ khó.
- Reset game giữ hoặc clear difficulty theo UX đã chọn.

**File chính**

- `backend/main.py`
- `backend/ai_core.py`
- `frontend/src/App.jsx`
- `frontend/src/App.css`

**Done khi**

- Người chơi đổi difficulty được từ UI.
- Backend fallback an toàn nếu thiếu difficulty.

### 10. Trả thêm lý do nước đi

**Mục tiêu**

Hỗ trợ debug và giúp hiểu vì sao bot chọn nước đó.

**Việc cần làm**

- Backend trả thêm `reason`, ví dụ:
  - `winning_move`;
  - `blocking_win`;
  - `creating_open_four`;
  - `blocking_open_four`;
  - `best_search_score`;
  - `timeout_best_known`.
- Frontend hiển thị reason trong status hoặc debug panel nhỏ.
- Không để reason ảnh hưởng tới logic đặt quân.

**File chính**

- `backend/main.py`
- `backend/ai_core.py`
- `frontend/src/App.jsx`

**Done khi**

- Response có lý do nước đi.
- UI hiển thị lý do ngắn gọn.

## Test Plan

### Unit tests cho AI core

- Empty board chọn trung tâm.
- AI có 4 quân liên tiếp thì đánh thắng ngay.
- Human có 4 quân liên tiếp thì AI chặn.
- Board đã kết thúc thì không trả move.
- Candidate generation không trả ô đã có quân.
- Transposition table phân biệt side-to-move.
- Pattern evaluator nhận ra open four, closed four, broken three.

### API tests

- `/api/health` trả `ok`.
- `/api/get-move` reject board sai kích thước.
- `/api/get-move` reject cell ngoài `-1, 0, 1`.
- `/api/get-move` trả move hợp lệ cho board thường.
- Difficulty thiếu thì dùng default.

### Manual tests

- Chơi vài ván ở Easy/Medium/Hard.
- Kiểm tra bot không delay quá lâu.
- Kiểm tra UI không cho click khi bot đang suy nghĩ.
- Kiểm tra arena vẫn chạy sau khi core thay đổi.

## Thứ tự ưu tiên khuyến nghị

1. Sửa transposition table và perspective.
2. Thêm immediate win/block.
3. Nâng move ordering.
4. Thêm iterative deepening với time limit.
5. Cải thiện candidate generation.
6. Thêm threat detection.
7. Cải thiện heuristic pattern-based.
8. Thêm threat extension có giới hạn.
9. Thêm difficulty ở API/UI.
10. Trả reason cho nước đi.

## Rủi ro chính

- Threat evaluator phức tạp có thể làm search chậm nếu gọi quá nhiều lần.
- Candidate limit quá thấp có thể bỏ sót nước phòng thủ nếu không giữ tactical candidates.
- Transposition table lưu ra file có thể phình to; cần cân nhắc giới hạn kích thước sau này.
- Iterative deepening cần timeout sạch để không để board mutate dở trong recursion.

## Kết quả mong muốn

Sau khi hoàn thành, chế độ người - máy sẽ có bot:

- đánh thắng/chặn thắng ngay ổn định;
- ít bỏ sót threat quan trọng;
- phản hồi trong thời gian kiểm soát được;
- có nhiều mức độ khó;
- dễ debug hơn nhờ reason/evaluation rõ ràng.
