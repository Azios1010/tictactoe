# Checklist phan viec can bang cho 3 thanh vien

Muc tieu: 3 thanh vien con lai co khoi luong cong viec tuong duong nhau. Moi nguoi deu co 4 loai viec:

- Viec ky thuat/cau hinh.
- Viec kiem tra va thu thap minh chung.
- Viec viet noi dung de dua vao report.
- Viec chuan bi phan noi/demo khi thuyet trinh.

Nguoi lam report se tong hop ket qua tu file nay vao `REPORT_BTL.md`, slide va kich ban thuyet trinh.

## Thong tin chung can dien

- [ ] Link GitHub repository:
- [ ] Link Vercel frontend:
- [ ] Link Render backend:
- [ ] Link Render arena:
- [ ] Ngay demo/thuyet trinh:
- [ ] Thanh vien A:
- [ ] Thanh vien B:
- [ ] Thanh vien C:

## Nguyen tac chia viec

- [ ] Moi thanh vien phai nop it nhat 1 bang/tom tat co cau truc.
- [ ] Moi thanh vien phai nop it nhat 2 anh chup man hinh hoac minh chung.
- [ ] Moi thanh vien phai viet 1 doan 5-7 cau cho report.
- [ ] Moi thanh vien phai chuan bi 3-4 phut noi trong buoi thuyet trinh.
- [ ] Neu co thay doi code/tai lieu, phai commit va push len GitHub.

## Bang phan viec tong quan

| Thanh vien | Vai tro chinh | Phan ky thuat | Phan minh chung | Phan report | Phan thuyet trinh |
|---|---|---|---|---|---|
| A | AI va tactical demo | Giai thich AI core, tao case demo | Anh/case AI chon nuoc | Phuong phap AI | 3-4 phut |
| B | Deploy va tich hop he thong | Vercel, Render, env, CORS | Link online, health check, docs | Kien truc deploy | 3-4 phut |
| C | Benchmark, UI va danh gia | Build/test, benchmark, UI test | Bang benchmark, anh UI | Danh gia ket qua | 3-4 phut |

## Thanh vien A: AI core va tactical demo

### Muc tieu

Chung minh phan AI cua du an co co so thuat toan ro rang, co the giai thich duoc ly do chon nuoc di, va co cac case chien thuat de demo.

### A1. Doc va tom tat AI core

- [ ] Doc `backend/ai_core.py`.
- [ ] Doc `backend/ai_types.py`.
- [ ] Doc `backend/board_rules.py`.
- [ ] Doc `backend/threats.py`.
- [ ] Doc `backend/evaluator.py`.
- [ ] Doc `backend/move_ordering.py`.
- [ ] Viet tom tat 8-10 gach dau dong ve luong AI.

Goi y luong AI:

```text
Board -> validate/normalize -> immediate win/block -> candidate generation -> move ordering -> iterative deepening -> minimax/alpha-beta -> evaluator -> MoveAnalysis
```

### A2. Lap bang thuat toan

- [ ] Lap bang giai thich ngan gon cac thanh phan sau:
  - Minimax.
  - Alpha-beta pruning.
  - Iterative deepening.
  - Candidate pruning.
  - Move ordering.
  - Threat detection.
  - Heuristic evaluator.
  - Zobrist hash/transposition table.

Mau bang:

| Thanh phan | Vai tro trong du an | Loi ich |
|---|---|---|
| Minimax | Gia lap hai ben di toi uu | Chon nuoc co diem search tot |
| Alpha-beta | Cat nhanh nhanh khong can xet | Giam so node phai duyet |

### A3. Chuan bi 3 tactical demo cases

- [ ] Case 1: AI thang ngay bang `winning_move`.
- [ ] Case 2: AI chan nguoi choi thang ngay bang `blocking_win`.
- [ ] Case 3: AI tao threat, vi du `creating_open_four`, `creating_double_threat` hoac `best_search_score`.
- [ ] Ghi lai board/cach tao case.
- [ ] Chup anh UI hoac Swagger response cho moi case.

Mau ghi case:

| Case | Mo ta board | Difficulty | AI move | Reason | Evaluation | Completed depth |
|---|---|---|---|---|---:|---:|
| A1 | AI co 4 quan lien tiep | Medium | | | | |

### A4. Viet noi dung cho report

- [ ] Viet 1 doan 5-7 cau ve AI.
- [ ] Viet 1 bang reason cua AI.
- [ ] Viet 3 han che cua AI hien tai.
- [ ] Viet 3 huong cai tien tiep theo.

Doan mau co the sua:

```text
AI cua du an la classical Gomoku engine, khong dung reinforcement learning hay neural network. Engine ket hop minimax/alpha-beta voi iterative deepening, candidate pruning, move ordering, threat detection va heuristic evaluator. Truoc khi search sau, AI uu tien cac nuoc thang ngay hoac chan doi thu thang ngay. Cac threat Gomoku nhu open-four, closed-four, open-three va double-threat duoc dung de cham diem va sap xep nuoc di. Ket qua tra ve cho frontend gom move, evaluation, reason va completed_depth, giup viec demo va giai thich tro nen ro rang hon. Han che hien tai la AI van dua tren pattern heuristic va time limit, chua phai engine SOTA.
```

### A5. Chuan bi phan thuyet trinh

- [ ] Noi trong 3-4 phut.
- [ ] Giai thich vi sao Gomoku 15x15 kho hon tic-tac-toe 3x3.
- [ ] Giai thich AI khong hoc tu du lieu, ma dung search + heuristic.
- [ ] Demo 1 case AI chan thang hoac thang ngay.
- [ ] Giai thich `reason`, `evaluation`, `completed_depth`.

### Dau ra cua thanh vien A

- [ ] Bang thuat toan.
- [ ] Bang reason.
- [ ] 3 tactical demo cases.
- [ ] It nhat 2 anh chup minh chung.
- [ ] 1 doan report 5-7 cau.
- [ ] 3-4 bullet cho slide.

## Thanh vien B: Deploy, tich hop va van hanh online

### Muc tieu

Chung minh he thong full-stack chay duoc tren internet, frontend va backend tach rieng, cau hinh dung env, CORS va health check.

### B1. Kiem tra GitHub va cau hinh deploy

- [ ] Kiem tra GitHub da co commit moi nhat.
- [ ] Kiem tra file `render.yaml`.
- [ ] Kiem tra file `DEPLOYMENT.md`.
- [ ] Kiem tra `frontend/.env.example`.
- [ ] Kiem tra `backend/.env.example`.
- [ ] Ghi lai commit hash moi nhat.

Mau bang:

| Hang muc | Ket qua | Minh chung |
|---|---|---|
| GitHub co `render.yaml` | Dat/Chua dat | Link file |
| GitHub co `DEPLOYMENT.md` | Dat/Chua dat | Link file |

### B2. Kiem tra Render backend va arena

- [ ] Mo backend `/api/health`.
- [ ] Mo backend `/docs`.
- [ ] Mo arena `/arena/api/health`.
- [ ] Mo arena `/docs`.
- [ ] Chup anh 2 health checks.
- [ ] Chup anh 2 Swagger docs hoac ghi link.

Ket qua health mong doi:

```json
{"status":"ok"}
```

### B3. Kiem tra Vercel env va luong API

- [ ] Kiem tra Vercel co `VITE_API_BASE_URL`.
- [ ] Kiem tra Vercel co `VITE_ARENA_API_BASE_URL`.
- [ ] Kiem tra Render backend co `FRONTEND_ORIGINS`.
- [ ] Kiem tra Render arena co `FRONTEND_ORIGINS`.
- [ ] Dam bao value khong co dau `/` cuoi URL.
- [ ] Sau khi sua env, redeploy frontend neu can.

Mau cau hinh:

```text
VITE_API_BASE_URL=https://<render-backend-url>
VITE_ARENA_API_BASE_URL=https://<render-arena-url>
FRONTEND_ORIGINS=https://<vercel-frontend-url>
```

### B4. Test demo online

- [ ] Mo link Vercel.
- [ ] Choi mot nuoc tren Easy.
- [ ] Choi mot nuoc tren Medium.
- [ ] Chuyen sang Arena va bam `Run arena`.
- [ ] Ghi lai neu request dau tien cham do Render warm up.
- [ ] Chup anh app online sau khi AI da di nuoc.

Mau bang:

| Tinh nang online | Ket qua | Ghi chu |
|---|---|---|
| Play Vs AI Easy | Dat/Chua dat | |
| Play Vs AI Medium | Dat/Chua dat | |
| Arena self-play | Dat/Chua dat | |

### B5. Viet noi dung cho report va slide

- [ ] Viet 1 doan 5-7 cau ve kien truc deploy.
- [ ] Viet 1 bang link he thong.
- [ ] Viet 3 loi deploy thuong gap va cach sua.
- [ ] Viet 3 bullet ve loi ich cua deploy online so voi chi nop source.

Doan mau co the sua:

```text
He thong duoc deploy public voi frontend React/Vite tren Vercel va hai FastAPI service tren Render. Frontend khong hard-code URL backend ma doc qua cac bien moi truong VITE_API_BASE_URL va VITE_ARENA_API_BASE_URL. Backend va arena doc FRONTEND_ORIGINS de cau hinh CORS, giup chi domain frontend duoc phep goi API sau khi deploy on dinh. Render cung cap health check cho tung service, con Vercel phuc vu giao dien web. Cach trien khai nay chung minh du an khong chi chay local ma co the demo truc tiep qua internet.
```

### Dau ra cua thanh vien B

- [ ] Bang link he thong.
- [ ] Bang cau hinh env.
- [ ] Bang test online.
- [ ] It nhat 2 anh chup minh chung.
- [ ] 1 doan report 5-7 cau.
- [ ] 3-4 bullet cho slide.

## Thanh vien C: Benchmark, kiem thu va danh gia UI

### Muc tieu

Chung minh du an co kiem thu, co benchmark doc lap voi deploy, va co danh gia ro Easy/Medium/Hard cung trai nghiem UI.

### C1. Chay cac lenh kiem tra co ban

- [ ] Chay Python compile check.
- [ ] Chay frontend build.
- [ ] Chay arena smoke test.
- [ ] Ghi lai ket qua moi lenh.
- [ ] Kiem tra `git status --short` sau khi test.
- [ ] Khong commit cache/test output neu khong duoc yeu cau.

Lenh goi y:

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py arena\service.py
cd frontend
npm.cmd run build
```

### C2. Benchmark Easy/Medium/Hard

- [ ] Chay benchmark hoac test API cho Easy.
- [ ] Chay benchmark hoac test API cho Medium.
- [ ] Chay benchmark hoac test API cho Hard.
- [ ] Ghi lai time, reason, completed depth.
- [ ] So sanh trade-off toc do va do sau.
- [ ] Neu Hard cham tren deploy, ghi chu dung Medium khi demo.

Mau bang:

| Difficulty | Case | AI move | Reason | Completed depth | Time (ms) | Ket qua |
|---|---|---|---|---:|---:|---|
| Easy | Immediate win | | | | | |
| Easy | Immediate block | | | | | |
| Medium | Immediate win | | | | | |
| Medium | Immediate block | | | | | |
| Hard | Immediate win | | | | | |
| Hard | Immediate block | | | | | |

### C3. Test UI va UX

- [ ] Test Play Vs AI.
- [ ] Test doi difficulty.
- [ ] Test reset game.
- [ ] Test AI debug panel: reason, evaluation, completed depth, elapsed time.
- [ ] Test Arena Self-Play.
- [ ] Test tren man hinh laptop.
- [ ] Neu co thoi gian, test tren mobile hoac resize browser.

Mau bang:

| UI item | Ket qua | Ghi chu |
|---|---|---|
| Board khong vo layout | Dat/Chua dat | |
| Click bi khoa khi AI dang nghi | Dat/Chua dat | |
| Reason hien dung | Dat/Chua dat | |
| Arena replay chay | Dat/Chua dat | |

### C4. Danh gia theo tieu chi cham diem

- [ ] Danh gia muc do phuc tap bai toan.
- [ ] Danh gia chat luong phuong phap AI.
- [ ] Danh gia chat luong he thong/demo.
- [ ] Danh gia chat luong benchmark.
- [ ] Danh gia diem manh.
- [ ] Danh gia han che.

Mau bang:

| Tieu chi | Bang chung | Nhan xet |
|---|---|---|
| Do phuc tap bai toan | Gomoku 15x15, branching factor lon | |
| Chat luong AI | Alpha-beta, heuristic, threat detection | |
| Demo he thong | Vercel + Render | |
| Benchmark | Bang Easy/Medium/Hard | |

### C5. Viet noi dung cho report va slide

- [ ] Viet 1 doan 5-7 cau ve benchmark/kiem thu.
- [ ] Viet 1 bang benchmark cuoi cung.
- [ ] Viet 3 nhan xet ket qua.
- [ ] Viet 3 de xuat cai tien neu co them thoi gian.

Doan mau co the sua:

```text
Benchmark duoc dung de danh gia AI doc lap voi viec deploy. Cac case tap trung vao kha nang xu ly chien thuat Gomoku nhu thang ngay, chan doi thu thang va tao threat. Ket qua duoc so sanh giua Easy, Medium va Hard thong qua nuoc di duoc chon, reason, completed_depth va thoi gian phan hoi. Medium thuong phu hop cho demo tuong tac vi can bang giua toc do va chat luong, trong khi Hard co the tim sau hon nhung cham hon. Phan UI duoc kiem tra tren cac luong chinh nhu Play Vs AI, doi difficulty, reset va Arena Self-Play.
```

### Dau ra cua thanh vien C

- [ ] Bang ket qua test command.
- [ ] Bang benchmark Easy/Medium/Hard.
- [ ] Bang test UI.
- [ ] It nhat 2 anh chup minh chung.
- [ ] 1 doan report 5-7 cau.
- [ ] 3-4 bullet cho slide.

## Checklist tong hop cho nguoi lam report

Nguoi lam report chi can tick khi da nhan du tu 3 thanh vien:

- [ ] Tu thanh vien A: bang thuat toan AI.
- [ ] Tu thanh vien A: 3 tactical demo cases.
- [ ] Tu thanh vien A: doan report ve AI.
- [ ] Tu thanh vien B: bang link deploy.
- [ ] Tu thanh vien B: bang env/CORS.
- [ ] Tu thanh vien B: doan report ve deploy.
- [ ] Tu thanh vien C: bang benchmark.
- [ ] Tu thanh vien C: bang test UI.
- [ ] Tu thanh vien C: doan report ve danh gia.
- [ ] Co anh chup minh chung tu ca 3 nguoi.
- [ ] Co commit hash moi nhat sau khi cap nhat tai lieu.

## Kich ban thuyet trinh 15 phut can bang

| Thoi luong | Nguoi | Noi dung |
|---:|---|---|
| 2 phut | Nguoi lam report | Gioi thieu bai toan, muc tieu, tech stack |
| 3 phut | Thanh vien A | AI core, minimax/alpha-beta, threat detection |
| 3 phut | Thanh vien B | Deploy online, kien truc Vercel/Render, env/CORS |
| 3 phut | Thanh vien C | Benchmark, UI test, danh gia Easy/Medium/Hard |
| 2 phut | Nguoi lam report | Kho khan, han che, huong phat trien |
| 2 phut | Ca nhom | Demo nhanh va Q&A |

## Tieu chi hoan thanh toi thieu

- [ ] Moi thanh vien co it nhat 1 bang ket qua.
- [ ] Moi thanh vien co it nhat 2 minh chung.
- [ ] Moi thanh vien co 1 doan report 5-7 cau.
- [ ] Moi thanh vien co 3-4 bullet cho slide.
- [ ] App online chay duoc.
- [ ] AI co demo tactical case.
- [ ] Benchmark co so sanh Easy/Medium/Hard.

## Tieu chi huong toi diem cao

- [ ] Report co bang chung ro rang, khong noi chung chung.
- [ ] Demo online dung link public, khong phu thuoc localhost.
- [ ] AI duoc giai thich bang reason/evaluation/completed_depth.
- [ ] Benchmark doc lap voi deploy.
- [ ] Co noi ro han che: chua SOTA, chua RL, chua full TSS/VCF.
- [ ] Ca 3 thanh vien deu co phan noi ngang nhau trong thuyet trinh.
