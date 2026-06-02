# Checklist phan viec cho 3 thanh vien con lai

Muc tieu: moi thanh vien co phan viec ro rang, co dau ra cu the de ban tong hop vao report va dung khi thuyet trinh/demo. Moi nguoi can cap nhat tien do bang cach tick checklist va gui lai minh chung.

Nguoi lam report: tong hop ket qua tu 3 nguoi nay vao `REPORT_BTL.md`, slide va phan trinh bay.

## Thong tin can dien truoc khi bat dau

- [ ] Link GitHub repository:
- [ ] Link Vercel frontend:
- [ ] Link Render backend:
- [ ] Link Render arena:
- [ ] Ngay demo/thuyet trinh:
- [ ] Ten thanh vien phu trach Deploy:
- [ ] Ten thanh vien phu trach AI core:
- [ ] Ten thanh vien phu trach Benchmark/UI:

## Quy uoc nop lai ket qua

Moi thanh vien nop lai cho nguoi lam report:

- [ ] 3-5 gach dau dong tom tat viec da lam.
- [ ] Anh chup man hinh hoac link minh chung.
- [ ] Loi/kho khan gap phai va cach xu ly.
- [ ] 1 doan ngan 5-7 cau de dua vao report.
- [ ] Neu co thay doi code, commit len GitHub va ghi ma commit.

## Thanh vien 1: Deploy va van hanh demo online

### Muc tieu

Dam bao du an chay duoc tren internet, co link demo cong khai, backend/arena hoat dong va frontend goi dung API.

### Nhiem vu chi tiet

- [ ] Kiem tra GitHub da co commit moi nhat.
  - Len GitHub repository.
  - Kiem tra cac file `render.yaml`, `DEPLOYMENT.md`, `frontend/.env.example`, `backend/.env.example` da xuat hien.

- [ ] Kiem tra Render backend.
  - Mo URL backend Render.
  - Mo endpoint `/api/health`.
  - Ket qua mong doi:

```json
{"status":"ok"}
```

- [ ] Kiem tra Render arena.
  - Mo URL arena Render.
  - Mo endpoint `/arena/api/health`.
  - Ket qua mong doi:

```json
{"status":"ok"}
```

- [ ] Kiem tra Swagger docs.
  - Mo `https://<render-backend-url>/docs`.
  - Mo `https://<render-arena-url>/docs`.
  - Chup anh man hinh 2 trang docs.

- [ ] Kiem tra bien moi truong Vercel.
  - Vao Vercel Project -> Settings -> Environment Variables.
  - Dam bao co:

```text
VITE_API_BASE_URL=https://<render-backend-url>
VITE_ARENA_API_BASE_URL=https://<render-arena-url>
```

- [ ] Kiem tra bien moi truong Render.
  - Vao tung service backend/arena tren Render.
  - Dam bao co:

```text
FRONTEND_ORIGINS=https://<vercel-frontend-url>
```

  - Neu chua khoa CORS, tam thoi co the de `*`, nhung khi nop nen doi ve dung link Vercel.

- [ ] Test frontend online.
  - Mo link Vercel.
  - Choi mot van o Easy.
  - Choi mot van o Medium.
  - Chuyen sang Arena va bam `Run arena`.
  - Chup anh man hinh app sau khi AI da di nuoc.

- [ ] Ghi lai loi deploy neu co.
  - Vi du: CORS, backend sleep, sai env, Render build fail, Vercel build fail.
  - Ghi cach khac phuc bang 2-3 cau.

### Dau ra can nop

- [ ] Link Vercel frontend.
- [ ] Link Render backend `/api/health`.
- [ ] Link Render backend `/docs`.
- [ ] Link Render arena `/arena/api/health`.
- [ ] Link Render arena `/docs`.
- [ ] 3-5 anh chup minh chung.
- [ ] Doan mo ta ngan cho report:

```text
He thong duoc deploy public bang Vercel cho frontend React/Vite va Render cho cac FastAPI service. Frontend doc URL API thong qua bien moi truong VITE_API_BASE_URL va VITE_ARENA_API_BASE_URL. Backend/arena gioi han CORS bang FRONTEND_ORIGINS de chi cho phep domain frontend goi API sau khi demo URL da on dinh.
```

### Phan thuyet trinh nen noi

- [ ] Noi ro frontend va backend tach rieng.
- [ ] Giai thich vi sao can env variable.
- [ ] Demo app online, khong chay localhost.
- [ ] Neu backend dau tien cham, giai thich Render can warm up.

## Thanh vien 2: AI core va giai thich thuat toan

### Muc tieu

Nam vung phan AI de giai thich duoc model hien tai "thong minh" o dau, dung thuat toan nao, vi sao AI chon nuoc di.

### Nhiem vu chi tiet

- [ ] Doc cac file AI chinh.
  - `backend/ai_core.py`
  - `backend/ai_types.py`
  - `backend/board_rules.py`
  - `backend/threats.py`
  - `backend/evaluator.py`
  - `backend/move_ordering.py`

- [ ] Tom tat kien truc AI bang 1 so do hoac danh sach.
  - Input: board 15x15.
  - Validate/normalize board.
  - Immediate win/block.
  - Candidate generation.
  - Move ordering.
  - Iterative deepening.
  - Minimax/alpha-beta.
  - Evaluator/threat detection.
  - Output: row, col, evaluation, reason, completed depth.

- [ ] Giai thich tung thanh phan chinh.
  - Minimax: gia dinh 2 ben di toi uu.
  - Alpha-beta pruning: cat nhanh cac nhanh khong can xet.
  - Iterative deepening: tim theo do sau tang dan trong gioi han thoi gian.
  - Candidate pruning: chi xet cac o gan quan da danh.
  - Move ordering: uu tien nuoc co threat/manh truoc de cat nhanh hon.
  - Threat detection: nhan dien open-four, closed-four, open-three, broken-three, double-threat.
  - Evaluator: cham diem the co theo mau tan cong/phong thu.
  - Zobrist hash/transposition table: nho trang thai da tim de tranh lap lai.

- [ ] Chuan bi bang reason cua AI.

| Reason | Y nghia |
|---|---|
| `opening_center` | Ban co rong, AI uu tien trung tam |
| `winning_move` | AI co nuoc thang ngay |
| `blocking_win` | AI chan nguoi choi thang ngay |
| `creating_double_threat` | AI tao hai moi de doa cung luc |
| `creating_open_four` | AI tao bon lien tiep mo |
| `creating_closed_four` | AI tao bon lien tiep bi chan mot dau |
| `blocking_double_threat` | AI chan the de doa kep cua doi thu |
| `blocking_open_four` | AI chan open-four cua doi thu |
| `building_attack` | AI xay dung tan cong |
| `reducing_threat` | AI giam nguy co phong thu |
| `best_search_score` | AI chon nuoc co diem search tot nhat |
| `timeout_best_known` | Het thoi gian, dung nuoc tot nhat da biet |

- [ ] Tao 3 case demo AI.
  - Case 1: AI co 4 quan lien tiep va thang ngay.
  - Case 2: Nguoi choi co 4 quan lien tiep, AI phai chan.
  - Case 3: AI tao threat/double-threat hoac open-four.

- [ ] Chay app va ghi lai reason/evaluation/completed depth cua 3 case.
  - Neu kho tao case tren UI, co the ghi lai board va goi API qua Swagger `/docs`.

- [ ] Viet phan han che cua AI.
  - Khong phai SOTA engine.
  - Chua co full Threat Space Search/VCF solver.
  - Chua dung reinforcement learning/neural network.
  - Search bi gioi han boi time limit va candidate pruning.
  - Mot so double-threat phuc tap co the danh gia chua chuan.

### Dau ra can nop

- [ ] 1 bang tom tat thuat toan.
- [ ] 1 bang reason cua AI.
- [ ] 3 case demo co anh chup hoac mo ta board.
- [ ] 1 doan ngan cho report:

```text
AI cua du an la classical Gomoku engine, ket hop minimax/alpha-beta voi iterative deepening, candidate pruning, move ordering, threat detection va heuristic evaluator. He thong uu tien cac nuoc thang/chan thang ngay truoc khi search sau hon, sau do danh gia cac nuoc ung vien dua tren threat Gomoku nhu open-four, closed-four, open-three va double-threat. Cach tiep can nay giup AI giai thich duoc ly do chon nuoc di thong qua cac truong reason, evaluation va completed_depth.
```

### Phan thuyet trinh nen noi

- [ ] Giai thich AI khong hoc tu du lieu, ma search va heuristic.
- [ ] Noi ro vi sao Gomoku 15x15 kho hon tic-tac-toe 3x3.
- [ ] Demo AI chan thang hoac thang ngay.
- [ ] Giai thich `completed_depth` de chung minh search co gioi han thoi gian.

## Thanh vien 3: Benchmark, kiem thu va UI demo

### Muc tieu

Chung minh he thong da duoc test, AI co cai thien va UI demo duoc cac tinh nang chinh.

### Nhiem vu chi tiet

- [ ] Doc tai lieu benchmark va test.
  - `PIPELINE.md`
  - `IMPLEMENTATION_PLAN.md`
  - `Gomoku_AI_Improvement_Roadmap.md`
  - Neu co script benchmark trong repo, doc va chay theo huong dan hien co.

- [ ] Chay backend compile check.

```powershell
.\backend\venv\Scripts\python.exe -m py_compile backend\ai_types.py backend\board_rules.py backend\threats.py backend\evaluator.py backend\move_ordering.py backend\ai_core.py backend\main.py arena\engine.py arena\run_arena.py arena\service.py
```

- [ ] Chay frontend build.

```powershell
cd frontend
npm.cmd run build
```

- [ ] Chay arena smoke test.

```powershell
.\backend\venv\Scripts\python.exe -m arena.run_arena --games 1 --depth 1 --candidate-radius 1 --candidate-limit 4 --max-moves 6 --no-save
```

- [ ] Test UI local hoac online.
  - Choi mode Play Vs AI.
  - Doi difficulty Easy/Medium/Hard.
  - Kiem tra AI co hien:
    - Move.
    - Reason.
    - Evaluation.
    - Completed depth.
    - Elapsed time.
  - Chuyen Arena Self-Play.
  - Bam `Run arena`.
  - Kiem tra replay chay va co summary.

- [ ] Tao bang benchmark Easy/Medium/Hard.

| Difficulty | Case | AI move | Reason | Completed depth | Time (ms) | Ket qua |
|---|---|---|---|---:|---:|---|
| Easy | Immediate win | | | | | |
| Easy | Immediate block | | | | | |
| Medium | Immediate win | | | | | |
| Medium | Immediate block | | | | | |
| Hard | Immediate win | | | | | |
| Hard | Immediate block | | | | | |

- [ ] Danh gia theo tieu chi.
  - Do dung chien thuat: AI co chon dung nuoc thang/chan khong?
  - Toc do: co phu hop demo tuong tac khong?
  - Do sau: `completed_depth` co thuong lon hon 0 khong?
  - UI: co de dung, de doc va khong bi loi khi deploy khong?

- [ ] Ghi lai cac loi va cach xu ly.
  - Vi du: backend unreachable, sai env, CORS, build fail, AI Hard cham.
  - Moi loi ghi: nguyen nhan, cach tai hien, cach sua.

- [ ] Kiem tra repo sach sau khi chay test.

```powershell
git status --short
```

  - Khong commit `backend/gomoku_tt.pkl` neu chi thay doi do test.
  - Khong commit `arena/data/*.jsonl` neu khong duoc yeu cau.
  - Khong commit `frontend/dist`.

### Dau ra can nop

- [ ] Ket qua cac lenh test/build.
- [ ] Bang benchmark Easy/Medium/Hard.
- [ ] Anh chup UI Play mode.
- [ ] Anh chup UI Arena mode.
- [ ] Danh sach loi da gap va cach sua.
- [ ] 1 doan ngan cho report:

```text
Qua kiem thu, he thong co the build frontend thanh cong, backend/arena import duoc va AI phan hoi trong cac case demo chinh. Benchmark duoc dung de so sanh Easy/Medium/Hard theo thoi gian phan hoi, completed_depth va kha nang xu ly threat nhu thang ngay hoac chan doi thu thang. Ket qua cho thay muc Hard tim sau hon nhung co the cham hon, trong khi Medium phu hop hon cho demo tuong tac.
```

### Phan thuyet trinh nen noi

- [ ] Trinh bay bang benchmark ngan gon.
- [ ] Noi ro benchmark doc lap voi deploy.
- [ ] Giai thich Easy/Medium/Hard khac nhau o depth, candidate limit va time limit.
- [ ] Demo UI online voi mot van choi that.

## Checklist tong hop cho nguoi lam report

Sau khi nhan ket qua tu 3 thanh vien, nguoi lam report tick cac muc sau:

- [ ] Da co link GitHub.
- [ ] Da co link Vercel.
- [ ] Da co link Render backend.
- [ ] Da co link Render arena.
- [ ] Da co anh chup app online.
- [ ] Da co anh chup Swagger docs.
- [ ] Da co bang giai thich thuat toan AI.
- [ ] Da co 3 tactical demo cases.
- [ ] Da co bang benchmark Easy/Medium/Hard.
- [ ] Da co danh sach kho khan va cach khac phuc.
- [ ] Da co huong phat trien tuong lai.

## Goi y chia phan trinh bay 15 phut

| Thoi luong | Nguoi trinh bay | Noi dung |
|---:|---|---|
| 2 phut | Nguoi lam report | Gioi thieu bai toan Gomoku/Caro 15x15 va muc tieu |
| 4 phut | Thanh vien AI core | Giai thich thuat toan va evaluator |
| 3 phut | Thanh vien Benchmark/UI | Benchmark, test va UI |
| 3 phut | Thanh vien Deploy | Demo online Vercel/Render |
| 2 phut | Nguoi lam report | Kho khan, han che, huong phat trien |
| 1 phut | Ca nhom | Q&A va ket luan |

## Tieu chi hoan thanh toi thieu

- [ ] App online mo duoc bang link Vercel.
- [ ] Backend health check tra ve `{"status":"ok"}`.
- [ ] AI di duoc nuoc tren frontend online.
- [ ] Co bang benchmark it nhat 2 case cho 3 difficulty.
- [ ] Co giai thich thuat toan AI bang ngon ngu de hieu.
- [ ] Co minh chung deploy va test de dua vao report.

## Tieu chi huong toi diem cao

- [ ] Demo duoc AI thang ngay va AI chan thang ngay.
- [ ] Giai thich duoc vi sao AI chon nuoc qua `reason`.
- [ ] Co so sanh Easy/Medium/Hard bang so lieu.
- [ ] Co noi ro he thong khong phai SOTA/RL, nhung co classical AI explainable.
- [ ] Co deploy public that, khong chi nop source code.
- [ ] Bao cao, slide va demo thong nhat voi nhau.
