# 20 Cau Hoi Giang Vien Kho Tinh Co The Hoi Va Dap An Chi Tiet

Tai lieu nay dung de tap Q&A sau khi thuyet trinh. Moi cau co:

- **Tra loi ngan:** cau tra loi 15-30 giay.
- **Giai thich chi tiet:** noi them neu giang vien hoi sau.
- **Can tranh:** nhung cau noi de bi bat be.

Nguyen tac chung:

- Khong claim AI la SOTA.
- Khong claim manh hon Rapfi/Yixin.
- Khong noi model thay the classical engine.
- Khong noi A/B benchmark nho la bang chung playing strength tang ro ret.
- Neu gap cau hoi kho, thua nhan gioi han va noi huong cai tien.

## 1. Vi sao repo ten `Tictactoe` nhung de tai lai la Gomoku/Caro 15x15?

**Tra loi ngan:**

> `Tictactoe` la ten lich su cua repository. Bai toan hien tai da duoc phat trien thanh Gomoku/Caro 15x15, khong phai tic-tac-toe 3x3. Trong report va code, board size, rule win 5 quan va AI core deu theo Gomoku 15x15.

**Giai thich chi tiet:**

Ban dau repo co the duoc tao voi ten tong quat/cu, nhung kien truc hien tai da thay doi. Evidence nam o:

- Board 15x15.
- Luat thang la 5 quan lien tiep.
- Backend co `BOARD_SIZE = 15`, `WIN_LENGTH = 5`.
- Frontend render board 15x15.
- Report va slide deu ghi ro project khong phai tic-tac-toe 3x3.

**Can tranh:**

> "Ten repo khong quan trong."

Nen noi ro day la ten lich su, con noi dung ky thuat hien tai la Gomoku.

## 2. Vi sao Gomoku 15x15 kho hon tic-tac-toe 3x3?

**Tra loi ngan:**

> Tic-tac-toe 3x3 chi co 9 o, con Gomoku 15x15 co 225 o. Neu dung minimax xet tat ca o trong, branching factor tang rat nhanh theo do sau search. Vi vay Gomoku can candidate pruning, move ordering, heuristic evaluator va time limit.

**Giai thich chi tiet:**

Trong game doi khang, minimax mo rong cay tim kiem theo so nuoc hop le. O dau game Gomoku co toi da 225 nuoc hop le. Neu search do sau 3 ma khong giam nhanh, so nhanh co the rat lon. Do do du an chi xet candidate quanh cac quan da co va uu tien tactical moves.

**Can tranh:**

> "May tinh hien nay manh nen van search duoc."

Sai framing. Nen nhan manh 15x15 can toi uu de chay tuong tac.

## 3. Minimax trong du an hoat dong nhu the nao?

**Tra loi ngan:**

> Minimax gia lap hai ben di toi uu: AI chon nuoc lam diem cao nhat, nguoi choi chon nuoc lam diem cua AI thap nhat. Diem board duoc tinh bang heuristic evaluator ket hop attack, defense va threat patterns.

**Giai thich chi tiet:**

Tai node cua AI, engine thu cac candidate moves va lay score lon nhat. Tai node cua doi thu, engine gia dinh doi thu cung choi hop ly va chon score nho nhat cho AI. Vi khong the search den het van, evaluator uoc luong gia tri board tai leaf node.

**Can tranh:**

> "Minimax dam bao tim nuoc toi uu."

Chi dung neu search full game tree. O day search bi gioi han depth, candidate va time limit, nen chi la toi uu trong pham vi search.

## 4. Alpha-beta pruning co lam thay doi ket qua minimax khong?

**Tra loi ngan:**

> Khong, alpha-beta pruning khong lam thay doi ket qua minimax tren cung tap candidate va cung do sau search. No chi cat nhung nhanh da chac chan khong anh huong den quyet dinh cuoi cung.

**Giai thich chi tiet:**

Alpha la diem tot nhat hien co cua maximizing player, beta la diem tot nhat hien co cua minimizing player. Khi alpha >= beta, nhanh hien tai khong the tao ket qua tot hon nua nen co the bo qua. Move ordering tot giup alpha-beta cat nhanh som hon.

**Can tranh:**

> "Alpha-beta la heuristic nen co the sai."

Alpha-beta khong phai heuristic danh gia; no la toi uu hoa cua minimax.

## 5. Candidate pruning co the bo sot nuoc thang hoac nuoc chan quan trong khong?

**Tra loi ngan:**

> Co rui ro neu pruning qua manh, nen engine xu ly immediate win/block truoc va sinh candidate quanh vung da co quan. Trong Gomoku, phan lon nuoc co y nghia chien thuat nam gan cac quan da danh. Tuy vay, day van la gioi han cua engine.

**Giai thich chi tiet:**

Du an giam rui ro bang cac buoc:

- Kiem tra nuoc thang ngay.
- Kiem tra nuoc chan doi thu thang ngay.
- Threat-aware move ordering.
- Regression tactical tests.

Nhung khong nen noi candidate pruning khong bao gio bo sot. Trong cac the dac biet, mot nuoc xa co the co y nghia chien luoc, va engine hien tai co the chua xet.

**Can tranh:**

> "Khong bao gio bo sot."

Nen noi "giam rui ro" thay vi "dam bao tuyet doi".

## 6. Vi sao `completed_depth = 0` van hop ly?

**Tra loi ngan:**

> Vi engine co cac rule xu ly nhanh truoc search sau. Neu board trong thi tra `opening_center`; neu co nuoc thang ngay thi tra `winning_move`; neu phai chan thang thi tra `blocking_win`. Cac case nay khong can iterative deepening, nen depth 0 la hop ly.

**Giai thich chi tiet:**

`completed_depth` cho biet do sau iterative search da hoan thanh. Neu engine quyet dinh truoc search bang tactical rule, no khong vao minimax depth 1/2/3, nen `completed_depth = 0`.

**Can tranh:**

> "Depth 0 la loi UI."

Khong. Phai giai thich no la fast-path tactical.

## 7. Threat detection cua nhom co phai full Threat Space Search khong?

**Tra loi ngan:**

> Khong. Threat detection cua nhom la pattern-based detector cho cac mau nhu open-four, closed-four, open-three, broken-three va double-threat. No ho tro evaluator va move ordering, nhung chua phai full Threat Space Search hay VCF solver.

**Giai thich chi tiet:**

Full Threat Space Search thuong tim chuoi forcing moves dai va co logic chuyen sau hon. Du an hien tai moi nhan dien threat patterns va co limited threat extension. Day la thanh phan tri thuc mien, khong phai solver day du.

**Can tranh:**

> "Co threat detection nen coi nhu TSS."

Giang vien de bat loi cau nay.

## 8. Open-four, closed-four, open-three, broken-three khac nhau the nao?

**Tra loi ngan:**

> Open-four la bon quan lien tiep co hai dau mo, rat nguy hiem vi co hai diem thang. Closed-four la bon quan nhung bi chan mot dau, van nguy hiem nhung de phong thu hon. Open-three la ba quan co kha nang phat trien thanh open-four. Broken-three la threat co khoang trong o giua, vi du dang bi dut mot o nhung van co tiem nang tao threat.

**Giai thich chi tiet:**

Do uu tien thuong la:

1. Five/winning move.
2. Open-four.
3. Closed-four/block win.
4. Double-threat.
5. Open-three/broken-three.

Tuy nhien, do nguy hiem thuc te phu thuoc vao context board.

**Can tranh:**

> "Open-three luon thua closed-four."

Khong tuyet doi, vi double open-three co the rat nguy hiem.

## 9. Evaluator can bang tan cong va phong thu nhu the nao?

**Tra loi ngan:**

> Evaluator cham diem board dua tren attack score va defense score, ket hop pattern score va threat score. AI khong chi toi da hoa threat cua minh, ma con tinh den threat cua doi thu. Immediate block cung duoc xu ly truoc search de tranh bo qua nuoc phong thu bat buoc.

**Giai thich chi tiet:**

Neu evaluator chi thien tan cong, AI co the bo qua doi thu sap thang. Du an giam rui ro bang:

- Immediate win/block.
- Threat detection cho ca hai ben.
- Move reason nhu `blocking_win`, `blocking_open_four`, `reducing_threat`.
- Tactical regression tests.

**Can tranh:**

> "Evaluator da toi uu hoan toan."

Nen noi evaluator van con la pattern-based va can cai tien.

## 10. Zobrist hashing va transposition table co vai tro gi?

**Tra loi ngan:**

> Zobrist hashing tao key nhanh cho trang thai board. Transposition table luu ket qua search cua cac trang thai da tinh de tranh tinh lai. Hash co tinh ca side-to-move de phan biet cung board nhung khac nguoi den luot.

**Giai thich chi tiet:**

Trong game tree, cung mot board co the dat duoc bang nhieu thu tu nuoc di. Neu khong cache, engine co the tinh lai. Transposition table luu depth, score, flag va co the luu best move. Du an hien co Zobrist hash va TT de ho tro search.

**Can tranh:**

> "TT lam AI nho va hoc nhu neural network."

Sai. TT la cache search, khong phai learning model.

## 11. Zobrist hash co collision khong? Neu co thi sao?

**Tra loi ngan:**

> Ve ly thuyet co the collision, vi hash la so huu han. Nhung voi 64-bit random keys, xac suat collision trong pham vi project rat thap. Du an chap nhan rui ro nay nhu nhieu engine game co dien.

**Giai thich chi tiet:**

Neu muon chac hon, co the luu them board signature hoac verify board khi lay entry tu TT. Hien tai project uu tien don gian va toc do, nen dung Zobrist hash theo cach thong dung.

**Can tranh:**

> "Khong the collision."

Ve ly thuyet la sai.

## 12. Data train model den tu dau va co dang tin khong?

**Tra loi ngan:**

> Data den tu arena/self-play JSONL. Tong du lieu khoang 1.78 trieu sample. Day la data phu hop de train supervised advisor, nhung vi sinh tu engine/self-play noi bo nen khong the coi la du lieu chuan toi uu nhu engine thi dau.

**Giai thich chi tiet:**

Data co gia tri vi:

- Cung format voi board backend.
- Co nhieu sample.
- Phan anh distribution nuoc di ma engine gap trong self-play.

Gioi han:

- Neu AI sinh data chua manh, model co the hoc lai diem yeu.
- Cac sample co prob all-zero/reward 0 can loc khi train policy.
- Can benchmark doc lap de danh gia model.

**Can tranh:**

> "Data self-play dam bao model hoc nuoc dung."

Khong dam bao. Chi la supervised signal.

## 13. Neu data sinh tu AI chua manh, model co hoc lai diem yeu khong?

**Tra loi ngan:**

> Co, do la rui ro thuc te. Vi vay nhom khong dung model lam player doc lap. Model chi lam advisor va policy prior. Quyet dinh cuoi cung van duoc bao ve bang immediate win/block, threat detection va alpha-beta search.

**Giai thich chi tiet:**

Model hoc theo distribution du lieu. Neu du lieu co bias, model co the lap lai bias. Cac cach cai tien:

- Sinh data tu engine manh hon.
- Loc tactical mistakes.
- Them benchmark tactical vao validation.
- Ket hop data tu nhieu difficulty.
- Chay A/B self-play de do playing strength.

**Can tranh:**

> "Nhieu data thi se tu het bias."

Nhieu data khong dam bao het bias neu source data cung bias.

## 14. Top-1 accuracy 40.244% co tot khong?

**Tra loi ngan:**

> Tot hon baseline rat nhieu, nhung chua du de model tu quyet dinh. Random legal top-1 khoang 0.585%, center-first khoang 2.352%, con CNN dat 40.244%. Ket qua nay tot cho advisor/top-k prior, nhung chua du de claim model la engine manh.

**Giai thich chi tiet:**

Trong game board 15x15, mot trang thai co nhieu nuoc hop ly gan nhau, nen top-1 khong nhat thiet phai gan 100%. Top-3 59.974% va top-5 69.194% cho thay model co kha nang dua nuoc hop ly vao nhom de xet. Do do top-k prior la cach dung phu hop hon so voi cho model tu danh.

**Can tranh:**

> "40% la thap nen model vo dung."

Khong dung. No co ich trong top-k advisor, nhung khong du lam player doc lap.

## 15. Legal mask la gi va vi sao quan trong?

**Tra loi ngan:**

> Legal mask la buoc gan diem rat thap cho cac o da co quan truoc khi softmax/top-k, de model khong chon nuoc bat hop le. Trong ket qua, illegal top-1 sau mask bang 0, nghia la output cuoi cung khong goi y o da bi chiem.

**Giai thich chi tiet:**

Policy head tra 225 logits cho ca board. Neu khong mask, model co the cho xac suat cao vao o da co quan. Legal mask dung occupancy cua board goc de loai cac o nay. Vi the illegal top-1 before mask co the cao, nhung after mask bang 0.

**Can tranh:**

> "Model tu hieu luat nen khong can mask."

Khong nen noi vay. Mask la lop bao ve bat buoc.

## 16. Model co that su cai thien quyet dinh cua AI chinh khong?

**Tra loi ngan:**

> Hien tai co the noi model cai thien pipeline bang advisor va policy prior, nhung chua du bang chung de ket luan playing strength tang ro ret. A/B benchmark cuc bo cho thay hybrid khong pha tactical rules va completed depth tuong duong, nhung can self-play A/B nhieu van hon.

**Giai thich chi tiet:**

Model co the cai thien move ordering neu dua move tot len som, giup alpha-beta prune tot hon. Tuy nhien benchmark hien tai nho:

- Tactical cases da duoc classical rules xu ly tot.
- Midgame cases gan time limit nen latency khong giam ro.
- Chua co tournament self-play du lon.

Vay ket luan dung muc la "co tiem nang va da tich hop an toan", khong phai "chac chan manh hon".

**Can tranh:**

> "Co model nen AI thong minh hon chac chan."

Day la claim de bi hoi vat.

## 17. A/B benchmark cua nhom da du chua?

**Tra loi ngan:**

> Chua du de ket luan suc choi tong quat. No du de kiem tra tich hop ban dau: hybrid khong pha opening, winning move, blocking move va giu completed depth tuong duong trong mot so case. De ket luan manh hon, can A/B self-play nhieu van voi cung time limit.

**Giai thich chi tiet:**

A/B hien tai co gia tri vi:

- Cung Medium config.
- Cung depth/candidate/time limit.
- Model warm-up truoc khi do.
- Co case tactical va non-forcing.

Nhung han che:

- So case nho.
- Chua phai tournament.
- Chua co confidence interval.
- Chua so sanh win-rate.

**Can tranh:**

> "A/B nay chung minh hybrid tot hon classical."

Nen noi "cho thay hybrid tich hop an toan".

## 18. Vi sao latency hybrid khong giam ro ret?

**Tra loi ngan:**

> Vi cac case non-forcing van gan cham time limit Medium. Policy prior co the thay doi thu tu candidate, nhung neu search van chay den gan deadline thi latency trung binh khong giam ro. Model inference sau warm-up chi khoang 1-2 ms, khong phai nut that lon.

**Giai thich chi tiet:**

Latency phu thuoc vao:

- Time limit.
- Candidate count.
- Branching factor.
- Move ordering.
- Transposition table hit.
- Tactical fast-path.

Trong tactical cases, engine tra nhanh truoc search sau. Trong non-forcing cases, engine search den deadline, nen prior chua chac lam giam elapsed time.

**Can tranh:**

> "Hybrid nhanh hon."

Chi co mot vai case nhanh hon; tong quat chua ro.

## 19. Nhom co so sanh voi Rapfi/Yixin/AlphaZero-Gomoku khong?

**Tra loi ngan:**

> Khong so sanh truc tiep. Nhom chi so sanh theo phuong phap va baseline noi bo. Rapfi/Yixin la engine chuyen sau, AlphaZero-Gomoku la huong RL/MCTS/neural network khac. Du an khong claim manh hon cac he thong do.

**Giai thich chi tiet:**

Ly do khong so sanh truc tiep:

- Can cung rule set.
- Can adapter engine.
- Can nhieu van dau.
- Can cung hardware/time control.
- Vuot pham vi mon hoc.

Framing dung la: project minh hoa classical search + Gomoku threat knowledge + supervised advisor.

**Can tranh:**

> "Gan bang engine chuyen nghiep."

Khong co bang chung.

## 20. Neu co them 2 tuan, nhom uu tien cai tien gi?

**Tra loi ngan:**

> Em se uu tien mo rong A/B benchmark va tactical suite truoc, sau do cai thien evaluator/threat detector. Ly do la phai co benchmark du tot moi biet cai tien co that su giup AI hay khong. Sau do moi tang vai tro model hoac them VCF-lite/TSS-lite.

**Giai thich chi tiet:**

Thu tu uu tien hop ly:

1. A/B self-play nhieu van: do win-rate, latency, illegal move, completed depth.
2. Tactical suite: broken-four, double-threat, diagonal forcing, defense traps.
3. Evaluator/threat detector: giam false positive/false negative.
4. Transposition table luu best move de cai thien ordering.
5. VCF-lite/TSS-lite cho cac chuoi forcing.
6. Data/model: train voi data chat luong hon, them tactical validation.

**Can tranh:**

> "Tang depth la xong."

Tang depth co the lam cham rat nhanh neu khong cai thien ordering/evaluator/benchmark.

## 21. Vi sao khong dung model neural network de danh truc tiep nhu AlphaZero?

**Tra loi ngan:**

> Vi pham vi du an va chat luong model hien tai chua phu hop. AlphaZero can self-play RL, MCTS va nhieu tai nguyen train. Model cua nhom la supervised CNN, top-1 khoang 40%, nen phu hop lam advisor/prior hon la player doc lap.

**Giai thich chi tiet:**

AlphaZero-style gom:

- Neural policy-value network.
- MCTS trong moi move.
- Self-play RL lap lai nhieu vong.
- Training compute lon.

Du an hien tai tap trung classical AI explainable, nen tich hop model nhu prior la cach vua suc va an toan.

**Can tranh:**

> "Model cua nhom la AlphaZero thu nho."

Khong dung.

## 22. Heuristic evaluator co the bi overfit vao benchmark khong?

**Tra loi ngan:**

> Co kha nang neu chi toi uu theo vai case benchmark. Vi vay benchmark can mo rong va tach tactical tests thanh nhieu nhom. Hien tai nhom chi ket luan AI xu ly tot cac case co ban, khong ket luan tong quat cho moi the co.

**Giai thich chi tiet:**

De giam overfit benchmark:

- Them nhieu case khac nhau.
- Randomize midgame positions.
- Chay self-play A/B.
- Giu regression tests cho bug cu.
- Kiem tra latency va completed depth.

**Can tranh:**

> "Benchmark 8/8 nen AI da tot."

8/8 chi co nghia dung tren benchmark do.

## 23. Neu nguoi choi danh mot nuoc bat ngo hoac xa vung trung tam, AI co xu ly khong?

**Tra loi ngan:**

> AI van validate board va sinh candidate quanh cac quan da co. Neu nguoi choi danh xa, vung candidate se mo quanh quan do. Tuy nhien, candidate pruning co gioi han radius/limit, nen cac chien luoc xa phuc tap co the chua duoc xu ly toi uu.

**Giai thich chi tiet:**

Board 15x15 lon nen engine chap nhan trade-off:

- Candidate gan quan giup chay nhanh.
- Tactical fast-path giup tranh loi mot nuoc.
- Nhung long-term global strategy chua phai diem manh.

**Can tranh:**

> "AI xu ly tot moi chien luoc bat ngo."

Khong co bang chung.

## 24. Cac test hien tai kiem tra cai gi?

**Tra loi ngan:**

> Test hien tai tap trung vao syntax/compile, tactical cases, policy prior ordering, consultant API va arena smoke test. Muc tieu la dam bao engine khong bi loi co ban, tactical fast-path con dung va model integration khong pha backend.

**Giai thich chi tiet:**

Nhung nhom test chinh:

- Python compile backend/arena/dl.
- `tests.test_policy_prior_ordering`: prior chi anh huong khi bat, khong dung sai luc.
- `tests.test_tactical_cases`: immediate win/block va case chien thuat.
- `tests.test_consultant_api`: model path, fallback, validation.
- Arena smoke: chay self-play nho.

**Can tranh:**

> "Tests pass nen AI manh."

Tests pass chi chung minh cac hanh vi da test dung.

## 25. Tai sao Easy tat policy prior, con Medium/Hard bat?

**Tra loi ngan:**

> Easy uu tien toc do va don gian, nen tat policy prior. Medium va Hard co time limit lon hon, nen co the dung model prior de sap xep candidate. Day cung giup demo ro su khac biet giua che do nhanh va che do co hybrid.

**Giai thich chi tiet:**

Policy prior co chi phi inference nho sau warm-up, nhung van la mot thanh phan phu. Easy nen tra nhanh va tranh phu thuoc model. Medium/Hard co search sau hon, move ordering quan trong hon, nen prior co y nghia hon.

**Can tranh:**

> "Easy yeu vi khong co model."

Easy duoc thiet ke uu tien latency, khong phai phien ban day du.

## Tom Tat Cau Tra Loi An Toan Nhat

Neu bi hoi bat ngo, co the dua ve 5 y sau:

1. AI chinh la classical search engine, model chi la advisor/policy prior.
2. Tactical rules nhu immediate win/block duoc xu ly truoc search sau.
3. Model top-1 40.244% tot hon baseline nhung chua du lam player doc lap.
4. A/B benchmark cho thay hybrid tich hop an toan, chua chung minh manh hon ro ret.
5. Gioi han tiep theo la can A/B self-play nhieu van, tactical suite lon hon va evaluator/threat detector tot hon.
