# Noi dung chi tiet slide thuyet trinh Gomoku AI

Muc tieu: tao slide 15 phut, bam sat bao cao `REPORT_BTL.tex`, co phan noi can bang cho cac thanh vien va co cho dien minh chung that tu deploy/benchmark/UI.

Tong thoi luong de xuat: 15 phut trinh bay + Q&A.

## Phan cong noi

| Nguoi | Thoi luong | Slide chinh | Vai tro |
|---|---:|---|---|
| Nguoi lam report | 3-4 phut | 1, 2, 11, 12 | Gioi thieu, tong hop, ket luan |
| Thanh vien 1 | 3-4 phut | 3, 4, 5 | AI core va tactical demo |
| Thanh vien 2 | 3-4 phut | 6, 7 | Deploy, API validation, system integration |
| Thanh vien 3 | 3-4 phut | 8, 9, 10 | Benchmark, UI test, danh gia |

## Slide 1: Tieu de va thong tin nhom

**Tieu de:** Gomoku/Caro 15x15 AI

**Noi dung tren slide:**

- Ten du an: Gomoku AI 15x15.
- Bai toan: nguoi choi vs AI tren board 15x15.
- Huong tiep can: classical game AI, explainable search.
- Tech stack: React/Vite, FastAPI, Python AI engine.
- Link GitHub: `https://github.com/Azios1010/tictactoe`.
- Link demo: `[dien link Vercel]`.

**Nguoi noi:** Nguoi lam report.

**Loi thoai goi y:**

> Nhom em xay dung mot he thong choi Gomoku/Caro 15x15 giua nguoi choi va AI. Trong du an nay, trong tam khong phai la web app don thuan ma la mot AI engine theo huong classical search, co the giai thich duoc ly do chon nuoc di. He thong co frontend React/Vite, backend FastAPI va da duoc deploy public de demo truc tiep.

**Minh chung can co:**

- Anh chup trang app online.
- QR/link GitHub hoac Vercel neu muon.

## Slide 2: Bai toan va muc tieu

**Tieu de:** Bai toan Gomoku/Caro 15x15

**Noi dung tren slide:**

- Board 15x15, hai ben lan luot dat quan.
- Thang khi co 5 quan lien tiep theo ngang/doc/cheo.
- Quy uoc engine:
  - `0`: o trong.
  - `1`: AI/O.
  - `-1`: nguoi choi/X.
- Thach thuc: branching factor lon, toi da 225 nuoc hop le dau game.
- Muc tieu: AI danh hop ly, phan hoi nhanh, giai thich duoc reason.

**Nguoi noi:** Nguoi lam report.

**Loi thoai goi y:**

> Gomoku 15x15 co khong gian trang thai lon hon rat nhieu so voi tic-tac-toe 3x3. Neu moi luot deu xet tat ca o trong thi minimax se no nhanh theo ham mu. Vi vay muc tieu cua nhom la ket hop search voi tri thuc Gomoku, de AI vua danh duoc trong thoi gian ngan vua tra ve ly do nhu winning_move, blocking_win hay creating_open_four.

**Hinh anh goi y:**

- Mot hinh board 15x15.
- Mot icon/diagram 5 quan lien tiep.

## Slide 3: Kien truc AI core

**Tieu de:** AI core pipeline

**Noi dung tren slide:**

```text
Board
-> Validate / Normalize
-> Immediate win/block
-> Candidate generation
-> Move ordering
-> Iterative deepening
-> Minimax + alpha-beta
-> Evaluator + threat detection
-> MoveAnalysis
```

**Cac file lien quan:**

- `backend/ai_core.py`
- `backend/ai_types.py`
- `backend/board_rules.py`
- `backend/threats.py`
- `backend/evaluator.py`
- `backend/move_ordering.py`

**Nguoi noi:** Thanh vien 1.

**Loi thoai goi y:**

> Day la luong xu ly chinh cua AI. Truoc khi search sau, AI kiem tra cac truong hop chien thuat mot buoc nhu thang ngay hoac chan doi thu thang. Sau do engine sinh cac nuoc ung vien quanh vung dang co quan, sap xep nuoc theo threat va local score, roi chay minimax alpha-beta voi iterative deepening.

**Thanh vien 1 can dien:**

- 1 so do pipeline dep hon neu lam slide.
- 1-2 cau tu giai thich theo cach hieu ca nhan.

## Slide 4: Thuat toan va heuristic

**Tieu de:** Classical AI search + Gomoku threats

**Noi dung tren slide:**

| Thanh phan | Vai tro |
|---|---|
| Minimax | Gia lap hai ben di toi uu |
| Alpha-beta | Cat nhanh cac nhanh khong can xet |
| Iterative deepening | Tim sau dan trong time limit |
| Candidate pruning | Giam branching factor |
| Move ordering | Uu tien nuoc co threat truoc |
| Threat detection | Nhan dien open-four, broken-four, double-threat |
| Evaluator | Cham diem `AttackScore - DefenseScore` |
| Zobrist/TT | Cache trang thai da tim |

**Nguoi noi:** Thanh vien 1.

**Loi thoai goi y:**

> Diem quan trong la AI khong chi dung minimax thuan tuy. Neu chi minimax tren board 15x15 thi qua cham. Nhom them candidate pruning de giam so nuoc can xet, move ordering de alpha-beta cat nhanh hon, va threat detection de engine hieu cac pattern dac thu cua Gomoku nhu open-four, closed-four, open-three, broken-three va double-threat.

**Can tranh noi qua:**

- Khong noi AI manh hon Rapfi/Yixin.
- Khong noi full Threat Space Search.
- Khong noi reinforcement learning/neural network.

## Slide 5: Tactical demo va reason cua AI

**Tieu de:** AI explainability qua reason

**Noi dung tren slide:**

| Case | Difficulty | AI move | Reason | Completed depth |
|---|---|---|---|---:|
| AI thang ngay | `[dien]` | `[dien]` | `winning_move` | `[dien]` |
| AI chan thang | `[dien]` | `[dien]` | `blocking_win` | `[dien]` |
| AI tao threat | `[dien]` | `[dien]` | `[dien]` | `[dien]` |

**Reason can giai thich:**

- `winning_move`: AI co nuoc thang ngay.
- `blocking_win`: AI chan nguoi choi thang ngay.
- `creating_open_four`: AI tao bon quan mo.
- `best_search_score`: AI chon nuoc co diem search tot nhat.

**Nguoi noi:** Thanh vien 1.

**Loi thoai goi y:**

> De viec demo khong chi la nhin AI danh, backend tra ve reason va completed_depth. Reason cho biet vi sao AI chon nuoc do. Vi du, trong case doi thu co bon quan lien tiep, AI uu tien blocking_win truoc khi search sau. Trong case AI co co hoi ket thuc van, AI tra ve winning_move.

**Thanh vien 1 phai chuan bi:**

- It nhat 2 anh UI hoac Swagger response.
- Dien bang tactical demo trong slide.
- Neu khong tao duoc `creating_open_four`, co the dung `best_search_score` va giai thich la nuoc tot nhat theo search/evaluator.

## Slide 6: Kien truc he thong va deploy

**Tieu de:** Full-stack architecture

**Noi dung tren slide:**

```text
User Browser
  |
  v
Vercel Frontend (React/Vite)
  |-- POST /api/get-move
  v
Render Backend (FastAPI + AI core)

Vercel Frontend
  |-- POST /arena/api/self-play
  v
Render Arena Service
```

**Cau hinh deploy:**

- `render.yaml`: tao 2 service Render.
- Backend health: `/api/health`.
- Arena health: `/arena/api/health`.
- Vercel env:
  - `VITE_API_BASE_URL`
  - `VITE_ARENA_API_BASE_URL`
- Render env:
  - `FRONTEND_ORIGINS`

**Nguoi noi:** Thanh vien 2.

**Loi thoai goi y:**

> He thong duoc deploy tach frontend va backend. Frontend tren Vercel chi phu trach UI, con logic AI nam trong FastAPI backend tren Render. Arena service cung chay rieng tren Render de phuc vu che do AI tu dau. Cac URL backend khong hard-code trong source ma duoc doc qua bien moi truong.

**Thanh vien 2 phai chuan bi:**

- Link Vercel.
- Link Render backend `/api/health`.
- Link Render arena `/arena/api/health`.
- Anh Swagger docs.

## Slide 7: API validation va do on dinh online

**Tieu de:** API contract, CORS va latency

**Noi dung tren slide:**

| API | Input | Output | Muc dich |
|---|---|---|---|
| `/api/get-move` | board, player, difficulty | row, col, reason, evaluation, completed_depth | AI chon nuoc |
| `/arena/api/self-play` | games, save_to_disk | samples, latest_game, config | AI tu dau |

**Bang latency can dien:**

| Endpoint | Lan 1 | Lan 2 | Lan 3 | Nhan xet |
|---|---:|---:|---:|---|
| Backend health | `[ms]` | `[ms]` | `[ms]` | `[dien]` |
| Arena health | `[ms]` | `[ms]` | `[ms]` | `[dien]` |
| Get move Medium | `[ms]` | `[ms]` | `[ms]` | `[dien]` |
| Arena self-play | `[ms]` | `[ms]` | `[ms]` | `[dien]` |

**Nguoi noi:** Thanh vien 2.

**Loi thoai goi y:**

> Phan deploy khong chi la dua app len internet. Nhom con kiem tra API contract, nghia la request gui len co dung schema va response co du cac truong can cho UI hay khong. Ngoai ra, do frontend va backend o hai domain khac nhau, CORS phai dung. Bang latency cho thay tinh on dinh cua demo online va giup nhan dien cold start cua Render.

**Thanh vien 2 phai chuan bi:**

- Dien bang latency that.
- Ghi 2-3 rui ro: sai env, CORS, Render cold start.
- Anh/chung cu Swagger response.

## Slide 8: Benchmark design

**Tieu de:** Benchmark doc lap voi deploy

**Noi dung tren slide:**

- Benchmark chay bang `benchmark_ai.py`.
- Output: `benchmark_results.json`.
- Muc tieu: kiem tra tactical correctness, khong phai do uptime deploy.
- Case benchmark:
  - Opening center.
  - AI win horizontal/diagonal.
  - Block human open-four.
  - Block broken-four.
  - Threat/open-four.
- Agents so sanh:
  - Random baseline.
  - Center-first baseline.
  - Greedy 1-ply.
  - Basic minimax.
  - Project Easy/Medium/Hard.

**Nguoi noi:** Thanh vien 3.

**Loi thoai goi y:**

> Benchmark doc lap voi deploy. Deploy tra loi cau hoi he thong co chay online khong, con benchmark tra loi cau hoi AI co chon dung nuoc trong cac tinh huong chien thuat khong. Nhom so sanh AI cua du an voi cac baseline noi bo, tu random cho den minimax nong.

**Thanh vien 3 phai chuan bi:**

- Ghi ngay chay benchmark.
- Ghi commit hash.
- Ghi moi truong chay: local hay API deploy.

## Slide 9: Benchmark results Easy/Medium/Hard

**Tieu de:** Ket qua benchmark

**Bang accuracy hien co:**

| Agent | Correct | Total | Accuracy |
|---|---:|---:|---:|
| random_baseline | 0 | 8 | 0.00 |
| center_first_baseline | 4 | 8 | 0.50 |
| greedy_1ply_baseline | 6 | 8 | 0.75 |
| basic_minimax_baseline | 8 | 8 | 1.00 |
| project_easy | 8 | 8 | 1.00 |
| project_medium | 8 | 8 | 1.00 |
| project_hard | 8 | 8 | 1.00 |

**Bang Easy/Medium/Hard can nguoi 3 dien lai neu chay moi:**

| Difficulty | Case | Move | Reason | Depth | Time |
|---|---|---|---|---:|---:|
| Easy | Immediate win | `[dien]` | `[dien]` | `[dien]` | `[dien]` |
| Easy | Immediate block | `[dien]` | `[dien]` | `[dien]` | `[dien]` |
| Medium | Immediate win | `[dien]` | `[dien]` | `[dien]` | `[dien]` |
| Medium | Immediate block | `[dien]` | `[dien]` | `[dien]` | `[dien]` |
| Hard | Immediate win | `[dien]` | `[dien]` | `[dien]` | `[dien]` |
| Hard | Immediate block | `[dien]` | `[dien]` | `[dien]` | `[dien]` |

**Nguoi noi:** Thanh vien 3.

**Loi thoai goi y:**

> Ket qua hien tai cho thay project_easy, project_medium va project_hard deu dat 8/8 tren bo tactical benchmark noi bo. Tuy nhien day la benchmark noi bo, chua tich hop engine ngoai nhu Rapfi hay Yixin, nen khong ket luan la SOTA. Dieu quan trong la AI xu ly dung cac case co ban va tra ve reason ro rang.

**Can nhan manh:**

- Benchmark noi bo.
- Chua so voi engine ngoai.
- Medium phu hop demo neu Hard cham tren cloud.

## Slide 10: UI, demo flow va user experience

**Tieu de:** UI demo va kha nang trinh bay AI

**Noi dung tren slide:**

- Play Vs AI:
  - Click board.
  - Doi difficulty.
  - AI tra nuoc di.
  - Panel hien reason/evaluation/completed depth/elapsed time.
- Arena Self-Play:
  - Run arena.
  - Replay game moi nhat.
  - Summary samples/wins/draws.
- Error handling:
  - Backend unreachable.
  - Arena unreachable.
  - Disable click khi AI dang nghi.

**Bang test UI can dien:**

| UI item | Ket qua | Ghi chu |
|---|---|---|
| Board khong vo layout | `[Dat/Chua]` | `[dien]` |
| AI reason hien dung | `[Dat/Chua]` | `[dien]` |
| Doi difficulty duoc | `[Dat/Chua]` | `[dien]` |
| Arena replay chay | `[Dat/Chua]` | `[dien]` |

**Nguoi noi:** Thanh vien 3.

**Loi thoai goi y:**

> UI duoc thiet ke de phuc vu demo AI, khong chi de choi game. Vi vay panel ben canh hien cac thong tin debug nhu reason, evaluation va completed depth. Dieu nay giup giai thich tai sao AI chon nuoc di, dong thoi cho thay su khac nhau giua cac difficulty.

**Thanh vien 3 phai chuan bi:**

- Anh Play Vs AI sau khi AI di nuoc.
- Anh Arena Self-Play.
- Bang test UI.

## Slide 11: Kho khan, han che va cach xu ly

**Tieu de:** Lessons learned

**Noi dung tren slide:**

| Kho khan | Cach xu ly |
|---|---|
| Branching factor lon | Candidate pruning, move ordering, alpha-beta |
| AI can phan hoi nhanh | Iterative deepening + time limit |
| Threat phuc tap | Threat detector + evaluator rieng |
| Deploy frontend/backend khac domain | Env variables + CORS |
| Render cold start | Warm up backend truoc khi demo |

**Han che can noi ro:**

- Chua phai SOTA Gomoku engine.
- Chua co full TSS/VCF solver.
- Chua dung RL/neural network.
- Chua benchmark doi dau Rapfi/Yixin.
- Mot so double-threat phuc tap co the chua danh gia chuan.

**Nguoi noi:** Nguoi lam report.

**Loi thoai goi y:**

> Nhom khong claim AI la engine manh nhat. Gia tri cua du an nam o viec tich hop cac ky thuat AI co dien vao mot bai toan co branching factor lon va co the demo/giai thich duoc. Cac han che nay cung la co so cho huong phat trien tiep theo.

## Slide 12: Ket luan va huong phat trien

**Tieu de:** Ket luan

**Noi dung tren slide:**

- Da xay dung he thong Gomoku/Caro 15x15 full-stack.
- AI dung classical search:
  - minimax/alpha-beta,
  - iterative deepening,
  - candidate pruning,
  - threat detection,
  - evaluator,
  - transposition table.
- Co UI explainability: reason, evaluation, completed depth.
- Co benchmark noi bo va deploy public.
- Co arena self-play cho phan tich/du lieu sau nay.

**Huong phat trien:**

- Mo rong tactical benchmark suite.
- Cai thien evaluator cho broken-four/double-threat.
- Minimal Threat Space Search/VCF solver.
- Tich hop engine ngoai de benchmark khach quan.
- Khai thac arena JSONL cho huong learning-based.

**Nguoi noi:** Nguoi lam report.

**Loi thoai goi y:**

> Tong ket lai, du an da dap ung ca phan AI lan phan he thong: co engine classical search, co benchmark, co UI giai thich va co deploy online. Neu phat trien tiep, nhom se uu tien benchmark sau hon, threat search day du hon va so sanh voi engine ngoai de danh gia khach quan hon.

## Slide 13 neu can: Demo truc tiep

**Tieu de:** Live demo

**Noi dung tren slide:**

- Link Vercel: `[dien]`
- Link backend health: `[dien]`
- Link arena health: `[dien]`
- Demo flow:
  1. Mo app online.
  2. Choi 1 nuoc Medium.
  3. Chi vao reason/evaluation/completed depth.
  4. Chuyen Arena.
  5. Bam Run arena.

**Nguoi noi:** Ca nhom, uu tien Thanh vien 2 dieu khien demo.

**Luu y truoc demo:**

- Mo backend Render truoc de warm up.
- Kiem tra Vercel env dung URL Render.
- Neu Hard cham, demo Medium.
- Chuan bi anh/video backup neu internet loi.

## Checklist tao slide

- [ ] Slide co link GitHub.
- [ ] Slide co link Vercel/Render that.
- [ ] Slide AI co pipeline va bang thuat toan.
- [ ] Slide tactical demo da dien so lieu that.
- [ ] Slide deploy co so do Vercel -> Render.
- [ ] Slide API validation co bang contract/latency.
- [ ] Slide benchmark co bang accuracy va Easy/Medium/Hard.
- [ ] Slide UI co anh Play Vs AI va Arena.
- [ ] Slide han che khong claim qua muc.
- [ ] Slide ket luan co huong phat trien.

## Checklist truoc ngay thuyet trinh

- [ ] Push commit moi nhat len GitHub.
- [ ] Vercel app mo duoc.
- [ ] Backend `/api/health` tra `{"status":"ok"}`.
- [ ] Arena `/arena/api/health` tra `{"status":"ok"}`.
- [ ] Da warm up Render truoc khi vao phong.
- [ ] Co PDF report bien dich tu `REPORT_BTL.tex`.
- [ ] Co anh/video backup cho demo.
- [ ] Moi thanh vien thu noi phan cua minh it nhat 1 lan.

## Loi noi ngan cho Q&A

**Hoi: AI co dung machine learning khong?**

> Khong. AI hien tai la classical game AI, dung minimax/alpha-beta, heuristic evaluator va threat detection. Arena co the sinh du lieu JSONL cho huong phat trien learning-based sau nay.

**Hoi: Benchmark nay co so voi SOTA chua?**

> Chua. Benchmark hien tai la benchmark noi bo voi baseline don gian va cac tactical case. Nhom khong claim SOTA; huong tiep theo la tich hop engine ngoai nhu Rapfi/Yixin de so sanh khach quan hon.

**Hoi: Vi sao completed depth co luc bang 0?**

> Vi AI co cac rule xu ly nhanh truoc search sau, vi du opening center, winning_move hoac blocking_win. Trong cac case do, AI tra ket qua ngay nen completed_depth co the la 0.

**Hoi: Deploy co lien quan benchmark khong?**

> Deploy va benchmark la hai phan doc lap. Deploy chung minh he thong chay public va API tich hop dung. Benchmark chung minh AI chon nuoc dung trong cac case chien thuat.

**Hoi: Neu Render cham thi sao?**

> Render co the cold start, dac biet goi free. Nhom co health check va se warm up backend truoc khi demo. Khi demo gameplay, Medium la muc can bang hon neu Hard phan hoi cham.
