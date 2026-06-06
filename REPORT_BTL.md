# Bao Cao Bai Tap Lon: Gomoku/Caro 15x15 AI

## 1. Gioi Thieu Thuat Toan

### 1.1. Gioi thieu bai toan

Du an xay dung he thong choi Gomoku/Caro 15x15 giua nguoi choi va AI. Ten thu muc repository la `Tictactoe`, nhung bai toan hien tai khong phai tic-tac-toe 3x3. Game su dung ban co 15x15, hai ben lan luot dat quan, va ben thang la ben tao duoc 5 quan lien tiep theo hang ngang, hang doc hoac duong cheo.

Bai toan AI la chon nuoc di tot trong khong gian trang thai lon. O dau game, board co toi da 225 o trong. Neu dung minimax tren toan bo o trong, branching factor tang rat nhanh. Vi vay, du an khong chi dung minimax thuan tuy ma ket hop nhieu ky thuat AI co dien va tri thuc rieng cua Gomoku.

### 1.2. Huong tiep can AI

AI cua du an la classical game engine, khong dung reinforcement learning, khong huan luyen neural network va khong claim la engine SOTA. Trong tam cua du an la tao mot AI co the choi hop ly, phan hoi trong thoi gian ngan, va giai thich duoc ly do chon nuoc di thong qua cac truong `reason`, `evaluation` va `completed_depth`.

### 1.3. Cac thanh phan thuat toan chinh

| Thanh phan | Vai tro trong du an |
|---|---|
| Minimax | Mo phong hai ben di toi uu trong game doi khang |
| Alpha-beta pruning | Cat cac nhanh khong can xet de giam so node |
| Iterative deepening | Tim sau dan trong gioi han thoi gian |
| Candidate generation | Chi sinh nuoc quanh vung da co quan de giam branching factor |
| Move ordering | Uu tien nuoc co threat de alpha-beta cat tot hon |
| Threat detection | Nhan dien five, open-four, closed-four, open-three, broken-three, double-threat |
| Pattern evaluator | Cham diem board theo `AttackScore - DefenseScore` |
| Immediate win/block | Xu ly thang ngay va chan thang truoc khi search sau |
| Zobrist hash/TT | Cache trang thai da search, co side-to-move va best move |
| Loss memory | Ghi cac nuoc AI trong van thua va tru penalty khi gap lai board tuong ung |
| Forcing search toi gian | Tim mot so nuoc tao threat bat buoc nhu open-four |

Luu y: du an chua co full Threat Space Search, full VCF solver, PVS, killer move heuristic, history heuristic hoac parallel search. Cac muc nay duoc xem la huong phat trien tuong lai.

## 2. Tong Quan Va Xu Ly Du Lieu

### 2.1. Kien truc tong quan

Du an gom ba phan chinh:

```text
Frontend React/Vite
  -> Backend FastAPI
      -> GomokuAI core

Frontend React/Vite
  -> Arena FastAPI service
      -> Self-play engine
```

Cac thu muc chinh:

| Thu muc/File | Vai tro |
|---|---|
| `frontend/` | UI React/Vite cho che do choi voi AI va arena |
| `backend/main.py` | FastAPI API cho che do nguoi choi voi AI |
| `backend/ai_core.py` | Orchestration search, minimax, alpha-beta, iterative deepening, TT |
| `backend/threats.py` | Threat detection pattern-based |
| `backend/evaluator.py` | Heuristic evaluator |
| `backend/move_ordering.py` | Candidate generation, move scoring, reason classification |
| `arena/` | Self-play engine va service |
| `tests/` | Tactical regression tests, benchmark helper tests |
| `benchmark_ai.py` | Benchmark script xuat `benchmark_results.json` |

### 2.2. Bieu dien board

Board la ma tran 15x15:

| Gia tri | Y nghia |
|---:|---|
| `0` | O trong |
| `1` | AI/O/black trong internal engine |
| `-1` | Nguoi choi/X/white |

Backend validate board bang Pydantic trong `backend/main.py`. Moi request `/api/get-move` phai co board dung kich thuoc 15x15 va moi cell thuoc tap `{-1, 0, 1}`.

### 2.3. Luong nguoi choi voi AI

```text
Nguoi choi click board
-> Frontend dat quan -1
-> POST /api/get-move
-> Backend validate board + difficulty
-> GomokuAI.get_move_analysis()
-> Backend tra row, col, evaluation, reason, completed_depth
-> Frontend dat quan AI 1 va hien thong tin phan tich
```

Endpoint chinh:

```http
GET /api/health
POST /api/get-move
POST /api/report-game-result
```

Response mau:

```json
{
  "row": 7,
  "col": 9,
  "evaluation": 9830013,
  "reason": "blocking_win",
  "difficulty": "medium",
  "completed_depth": 0,
  "message": "Move generated successfully."
}
```

### 2.4. Arena va du lieu self-play

Arena cho phep AI tu dau AI vs AI. Khi ghi mau, arena co the luu JSONL gom board, normalized board, move, evaluation, winner va outcome. Du an hien khong dung dataset ngoai de huan luyen AI. Arena duoc xem la cong cu sinh du lieu phan tich hoac lam nen tang cho huong learning-based trong tuong lai.

## 3. Co So Ly Thuyet

### 3.1. Minimax va alpha-beta pruning

Minimax la thuat toan tim kiem trong game doi khang. AI gia dinh minh se chon nuoc toi da hoa diem, con doi thu se chon nuoc toi thieu hoa diem cua AI. Alpha-beta pruning giup cat cac nhanh khong can xet khi da biet chung khong the tao ket qua tot hon.

Trong code, logic nam o `GomokuAI._search_root()` va `GomokuAI._minimax()`.

### 3.2. Iterative deepening va time limit

AI search tu depth thap len depth cao trong gioi han thoi gian. Cach nay giup AI luon co `best_move` da biet neu cham time limit. Difficulty hien cau hinh trong `backend/main.py`:

| Difficulty | Depth | Candidate radius | Candidate limit | Time limit |
|---|---:|---:|---:|---:|
| Easy | 2 | 2 | 8 | 400 ms |
| Medium | 3 | 2 | 10 | 1200 ms |
| Hard | 4 | 3 | 12 | 2200 ms |

### 3.3. Candidate generation va move ordering

Gomoku 15x15 co qua nhieu o trong, nen AI chi sinh candidate quanh cac quan da co. Sau do, candidate duoc sap xep theo:

- Nuoc thang ngay.
- Nuoc chan doi thu thang ngay.
- Threat cua AI: open-four, closed-four, open-three, broken-three, double-threat.
- Threat cua doi thu can chan.
- Local shape score va center bias.

Dieu nay vua giam branching factor, vua giup alpha-beta pruning cat nhanh hon.

### 3.4. Threat detection

Threat detection nhan dien cac mau co dac thu cua Gomoku:

| Threat | Mo ta |
|---|---|
| Five | 5 quan lien tiep, ket thuc game |
| Open-four | 4 quan lien tiep co hai dau mo |
| Closed-four | 4 quan co the thang o mot dau hoac broken-four khan cap |
| Open-three | 3 quan co kha nang phat trien thanh open-four |
| Broken-three | 3 quan co khoang trong, van co gia tri tan cong/phong thu |
| Double-threat | Nhieu threat dong thoi, doi thu kho chan het |

Trong lan cai tien gan nhat, `backend/threats.py` da duoc sua de giam false positive:

- Cac shape bi chan hai dau nhu `2011102`, `2110102`, `2011012`, `2101102` khong con bi tinh la forcing threat.
- Cac jump-open-three nhu `011010`, `010110` khong bi dem trung thanh double-threat gia.
- Regression tests duoc them trong `tests/test_advanced_tactics.py`.

### 3.5. Pattern-based evaluation

Evaluator cham diem theo cong thuc:

```text
Score = AttackScore - DefenseScore
```

Trong do `AttackScore` la diem threat/pattern co loi cho AI, con `DefenseScore` la diem threat/pattern nguy hiem cua doi thu. Terminal win/loss co diem cao hon cac heuristic thong thuong de tranh danh gia sai trang thai ket thuc.

### 3.6. Zobrist hashing va transposition table

Zobrist hashing ma hoa board thanh hash 64-bit. Transposition table luu ket qua search de tranh tinh lai trang thai da gap. Du an hien luu ca side-to-move trong hash va luu `best_move`, giup move ordering tot hon khi gap lai trang thai tuong tu.

Can phan biet ro: transposition table trong du an la co che toi uu hoa search, khong phai co che giai quyet toan bo van co. Cache chi luu ket qua cac trang thai da duoc minimax/alpha-beta danh gia, gom score, depth, flag va best move. No giup AI tranh tinh lap va sap xep nuoc tot hon, nhung khong tu chung minh duoc the thang/thua chac chan nhu solver.

Viec giai quyet cac chuoi thang bat buoc trong Gomoku thuong can cac ky thuat manh hon, vi du full Threat Space Search, VCF solver hoac proof-number search. Du an hien moi co forcing search toi gian cho mot so threat ngan, nen vai tro cua cache la ho tro minimax/alpha-beta thay vi thay the solver.

### 3.7. Loss memory cho cac van thua

Ben canh transposition table, du an da them `loss_memory` de ghi lai cac nuoc AI trong nhung van ma nguoi choi thang. Moi ban ghi loss memory gan voi hash cua board truoc khi AI di va toa do nuoc AI da chon. Khi gap lai cung board, AI tru penalty cho nuoc da tung nam trong van thua, tu do uu tien cac candidate khac neu van con lua chon hop le.

Co che nay khong phai reinforcement learning va khong huan luyen model. No la mot dang memory-based avoidance don gian, phu hop voi classical search engine: AI ghi nho kinh nghiem that bai cu the va tranh lap lai trong nhung the co tuong ung. De dua vao luong choi that, frontend luu lich su cac board truoc moi nuoc AI. Khi nguoi choi thang, frontend gui `winner = -1` va danh sach `ai_moves` ve endpoint `POST /api/report-game-result`. Backend goi `GomokuAI.record_game_outcome()`, ghi loss memory va luu cache ngay.

## 4. Thuc Nghiem Va Danh Gia

### 4.1. Benchmark design

Benchmark duoc chay bang:

```powershell
.\backend\venv\Scripts\python.exe benchmark_ai.py
```

Output luu tai:

```text
benchmark_results.json
```

Benchmark so sanh project AI voi cac baseline noi bo:

| Agent | Mo ta |
|---|---|
| `random_baseline` | Chon o trong ngau nhien voi seed co dinh |
| `center_first_baseline` | Chon trung tam truoc |
| `greedy_1ply_baseline` | Thu tung nuoc 1-ply va lay diem evaluator cao nhat |
| `basic_minimax_baseline` | Shallow minimax/alpha-beta, khong dung day du pipeline project AI |
| `project_easy/medium/hard` | AI cua du an theo difficulty |

Benchmark nay la internal benchmark, khong phai so sanh SOTA voi Rapfi, Yixin hay AlphaZero-Gomoku.

### 4.2. Ket qua accuracy

Ket qua hien tai tu `benchmark_results.json`:

| Agent | Correct | Total | Accuracy |
|---|---:|---:|---:|
| random_baseline | 0 | 8 | 0.00 |
| center_first_baseline | 4 | 8 | 0.50 |
| greedy_1ply_baseline | 6 | 8 | 0.75 |
| basic_minimax_baseline | 8 | 8 | 1.00 |
| project_easy | 8 | 8 | 1.00 |
| project_medium | 8 | 8 | 1.00 |
| project_hard | 8 | 8 | 1.00 |

### 4.3. Mot so case tieu bieu

| Case | Project move | Reason | Completed depth | Nhan xet |
|---|---|---|---:|---|
| opening | `[7, 7]` | `opening_center` | 0 | AI chon trung tam |
| ai_win_horizontal | `[7, 9]` | `winning_move` | 0 | AI thang ngay |
| block_open_four | `[7, 9]` | `blocking_win` | 0 | AI chan doi thu thang |
| block_broken_four | `[7, 7]` | `blocking_win` | 0 | AI chan broken-four |
| forcing_open_four | `[6, 4]` | `creating_open_four` | 0 | AI tao threat khan cap |
| create_double_three | `[7, 7]` | `creating_double_threat` | 0 | AI tao double-threat |
| block_double_three | `[7, 7]` | `blocking_double_threat` | 0 | AI chan double-threat |
| diagonal_win | `[8, 8]` | `winning_move` | 0 | AI thang theo duong cheo |

### 4.4. Kiem thu

Cac lenh kiem thu da chay sau khi cai thien tactical/threat detection:

```powershell
.\backend\venv\Scripts\python.exe -m unittest discover tests -v
```

Ket qua: 11 tests pass.

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py
```

Ket qua: pass.

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

Ket qua smoke test: 1 game, 6 samples, khong loi runtime.

### 4.5. Danh gia

Ket qua cho thay project AI xu ly tot cac tactical case co ban: thang ngay, chan thang, chan broken-four, tao open-four va xu ly double-threat. Diem manh cua du an la AI co tinh explainable: backend khong chi tra nuoc di ma con tra `reason`, `evaluation`, `completed_depth`.

Han che la benchmark van la benchmark noi bo, so case con nho, va AI chua phai engine Gomoku cap thi dau. Mot so the co phuc tap hon co the can full Threat Space Search hoac VCF solver de xu ly chuan.

## 5. Cai Dat He Thong Va Kho Khan Gap Phai

### 5.1. Cai dat local

Backend:

```powershell
cd backend
.\start_backend.ps1
```

Frontend:

```powershell
cd frontend
npm install
npm.cmd run dev
```

Arena:

```powershell
.\arena\start_arena.ps1
```

Dia chi local mac dinh:

| Thanh phan | URL |
|---|---|
| Backend | `http://127.0.0.1:8000` |
| Frontend | `http://127.0.0.1:5173` |
| Arena | `http://127.0.0.1:8100` |

### 5.2. Deploy online

Phuong an deploy trong du an:

| Thanh phan | Nen tang |
|---|---|
| Frontend React/Vite | Vercel |
| Backend FastAPI | Render |
| Arena FastAPI service | Render |

`render.yaml` hien khai bao hai service:

- `gomoku-ai-backend`, health check `/api/health`.
- `gomoku-ai-arena`, health check `/arena/api/health`.

Frontend can cau hinh:

```text
VITE_API_BASE_URL=https://<render-backend-url>
VITE_ARENA_API_BASE_URL=https://<render-arena-url>
```

Backend/arena doc:

```text
FRONTEND_ORIGINS=https://<vercel-frontend-url>
```

### 5.3. Kho khan va cach xu ly

| Kho khan | Cach xu ly trong du an |
|---|---|
| Branching factor lon | Candidate generation, candidate limit, alpha-beta pruning |
| AI can phan hoi nhanh | Iterative deepening, time limit theo difficulty |
| Threat Gomoku phuc tap | ThreatDetector, evaluator, move ordering rieng |
| False positive trong threat detection | Them regression tests va sua logic dem open-three/broken-three |
| AI co the bo qua threat ngan | Immediate win/block va forcing search toi gian |
| Cache search co the bi stale | Zobrist hash co side-to-move va memory version |
| Cache khong tu giai quyet van co | Them loss memory de tranh move thua cu the; de xuat VCF/TSS/proof-number search cho solver that su |
| Deploy khac domain | Env variables va CORS |
| Render cold start | Warm up backend/arena truoc khi demo |

## 6. Ket Luan

Du an da xay dung duoc mot he thong Gomoku/Caro 15x15 full-stack co AI theo huong classical search. AI ket hop minimax, alpha-beta pruning, iterative deepening, candidate pruning, move ordering, threat detection, pattern evaluator, immediate win/block, transposition table va loss memory. Khac voi AI black-box, backend tra ve them `reason`, `evaluation`, `completed_depth`, giup viec demo va giai thich ro rang hon.

Thuc nghiem noi bo cho thay project AI dat 8/8 tren cac tactical benchmark case hien tai, xu ly duoc cac tinh huong quan trong nhu thang ngay, chan thang, chan broken-four, tao open-four va xu ly double-threat. Ngoai ra, he thong co frontend, backend, arena, benchmark script va test suite, phu hop de nop va demo BTL.

Han che hien tai la AI van dua tren heuristic va search gioi han thoi gian. Transposition table moi dong vai tro cache de giam tinh toan lap lai, chua phai solver co the chung minh thang/thua cho toan bo the co. Du an cung chua tich hop engine ngoai de so sanh khach quan, chua co full Threat Space Search/VCF solver va chua dung reinforcement learning/neural network. Cac huong phat trien hop ly gom mo rong tactical benchmark, cai thien evaluator cho threat phuc tap, them VCF-lite/TSS, so sanh voi Rapfi/Yixin neu co dieu kien, va khai thac arena JSONL cho phan tich hoac learning-based AI trong tuong lai.
