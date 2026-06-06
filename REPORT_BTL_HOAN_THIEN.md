# Bao Cao Bai Tap Lon: Gomoku/Caro 15x15 AI

## Thong Tin Chung

| Muc | Noi dung |
|---|---|
| Ten de tai | Xay dung AI cho game Gomoku/Caro 15x15 |
| Loai bai toan | Game doi khang, turn-based, zero-sum |
| Nen tang | Full-stack React/Vite + FastAPI |
| AI chinh | Classical game engine |
| Thuat toan chinh | Minimax, alpha-beta pruning, iterative deepening |
| Tri thuc mien | Threat detection, heuristic pattern evaluator, immediate win/block |
| Thanh phan mo rong | Supervised CNN consultant model va hybrid policy prior |

Luu y: ten thu muc repository la `Tictactoe`, nhung bai toan hien tai la Gomoku/Caro 15x15, khong phai tic-tac-toe 3x3.

---

## 1. Gioi Thieu Bai Toan

### 1.1. Gomoku/Caro 15x15

Gomoku/Caro la tro choi hai nguoi, moi nguoi lan luot dat quan len ban co. Trong du an nay, ban co co kich thuoc 15x15. Mot ben chien thang khi tao duoc 5 quan lien tiep theo hang ngang, hang doc, duong cheo chinh hoac duong cheo phu.

Quy uoc board trong engine:

| Gia tri | Y nghia |
|---:|---|
| `0` | O trong |
| `1` | AI/O/black trong internal engine |
| `-1` | Nguoi choi/X/white |

Bai toan AI la chon nuoc di hop ly trong khong gian trang thai rat lon. O dau game, board co toi da 225 o trong. Neu ap dung minimax tren tat ca o trong, branching factor tang qua nhanh va khong phu hop cho ung dung tuong tac. Vi vay, du an ket hop search co dien voi nhieu ky thuat giam nhanh va tri thuc rieng cua Gomoku.

### 1.2. Muc tieu du an

Du an huong toi mot AI co kha nang:

1. Chon nuoc di hop ly trong thoi gian ngan.
2. Xu ly dung cac tinh huong chien thuat co ban: thang ngay, chan thang, tao/chan open-four, double-threat.
3. Giai thich duoc ly do chon nuoc di thong qua `reason`, `evaluation`, `completed_depth`.
4. Hoat dong trong ung dung full-stack gom frontend, backend va che do arena self-play.
5. Co du lieu benchmark va test regression de danh gia tien bo.
6. Mo rong bang supervised learning advisor ma khong thay the engine co dien.

Muc tieu cua du an khong phai la xay dung mot engine thi dau cap cao nhu Rapfi hoac Yixin. Du an tap trung minh hoa cach ket hop cac ky thuat classical AI voi threat knowledge cua Gomoku de tao mot bot co kha nang choi thuc te va de giai thich.

---

## 2. Kien Truc He Thong

### 2.1. Tong quan

He thong gom ba phan chinh:

```text
Frontend React/Vite
  -> Backend FastAPI
      -> GomokuAI classical engine
      -> Consultant CNN advisor

Frontend React/Vite
  -> Arena FastAPI service
      -> Self-play engine
      -> JSONL data generation
```

### 2.2. Cac thanh phan trong repository

| Thanh phan | Vai tro |
|---|---|
| `frontend/src/App.jsx` | UI chinh, play mode, arena mode, consultant advisor toggle |
| `frontend/src/components/Board.jsx` | Render board 15x15 |
| `frontend/src/components/Square.jsx` | Render tung o, quan co va advisor badge |
| `backend/main.py` | FastAPI API cho che do nguoi choi voi AI |
| `backend/ai_core.py` | Search orchestration, minimax, alpha-beta, iterative deepening, TT |
| `backend/ai_types.py` | Constants, dataclass config va result |
| `backend/board_rules.py` | Luat board co ban, winner check, normalize board |
| `backend/threats.py` | Threat detection theo pattern |
| `backend/evaluator.py` | Heuristic evaluator |
| `backend/move_ordering.py` | Candidate generation, tactical score, policy prior ordering |
| `arena/` | Self-play engine va arena service |
| `dl/model.py` | CNN policy-value model |
| `dl/predict_policy.py` | Inference wrapper cho consultant model |
| `model/` | Checkpoint va metrics model da train |
| `tests/` | Unit tests va tactical regression |

### 2.3. Luong nguoi choi voi AI

```text
Nguoi choi click mot o
-> Frontend dat quan -1
-> Frontend goi POST /api/get-move
-> Backend validate board va difficulty
-> GomokuAI.get_move_analysis()
-> Backend tra row, col, evaluation, reason, completed_depth
-> Frontend dat quan AI 1 va hien ly do nuoc di
```

Endpoint chinh:

```http
GET /api/health
POST /api/get-move
POST /api/get-consultation
POST /api/report-game-result
```

Response mau cua `/api/get-move`:

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

---

## 3. AI Classical Engine

### 3.1. Tong quan thuat toan

Engine chinh la `GomokuAI`. Day la mot classical game engine, khong phai reinforcement learning. Cac thanh phan quan trong:

| Thanh phan | Vai tro |
|---|---|
| Minimax | Mo phong hai ben di toi uu trong game doi khang |
| Alpha-beta pruning | Cat nhanh cac nhanh khong can xet |
| Iterative deepening | Search tang dan depth trong gioi han thoi gian |
| Candidate generation | Chi xet cac o gan quan da danh |
| Move ordering | Uu tien tactical moves truoc de alpha-beta cat tot hon |
| Threat detection | Nhan dien five, open-four, closed-four, open-three, broken-three |
| Pattern evaluator | Cham diem board theo attack va defense |
| Immediate win/block | Xu ly thang ngay va chan thang truoc search sau |
| Zobrist hashing | Ma hoa board thanh hash 64-bit |
| Transposition table | Cache ket qua search da tinh |
| Loss memory | Ghi nho cac nuoc AI nam trong van thua |
| Policy prior hybrid | Dung CNN de ho tro sap xep candidate o root |

### 3.2. Minimax va alpha-beta pruning

Minimax danh gia game doi khang bang cach gia dinh AI toi da hoa diem, con doi thu toi thieu hoa diem cua AI. Tuy nhien, Gomoku 15x15 co branching factor qua lon. Alpha-beta pruning duoc dung de loai bo cac nhanh chac chan khong lam thay doi ket qua tot nhat.

Trong code:

- Root search nam o `GomokuAI._search_root()`.
- Recursive search nam o `GomokuAI._minimax()`.
- Gia tri terminal win/loss duoc dat rat cao de uu tien ket qua thang/thua hon heuristic thong thuong.

### 3.3. Iterative deepening va time limit

AI khong search mot lan o depth cao ngay lap tuc. Thay vao do, engine search tu depth 1 den depth toi da. Neu het gio, AI van co best move tu depth truoc.

Difficulty hien tai:

| Difficulty | Depth | Candidate radius | Candidate limit | Time limit | Policy prior |
|---|---:|---:|---:|---:|---:|
| Easy | 2 | 2 | 8 | 400 ms | 0 |
| Medium | 3 | 2 | 10 | 1200 ms | 10,000 |
| Hard | 4 | 3 | 12 | 2200 ms | 20,000 |

Easy khong dung CNN policy prior de giu toc do nhanh va tranh dependency ML trong mode don gian. Medium/Hard dung model nhu tin hieu sap xep candidate, nhung alpha-beta van la thanh phan quyet dinh cuoi.

### 3.4. Candidate generation

Thay vi xet tat ca o trong, engine chi sinh candidate quanh cac quan da co tren board. Ban dau, neu board trong, AI chon trung tam. Khi board da co quan, engine lay cac o trong trong ban kinh cau hinh quanh nhung quan da danh.

Loi ich:

- Giam branching factor tu hang tram nuoc con xuong mot tap nho.
- Tap trung vao khu vuc co kha nang tao threat.
- Giup search sau hon trong gioi han thoi gian.

Can than: candidate pruning co the lam mat nuoc quan trong neu qua manh. Vi vay engine luon giu forcing candidates va tactical candidates quan trong, khong de candidate limit loai bo cac nuoc khan cap.

### 3.5. Move ordering

Move ordering sap xep candidate truoc khi alpha-beta search. Nuoc tot duoc xet truoc giup alpha-beta cat nhanh hon. Score cua mot candidate gom:

1. AI win ngay.
2. Human win ngay can chan.
3. AI threat: open-four, closed-four, open-three, broken-three, double-threat.
4. Human threat can phong thu.
5. Local shape score.
6. Center bias.
7. Policy prior bonus tu CNN neu config bat.

Logic nam trong `backend/move_ordering.py`.

### 3.6. Threat detection

ThreatDetector nhan dien cac mau quan co y nghia chien thuat:

| Threat | Mo ta |
|---|---|
| Five | 5 quan lien tiep, thang game |
| Open-four | 4 quan lien tiep co hai dau mo |
| Closed-four | 4 quan co mot dau mo hoac threat four khan cap |
| Open-three | 3 quan co hai dau mo, co the phat trien thanh open-four |
| Broken-three | 3 quan co khoang trong, van co kha nang tao threat |
| Double-threat | Nhieu threat dong thoi, doi thu kho chan het |

Threat detection duoc dung o ba noi:

- Move ordering.
- Board evaluation.
- Reason classification.

### 3.7. Pattern-based evaluator

Evaluator cham diem board theo cong thuc:

```text
Score = AttackScore - DefenseScore
```

Trong do:

- `AttackScore`: threat va pattern co loi cho AI.
- `DefenseScore`: threat nguy hiem cua doi thu.

Evaluator la heuristic, khong phai oracle. No giup minimax danh gia leaf node khi search chua the di den trang thai thang/thua.

### 3.8. Immediate win/block

Truoc khi vao search sau, engine kiem tra:

1. AI co nuoc thang ngay khong.
2. Doi thu co nuoc thang ngay can chan khong.
3. Co double-threat khan cap can tao/chan khong.
4. Co forcing line ngan co the khai thac khong.

Day la tang bao ve quan trong. Ngay ca khi model CNN hoac heuristic chua tot, engine van khong nen bo qua cac nuoc thang/chan thang ro rang.

### 3.9. Transposition table va Zobrist hash

Zobrist hashing ma hoa board thanh hash 64-bit. Transposition table luu:

```text
depth, score, flag, best_move
```

Trong do `flag` co the la:

- `EXACT`
- `LOWERBOUND`
- `UPPERBOUND`

Hash co them side-to-move de tranh nham lan cung board nhung khac luot di. Best move trong cache duoc dung de uu tien lai candidate khi gap cung state hoac state tuong tu.

Can nhan manh: transposition table khong phai solver. No chi cache ket qua search da tinh, giup giam tinh lap va cai thien ordering. De chung minh thang/thua trong Gomoku can cac ky thuat manh hon nhu full Threat Space Search, VCF solver hoac proof-number search.

### 3.10. Loss memory

Loss memory ghi lai cac nuoc AI da di trong nhung van nguoi choi thang. Khi gap lai board tuong ung, engine tru penalty cho nuoc do, tu do tranh lap lai sai lam cu neu con lua chon hop le.

Co che nay khong phai reinforcement learning. No la memory-based avoidance don gian:

```text
board hash truoc nuoc AI
-> move AI da chon
-> so lan nam trong van thua
-> penalty khi gap lai
```

Frontend gui ket qua game ve backend qua `/api/report-game-result`. Backend ghi loss memory va luu cache.

---

## 4. Consultant CNN Advisor

### 4.1. Ly do them model

Classical engine co kha nang suy luan qua search, nhung heuristic va move ordering van co han che. Model CNN duoc them nhu mot thanh phan supervised learning de:

1. Hoc pattern nuoc di tu self-play data.
2. Dua ra top-K goi y nhanh cho nguoi choi.
3. Tao them mot policy prior de ho tro move ordering cua AI chinh.

Model khong thay the minimax. No khong phai reinforcement learning va khong phai AlphaZero-style training. Model duoc train supervised tu du lieu JSONL.

### 4.2. Du lieu train

Du lieu nam trong `data/` va `data/additional/`.

Thong ke da doc:

| Nguon | So file | So sample | Dung luong |
|---|---:|---:|---:|
| `data/` | 79 | 945,506 | ~1.64 GB |
| `data/additional/` | 70 | 836,244 | ~1.49 GB |
| Tong | 149 | 1,781,750 | ~3.14 GB |

Schema JSONL:

```json
{
  "board": [[0, 0, 0]],
  "prob": [225 values],
  "reward": 1
}
```

Trong phan lon sample, `prob` la one-hot vector dai 225. Nuoc label duoc lay bang:

```python
idx = argmax(prob)
row = idx // 15
col = idx % 15
```

Cac dong `prob` toan 0 thuong di kem `reward = 0`, duoc bo qua khi train policy.

### 4.3. Input representation

Board duoc ma hoa thanh tensor 3 kenh:

```text
Channel 0: quan cua player dang can du doan
Channel 1: quan doi thu
Channel 2: o trong
```

Shape:

```text
(3, 15, 15)
```

Khi inference cho player `-1`, board duoc normalize:

```python
normalized_board = board * player
```

Nhu vay, voi model, ben dang di luon la `1`.

### 4.4. Kien truc model

Model la CNN nho, du chay nhanh tren CPU:

```text
Input 3x15x15
-> ConvBlock 3 -> 64
-> ConvBlock 64 -> 64
-> ConvBlock 64 -> 128
-> ConvBlock 128 -> 128
-> Policy head: 225 logits
-> Value head: scalar tanh [-1, 1]
```

Policy head du doan diem cho 225 o. Value head du doan gia tri board trong khoang `[-1, 1]`.

### 4.5. Loss function

Training dung loss ket hop:

```text
total_loss = policy_cross_entropy + 0.25 * value_mse
```

Trong do:

- Policy loss hoc one-hot move label tu `prob`.
- Value loss hoc reward/value target tu `reward`.

### 4.6. Evaluation metrics

Model duoc danh gia bang:

| Metric | Y nghia |
|---|---|
| Top-1 accuracy | Nuoc top-1 cua model trung voi label self-play |
| Top-3 accuracy | Label nam trong 3 nuoc goi y dau |
| Top-5 accuracy | Label nam trong 5 nuoc goi y dau |
| Illegal Top-1 | Ty le top-1 nam tren o da co quan sau khi mask |
| Value MAE | Sai so tuyet doi trung binh cua value head |
| Latency | Thoi gian inference |

Quan trong: Top-1 trong report duoc hieu la **agreement with self-play engine label**, khong phai "best move accuracy" tuyet doi. Gomoku co nhieu vi tri co nhieu nuoc hop ly, nen Top-3 va Top-5 cung rat quan trong.

### 4.7. Ket qua model

Training config:

| Tham so | Gia tri |
|---|---:|
| Train samples moi epoch | 200,000 |
| Eval samples | 50,000 |
| Epochs | 20 |
| Batch size | 256 |
| Learning rate | 0.001 |
| Device train | CUDA |
| Best validation epoch | 19 |
| Best validation Top-1 | 0.40372 |

Test result:

| Model | Top-1 | Top-3 | Top-5 | Illegal Top-1 | Value MAE | Mean Latency ms |
|---|---:|---:|---:|---:|---:|---:|
| Random legal | 0.0059 | 0.0171 | 0.0281 | 0.0000 | - | - |
| Center-first | 0.0235 | 0.0478 | 0.0641 | 0.0000 | - | - |
| Consultant CNN | 0.4024 | 0.5997 | 0.6919 | 0.0000 | 0.7256 | 0.98 |

Nhan xet:

- Policy head hoc duoc pattern nuoc di tot hon baseline rat nhieu.
- Top-3 gan 60% cho thay model phu hop voi vai tro advisor.
- Value head con yeu, vi `Value MAE = 0.7256`. Do do report chi nen xem value la thong tin phu.
- `illegal_top1_rate_before_mask = 0.65078`, nghia la raw logits hay uu tien o da co quan. Vi vay inference bat buoc phai legal-mask. Sau mask, illegal top-1 bang 0.

### 4.8. Latency

Do tren local CPU sau khi tich hop:

| Phep do | Ket qua |
|---|---:|
| First model load | ~101.4 ms |
| Model inference mean | ~1.334 ms |
| Model inference p95 | ~1.652 ms |
| Direct FastAPI handler mean | ~2.285 ms |
| Direct FastAPI handler p95 | ~2.632 ms |

Do do model du nhanh cho advisor overlay va policy prior. Backend warm model khi startup de tranh delay o request dau tien.

---

## 5. Hybrid Policy Prior Cho AI Chinh

### 5.1. Van de

Model CNN co Top-1 40.24%, nen khong du tin cay de thay the engine chinh. Tuy nhien, model co the cung cap mot policy prior: mot tin hieu ve nhung o co kha nang la nuoc tot. Alpha-beta can move ordering tot de prune hieu qua. Vi vay, cach tich hop an toan la dung model de sap xep candidate, khong dung model de quyet dinh cuoi.

### 5.2. Nguyen tac an toan

Hybrid duoc thiet ke theo cac nguyen tac:

1. CNN khong duoc thay minimax.
2. CNN khong duoc bo qua immediate win/block.
3. CNN khong duoc loai candidate bang pruning cung.
4. CNN chi cong bonus nho vao root candidate ordering.
5. Node minimax ben duoi van dung classical ordering.
6. Neu model khong load duoc, engine quay ve classical mode.

### 5.3. Pipeline hybrid

```text
Input board
-> Classical candidate generation
-> Immediate win/block/double-threat/forcing checks
-> Neu chua co nuoc tactical bat buoc:
     -> CNN predict top-K legal moves
     -> Cong policy prior bonus vao candidate score
     -> Sap xep root candidates
-> Alpha-beta search quyet dinh nuoc cuoi
```

Policy prior bonus:

```text
bonus(move) = probability(move) * policy_prior_weight
```

Trong config hien tai:

| Difficulty | policy_prior_weight | policy_prior_top_k |
|---|---:|---:|
| Easy | 0 | 24 |
| Medium | 10,000 | 24 |
| Hard | 20,000 | 32 |

### 5.4. Tai sao khong dung pruning cung?

Neu chi lay top-K cua CNN va bo cac candidate khac, AI co the mat nuoc chan thang hoac threat quan trong. Vi Top-1 cua model chi 40.24%, pruning cung la rui ro. Vi vay, model chi lam move ordering. Alpha-beta van co quyen danh gia tat ca candidate trong limit classical.

### 5.5. Ket qua smoke test hybrid

Sau khi sua, tactical case khong goi model truoc immediate checks:

| Case | Ket qua |
|---|---|
| Tactical forcing board | ~38-48 ms, reason `creating_open_four`, depth 0 |
| Non-tactical prewarmed hybrid | ~194-210 ms o cac lan sau, completed depth 2 |

Nhan xet:

- Model load khong con chen vao immediate tactical checks.
- Backend startup warm model de giam delay request dau.
- Hybrid giup AI co them tin hieu ordering, nhung chua co A/B benchmark du lon de claim AI manh hon ro rang.

Ket luan can than:

```text
CNN policy prior co tiem nang cai thien thu tu search cua alpha-beta.
No chua duoc chung minh la tang playing strength mot cach tong quat neu chua co A/B benchmark day du.
```

---

## 6. Arena Va Self-Play

Arena la che do AI vs AI, dung de:

1. Chay self-play games.
2. Replay van dau moi nhat tren frontend.
3. Sinh sample JSONL cho phan tich hoac training sau nay.

Arena API:

```http
GET /arena/api/health
POST /arena/api/self-play
```

Arena smoke test:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

Ket qua smoke gan nhat:

```json
{
  "games": 1,
  "samples": 6,
  "black_wins": 0,
  "white_wins": 0,
  "draws": 1
}
```

---

## 7. Thuc Nghiem Va Danh Gia

### 7.1. Benchmark design

Benchmark trong du an so sanh project AI voi cac baseline noi bo:

| Agent | Mo ta |
|---|---|
| `random_baseline` | Chon o trong ngau nhien voi seed co dinh |
| `center_first_baseline` | Chon trung tam hoac o trong gan trung tam |
| `greedy_1ply_baseline` | Thu tung nuoc va lay evaluation cao nhat |
| `basic_minimax_baseline` | Shallow minimax/alpha-beta baseline |
| `project_easy` | Engine du an difficulty easy |
| `project_medium` | Engine du an difficulty medium |
| `project_hard` | Engine du an difficulty hard |

Benchmark la internal benchmark, khong phai so sanh voi Rapfi, Yixin hay AlphaZero-Gomoku.

### 7.2. Accuracy theo tactical cases

Ket qua tu `benchmark_results.json`:

| Agent | Correct | Total | Accuracy |
|---|---:|---:|---:|
| random_baseline | 0 | 8 | 0.000 |
| center_first_baseline | 4 | 8 | 0.500 |
| greedy_1ply_baseline | 7 | 8 | 0.875 |
| basic_minimax_baseline | 8 | 8 | 1.000 |
| project_easy | 8 | 8 | 1.000 |
| project_medium | 8 | 8 | 1.000 |
| project_hard | 8 | 8 | 1.000 |

### 7.3. Mot so case tieu bieu

| Case | Project move | Reason | Completed depth | Nhan xet |
|---|---|---|---:|---|
| opening | `[7, 7]` | `opening_center` | 0 | Chon trung tam khi board trong |
| ai_win_horizontal | `[7, 9]` | `winning_move` | 0 | Thang ngay |
| block_open_four | `[7, 9]` | `blocking_win` | 0 | Chan doi thu thang |
| block_broken_four | `[7, 7]` | `blocking_win` | 0 | Chan broken-four |
| forcing_open_four | `[6, 4]` | `creating_open_four` | 0 | Tao open-four bat buoc |
| create_double_three | `[7, 7]` | `creating_double_threat` | 0 | Tao double-threat |
| block_double_three | `[7, 7]` | `blocking_double_threat` | 0 | Chan double-threat |
| diagonal_win | `[8, 8]` | `winning_move` | 0 | Thang theo duong cheo |

### 7.4. Midgame benchmark

Trong case midgame, khong co expected move duy nhat. Benchmark dung de xem latency, depth va reason:

| Agent | Move | Reason | Completed depth | Time ms |
|---|---|---|---:|---:|
| project_easy | `[6, 6]` | `building_attack` | 2 | 158.61 |
| project_medium | `[6, 6]` | `building_attack` | 2 | 1211.72 |
| project_hard | `[6, 6]` | `building_attack` | 2 | 2211.69 |

Medium va Hard dung time limit cao hon, nen thoi gian gan sat gioi han. Dieu nay phu hop voi iterative deepening trong che do tuong tac: AI co gang search sau hon nhung van bi gioi han thoi gian.

### 7.5. Test va verification

Sau khi tich hop consultant model va hybrid policy prior, cac lenh verification da chay:

```powershell
.\backend\venv\Scripts\python.exe -m unittest tests.test_policy_prior_ordering tests.test_tactical_cases tests.test_consultant_api -v
```

Ket qua:

```text
Ran 8 tests
OK
```

Syntax check:

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py dl\model.py dl\predict_policy.py
```

Ket qua: pass.

Arena smoke:

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

Ket qua: pass.

---

## 8. So Sanh Dinh Tinh Voi Cac Huong AI Gomoku Khac

### 8.1. Basic minimax

Basic minimax de cai dat va de hieu, nhung khong phu hop voi Gomoku 15x15 neu khong co pruning va candidate selection. Branching factor qua lon lam search nhanh chong vuot qua gioi han thoi gian.

Du an cai thien basic minimax bang:

- Candidate generation quanh quan da co.
- Alpha-beta pruning.
- Move ordering threat-aware.
- Immediate win/block.
- Transposition table.
- Iterative deepening va time limit.

### 8.2. Rapfi va Yixin

Rapfi va Yixin la cac engine Gomoku/Renju manh, co nhieu toi uu sau va duoc thiet ke cho thi dau. Du an nay khong claim manh hon cac engine do. Diem khac biet cua du an la tinh hoc thuat va minh hoa:

- Tach ro cac thanh phan search, evaluator, threat detection.
- Co API va UI de demo.
- Co benchmark noi bo va test tactical.
- Co supervised consultant model lam advisor va policy prior.

### 8.3. AlphaZero-Gomoku

AlphaZero-style Gomoku dung self-play reinforcement learning, neural network va MCTS. Huong nay can nhieu tai nguyen training va pipeline phuc tap hon. Du an hien tai khong dung RL. CNN trong du an la supervised model hoc lai label tu self-play data, khong phai AlphaZero.

### 8.4. Vi tri cua du an

Du an nam giua hai huong:

```text
Classical search engine
  + Gomoku threat knowledge
  + supervised policy advisor
  + hybrid move ordering
```

No khong phai engine SOTA, nhung co day du thanh phan de minh hoa mot AI Gomoku co kha nang suy luan, co giai thich va co du lieu thuc nghiem.

---

## 9. Cai Dat Va Huong Dan Chay

### 9.1. Backend classical

```powershell
cd backend
.\start_backend.ps1
```

Hoac:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

Backend mac dinh:

```text
http://127.0.0.1:8000
```

### 9.2. Backend voi consultant model

De dung CNN advisor va hybrid policy prior:

```powershell
.\backend\venv\Scripts\python.exe -m pip install -r backend\requirements-ml.txt
```

Checkpoint mac dinh:

```text
model/consultant_model.pt
```

Neu muon override path:

```powershell
$env:GOMOKU_CONSULTANT_MODEL_PATH="D:\path\to\consultant_model.pt"
```

### 9.3. Frontend

```powershell
cd frontend
npm install
npm.cmd run dev
```

Frontend mac dinh:

```text
http://127.0.0.1:5173
```

### 9.4. Arena

```powershell
.\arena\start_arena.ps1
```

Arena mac dinh:

```text
http://127.0.0.1:8100
```

---

## 10. Kho Khan Va Cach Xu Ly

| Kho khan | Cach xu ly |
|---|---|
| Branching factor lon | Candidate generation va candidate limit |
| Search cham | Alpha-beta pruning, move ordering, iterative deepening |
| AI bo qua nuoc thang/chan thang | Immediate win/block truoc search |
| Threat Gomoku phuc tap | ThreatDetector va tactical regression tests |
| Evaluator khong phai oracle | Ket hop evaluator voi minimax va threat checks |
| Cache co the nham state | Zobrist hash co side-to-move |
| Model CNN co raw illegal top-1 cao | Legal mask bat buoc trong inference |
| Model chua du tin cay de thay engine | Chi dung lam advisor va policy prior |
| Request dau load model cham | Warm consultant model luc FastAPI startup |
| Dependency ML nang | Tach `requirements-ml.txt` rieng voi backend co ban |

---

## 11. Han Che

Du an da cai thien dang ke so voi minimax don gian, nhung van co nhieu han che:

1. Benchmark tactical con nho, moi co 8 case accuracy chinh.
2. Chua co A/B benchmark lon de chung minh hybrid policy prior tang playing strength tong quat.
3. Threat detection van la pattern-based, co the sai o cac the phuc tap.
4. Chua co full Threat Space Search hoac VCF solver.
5. Value head cua CNN con yeu, khong nen dung thay evaluator.
6. Chua so sanh truc tiep voi engine ngoai nhu Rapfi/Yixin.
7. Search bi gioi han boi time limit va candidate pruning.
8. Loss memory chi tranh lai mot so nuoc thua cu the, khong phai hoc chien luoc tong quat.

---

## 12. Huong Phat Trien

Huong phat trien hop ly:

1. Mo rong tactical benchmark len nhieu board hon, gom broken-four, diagonal, double-threat phuc tap.
2. Viet A/B benchmark `classical vs hybrid policy prior`.
3. Do self-play win rate giua AI cu va AI hybrid.
4. Cai thien evaluator cho broken-four, open-three va double-threat.
5. Them VCF-lite hoac Threat Space Search toi gian.
6. Luu best move va policy prior statistics de phan tich search.
7. Cai thien CNN bang legal-mask-aware training hoac them channel legality.
8. Train model voi nhieu sample hon va tach split theo game neu co game id.
9. So sanh voi engine ngoai neu co pipeline match hop ly.
10. Toi uu latency khi deploy tren CPU server.

---

## 13. Ket Luan

Du an da xay dung mot he thong Gomoku/Caro 15x15 full-stack co AI theo huong classical search. Engine chinh ket hop minimax, alpha-beta pruning, iterative deepening, candidate generation, move ordering, threat detection, pattern evaluator, immediate win/block, Zobrist hashing, transposition table va loss memory.

Ket qua benchmark noi bo cho thay project AI dat 8/8 tren cac tactical cases hien tai, xu ly duoc cac tinh huong quan trong nhu thang ngay, chan thang, chan broken-four, tao open-four, tao/chan double-threat va thang duong cheo. Cac difficulty Easy/Medium/Hard deu co the tra ve reason va completed depth, giup AI de giai thich hon so voi black-box model.

Ben canh classical engine, du an da huan luyen mot supervised CNN consultant model tu self-play data. Model dat Top-1 agreement 40.24%, Top-3 59.97%, Top-5 69.19% tren held-out test samples, voi latency inference rat thap. Model duoc tich hop lam advisor overlay va policy prior cho move ordering, nhung khong thay the alpha-beta. Cach tich hop nay giu duoc su an toan chien thuat: immediate win/block van di truoc, model chi ho tro sap xep candidate khi can search sau.

Noi cach khac, dong gop chinh cua du an la mot AI Gomoku co kha nang suy luan bang search, co tri thuc threat-specific, co benchmark/test de danh gia, va co mo rong supervised learning dung dung muc. Du an chua phai engine Gomoku hoan chinh cap thi dau, nhung da dat muc tieu cua mot bai tap lon AI: co thuat toan ro rang, co cai tien ky thuat, co thuc nghiem, co giai thich va co huong phat trien tiep theo.
