# Huong Dan Cong Viec 3 Nguoi: Rapfi Teacher Data Va DL Policy Baseline

Muc tieu: tao du lieu huan luyen deep learning bang cach dung Rapfi/Gomocup engine lam teacher, train mot policy model nho, va neu kip thi nhung model vao AI hien tai nhu policy booster. AI chinh cua du an van la classical search engine gom minimax/alpha-beta, threat detection, evaluator va loss memory.

Khong claim model deep learning la SOTA, khong claim manh hon Rapfi/Yixin. Phan DL duoc trinh bay nhu mot baseline/hybrid extension hoc tu teacher engine.

## 1. Ket Qua Cuoi Cung Can Co

### Bat buoc

- Rapfi chay duoc local va co ghi ro version/rule/time limit.
- Dataset teacher-labeled:
  - `data/teacher/rapfi_teacher_raw.jsonl`
  - `data/teacher/train.jsonl`
  - `data/teacher/val.jsonl`
  - `data/teacher/test.jsonl`
  - `data/teacher/data_stats.json`
- Script tao du lieu:
  - `teacher/rapfi_client.py`
  - `scripts/build_teacher_dataset.py`
  - `scripts/augment_policy_dataset.py`
- Model policy baseline:
  - `dl/model.py`
  - `dl/train_policy.py`
  - `dl/evaluate_policy.py`
  - `dl/predict_policy.py`
- Ket qua danh gia:
  - `policy_eval_results.json`
  - Bang top-1/top-3/top-5 accuracy.
- Noi dung report/slide:
  - Nguon du lieu.
  - Teacher engine.
  - Kich thuoc dataset.
  - Accuracy.
  - Han che.

### Neu con thoi gian

- Hybrid policy booster:
  - Model du doan top-k moves.
  - Engine them top-k vao candidates.
  - Classical minimax/alpha-beta van quyet dinh cuoi.
- Benchmark nho:
  - `project_medium`
  - `dl_policy_only`
  - `hybrid_policy_booster`
- Arena nho 5-20 games de so sanh classical vs hybrid.

## 2. Kien Truc Du Kien

```text
Board sources
  -> tactical cases
  -> random legal boards
  -> arena states
  -> loss-memory / human correction states

Board samples
  -> Rapfi teacher
  -> teacher best move
  -> raw JSONL
  -> augmentation
  -> train/val/test
  -> CNN policy model
  -> top-k move prediction
  -> optional hybrid candidate booster
```

## 3. Format Du Lieu

Moi sample nen co dang:

```json
{
  "board": [[0, 0, 0]],
  "target_move": [7, 8],
  "target_index": 113,
  "teacher": "rapfi",
  "teacher_version": "dien_version",
  "rule": "freestyle_15x15",
  "source": "random_midgame",
  "tag": "midgame",
  "moves_played": 12
}
```

Quy uoc:

- `board`: 15x15, gia tri `0`, `1`, `-1`.
- `target_move`: `[row, col]` do Rapfi teacher chon.
- `target_index = row * 15 + col`.
- `source`: `tactical`, `random_midgame`, `arena_state`, `loss_memory`, `human_correction`.
- `tag`: `winning_move`, `blocking_win`, `broken_four`, `double_threat`, `midgame`, ...

## 4. Chia Viec 3 Nguoi

## Nguoi 1: Rapfi Integration

### Muc tieu

Lam cho project goi duoc Rapfi nhu teacher engine tu script Python.

### Viec can lam

1. Tai Rapfi tu Gomocup hoac GitHub.
2. Chay thu Rapfi local.
3. Ghi lai:
   - Link tai.
   - Version.
   - Rule dang dung.
   - Time limit moi move.
   - Cach chay tren Windows.
4. Viet `teacher/rapfi_client.py`.
5. Input cua client:
   - board 15x15.
   - player dang di, neu can.
   - time limit.
6. Output cua client:
   - `target_move`.
   - raw response/log neu can debug.
7. Xu ly loi:
   - teacher timeout.
   - teacher tra move occupied.
   - teacher tra move ngoai board.
   - process crash.

### Ket qua can nop

- `teacher/rapfi_client.py`
- `teacher/test_rapfi_client.py` neu kip
- `docs/rapfi_teacher_notes.md` hoac mot section trong file nay gom:
  - Cach tai/chay Rapfi.
  - Rule/time limit.
  - Vi du board input va move output.

### Yeu to quan trong

- Rule phai gan voi project: Gomoku/Caro 15x15 freestyle neu co.
- Neu Rapfi rule khac, phai ghi ro trong report.
- Teacher move phai la o trong hop le.
- Khong de script treo vo han; phai co timeout.

## Nguoi 2: Dataset Engineer

### Muc tieu

Tao board samples, goi Rapfi teacher lay label, augment va chia train/val/test.

### Viec can lam

1. Tao board source:
   - Lay tactical cases tu `tests/fixtures/tactical_cases.jsonl`.
   - Sinh random legal boards 5-30 nuoc.
   - Lay arena states neu co.
   - Lay loss-memory/human correction states neu co.
2. Viet `scripts/build_teacher_dataset.py`.
3. Voi moi board:
   - Kiem tra board 15x15.
   - Kiem tra chua co winner.
   - Goi `rapfi_client`.
   - Kiem tra teacher move hop le.
   - Luu vao `rapfi_teacher_raw.jsonl`.
4. Viet augmentation:
   - rotate 90/180/270.
   - mirror ngang/doc.
   - optional shift neu khong vuot bien.
5. Transform dung target move.
6. Loai duplicate.
7. Chia dataset:
   - train: 80%.
   - val: 10%.
   - test: 10%.
8. Xuat `data_stats.json`.

### Ket qua can nop

- `data/teacher/rapfi_teacher_raw.jsonl`
- `data/teacher/train.jsonl`
- `data/teacher/val.jsonl`
- `data/teacher/test.jsonl`
- `data/teacher/data_stats.json`
- `scripts/build_teacher_dataset.py`
- `scripts/augment_policy_dataset.py`

### Yeu to quan trong

- Label chinh phai den tu Rapfi, khong lay move cua AI hien tai lam nhan chinh.
- Tactical labels co the uu tien nhan thu cong neu Rapfi rule cho move khac do khac luat.
- Board co winner phai bi loai.
- Target move phai nam tren o trong.
- Augmentation phai transform ca board va target move.
- Khong de train/val/test bi leak duplicate sau augmentation.

### Muc tieu so luong

| Muc | Board goc | Sau augmentation | Ghi chu |
|---|---:|---:|---|
| Toi thieu | 300-500 | 2400-4000 | Du demo pipeline |
| Tot | 1000-2000 | 8000-16000 | Du train CNN nho on hon |
| Rat tot | 3000+ | 24000+ | Chi lam neu Rapfi wrapper on dinh |

## Nguoi 3: DL Model, Evaluation Va Hybrid

### Muc tieu

Train CNN policy model tu dataset Rapfi teacher, danh gia top-k accuracy, va neu kip nhung model vao engine nhu policy booster.

### Viec can lam

1. Viet dataset loader doc JSONL.
2. Chuyen board thanh tensor:
   - channel 1: AI stones.
   - channel 2: human stones.
   - optional channel 3: empty/current player.
3. Viet CNN nho:
   - 2-4 convolution layers.
   - output 225 logits.
   - loss: cross entropy voi `target_index`.
4. Train:
   - train loss.
   - val top-1/top-3/top-5.
   - save checkpoint tot nhat.
5. Evaluate tren test set.
6. Viet `predict_policy.py`:
   - input board.
   - output top-k moves.
7. Neu kip, hybrid:
   - load model optional trong backend.
   - lay top-5 moves.
   - them vao candidate list neu hop le.
   - cong bonus nho trong move ordering.
   - immediate win/block/loss memory van uu tien hon model.

### Ket qua can nop

- `dl/model.py`
- `dl/train_policy.py`
- `dl/evaluate_policy.py`
- `dl/predict_policy.py`
- `models/rapfi_policy_baseline.pt`
- `policy_eval_results.json`
- Bang so sanh:
  - top-1 accuracy.
  - top-3 accuracy.
  - top-5 accuracy.
  - inference time.

### Yeu to quan trong

- Model khong thay engine chinh.
- Model khong duoc override immediate win/block.
- Neu model goi y illegal move thi bo qua.
- Nen demo top-k prediction truoc, hybrid la optional.
- Bao cao phai noi ro model hoc theo Rapfi teacher, khong phai tu RL.

## 5. Timeline 7 Ngay

| Ngay | Nguoi 1: Rapfi | Nguoi 2: Data | Nguoi 3: Model |
|---|---|---|---|
| 1 | Tai/chay Rapfi, ghi version/rule | Chuan bi board source | Tao skeleton model + loader |
| 2 | Viet wrapper Rapfi | Sinh tactical/random boards | Doc JSONL, train mock data |
| 3 | Test wrapper voi 20-50 board | Goi teacher tao raw data nho | Train thu data nho |
| 4 | Fix timeout/protocol | Tao dataset chinh + clean | Train model chinh |
| 5 | Ho tro debug teacher | Augment + split + stats | Evaluate top-k |
| 6 | Dong goi cach chay Rapfi | Final dataset | Predict script + optional hybrid |
| 7 | Ghi notes cho report | Ho tro bang data stats | Report/slide/demo evidence |

## 6. Checklist Chat Luong Dataset

- [ ] Moi board co kich thuoc 15x15.
- [ ] Moi cell thuoc `-1`, `0`, `1`.
- [ ] Board chua co winner truoc khi teacher move.
- [ ] `target_move` nam trong board.
- [ ] `target_move` la o trong.
- [ ] `target_index = row * 15 + col`.
- [ ] Co truong `teacher`, `rule`, `source`, `tag`.
- [ ] Khong co duplicate giua train/val/test.
- [ ] Augmentation transform dung target move.
- [ ] Co thong ke so sample theo source/tag.

## 7. Checklist Model

- [ ] Train script chay duoc tu dau den cuoi.
- [ ] Co validation accuracy.
- [ ] Co test accuracy.
- [ ] Co top-1/top-3/top-5.
- [ ] Co checkpoint model.
- [ ] `predict_policy.py` tra top-k moves hop le.
- [ ] Model inference khong qua cham cho demo.
- [ ] Neu hybrid, tactical rules van uu tien truoc model.

## 8. Checklist Bao Cao Va Slide

- [ ] Noi ro Rapfi la teacher engine.
- [ ] Noi ro dataset khong lay label tu AI yeu hien tai.
- [ ] Co bang so luong dataset.
- [ ] Co bang top-k accuracy.
- [ ] Co minh hoa pipeline:

```text
Rapfi teacher -> teacher-labeled dataset -> CNN policy -> top-k moves -> hybrid search
```

- [ ] Noi ro model khong thay the classical engine.
- [ ] Khong claim SOTA.
- [ ] Khong claim reinforcement learning.
- [ ] Neu khong nhung hybrid kip, trinh bay model nhu baseline phu.

## 9. Fallback Neu Rapfi Kho Tich Hop

Neu sau 2 ngay khong goi duoc Rapfi tu script:

1. Dung Rapfi/Gomocup manager de tao mot so game logs neu co the.
2. Lay board tu logs va chuyen thanh JSONL.
3. Neu van khong duoc, chuyen sang manual teacher:
   - Chon 50-100 board quan trong.
   - Lay move tu Rapfi bang cach thu cong/GUI/manager.
   - Augment thanh 400-800 samples.
4. Neu van khong kip:
   - Dung tactical labels thu cong.
   - Ghi Rapfi teacher la huong tiep theo, khong claim da lam.

## 10. Cau Van Dua Vao Bao Cao

```text
Nhom su dung Rapfi/Gomocup engine nhu teacher de gan nhan best move cho cac board Gomoku 15x15. Dataset khong lay nhan tu AI hien tai cua du an, vi dieu do co the lam model hoc lai diem yeu cua heuristic engine. Policy model duoc train theo huong supervised learning va duoc dung nhu policy prior/top-k suggestion. Classical search cua du an van giu vai tro quyet dinh cuoi cung de dam bao tactical rules va kha nang giai thich.
```

## 11. Tieu Chi Hoan Thanh Toi Thieu

- [ ] Rapfi teacher tao duoc it nhat 300 board goc.
- [ ] Sau augmentation co it nhat 2000 samples.
- [ ] Co train/val/test split.
- [ ] CNN train duoc va co top-k accuracy.
- [ ] Co bang ket qua trong report/slide.
- [ ] AI chinh cua project van build/test pass.

## 12. Tieu Chi Diem Cao

- [ ] Rapfi teacher tao duoc 1000+ board goc.
- [ ] Dataset co nhieu source: tactical, random, arena, loss-memory.
- [ ] Co top-5 prediction demo.
- [ ] Co hybrid policy booster.
- [ ] Co benchmark classical vs hybrid.
- [ ] Co ghi ro han che va khong claim qua muc.

