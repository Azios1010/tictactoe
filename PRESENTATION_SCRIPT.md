# Script Thuyet Trinh Chi Tiet - Gomoku/Caro 15x15 AI

Muc tieu cua script nay: giup nhom thuyet trinh trong khoang 15 phut, noi dung bam sat `SLIDE_PRESENTATION_PLAN.md` va `REPORT_BTL.tex`.

Cach dung:

- Khong can doc y het tung chu tren san khau; dung nhu ban tap noi.
- Moi slide nen noi dung thoi gian goi y. Neu sap qua gio, bo cac cau co nhan `[co the rut gon]`.
- Khi noi ve model, giu dung framing: model la consultant/advisor va policy prior, khong thay the classical engine.
- Khi noi ve benchmark, khong claim AI manh hon Rapfi/Yixin hoac SOTA.

Tong thoi luong muc tieu: 15 phut.

## Phan Chia Thoi Gian Tong

| Phan | Slide | Thoi gian |
|---|---|---:|
| Mo dau va bai toan | 1-2 | 2.0 phut |
| Kien truc va AI core | 3-6 | 4.5 phut |
| Data va model | 7-10 | 4.0 phut |
| A/B benchmark va demo | 11-12 | 2.5 phut |
| Ket luan | 13 | 1.0 phut |
| Buffer | - | 1.0 phut |

## Slide 1: Tieu De Va Mo Ta Ngan

**Thoi gian:** 45 giay.

**Muc tieu:** Gioi thieu nhanh de tai, diem khac biet va tech stack.

**Loi noi chi tiet:**

> Kinh chao thay/co va cac ban. Nhom em xin trinh bay de tai Gomoku/Caro 15x15 AI.
>
> Day la mot he thong choi Gomoku giua nguoi choi va AI tren ban co 15x15. Diem trong tam cua du an khong chi la lam mot giao dien choi game, ma la xay dung mot AI co the dua ra nuoc di hop ly va giai thich duoc vi sao no chon nuoc do.
>
> AI chinh cua nhom la classical game search engine, gom minimax, alpha-beta pruning, iterative deepening, heuristic evaluator va threat detection. Ngoai ra, nhom co mo rong them mot CNN consultant model duoc train supervised tren data self-play. Model nay khong thay the AI chinh, ma dung de goi y nuoc di va ho tro sap xep candidate.
>
> Ve he thong, frontend dung React/Vite, backend dung FastAPI, con phan AI core va model inference duoc viet bang Python.

**Neu co demo/link:**

> Source code cua du an nam tren GitHub, va neu mang/on deployment san sang thi nhom co the demo truc tiep ung dung o cuoi bai.

**Chuyen slide:**

> Truoc khi vao thuat toan, em xin noi qua vi sao Gomoku 15x15 la mot bai toan kho hon nhieu so voi tic-tac-toe don gian.

## Slide 2: Bai Toan Va Thach Thuc

**Thoi gian:** 1 phut 15 giay.

**Muc tieu:** Lam ro khong gian tim kiem lon va nhu cau giam nhanh.

**Loi noi chi tiet:**

> Gomoku hay Caro la game hai nguoi choi. Moi nguoi lan luot dat quan len ban co. Ben nao tao duoc nam quan lien tiep theo hang ngang, hang doc hoac duong cheo thi thang.
>
> Trong du an nay, ban co co kich thuoc 15x15, tuc la co 225 o. Neu o dau game AI xet tat ca cac o trong, moi tang search co the co hang tram lua chon. Khi ap dung minimax nhieu tang, so trang thai tang theo ham mu.
>
> Vi vay, neu chi viet minimax don gian thi AI se rat cham, va trong ung dung that nguoi choi se phai doi lau. Muc tieu cua nhom la AI phai danh hop ly trong thoi gian ngan, dong thoi co the giai thich quyet dinh bang cac truong nhu `reason`, `evaluation` va `completed_depth`.
>
> Board trong engine duoc quy uoc rat don gian: `0` la o trong, `1` la quan AI, va `-1` la quan nguoi choi. Cach ma hoa nay giup backend va model deu xu ly board thong nhat.

**Diem nhan manh:**

> Y tuong chinh cua nhom la khong search tat ca moi thu, ma ket hop search co dien voi tri thuc rieng cua Gomoku: threat, open-four, block win, double-threat va cac pattern chien thuat.

**Chuyen slide:**

> Sau day la kien truc tong the cua he thong va cach cac thanh phan noi voi nhau.

## Slide 3: Kien Truc He Thong

**Thoi gian:** 1 phut.

**Muc tieu:** Noi ro frontend, backend, AI core, model, arena.

**Loi noi chi tiet:**

> He thong cua nhom duoc tach thanh ba phan chinh.
>
> Phan dau tien la frontend React/Vite. Frontend hien thi board, nhan thao tac click cua nguoi choi va goi API.
>
> Phan thu hai la backend FastAPI. Khi frontend goi `POST /api/get-move`, backend validate board, chon difficulty, sau do goi `GomokuAI` de lay nuoc di.
>
> Trong backend co hai nhom logic AI. Nhom chinh la classical engine, nam trong cac file nhu `ai_core.py`, `threats.py`, `evaluator.py` va `move_ordering.py`. Nhom phu la CNN consultant model, nam trong `dl/model.py` va `dl/predict_policy.py`.
>
> Phan thu ba la arena service. Arena cho phep AI tu dau va sinh JSONL data. Data nay duoc dung de phan tich va sau do train supervised consultant model.

**Neu chi vao diagram:**

> Luong chinh la: user click tren frontend, frontend gui board len backend, backend tra ve move analysis, sau do UI cap nhat nuoc di va ly do AI chon.

**Chuyen slide:**

> Bay gio em di vao pipeline ra quyet dinh cua AI core.

## Slide 4: AI Core Pipeline

**Thoi gian:** 1 phut 20 giay.

**Muc tieu:** Giai thich engine khong vao minimax ngay, ma co cac buoc tactical truoc.

**Loi noi chi tiet:**

> Day la pipeline chinh khi AI nhan mot board.
>
> Dau tien backend validate va normalize board neu can. Sau do engine khong chay minimax ngay, ma kiem tra cac case bat buoc truoc.
>
> Case quan trong nhat la immediate win: neu AI co nuoc thang ngay, AI phai danh nuoc do. Case thu hai la immediate block: neu doi thu sap thang, AI phai chan ngay.
>
> Tiep theo engine xem cac threat manh nhu double-threat hoac forcing move. Chi khi khong co nuoc bat buoc, AI moi sinh candidate quanh khu vuc da co quan, sap xep candidate, va search bang minimax alpha-beta.
>
> Ket qua cuoi cung duoc dong goi thanh `MoveAnalysis`, gom move, score, reason va completed depth. Day la ly do UI co the hien thi khong chi nuoc di, ma ca giai thich.

**Vi du ngan:**

> Neu AI tra `winning_move`, completed depth co the bang 0. Dieu do khong co nghia AI khong search duoc; no co nghia la engine da tim thay nuoc thang ngay truoc khi can search sau.

**Chuyen slide:**

> De pipeline nay chay nhanh, nhom su dung mot so ky thuat classical AI sau.

## Slide 5: Co So Ly Thuyet Classical AI

**Thoi gian:** 1 phut 20 giay.

**Muc tieu:** Giai thich tung thanh phan bang ngon ngu de hieu.

**Loi noi chi tiet:**

> Thanh phan nen tang la minimax. Minimax gia lap viec hai ben deu co gang chon nuoc tot nhat: AI toi da hoa diem, nguoi choi toi thieu hoa diem.
>
> Nhung minimax thuan tuy rat cham, nen nhom dung alpha-beta pruning de cat bo nhung nhanh khong con anh huong den quyet dinh cuoi cung.
>
> Iterative deepening giup AI tim tu do sau nho den do sau lon trong time limit. Neu het thoi gian, AI van co mot nuoc tot nhat da biet o do sau gan nhat.
>
> Candidate pruning giup giam branching factor: thay vi xet tat ca 225 o, AI chi xet nhung o gan cac quan da danh.
>
> Move ordering dua cac nuoc co kha nang tot len truoc. Dieu nay rat quan trong vi alpha-beta pruning cat nhanh tot hon khi nuoc manh duoc search som.
>
> Cuoi cung, Zobrist hash va transposition table giup cache cac trang thai da search, tranh tinh lai qua nhieu lan.

**Difficulty:**

> Easy uu tien toc do nen tat policy prior. Medium va Hard bat policy prior tu model, nhung van giu search co dien lam thanh phan quyet dinh.

**Chuyen slide:**

> Rieng voi Gomoku, neu chi co minimax va evaluator chung chung thi chua du. Can dua tri thuc threat vao AI.

## Slide 6: Threat Detection Va Reason

**Thoi gian:** 1 phut 10 giay.

**Muc tieu:** Cho thay AI co tri thuc Gomoku va giai thich duoc.

**Loi noi chi tiet:**

> Threat detection la phan dua tri thuc Gomoku vao engine. Thay vi chi dem diem chung chung, AI can hieu cac pattern nhu open-four, closed-four, open-three, broken-three va double-threat.
>
> Vi du, `winning_move` nghia la AI da co nuoc tao nam quan lien tiep. `blocking_win` nghia la doi thu sap thang va AI phai chan. `creating_open_four` la AI tao bon quan lien tiep co kha nang thang o luot sau.
>
> Cac reason nay co hai tac dung. Thu nhat, no giup move ordering vi AI biet nuoc nao can uu tien. Thu hai, no giup demo va bao cao ro hon, vi nguoi xem thay duoc ly do AI ra quyet dinh.
>
> Trong qua trinh cai tien, nhom cung viet regression tests cho cac case tactical de tranh viec AI danh sai nhung tinh huong co ban.

**Demo cue:**

> Neu demo, day la slide nen chuan bi mot board co bon quan lien tiep. Khi AI tra `winning_move` hoac `blocking_win`, giai thich se rat truc quan.

**Chuyen slide:**

> Sau khi co engine classical, nhom mo rong them phan data va model supervised.

## Slide 7: Data Va Kaggle Training

**Thoi gian:** 1 phut 15 giay.

**Muc tieu:** Noi ro data den tu dau, training la supervised, khong phai RL.

**Loi noi chi tiet:**

> Data cua nhom den tu arena/self-play. Arena cho AI tu dau va ghi lai cac sample JSONL.
>
> Moi sample gom board, target policy hoac distribution nuoc di, reward/outcome va mot so thong tin phu. Data nay duoc dung de train supervised model.
>
> Tong data nhom da doc gom 149 file, voi khoang 1.78 trieu sample. Trong do `data/` co hon 945 nghin sample, va `data/additional/` co hon 836 nghin sample.
>
> Khi train tren Kaggle, nhom dung file-level split. Nghia la cac file duoc chia rieng train, validation va test, giam nguy co cac sample qua gan nhau bi roi vao nhieu tap khac nhau.
>
> Diem can nhan manh la day khong phai reinforcement learning kieu AlphaZero. Model cua nhom la supervised learning tu data co san. No hoc xu huong nuoc di de lam advisor va policy prior.

**Cau phong thu neu bi hoi:**

> Vi the, trong bao cao nhom khong claim day la AlphaZero hay RL. No la mot supervised consultant model.

**Chuyen slide:**

> Tiep theo la kien truc va ket qua cua consultant model.

## Slide 8: CNN Consultant Model

**Thoi gian:** 1 phut 20 giay.

**Muc tieu:** Giai thich model input/output va metrics.

**Loi noi chi tiet:**

> Model nhan board 15x15 va encode thanh 3 channel: quan cua nguoi dang xet, quan doi thu, va o trong. Cach encode nay giup model hoc pattern khong gian tren board.
>
> Backbone la CNN, phu hop voi bai toan board vi cac pattern Gomoku thuong nam cuc bo theo hang, cot va duong cheo.
>
> Model co hai dau ra. Policy head tra ve 225 logits, tuong ung 225 o tren board. Value head tra ve mot gia tri scalar de uoc luong trang thai.
>
> Truoc khi lay top-k move, backend ap dung legal mask de loai cac o da co quan. Vi vay illegal top-1 sau mask bang 0.
>
> Ket qua tren test set 50 nghin sample: top-1 accuracy la 40.244%, top-3 la 59.974%, va top-5 la 69.194%. So nay cao hon rat nhieu so voi random legal va center-first baseline.

**Dien giai can than:**

> Tuy nhien, top-1 40% khong du de noi model luon chon nuoc toi uu. Gomoku co nhieu the co chi sai mot nuoc la thua ngay. Do do nhom khong de model tu quyet dinh nuoc di.

**Chuyen slide:**

> Vay model duoc tich hop vao AI chinh nhu the nao? Do la hybrid policy prior.

## Slide 9: Hybrid Policy Prior

**Thoi gian:** 1 phut 15 giay.

**Muc tieu:** Giai thich cach tich hop model an toan.

**Loi noi chi tiet:**

> Hybrid policy prior la cach nhom tich hop model vao engine ma van giu an toan cho tactical rules.
>
> Dau tien, classical engine van sinh candidate va kiem tra immediate win/block truoc. Neu AI co the thang ngay, AI danh ngay. Neu doi thu co the thang, AI chan ngay.
>
> Chi khi khong co nuoc bat buoc, engine moi goi consultant model de lay top-k legal moves. Xac suat cua model duoc doi thanh bonus cho move ordering.
>
> Diem quan trong la model khong hard-prune. Nghia la neu model khong goi y mot nuoc, nuoc do khong bi loai khoi search chi vi model bo qua. Search alpha-beta van la thanh phan quyet dinh cuoi cung.
>
> Ly do thiet ke nhu vay la top-1 cua model chua du cao de tin tuyet doi. Dung model lam prior thi an toan hon dung model lam player doc lap.

**Cau chot slide:**

> Co the hieu model nhu mot nguoi co van: no de xuat nuoc nao nen xem truoc, nhung engine classical moi la nguoi ra quyet dinh cuoi cung.

**Chuyen slide:**

> De chung minh model co hoc duoc gi do, nhom so sanh no voi baseline.

## Slide 10: Benchmark Model Va Baseline

**Thoi gian:** 1 phut.

**Muc tieu:** Giai thich metrics model va baseline, khong noi qua.

**Loi noi chi tiet:**

> Bang nay so sanh CNN consultant voi hai baseline don gian.
>
> Random legal gan nhu chi dung top-1 khoang 0.585%, vi tren board co rat nhieu o hop le. Center-first tot hon mot chut, top-1 khoang 2.352%, vi nhieu van co xu huong bat dau gan trung tam.
>
> CNN consultant dat top-1 40.244%, top-3 gan 60%, top-5 gan 69.2%. Dieu nay cho thay model hoc duoc xu huong nuoc di tu data self-play.
>
> Nhom cung kiem tra hai tactical diagnostics don gian: AI win horizontal va block human horizontal. Model deu dat hit trong top-1 va top-3.
>
> Nhung can doc ket qua nay dung muc: day la bang chung model co gia tri lam advisor va prior, khong phai bang chung no la engine Gomoku manh.

**Chuyen slide:**

> Cau hoi tiep theo la khi dua model vao engine, no co lam hong logic hay giup tot hon khong. Nhom dung A/B benchmark de kiem tra.

## Slide 11: A/B Benchmark Classical vs Hybrid

**Thoi gian:** 1 phut 35 giay.

**Muc tieu:** Giai thich bang A/B trung thuc, day la slide quan trong nhat de phong thu claim.

**Loi noi chi tiet:**

> Day la A/B benchmark giua hai ban engine tren cung cau hinh Medium.
>
> Ban Classical tat `policy_prior_weight`, tuc la khong dung model trong ordering. Ban Hybrid bat `policy_prior_weight=10000` va `policy_prior_top_k=24`. Hai ban dung cung depth, candidate limit va time limit. Model duoc warm-up truoc khi do de khong tinh chi phi load model vao latency.
>
> O cac case tactical nhu opening center, AI win horizontal va block human horizontal, hybrid van ra cung loai quyet dinh dung. Dieu nay cho thay policy prior khong pha cac rule bat buoc.
>
> O two-stones opening, classical va hybrid chon hai move khac nhau nhung cung reason `best_search_score`, cung completed depth 2 va cung score. Dieu nay cho thay model co tac dong den ordering, nhung search van giu do sau tuong duong.
>
> O scattered midgame va quiet midgame, hai ban gan nhu tuong duong ve depth va latency. Cac case non-forcing van cham gan time limit Medium, nen chua thay loi the latency ro.

**Ket luan can noi ro:**

> Ket qua nay la trung thuc: hybrid policy prior an toan voi tactical rules va co y nghia ve advisor/ordering, nhung benchmark nho nay chua du de noi AI manh hon ro ret. De chung minh playing strength, can mo rong thanh nhieu van self-play A/B.

**Neu can rut gon:**

> [co the rut gon] Noi ngan: hybrid khong lam hong engine, nhung chua tao loi the ro ve latency.

**Chuyen slide:**

> Sau phan thuc nghiem, em noi nhanh ve API, kiem thu va demo.

## Slide 12: Cai Dat, Kiem Thu Va Demo

**Thoi gian:** 1 phut 20 giay.

**Muc tieu:** Chung minh project chay that, co API/test/demo.

**Loi noi chi tiet:**

> Ve API, backend co `GET /api/health` de kiem tra server, `POST /api/get-move` de AI chon nuoc, `POST /api/get-consultation` de lay top-k move tu consultant model, va arena endpoint de tu dau.
>
> Nhom da kiem tra Python compile cho backend, arena va dl. Cac test quan trong gom `test_policy_prior_ordering`, `test_tactical_cases` va `test_consultant_api` deu pass. Arena smoke test cung pass voi mot van nho.
>
> Trong demo, nhom se mo app, choi mot nuoc Medium, sau do chi vao phan reason/evaluation/completed_depth. Neu bat consultant advisor, UI se hien top-k nuoc model goi y. Neu co thoi gian, nhom co the chay arena self-play de cho thay AI tu dau va sinh sample.

**Demo cue chi tiet:**

1. Mo app.
2. Chon Medium.
3. Dat mot nuoc gan trung tam.
4. Doi AI tra move.
5. Noi: "Day la reason AI tra ve, completed depth cho biet search da hoan thanh den do sau nao."
6. Bat consultant advisor.
7. Noi: "Cac badge/nuoc goi y nay den tu CNN consultant, nhung nuoc AI chinh van do search quyet dinh."

**Neu demo loi/mang cham:**

> Neu deployment bi cold start hoac mang cham, nhom co anh/video backup va co the demo local.

**Chuyen slide:**

> Cuoi cung la ket luan va huong phat trien.

## Slide 13: Ket Luan Va Huong Phat Trien

**Thoi gian:** 1 phut 10 giay.

**Muc tieu:** Chot dong gop, han che, future work.

**Loi noi chi tiet:**

> Tong ket lai, nhom da xay dung duoc mot he thong Gomoku/Caro 15x15 full-stack gom frontend, backend, AI core, consultant model va arena self-play.
>
> Dong gop AI chinh la classical search engine co kha nang giai thich: candidate generation, move ordering, threat detection, heuristic evaluator, minimax alpha-beta, iterative deepening va transposition table.
>
> Dong gop mo rong la CNN consultant model. Model hoc duoc policy tot hon baseline, dat top-1 40.244% va top-5 gan 69.2%. Tuy nhien, nhom tich hop model mot cach than trong: model chi lam advisor va policy prior, khong thay the search.
>
> Han che hien tai la he thong chua phai engine Gomoku cap thi dau, chua so sanh truc tiep voi Rapfi/Yixin, chua co full Threat Space Search hay VCF solver, va A/B benchmark con nho.
>
> Huong phat trien tiep theo la mo rong A/B benchmark thanh nhieu van self-play, cai thien evaluator, them tactical cases phuc tap hon, luu best move trong transposition table va nghien cuu VCF-lite hoac TSS-lite.

**Cau ket:**

> Nhom em xin ket thuc phan trinh bay tai day. Em cam on thay/co va cac ban da lang nghe, va nhom san sang tra loi cau hoi.

## Slide 14: Backup Demo / Appendix

**Khi nao dung:** chi dung neu con thoi gian hoac khi bi hoi sau.

**Loi noi neu mo backup metrics:**

> Day la bang metrics day du hon cua model. Diem dang chu y la illegal top-1 sau mask bang 0, vi backend mask cac o da co quan truoc khi lay top-k.

**Loi noi neu mo backup A/B:**

> Day la bang A/B day du. Nhom khong dung bang nay de claim hybrid nhanh hon, vi ket qua latency chua ro. Nhom dung no de chung minh hybrid khong pha tactical rules va co the tich hop an toan.

**Loi noi neu mo Swagger/API:**

> Day la API contract. Frontend gui board 15x15, backend tra ve row, col, evaluation, reason va completed_depth.

## Script Demo Neu Co 2 Phut Rieng

**Buoc 1: Mo app**

> Day la giao dien game. Board co kich thuoc 15x15, nguoi choi va AI lan luot danh.

**Buoc 2: Choi mot nuoc**

> Em dat mot quan gan trung tam. Frontend se gui board len backend qua `/api/get-move`.

**Buoc 3: AI tra move**

> Sau khi backend xu ly, AI tra ve move. O panel ben canh co reason, evaluation va completed depth. Reason giup ta hieu AI dang tan cong, phong thu hay di theo best search score.

**Buoc 4: Bat consultant**

> Khi bat consultant advisor, model CNN se goi y top-k nuoc di. Day la dau ra cua model sau legal mask. Tuy nhien, day chi la goi y; nuoc AI chinh van do engine search quyet dinh.

**Buoc 5: Ket noi voi report**

> Phan demo nay tuong ung voi pipeline trong bao cao: frontend gui board, backend validate, AI core search, model advisor ho tro, va UI hien thi ly do.

## Q&A Chi Tiet

### 1. AI co dung machine learning khong?

**Tra loi ngan:**

> Co, nhung machine learning khong phai thanh phan quyet dinh duy nhat. AI chinh van la classical search engine. Model CNN duoc train supervised de lam consultant advisor va policy prior.

**Tra loi day du:**

> Ban dau du an la classical AI. Sau do nhom train them CNN policy-value model tu data self-play. Khi tich hop, nhom khong de model tu danh, vi top-1 chua du cao. Model chi goi y top-k nuoc va them bonus vao move ordering.

### 2. Day co phai reinforcement learning khong?

> Khong. Model hien tai la supervised learning tu JSONL data. Nhom khong co vong lap AlphaZero kieu self-play + MCTS + update policy lien tuc. Arena sinh data, nhung training hien tai van la supervised.

### 3. Vi sao top-1 40% van dung duoc?

> Vi model khong dung de quyet dinh duy nhat. Top-1 40% cho thay model hoc duoc distribution tot hon baseline, nhung chua du tin de tu choi. Khi dung lam prior, no chi anh huong thu tu search, con legal rules, immediate win/block va alpha-beta van bao ve quyet dinh cuoi.

### 4. Model co cai thien AI khong?

> O muc hien tai, co the noi model cai thien pipeline bang cach cung cap advisor va policy prior. A/B benchmark cho thay hybrid khong pha tactical rules va giu completed depth tuong duong. Tuy nhien, chua du bang chung de ket luan playing strength tang ro ret. Can benchmark nhieu van hon.

### 5. Vi sao latency hybrid khong giam ro?

> Vi trong cac case non-forcing, engine van search gan chạm time limit Medium. Policy prior co the thay doi thu tu candidate, nhung neu search van bi gioi han boi time limit thi latency trung binh chua chac giam. Day la ly do nhom trinh bay no nhu prior/advisor, khong claim toi uu latency.

### 6. Co manh hon Rapfi hoac Yixin khong?

> Khong claim nhu vay. Rapfi va Yixin la engine Gomoku chuyen sau. Du an nay tap trung vao minh hoa classical search ket hop threat knowledge va supervised advisor trong pham vi mon hoc.

### 7. Vi sao completed depth co luc bang 0?

> Vi AI co cac buoc xu ly nhanh truoc search sau. Neu board trong, AI co the tra `opening_center`. Neu co nuoc thang ngay, AI tra `winning_move`. Neu phai chan thang, AI tra `blocking_win`. Nhung case nay khong can iterative deepening, nen completed depth bang 0 la hop ly.

### 8. Neu model goi y nuoc sai thi sao?

> Do la ly do nhom khong hard-prune theo model. Model chi them bonus ordering. Cac candidate khac van co the duoc search, va tactical rules nhu immediate win/block van duoc kiem tra truoc.

### 9. Data co bi leakage khong?

> Notebook train dung file-level split. Nghia la file du lieu duoc chia theo train/validation/test, giam nguy co cac sample qua gan nhau xuat hien o nhieu tap khac nhau.

### 10. Huong cai tien quan trong nhat la gi?

> Theo nhom, quan trong nhat la mo rong A/B benchmark thanh nhieu van self-play va them tactical suite phuc tap hon. Neu muon tang suc manh engine, nen cai thien evaluator, threat detector va them VCF-lite/TSS-lite truoc khi tang vai tro model.

## Ban Rut Gon 7 Phut Neu Bi Gioi Han

Neu chi co 7 phut, noi theo thu tu nay:

1. Slide 1: Gioi thieu de tai trong 30 giay.
2. Slide 2: Branching factor 15x15 trong 45 giay.
3. Slide 4: AI core pipeline trong 1 phut.
4. Slide 5: Minimax/alpha-beta/candidate pruning trong 1 phut.
5. Slide 8: Model metrics trong 1 phut.
6. Slide 9: Hybrid policy prior trong 1 phut.
7. Slide 11: A/B benchmark trong 1 phut.
8. Slide 13: Ket luan trong 45 giay.

**Cau ket ban rut gon:**

> Tom lai, du an ket hop classical search engine voi CNN advisor. Engine chinh van dam bao tactical decisions, con model ho tro goi y va ordering. Ket qua cho thay model tot hon baseline va hybrid tich hop an toan, nhung nhom khong claim SOTA hay manh hon engine chuyen nghiep.

## Loi Khuyen Khi Tap Noi

- Noi ro tu "classical engine la thanh phan quyet dinh chinh".
- Moi khi noi "model", them ngu canh "advisor" hoac "policy prior".
- Khi noi benchmark, dung tu "cho thay" thay vi "chung minh tuyet doi".
- Neu bi hoi kho, thua nhan gioi han va noi huong phat trien.
- Slide 11 la slide phong thu quan trong nhat: dung no de cho thay nhom danh gia trung thuc.
