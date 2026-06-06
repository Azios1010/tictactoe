# Ke Hoach Slide Thuyet Trinh Gomoku/Caro 15x15 AI

Muc tieu: tao bai thuyet trinh 15 phut co cau chuyen ro rang:

1. Bai toan Gomoku 15x15 co khong gian tim kiem lon.
2. Thuat toan chinh la classical search engine co the giai thich.
3. CNN consultant model la phan mo rong hoc giam sat, dung lam advisor va policy prior.
4. Ket qua duoc danh gia bang benchmark tactical, metric model va A/B benchmark.
5. Ket luan trung thuc: AI da cai thien ve pipeline va kha nang giai thich, nhung chua claim SOTA hay manh hon Rapfi/Yixin.

Tong thoi luong de xuat: 15 phut trinh bay + Q&A.

## Phan Cong Noi

| Nguoi | Thoi luong | Slide chinh | Vai tro |
|---|---:|---|---|
| Nguoi mo dau/report | 2.5 phut | 1, 2, 13 | Bai toan, muc tieu, ket luan |
| Thanh vien A | 4 phut | 3, 4, 5 | AI core, threat detection, search |
| Thanh vien B | 4 phut | 6, 7, 8 | Data, Kaggle training, CNN consultant |
| Thanh vien C | 4.5 phut | 9, 10, 11, 12 | Benchmark, A/B, system, demo |

## Thong Diep Chinh Can Giu

- Project khong phai tic-tac-toe 3x3; day la Gomoku/Caro 15x15.
- AI chinh van la classical engine: minimax, alpha-beta, iterative deepening, heuristic evaluator, threat detection.
- CNN model khong tu thay AI chinh; model chi goi y top moves va them policy prior cho move ordering.
- Model co ket qua tot hon baseline, nhung top-1 40.244% chua du de claim model tu choi toi uu.
- A/B benchmark cho thay hybrid khong pha tactical rules, nhung chua co bang chung latency/playing strength tang ro ret.
- Khong claim SOTA, khong claim manh hon Rapfi/Yixin, khong claim full TSS/VCF solver.

## Slide 1: Tieu De Va Mo Ta Ngan

**Tieu de:** Gomoku/Caro 15x15 AI

**Noi dung tren slide:**

- Game doi khang tren board 15x15.
- AI chinh: classical game search.
- Mo rong: supervised CNN consultant model.
- Tech stack: React/Vite, FastAPI, Python AI core, Kaggle training.
- GitHub: `https://github.com/Azios1010/tictactoe`.
- Demo: `[dien link Vercel/Render neu co]`.

**Loi noi goi y:**

> Nhom em xay dung he thong choi Gomoku/Caro 15x15. Diem chinh cua du an la engine AI co the giai thich bang reason, evaluation va completed_depth. Sau do nhom mo rong them CNN consultant model de goi y nuoc di va ho tro sap xep candidate.

**Minh chung can co:** anh man hinh app, QR/link GitHub.

## Slide 2: Bai Toan Va Thach Thuc

**Noi dung tren slide:**

- Muc tieu: dat 5 quan lien tiep tren hang/doc/cheo.
- Board 15x15 co toi da 225 o trong luc dau game.
- Minimax thuong gap branching factor rat lon.
- AI can vua danh hop ly, vua phan hoi nhanh.
- Can giai thich duoc quyet dinh, khong chi tra ve move.

**Quy uoc board:**

| Gia tri | Y nghia |
|---:|---|
| `0` | O trong |
| `1` | AI/O/black |
| `-1` | Nguoi choi/X/white |

**Loi noi goi y:**

> Neu xet het tat ca o trong, search tree tang theo ham mu. Vi vay, bai toan khong nam o viec viet minimax don gian, ma nam o viec giam nhanh, sap xep nuoc di va dua tri thuc Gomoku vao evaluator.

## Slide 3: Kien Truc He Thong

**Noi dung tren slide:**

```text
React/Vite Frontend
  -> POST /api/get-move
  -> FastAPI Backend
      -> GomokuAI classical engine
      -> Consultant CNN advisor

React/Vite Frontend
  -> Arena service
      -> Self-play JSONL data
```

**Thanh phan chinh:**

| File/thu muc | Vai tro |
|---|---|
| `backend/ai_core.py` | Search orchestration |
| `backend/threats.py` | Threat detection |
| `backend/evaluator.py` | Heuristic evaluation |
| `backend/move_ordering.py` | Candidate + ordering + policy prior |
| `dl/model.py` | CNN policy-value network |
| `dl/predict_policy.py` | Inference wrapper |
| `arena/` | Self-play va data generation |

**Loi noi goi y:**

> Frontend chi hien thi va gui board. Backend validate request, chon difficulty, goi AI core va tra ve row, col, reason, evaluation, completed_depth. Consultant model la module phu, khong thay the engine chinh.

## Slide 4: AI Core Pipeline

**Noi dung tren slide:**

```text
Board
-> Validate / normalize
-> Immediate win
-> Immediate block
-> Double-threat / forcing checks
-> Candidate generation
-> Move ordering
-> Iterative deepening
-> Minimax + alpha-beta
-> Evaluator + threat detection
-> MoveAnalysis
```

**Y can nhan manh:**

- Tactical rules chay truoc search sau.
- Search chi xet candidate gan vung da co quan.
- MoveAnalysis giup giai thich vi sao AI di nuoc do.

**Loi noi goi y:**

> Engine khong dua tat ca o trong vao minimax. Truoc tien AI xu ly nhung nuoc bat buoc nhu thang ngay va chan thang. Neu khong co nuoc bat buoc, AI moi search tren danh sach candidate da duoc sap xep.

## Slide 5: Co So Ly Thuyet Classical AI

**Noi dung tren slide:**

| Thanh phan | Vai tro |
|---|---|
| Minimax | Gia lap hai ben toi uu |
| Alpha-beta pruning | Cat cac nhanh khong can xet |
| Iterative deepening | Tim sau dan trong time limit |
| Candidate pruning | Giam branching factor |
| Move ordering | Dua nuoc co kha nang tot len truoc |
| Zobrist hash + TT | Cache trang thai search |
| Threat extension | Mo rong search cho mot so forcing moves |

**Difficulty:**

| Difficulty | Depth | Candidate limit | Time limit | Policy prior |
|---|---:|---:|---:|---|
| Easy | 2 | 8 | 400 ms | Off |
| Medium | 3 | 10 | 1200 ms | On |
| Hard | 4 | 12 | 2200 ms | On |

**Loi noi goi y:**

> Easy uu tien toc do, Medium can bang cho demo, Hard tim sau hon. Medium va Hard co them policy prior tu model, nhung Easy giu classical thu gon de phan hoi nhanh.

## Slide 6: Threat Detection Va Reason

**Noi dung tren slide:**

| Reason | Y nghia |
|---|---|
| `opening_center` | Khai cuoc trung tam |
| `winning_move` | AI thang ngay |
| `blocking_win` | Chan doi thu thang ngay |
| `creating_open_four` | Tao open-four |
| `creating_double_threat` | Tao nhieu threat dong thoi |
| `blocking_double_threat` | Chan double-threat |
| `best_search_score` | Nuoc tot nhat theo search |

**Loi noi goi y:**

> Reason la diem khac biet quan trong trong demo. Nguoi xem khong chi biet AI di o dau, ma con biet AI dang thang ngay, dang chan doi thu, hay dang xay attack theo evaluator.

**Demo goi y:** chuan bi board co 4 quan lien tiep de AI tra `winning_move` hoac `blocking_win`.

## Slide 7: Data Va Kaggle Training

**Noi dung tren slide:**

- Data sinh tu arena/self-play, luu JSONL.
- Moi sample gom board, policy target/prob va reward/outcome.
- Chia file-level split de giam data leakage.
- Notebook Kaggle train supervised policy-value model.

**Thong ke data:**

| Nguon | So file | So sample |
|---|---:|---:|
| `data/` | 79 | 945,506 |
| `data/additional/` | 70 | 836,244 |
| Tong | 149 | 1,781,750 |

**Loi noi goi y:**

> Phan learning cua nhom khong phai reinforcement learning. Model duoc train supervised tu data JSONL. Muc tieu la hoc xu huong nuoc di de lam advisor va prior, khong phai tu thay the minimax.

## Slide 8: CNN Consultant Model

**Noi dung tren slide:**

```text
Board 15x15
-> Encode 3 channels
-> CNN backbone
-> Policy head: 225 logits
-> Value head: scalar value
-> Legal mask
-> Top-k suggested moves
```

**Ket qua test:**

| Metric | Ket qua |
|---|---:|
| Test samples | 50,000 |
| Top-1 accuracy | 40.244% |
| Top-3 accuracy | 59.974% |
| Top-5 accuracy | 69.194% |
| Illegal top-1 after mask | 0.000% |
| Value MAE | 0.725577 |

**Loi noi goi y:**

> Top-1 40% nghe chua tuyet doi, nhung tot hon rat nhieu so voi random legal va center-first. Diem quan trong la legal mask dam bao model khong goi y o da co quan.

## Slide 9: Hybrid Policy Prior

**Noi dung tren slide:**

**Cach tich hop:**

1. Classical engine sinh candidate.
2. Engine kiem tra immediate win/block truoc.
3. Neu khong co tactical move bat buoc, goi model lay top-k.
4. Xac suat model duoc doi thanh bonus ordering.
5. Alpha-beta search van quyet dinh cuoi cung.

**Vi sao khong cho model tu danh?**

- Top-1 chua du cao de tin tuyet doi.
- Gomoku co nhieu the bat buoc chi sai 1 nuoc la thua.
- Model co the hoc lech tu self-play data.
- Prior chi sap xep, khong hard-prune, nen an toan hon.

**Loi noi goi y:**

> Day la phan cai tien quan trong nhat ve thiet ke. Nhom khong thay engine bang model, ma dung model nhu mot la ban do uu tien cho search. Neu model sai, search va tactical rules van con co hoi sua.

## Slide 10: Benchmark Model Va Baseline

**Noi dung tren slide:**

| Phuong phap | Top-1 | Top-3 | Top-5 |
|---|---:|---:|---:|
| Random legal | 0.585% | 1.714% | 2.814% |
| Center-first | 2.352% | 4.778% | 6.412% |
| CNN consultant | 40.244% | 59.974% | 69.194% |

**Tactical diagnostics:**

| Case | Top-1 hit | Top-3 hit |
|---|---|---|
| AI win horizontal | Co | Co |
| Block human horizontal | Co | Co |

**Loi noi goi y:**

> Bang nay cho thay model hoc duoc distribution tu data, nhung bang nay khong dong nghia voi AI manh hon engine thi dau. No chi chung minh model co gia tri lam advisor va prior.

## Slide 11: A/B Benchmark Classical vs Hybrid

**Noi dung tren slide:**

Dieu kien: cung Medium config, cung depth/candidate/time limit; model warm-up truoc khi do.

| Case | Classical | Hybrid | Nhan xet |
|---|---|---|---|
| Opening center | [7,7], 0.08 ms | [7,7], 0.07 ms | Giu dung opening |
| AI win horizontal | winning_move, 12.88 ms | winning_move, 12.32 ms | Khong pha tactical |
| Block human horizontal | blocking_win, 12.61 ms | blocking_win, 9.65 ms | Khong pha block |
| Two-stones opening | depth 2, 1247.50 ms | depth 2, 1258.07 ms | Khac move, cung score |
| Scattered midgame | depth 2, 1279.52 ms | depth 2, 1282.87 ms | Tuong duong |
| Quiet midgame | depth 1, 1327.47 ms | depth 1, 1333.40 ms | Tuong duong |

**Ket luan tren slide:**

- Hybrid policy prior an toan voi tactical rules.
- Chua thay latency giam ro trong benchmark nho.
- Can mo rong A/B self-play de ket luan ve playing strength.

**Loi noi goi y:**

> Day la phan chung minh nhom danh gia trung thuc. Model co tac dung ve mat ordering/advisor, nhung benchmark hien tai chua du de noi no lam AI manh hon ro ret trong moi tinh huong.

## Slide 12: Cai Dat, Kiem Thu Va Demo

**Noi dung tren slide:**

**API:**

| Endpoint | Vai tro |
|---|---|
| `GET /api/health` | Check backend |
| `POST /api/get-move` | AI chon nuoc |
| `POST /api/get-consultation` | Model goi y top-k |
| `POST /arena/api/self-play` | Arena self-play |

**Verification da co:**

| Hang muc | Ket qua |
|---|---|
| Python compile backend/arena/dl | PASS |
| `tests.test_policy_prior_ordering` | PASS |
| `tests.test_tactical_cases` | PASS |
| `tests.test_consultant_api` | PASS |
| Arena smoke test | PASS |

**Demo flow:**

1. Mo app.
2. Choi mot nuoc Medium.
3. Bat consultant advisor de xem top-k moves.
4. Chi vao reason/evaluation/completed_depth.
5. Neu co thoi gian, chay arena self-play.

## Slide 13: Ket Luan Va Huong Phat Trien

**Ket luan:**

- Da xay dung full-stack Gomoku/Caro 15x15.
- AI chinh la classical search engine co the giai thich.
- Threat detection va immediate win/block giup tranh loi tactical mot nuoc.
- CNN consultant model hoc duoc policy tot hon baseline.
- Hybrid policy prior duoc tich hop than trong: ho tro ordering, khong thay the search.
- A/B benchmark cuc bo cho thay hybrid khong pha tactical, nhung chua chung minh manh hon ro ret.

**Han che:**

- Chua phai engine Gomoku cap thi dau.
- Chua so sanh truc tiep voi Rapfi/Yixin.
- Chua co full Threat Space Search/VCF solver.
- Model top-1 chua du cao de tu quyet dinh.
- A/B benchmark con nho, chua phai self-play tournament.

**Huong phat trien:**

- Mo rong A/B benchmark thanh nhieu van self-play.
- Them tactical suite cho broken-four, double-threat phuc tap.
- Cai thien evaluator va threat detector.
- Luu best move trong transposition table.
- Nghien cuu VCF-lite/TSS-lite.
- Nang chat luong data va model neu muon tang vai tro neural advisor.

## Slide 14 Neu Can: Backup Demo / Appendix

Dung khi giang vien hoi sau hon hoac can backup luc demo online cham.

**Noi dung nen co:**

- Anh UI Play vs AI.
- Anh consultant advisor hien top-k.
- Anh Swagger docs.
- Bang metrics model day du.
- Bang A/B benchmark day du.
- Lenh chay backend/frontend/arena.

## Checklist Tao Slide

- [ ] Slide co link GitHub.
- [ ] Slide co link demo neu co.
- [ ] Slide co architecture Frontend -> Backend -> AI core/model.
- [ ] Slide co AI core pipeline.
- [ ] Slide co threat detection va reason.
- [ ] Slide co data + Kaggle training.
- [ ] Slide co model metrics top-1/top-3/top-5.
- [ ] Slide co A/B benchmark classical vs hybrid.
- [ ] Slide co verification/test results.
- [ ] Slide co han che trung thuc, khong claim qua muc.

## Checklist Truoc Ngay Thuyet Trinh

- [ ] Push commit moi nhat len GitHub.
- [ ] Dien link Vercel/Render neu dung demo online.
- [ ] Backend `/api/health` tra OK.
- [ ] Arena `/arena/api/health` tra OK neu demo arena.
- [ ] Chay `npm.cmd run build` trong frontend.
- [ ] Chay Python compile check.
- [ ] Chay focused tests neu kip.
- [ ] Chuan bi anh/video backup cho demo.
- [ ] Tap noi sao cho Slide 11 khong bi noi qua: model ho tro, chua claim manh hon chac chan.

## Q&A Ngan

**Hoi: AI co dung machine learning khong?**

> Co, nhung khong phai la thanh phan quyet dinh duy nhat. AI chinh van la classical search engine. Model CNN duoc train supervised tu data self-play de lam consultant advisor va policy prior cho move ordering.

**Hoi: Day co phai reinforcement learning khong?**

> Khong. Model hien tai la supervised learning tu JSONL data, khong co vong lap self-play RL kieu AlphaZero voi MCTS.

**Hoi: Model co lam AI manh hon khong?**

> Model giup cung cap prior thong ke va top-k advisor. A/B benchmark cuc bo cho thay hybrid khong pha tactical rules va giu completed depth tuong duong, nhung chua du de ket luan playing strength tang ro ret. Can benchmark nhieu van hon de chung minh.

**Hoi: Vi sao khong cho model tu danh luon?**

> Top-1 cua model khoang 40%, chua du an toan cho Gomoku vi mot nuoc sai trong tactical case co the thua ngay. Vi vay nhom chi dung model de sap xep candidate, con search va threat rules van quyet dinh cuoi cung.

**Hoi: Co manh hon Rapfi/Yixin khong?**

> Nhom khong claim nhu vay. Rapfi/Yixin la engine thi dau chuyen sau. Du an nay tap trung minh hoa classical AI search ket hop threat knowledge va supervised advisor trong pham vi mon hoc.

**Hoi: Vi sao completed depth bang 0?**

> Vi AI co cac buoc xu ly nhanh truoc search sau, vi du opening center, winning_move hoac blocking_win. Depth 0 trong cac case nay khong phai loi, ma la do rule tactical tra ve ngay.

**Hoi: Neu latency hybrid khong tot hon, vi sao van tich hop model?**

> Vi model van co gia tri voi advisor UI va ordering. Ket qua hien tai cho thay no an toan, nhung chua du manh de claim toi uu latency. Day la nen tang cho benchmark va cai tien tiep theo.
