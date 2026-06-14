# Presentation Q&A Detailed - Gomoku/Caro 15x15 AI

Tai lieu nay dung de tap tra loi phan hoi sau khi thuyet trinh slide moi. Moi cau co:

- **Tra loi ngan:** dung khi can tra loi trong 15-30 giay.
- **Giai thich chi tiet:** noi them khi giang vien hoi sau.
- **Can tranh:** nhung cach noi de bi bat be.

Nguyen tac an toan khi tra loi:

- Khong claim AI la state-of-the-art.
- Khong claim manh hon Rapfi/Yixin.
- Khong noi CNN thay the minimax/alpha-beta.
- Khong noi loss memory la reinforcement learning.
- Khong noi benchmark nho chung minh playing strength tong quat.
- Neu bi hoi kho, thua nhan gioi han va dua ra huong cai tien.

---

## 1. Vi sao repo ten `Tictactoe` nhung de tai la Gomoku/Caro 15x15?

**Tra loi ngan:**

> `Tictactoe` la ten lich su cua repository. Phan game hien tai da duoc phat trien thanh Gomoku/Caro 15x15, voi board 15x15 va dieu kien thang la 5 quan lien tiep.

**Giai thich chi tiet:**

Trong code, `BOARD_SIZE = 15`, `WIN_LENGTH = 5`. Frontend render ban co 15x15, backend validate board 15 hang 15 cot, AI core tim 5 quan lien tiep theo 4 huong. Vi vay noi dung ky thuat hien tai la Gomoku/Caro, khong phai tic-tac-toe 3x3.

**Can tranh:**

> "Ten repo khong quan trong."

Nen noi day la ten lich su, con noi dung hien tai da ro rang la Gomoku.

---

## 2. Bai toan chinh cua du an la gi?

**Tra loi ngan:**

> Bai toan la xay dung mot AI choi Gomoku/Caro 15x15 trong moi truong tuong tac, vua phai chon nuoc hop ly, vua phai phan hoi nhanh. Du an ket hop classical game search voi threat detection va CNN consultant model o vai tro ho tro.

**Giai thich chi tiet:**

Project co 3 phan chinh:

1. Frontend React/Vite de nguoi choi dau voi AI va xem arena.
2. Backend FastAPI de validate request va goi AI.
3. AI core gom minimax, alpha-beta, iterative deepening, candidate generation, evaluator, threat detection, Zobrist hash, transposition table, loss memory va policy prior.

**Can tranh:**

> "Day la web game la chinh."

Nen nhan manh trong mon AI, dong gop chinh la core AI va benchmark.

---

## 3. Vi sao Gomoku 15x15 kho hon tic-tac-toe 3x3?

**Tra loi ngan:**

> Tic-tac-toe chi co 9 o, con Gomoku 15x15 co 225 o. Neu search tat ca nuoc hop le, branching factor tang rat nhanh theo depth, nen can candidate pruning, move ordering, alpha-beta va heuristic evaluator.

**Giai thich chi tiet:**

O dau game, so nuoc hop le gan 225. Neu search depth 3 theo cach don gian, so nhanh co the len toi hang trieu. Vi vay AI khong duyet toan bo board ma chi sinh candidate quanh vung da co quan, dong thoi uu tien cac nuoc chien thuat.

**Can tranh:**

> "May tinh manh nen search het duoc."

Khong dung voi board 15x15 va yeu cau realtime.

---

## 4. Kien truc tong quan cua he thong la gi?

**Tra loi ngan:**

> He thong gom frontend, backend, AI core va CNN consultant model. Frontend gui board len FastAPI backend, backend goi `GomokuAI`, AI tra ve nuoc di, diem danh gia, reason va completed depth.

**Giai thich chi tiet:**

Luong chinh:

```text
Nguoi choi click
-> Frontend cap nhat board local
-> POST /api/get-move
-> Backend validate board/difficulty
-> GomokuAI.get_move_analysis()
-> Tra row, col, evaluation, reason, completed_depth
-> Frontend dat quan AI
```

Ngoai ra con co arena service cho self-play va consultant API cho model goi y top-K moves.

**Can tranh:**

> "Frontend tu tinh AI."

AI chinh nam o backend.

---

## 5. Cac file trong backend co vai tro gi?

**Tra loi ngan:**

> `main.py` la API FastAPI, `ai_core.py` la bo dieu phoi search, `ai_types.py` chua constants/config, `board_rules.py` chua luat ban co, `threats.py` nhan dien threat, `evaluator.py` cham diem board, `move_ordering.py` sinh va sap xep candidate.

**Giai thich chi tiet:**

Mapping nhanh:

| File | Vai tro |
|---|---|
| `main.py` | API, validation, difficulty config |
| `ai_core.py` | Minimax, alpha-beta, iterative deepening, TT, hash, loss memory |
| `ai_types.py` | `BOARD_SIZE`, `SearchConfig`, `MoveAnalysis`, `ThreatSummary` |
| `board_rules.py` | Winner check, bounds, empty cells, normalize |
| `threats.py` | Open-four, closed-four, open-three, broken-three |
| `evaluator.py` | Tinh `AI score - Human score` |
| `move_ordering.py` | Candidate generation, scoring, reason classification, policy prior |

**Can tranh:**

> "Tat ca AI nam trong mot file."

Hien tai AI da tach module ro rang.

---

## 6. Minimax trong du an hoat dong nhu the nao?

**Tra loi ngan:**

> Minimax gia dinh hai ben deu choi hop ly: AI chon nuoc lam diem cao nhat, nguoi choi chon nuoc lam diem AI thap nhat. Khi search den depth limit, AI dung evaluator de uoc luong board.

**Giai thich chi tiet:**

Tai node maximizing, AI thu cac candidate va lay score lon nhat. Tai node minimizing, engine gia dinh doi thu se chon nuoc lam score cua AI nho nhat. Vi khong the search den het van, leaf node duoc cham bang heuristic evaluator.

**Can tranh:**

> "Minimax dam bao tim nuoc toi uu."

Chi dung neu search toan bo game tree. O day co gioi han depth, candidate va time.

---

## 7. Alpha-beta pruning co lam thay doi ket qua minimax khong?

**Tra loi ngan:**

> Khong. Voi cung tap candidate va cung depth, alpha-beta chi cat cac nhanh khong anh huong den ket qua minimax, giup search nhanh hon.

**Giai thich chi tiet:**

`alpha` la diem tot nhat da biet cua AI, `beta` la diem tot nhat da biet cua doi thu. Khi `alpha >= beta`, nhanh hien tai khong the lam thay doi quyet dinh cuoi cung nen bo qua. Move ordering tot giup alpha-beta cat nhanh som hon.

**Can tranh:**

> "Alpha-beta la heuristic co the sai."

Alpha-beta la toi uu hoa cua minimax, khong phai ham danh gia.

---

## 8. Iterative deepening la gi?

**Tra loi ngan:**

> Iterative deepening search lan luot depth 1, depth 2, depth 3... Neu het thoi gian o depth cao, AI van co nuoc tot nhat tu depth da hoan thanh truoc do.

**Giai thich chi tiet:**

Co che nay phu hop voi UI realtime. Backend co time limit theo difficulty. AI khong bi treo vo han, va response tra ve `completed_depth` de biet search da hoan thanh den muc nao.

**Can tranh:**

> "AI luon search dung depth config."

Khong chac. Neu het time limit, completed depth co the thap hon depth config.

---

## 9. `completed_depth = 0` co phai loi khong?

**Tra loi ngan:**

> Khong. `completed_depth = 0` co the la fast-path tactical. Vi du board trong thi danh center, co nuoc thang ngay thi danh `winning_move`, can chan thang thi `blocking_win`, cac case nay khong can minimax.

**Giai thich chi tiet:**

`completed_depth` chi do depth cua iterative deepening. Neu AI quyet dinh truoc search bang tactical rule, depth se la 0 nhung do la hanh vi dung.

**Can tranh:**

> "Depth 0 nghia la AI khong suy nghi."

No co the da dung rule chien thuat nhanh.

---

## 10. Candidate generation la gi va vi sao can?

**Tra loi ngan:**

> Candidate generation la buoc loc ra cac o dang xem xet thay vi duyet ca 225 o. AI chi xet cac o trong gan cac quan da co va uu tien nuoc chien thuat, giup giam branching factor.

**Giai thich chi tiet:**

Trong Gomoku, phan lon nuoc co y nghia nam gan cac cum quan. `move_ordering.py` lay cac o trong trong radius quanh quan da danh, cham diem tung candidate, sap xep va cat theo `candidate_limit`.

**Can tranh:**

> "Candidate pruning khong bao gio bo sot."

Nen noi no la trade-off giua chat luong va toc do.

---

## 11. Candidate pruning co the bo sot nuoc tot khong?

**Tra loi ngan:**

> Ve ly thuyet co. Do do engine co cac lop bao ve nhu immediate win/block, forcing candidates va threat-aware ordering. Tuy nhien, cac chien luoc xa va dai han van la gioi han cua engine hien tai.

**Giai thich chi tiet:**

AI dam bao hon cho tactic gan:

- Thang ngay.
- Chan doi thu thang ngay.
- Tao/chan double threat.
- Open-four, closed-four.
- Candidate forcing khong bi cat bo chi vi `candidate_limit`.

Nhung khong nen claim engine tim moi chien luoc toan cuc.

**Can tranh:**

> "Loc candidate nhung van dam bao toi uu tuyet doi."

Khong dung.

---

## 12. Threat detection hoat dong nhu the nao?

**Tra loi ngan:**

> AI chuyen moi hang/cot/duong cheo thanh chuoi `0/1/2`: `1` la quan cua player dang xet, `0` la o trong, `2` la quan doi thu hoac bien. Sau do dem pattern nhu five, open-four, closed-four, open-three, broken-three.

**Giai thich chi tiet:**

Vi du `011110` la open-four: bon quan lien tiep va hai dau mo. Threat summary duoc dung trong evaluator, move ordering va reason classification.

**Can tranh:**

> "Threat detection la full Threat Space Search."

No chi la pattern-based detector, khong phai solver day du.

---

## 13. Open-four, closed-four, open-three, broken-three khac nhau the nao?

**Tra loi ngan:**

> Open-four la bon quan co hai dau mo, rat nguy hiem vi co hai diem thang. Closed-four la bon quan chi con mot dau mo hoac dang bi gioi han. Open-three la ba quan co the phat trien thanh open-four. Broken-three la ba quan co khoang trong o giua nhung van tao ap luc.

**Giai thich chi tiet:**

Thu tu uu tien thuong la:

1. Five/winning move.
2. Open-four.
3. Closed-four hoac block win.
4. Double threat.
5. Open-three/broken-three.

Tuy nhien context co the lam double open-three nguy hiem hon mot threat don le.

**Can tranh:**

> "Open-three luon kem closed-four."

Double threat co the thay doi do nguy hiem.

---

## 14. Double threat la gi?

**Tra loi ngan:**

> Double threat la khi mot nuoc di tao ra nhieu moi de doa cung luc, khien doi thu kho hoac khong the chan het trong mot luot.

**Giai thich chi tiet:**

Trong code, `ThreatSummary.double_threat` duoc tinh tu so forcing threats. AI co reason rieng nhu `creating_double_threat` va `blocking_double_threat`. Gomoku rat nhay voi double threat vi doi thu chi duoc di mot nuoc moi luot.

**Can tranh:**

> "Double threat luc nao cung thang."

Khong phai luc nao cung thang, nhung la tin hieu chien thuat rat manh.

---

## 15. Evaluator cham diem board nhu the nao?

**Tra loi ngan:**

> Evaluator tinh diem cho AI va nguoi choi rieng, sau do lay `AI score - Human score`. Diem gom threat score va contiguous pattern score, vi du open-four, closed-four, open-three, chuoi 2/3/4 quan co dau mo.

**Giai thich chi tiet:**

`evaluator.py` dung `ThreatDetector.summary()` de cham threat va quet cac chuoi lien tiep de cham local pattern. Diem thang/thua va open-four duoc cho rat cao de uu tien cac tinh huong bat buoc.

**Can tranh:**

> "Evaluator la oracle biet nuoc tot nhat."

Evaluator chi la heuristic approximation.

---

## 16. Tai sao tactical rules phai chay truoc minimax?

**Tra loi ngan:**

> Vi nhung tinh huong nhu thang ngay hoac doi thu sap thang khong can search sau. Xu ly truoc giup AI phan xa nhanh va tranh bo phi tai nguyen tinh toan.

**Giai thich chi tiet:**

Pipeline chinh:

```text
Validate/normalize
-> opening center
-> immediate win
-> immediate block
-> double-threat/forcing checks
-> candidate generation
-> iterative deepening minimax
```

Neu AI co nuoc thang ngay, no nen danh luon thay vi mat thoi gian search.

**Can tranh:**

> "Tactical rules chi la toi uu phu."

Trong Gomoku, tactical fast-path la lop an toan rat quan trong.

---

## 17. Forcing move va threat extension la gi?

**Tra loi ngan:**

> Forcing move la nuoc tao ap luc khien doi thu gan nhu bat buoc phai tra loi, vi du open-four. Threat extension cho phep AI search them mot doan ngan khi leaf node van con forcing threat.

**Giai thich chi tiet:**

Neu depth da ve 0 nhung board con cac threat nguy hiem, dung evaluator ngay co the bi "horizon effect". Threat extension giam rui ro do bang cach search them mot vai forcing candidates, nhung gioi han de khong bi no branching.

**Can tranh:**

> "Day la full VCF solver."

No chi la threat extension/forcing search gioi han.

---

## 18. Zobrist hash trong project dung de lam gi?

**Tra loi ngan:**

> Zobrist hash bien board thanh mot key 64-bit de tra cuu transposition table va loss memory. Hash nay giup AI nhan ra trang thai da tinh hoac trang thai tung co nuoc thua.

**Giai thich chi tiet:**

Moi o va moi loai quan co mot so random 64-bit co dinh. Hash board la XOR cua cac so tuong ung voi quan dang co tren board. O trong khong tham gia hash.

**Can tranh:**

> "Hash la ma hoa bao mat."

Khong. Day la hash cho game search/cache.

---

## 19. Vi sao hash phai co side-to-move?

**Tra loi ngan:**

> Cung mot board nhung neu toi luot AI di se khac voi toi luot nguoi choi di. Vi vay search hash phai XOR them key cua side-to-move de khong dung nham cache.

**Giai thich chi tiet:**

Trong minimax, node maximizing va minimizing co y nghia khac nhau. Neu chi hash board, transposition table co the lay diem cua trang thai "AI den luot" de dung cho trang thai "human den luot", lam sai ket qua search.

**Can tranh:**

> "Board giong nhau thi ket qua search giong nhau."

Khong dung neu khac nguoi den luot.

---

## 20. Transposition table luu nhung gi?

**Tra loi ngan:**

> Transposition table luu `depth`, `score`, `flag` va `best_move` cho moi search hash. No giup tai su dung ket qua khi game tree gap lai cung mot trang thai.

**Giai thich chi tiet:**

`flag` co 3 loai:

| Flag | Y nghia |
|---|---|
| `EXACT` | Diem chinh xac |
| `LOWERBOUND` | Diem la can duoi |
| `UPPERBOUND` | Diem la can tren |

Neu cached depth bang hoac sau hon depth hien tai, AI co the dung lai entry.

**Can tranh:**

> "Transposition table la tri nho hoc tap."

No la cache search, khac learning model.

---

## 21. Zobrist hash co collision khong?

**Tra loi ngan:**

> Ve ly thuyet co, vi hash 64-bit la huu han. Nhung xac suat collision trong pham vi project rat thap, nen engine chap nhan nhu nhieu game engine co dien.

**Giai thich chi tiet:**

Neu muon chat che hon co the luu them board signature de verify. Hien tai project uu tien don gian va toc do.

**Can tranh:**

> "Khong bao gio collision."

Ve ly thuyet la sai.

---

## 22. Loss memory da duoc trien khai chua?

**Tra loi ngan:**

> Da. Backend co `loss_memory`, frontend gui lich su cac nuoc AI khi nguoi choi thang. Backend ghi lai board truoc nuoc AI va nuoc AI da danh, sau do lan sau gap lai board do thi phat nang nuoc tung dan toi thua.

**Giai thich chi tiet:**

Luong hien tai:

```text
AI danh -> frontend luu board truoc nuoc AI
-> nguoi choi thang
-> POST /api/report-game-result
-> backend record_game_outcome()
-> save vao backend/gomoku_tt.pkl
-> lan sau _loss_memory_penalty() tru diem nuoc cu
```

Penalty hien tai la `2_500_000` moi lan thua.

**Can tranh:**

> "Loss memory la reinforcement learning."

Khong. No la bo nho kinh nghiem don gian dua tren hash board, khong co training policy/value.

---

## 23. Moi khi backend khoi dong co load lai cache va loss memory khong?

**Tra loi ngan:**

> Co. Khi `GomokuAI` duoc tao, no goi `load_memory()` de doc `backend/gomoku_tt.pkl`, load ca transposition table va loss memory. Khi tat backend binh thuong, `atexit` se save lai.

**Giai thich chi tiet:**

`main.py` tao AI bang:

```python
GomokuAI(memory_filename=BACKEND_DIR / "gomoku_tt.pkl")
```

`get_ai()` co `@lru_cache`, nen moi difficulty chi tao AI instance mot lan trong vong doi backend process. Cache khong load lai moi request, ma load khi instance duoc tao lan dau.

**Can tranh:**

> "Moi request deu doc file pkl."

Khong. AI instance duoc cache trong process.

---

## 24. Loss memory co gioi han gi?

**Tra loi ngan:**

> Co. No ghi tat ca nuoc AI trong van thua, khong phan biet chinh xac nuoc nao la sai lam quyet dinh. Vi vay no huu ich de tranh lap lai duong thua cu, nhung khong phai hoc chien luoc tong quat.

**Giai thich chi tiet:**

Rui ro:

- Phat ca nuoc khong thuc su sai.
- Chi khop khi gap lai board hash cu.
- Chua tong quat hoa sang cac the tuong tu.
- Arena self-play hien khong truc tiep report loss memory cho play backend.

Huong cai tien: chi record late-game blunder, giam trong so theo thoi gian, hoac ket hop phan tich tactical.

**Can tranh:**

> "Loss memory lam AI cang choi cang thong minh tong quat."

No chi la memory cuc bo.

---

## 25. CNN Consultant Model la gi?

**Tra loi ngan:**

> CNN Consultant la model policy-value supervised, nhan board 15x15 va goi y top-K nuoc di hop le. Trong project, no dong vai tro co van va policy prior, khong thay the AI core.

**Giai thich chi tiet:**

Input duoc encode thanh 3 channel:

1. Quan cua player dang xet.
2. Quan doi thu.
3. O trong.

Model co `policy_head` tra logits cho 225 o va `value_head` tra gia tri board tu -1 den 1. Trong AI core, policy probabilities duoc dung de sap xep candidate; value head chu yeu dung nhu thong tin phu/consultant.

**Can tranh:**

> "Model CNN la thanh phan quyet dinh nuoc di chinh."

Quyet dinh cuoi cung van dua tren classical search.

---

## 26. Policy prior la gi?

**Tra loi ngan:**

> Policy prior la xac suat nuoc di tu CNN duoc doi thanh bonus de sap xep candidate. Cong thuc la `bonus = probability * policy_prior_weight`.

**Giai thich chi tiet:**

Trong Medium:

```text
policy_prior_weight = 10,000
policy_prior_top_k = 24
```

Trong Hard:

```text
policy_prior_weight = 20,000
policy_prior_top_k = 32
```

Policy prior chi anh huong thu tu xet nuoc o root search. Neu model khong load duoc, bonus bang 0 va engine quay ve classical mode.

**Can tranh:**

> "Policy prior chon luon nuoc di."

Khong. No chi ho tro ordering.

---

## 27. Neu model CNN goi y sai thi AI co bi sai theo khong?

**Tra loi ngan:**

> Rui ro co, nhung duoc han che vi CNN khong hard-prune candidate va khong bo qua tactical rules. Immediate win/block, double threat va forcing checks van chay truoc search.

**Giai thich chi tiet:**

CNN chi cong bonus cho candidate ordering. Cac nuoc forcing van duoc giu lai. Sau do minimax/alpha-beta va evaluator van kiem tra cac line search. Do do model sai co the lam ordering kem hon, nhung khong truc tiep ep AI danh nuoc sai.

**Can tranh:**

> "Model sai khong anh huong gi ca."

Co the anh huong ordering/latency/chon candidate trong mot so truong hop, nhung da co co che bao ve.

---

## 28. Legal mask la gi?

**Tra loi ngan:**

> Legal mask la buoc gan diem rat thap cho cac o da co quan truoc khi softmax/top-K, de model khong goi y nuoc bat hop le.

**Giai thich chi tiet:**

Policy head tra logits cho ca 225 o. Nhung mot so o da co quan, nen `predict_policy.py` dung occupied mask de loai cac o nay. Sau mask, top-K chi gom o trong hop le.

**Can tranh:**

> "Model tu hieu luat nen khong can mask."

Mask la lop bao ve bat buoc.

---

## 29. Hybrid AI trong slide nghia la gi?

**Tra loi ngan:**

> Hybrid o day nghia la classical engine la thanh phan quyet dinh chinh, con CNN consultant ho tro bang advisor va policy prior. No khong phai hybrid theo nghia AlphaZero/MCTS/RL day du.

**Giai thich chi tiet:**

Classical engine dam nhiem:

- Immediate win/block.
- Threat detection.
- Evaluator.
- Minimax/alpha-beta.
- Time-limited search.

CNN ho tro:

- Goi y top-K cho nguoi dung.
- Cong policy prior vao move ordering.

**Can tranh:**

> "Hybrid AI nen AI cua minh ngang neural engine."

Khong co bang chung va khong dung pham vi.

---

## 30. Data train CNN den tu dau?

**Tra loi ngan:**

> Data den tu self-play/arena JSONL va cac sample duoc chuan hoa. Day la du lieu phu hop de train supervised advisor, nhung vi sinh tu engine noi bo nen khong the coi la label toi uu tuyet doi.

**Giai thich chi tiet:**

Arena co the luu:

- Board goc.
- Normalized board.
- Move duoc chon.
- Evaluation.
- Winner.
- Outcome.

Model hoc bat chuoc phan phoi nuoc di trong data. Neu data co bias, model co the hoc lai bias.

**Can tranh:**

> "Self-play data dam bao model hoc nuoc dung."

Khong dam bao. Can validation va benchmark rieng.

---

## 31. Top-1 accuracy khoang 40% co tot khong?

**Tra loi ngan:**

> Tot hon baseline random va center-first rat nhieu, nhung chua du de model tu danh doc lap. Ket qua nay phu hop voi vai tro advisor/top-K prior hon la thay the minimax.

**Giai thich chi tiet:**

Trong Gomoku, mot board co the co nhieu nuoc hop ly. Top-3 va Top-5 quan trong vi model chi can dua nuoc tot vao nhom ung vien. Vi vay dung model lam prior la hop ly hon dung lam player doc lap.

**Can tranh:**

> "40% chung minh model da manh."

No chung minh model hoc duoc distribution, khong chung minh suc choi tong quat.

---

## 32. Benchmark Classical vs Hybrid da chung minh dieu gi?

**Tra loi ngan:**

> Benchmark hien tai chu yeu chung minh hybrid tich hop an toan: khong pha tactical rules, khong chon illegal move va van giu duoc completed depth/latency hop ly. Chua du de ket luan hybrid manh hon tong quat.

**Giai thich chi tiet:**

De ket luan playing strength, can A/B self-play nhieu van voi cung time limit, do win rate, confidence interval, latency va tactical accuracy. Benchmark nho chi la bang chung ban dau.

**Can tranh:**

> "Hybrid chac chan manh hon classical."

Chua co bang chung du lon.

---

## 33. Vi sao latency hybrid khong giam ro ret?

**Tra loi ngan:**

> Vi trong cac case non-forcing, iterative deepening thuong search den gan time limit. Policy prior co the doi thu tu candidate, nhung neu search van dung het deadline thi latency khong nhat thiet giam.

**Giai thich chi tiet:**

Latency phu thuoc vao:

- Time limit.
- Candidate count.
- Move ordering.
- Transposition table hit.
- Tactical fast-path.
- Model inference.

Sau warm-up, inference model co the nho, nhung search van la phan ton thoi gian chinh.

**Can tranh:**

> "Hybrid nhanh hon trong moi case."

Khong nen noi qua muc.

---

## 34. Easy, Medium, Hard khac nhau the nao?

**Tra loi ngan:**

> Easy uu tien nhanh, depth va candidate limit thap. Medium can bang giua toc do va chat luong. Hard search sau hon, radius/candidate/time limit cao hon va policy prior manh hon.

**Giai thich chi tiet:**

Config hien tai:

| Difficulty | Depth | Candidate radius | Candidate limit | Time limit | Policy |
|---|---:|---:|---:|---:|---|
| Easy | 2 | 2 | 8 | 400 ms | Tat |
| Medium | 3 | 2 | 10 | 1200 ms | Weight 10,000 |
| Hard | 4 | 3 | 12 | 2200 ms | Weight 20,000 |

**Can tranh:**

> "Hard luon danh toi uu."

Hard chi search sau hon trong gioi han.

---

## 35. Frontend goi backend qua endpoint nao?

**Tra loi ngan:**

> Endpoint chinh la `POST /api/get-move`. Ngoai ra co `GET /api/health`, `POST /api/get-consultation` cho consultant va `POST /api/report-game-result` de report loss memory.

**Giai thich chi tiet:**

Request `get-move` gom board, player va difficulty. Response gom row, col, evaluation, reason, difficulty, completed_depth va message.

**Can tranh:**

> "Frontend tu tinh reason."

Reason tra tu backend AI.

---

## 36. Frontend co giup loss memory nhu the nao?

**Tra loi ngan:**

> Moi lan AI danh, frontend luu board truoc nuoc AI va toa do AI. Neu nguoi choi thang, frontend gui lich su do len `/api/report-game-result` de backend ghi loss memory.

**Giai thich chi tiet:**

Frontend khong hoc truc tiep. No chi dong vai tro thu thap history vong game. Backend moi la noi normalize, hash va save memory.

**Can tranh:**

> "Loss memory tu dong hoc moi van."

Hien tai chi ghi khi nguoi choi thang va frontend report duoc.

---

## 37. Arena mode dung de lam gi?

**Tra loi ngan:**

> Arena mode cho AI tu dau voi AI, sinh sample JSONL de phan tich, benchmark hoac train model sau nay. No cung giup demo self-play va smoke test engine.

**Giai thich chi tiet:**

Arena co API rieng:

```http
GET /arena/api/health
POST /arena/api/self-play
```

Sample co board, normalized board, move, evaluation, winner va outcome. Normalized board giup nguoi dang di luon duoc nhin nhu player `1`.

**Can tranh:**

> "Arena la reinforcement learning."

Hien tai arena sinh data/self-play, khong tu cap nhat policy bang RL.

---

## 38. Neu khong co model CNN thi he thong co chay duoc khong?

**Tra loi ngan:**

> Co. CNN consultant la optional. Neu PyTorch hoac checkpoint khong co, `predict_policy` tra `model_available = false`, policy prior bang 0 va classical engine van chay binh thuong.

**Giai thich chi tiet:**

Backend tach `requirements.txt` co ban va `requirements-ml.txt` cho ML. Dieu nay giup deploy backend classical nhe hon va khong phu thuoc GPU.

**Can tranh:**

> "Model la dependency bat buoc cua AI."

Khong dung.

---

## 39. Tai sao khong dung AlphaZero hoac reinforcement learning?

**Tra loi ngan:**

> Vi AlphaZero can self-play RL, MCTS, training lap lai va tai nguyen tinh toan lon. Pham vi project tap trung vao classical AI de giai thich duoc, co the demo realtime va ket hop CNN supervised nhu advisor.

**Giai thich chi tiet:**

AlphaZero-style can:

- Policy-value network.
- MCTS moi move.
- Self-play training nhieu vong.
- GPU/compute va benchmark lon.

Project hien tai khong claim RL, khong train online, khong phai AlphaZero thu nho.

**Can tranh:**

> "CNN cua minh la AlphaZero."

Khong dung.

---

## 40. Co so sanh voi Rapfi/Yixin khong?

**Tra loi ngan:**

> Khong so sanh truc tiep. Rapfi va Yixin la engine Gomoku/Renju chuyen sau. Du an chi so sanh theo phuong phap va baseline noi bo, khong claim manh hon cac engine do.

**Giai thich chi tiet:**

Muon so sanh cong bang can:

- Cung rule set.
- Adapter engine.
- Cung time control.
- Nhieu van dau.
- Cung hardware.
- Thong ke win rate.

Vuot pham vi project hien tai.

**Can tranh:**

> "Gan bang engine chuyen nghiep."

Khong co bang chung.

---

## 41. AI hien tai co manh khong?

**Tra loi ngan:**

> AI xu ly duoc cac tactical case co ban va choi hop ly trong demo, nhung chua nen claim la manh theo chuan thi dau. Suc manh bi gioi han boi depth, candidate pruning, evaluator va benchmark hien tai con nho.

**Giai thich chi tiet:**

Minh co the noi:

- Co immediate win/block.
- Co threat detection.
- Co alpha-beta va time limit.
- Co TT va loss memory.
- Co tactical benchmark noi bo.

Nhung can them self-play A/B lon hon de ket luan suc choi tong quat.

**Can tranh:**

> "AI danh tot moi the co."

Khong nen noi.

---

## 42. Cac test hien tai kiem tra gi?

**Tra loi ngan:**

> Test tap trung vao syntax/compile, tactical cases, policy prior ordering, consultant API va arena smoke test. Muc tieu la dam bao engine khong loi co ban va cac co che AI chinh van hoat dong.

**Giai thich chi tiet:**

Nhom test co the bao gom:

- `py_compile` backend/arena/dl.
- Tactical cases: immediate win/block, broken-four, double-threat.
- Policy prior ordering.
- Consultant fallback/model API.
- Arena smoke test.

**Can tranh:**

> "Tests pass nen AI da manh."

Tests chi chung minh hanh vi da test la dung.

---

## 43. Han che lon nhat cua AI hien tai la gi?

**Tra loi ngan:**

> Han che lon nhat la search van bi gioi han boi branching factor va time limit, threat detection con pattern-based, benchmark chua du lon va CNN prior chua du bang chung de claim tang playing strength tong quat.

**Giai thich chi tiet:**

Co the neu 4 diem:

1. Chua co full Threat Space Search/VCF.
2. Candidate pruning co the bo sot chien luoc xa.
3. Evaluator co the sai o the phuc tap.
4. CNN hoc tu data noi bo nen co the hoc lai bias.

**Can tranh:**

> "Khong co han che dang ke."

Giang vien rat de hoi xoay.

---

## 44. Neu co them thoi gian, nhom se cai tien gi?

**Tra loi ngan:**

> Uu tien dau tien la mo rong benchmark va tactical suite, sau do cai thien threat detector/evaluator, them VCF-lite/TSS-lite, roi moi toi uu search nhu killer move, history heuristic, PVS hoac parallel root search.

**Giai thich chi tiet:**

Thu tu hop ly:

1. Tactical benchmark lon hon.
2. A/B self-play Classical vs Hybrid.
3. Broken-four/double-threat evaluator tot hon.
4. VCF-lite hoac TSS-lite cho forcing lines.
5. Search optimization: killer/history/PVS.
6. Data/model: train voi data chat luong hon.

**Can tranh:**

> "Chi can tang depth."

Tang depth lam cham rat nhanh neu khong giam branching factor.

---

## 45. Slide co chu "THREAD DECTECTION", neu bi hoi thi tra loi sao?

**Tra loi ngan:**

> Do la loi chinh ta tren slide, dung phai la `THREAT DETECTION`. Phan code va noi dung ky thuat dang noi ve nhan dien threat trong Gomoku, khong phai thread.

**Giai thich chi tiet:**

Co the noi nhom se sua typo trong ban nop cuoi. Sau do quay lai noi dung chinh: threat detection gom open-four, closed-four, open-three, broken-three va double-threat.

**Can tranh:**

> "Thread cung duoc."

Khong. Thread va threat khac nhau.

---

## 46. Cau hoi demo: Neu backend offline thi sao?

**Tra loi ngan:**

> Frontend se bao backend unreachable va khong choi tiep duoc AI move cho den khi FastAPI backend chay lai. Day la hanh vi fallback UI, khong phai loi AI core.

**Giai thich chi tiet:**

Backend mac dinh chay o `http://127.0.0.1:8000`. Frontend goi API qua base URL/proxy. Neu request fail, UI set backend status offline va hien thong bao.

**Can tranh:**

> "Frontend van co AI offline."

Khong, AI chinh nam backend.

---

## 47. Neu nguoi choi danh nuoc rat bat ngo hoac xa trung tam thi AI co xu ly khong?

**Tra loi ngan:**

> AI van validate board va sinh candidate quanh cac quan da co, bao gom quan moi cua nguoi choi. Tuy nhien, cac chien luoc xa phuc tap van la gioi han cua candidate pruning.

**Giai thich chi tiet:**

Ngay khi nguoi choi dat mot quan xa, vung candidate moi se mo quanh quan do. AI se co the phan ung gan khu vuc nay. Nhung vi khong duyet toan bo board, khong nen claim no xu ly toi uu moi chien luoc toan cuc.

**Can tranh:**

> "AI khong bi anh huong boi pruning."

Pruning luon la trade-off.

---

## 48. Neu vua co nuoc thang cho AI vua doi thu cung dang doa thang thi AI chon gi?

**Tra loi ngan:**

> AI uu tien immediate win truoc. Neu AI co nuoc thang ngay, danh nuoc do ket thuc game, khong can chon block.

**Giai thich chi tiet:**

Pipeline trong `GomokuAI` kiem tra:

1. AI winning move.
2. Human winning move de block.
3. Double threat/forcing checks.

Thu tu nay hop ly vi thang ngay tot hon chan doi thu.

**Can tranh:**

> "AI luon block truoc."

Khong, neu AI co the thang ngay thi phai thang.

---

## 49. Vi sao reason trong response quan trong?

**Tra loi ngan:**

> `reason` giup giai thich vi sao AI chon nuoc do, vi du `winning_move`, `blocking_win`, `creating_open_four`, `building_attack`. No lam AI de debug va de trinh bay hon so voi chi tra toa do.

**Giai thich chi tiet:**

Reason duoc phan loai tu move ordering/threat summary. No khong phai giai thich hoan hao nhu proof tree, nhung du de UI va nguoi xem hieu do la nuoc tan cong, phong thu hay search score.

**Can tranh:**

> "Reason la chung minh toan hoc cho nuoc toi uu."

No la nhan loai heuristic.

---

## 50. Cau ket luan an toan nhat neu bi hoi tong quat la gi?

**Tra loi ngan:**

> Du an khong nham vuot cac engine thi dau, ma minh hoa cach xay mot AI Gomoku 15x15 thuc dung va giai thich duoc: classical search la loi chinh, threat knowledge giup xu ly chien thuat, cache/time limit giup realtime, CNN consultant chi ho tro advisor va policy prior.

**Giai thich chi tiet:**

Neu can tom tat trong 5 y:

1. Core la minimax/alpha-beta, khong phai RL.
2. Tactical rules chay truoc deep search.
3. Candidate generation giam branching factor.
4. Hash/TT/loss memory giup tai su dung va tranh lap loi cu.
5. CNN la ho tro hybrid, khong thay the engine.

**Can tranh:**

> "AI cua nhom da rat manh/gan SOTA."

Khong nen claim qua muc.

---

# Nhom Cau Hoi Can Hoc Thuoc

Neu thoi gian on tap it, uu tien 12 cau sau:

1. Hybrid AI trong project nghia la gi?
2. Policy prior co quyet dinh nuoc di khong?
3. Vi sao tactical rules chay truoc minimax?
4. Candidate generation giam branching factor nhu the nao?
5. Threat detection hoat dong bang pattern `0/1/2` ra sao?
6. Evaluator tinh `AI score - Human score` nhu the nao?
7. Zobrist hash va side-to-move de lam gi?
8. Transposition table khac loss memory nhu the nao?
9. Loss memory co phai reinforcement learning khong?
10. Neu khong co CNN model thi backend co chay khong?
11. Benchmark hien tai chung minh gi va chua chung minh gi?
12. Han che va huong phat trien tiep theo la gi?

# Cau Tra Loi Mau 1 Phut

> Du an cua nhom la Gomoku/Caro 15x15, khong phai tic-tac-toe 3x3. Core AI la classical game search: minimax, alpha-beta pruning, iterative deepening, candidate generation, move ordering, threat detection va heuristic evaluator. Vi board 15x15 co branching factor rat lon, AI khong duyet tat ca o ma chi xet candidate quanh cac quan da co, dong thoi uu tien tactical rules nhu thang ngay, chan thang, double threat va forcing moves. Zobrist hash va transposition table giup cache trang thai search, con loss memory giup tranh lap lai mot so nuoc tung dan toi thua. CNN consultant chi la thanh phan ho tro: goi y top-K va policy prior cho move ordering, khong thay the minimax. Nhom khong claim manh hon engine chuyen nghiep; muc tieu la minh hoa mot AI Gomoku thuc dung, giai thich duoc va co benchmark noi bo.
