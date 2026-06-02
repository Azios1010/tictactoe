# Các Hướng Cải Tiến AI Gomoku 15x15

## Hiện Trạng Dự Án

Dự án hiện tại đã triển khai:

- Minimax Search
- Alpha-Beta Pruning
- Iterative Deepening Search
- Zobrist Hashing
- Bàn cờ 15x15

---

# 1. Candidate Move Generation

## Vấn đề

Mỗi lượt có thể tồn tại tối đa:

```text
15 × 15 = 225 nước đi
```

## Giải pháp

Chỉ sinh nước đi tại các ô nằm gần quân cờ đã được đánh:

```text
distance <= 2
```

hoặc

```text
distance <= 3
```

## Lợi ích

Giảm số lượng nước đi cần xét từ 225 xuống còn khoảng 20–50 trong phần lớn trạng thái thực tế.

## Mức độ cải thiện

Rất lớn.

---

# 2. Move Ordering

## Giải pháp

Sắp xếp nước đi trước khi đưa vào Alpha-Beta:

1. Nước thắng ngay
2. Chặn thắng đối thủ
3. Open Four
4. Broken Four
5. Open Three
6. Double Three
7. Các nước còn lại

## Mức độ cải thiện

Rất cao.

---

# 3. Threat-Based Search

## Giải pháp

Nhận diện và ưu tiên:

- Five
- Open Four
- Closed Four
- Open Three
- Broken Three
- Double Three
- Double Four

## Mức độ cải thiện

Rất cao.

---

# 4. Pattern-Based Evaluation Function

## Ví dụ chấm điểm

```text
XXXXX      = 10000000

.XXXX.     = 100000

XXXX.      = 50000

.XXX.      = 10000

XXX.       = 5000

.XX.       = 1000
```

```text
Score = AttackScore - DefenseScore
```

## Mức độ cải thiện

Rất cao.

---

# 5. Principal Variation Search (PVS)

## Ý tưởng

- Search đầy đủ nước đi đầu tiên.
- Các nước còn lại search với cửa sổ hẹp.

## Mức độ cải thiện

Trung bình đến cao.

---

# 6. Killer Move Heuristic

Lưu các nước đi từng tạo Alpha-Beta Cutoff và ưu tiên xét trước.

## Mức độ cải thiện

Trung bình.

---

# 7. History Heuristic

Theo dõi:

```text
move -> số lần gây cutoff
```

## Mức độ cải thiện

Trung bình.

---

# 8. Quiescence Search

Tiếp tục search các nước chiến thuật quan trọng thay vì dừng ngay tại nút lá.

Ví dụ:

- Tạo Four
- Chặn Four
- Tạo Three mạnh

## Mức độ cải thiện

Trung bình đến cao.

---

# 9. Aspiration Window

Thay vì:

```text
[-INF, +INF]
```

Sử dụng:

```text
[S - delta, S + delta]
```

## Mức độ cải thiện

Trung bình.

---

# 10. Enhanced Transposition Table

Ngoài Zobrist Hashing, lưu thêm:

- Exact Score
- Lower Bound
- Upper Bound
- Best Move
- Search Depth

Ví dụ:

```cpp
struct TTEntry {
    uint64_t hash;
    int score;
    int depth;
    int flag;
    Move bestMove;
};
```

## Mức độ cải thiện

Cao.

---

# 11. Parallel Search

Song song hóa các nhánh tại root node.

## Mức độ cải thiện

Cao.

---

# 12. Threat Space Search

Chỉ xét:

- Nước thắng
- Nước tạo Four
- Nước tạo Three
- Nước bắt buộc phòng thủ

## Mức độ cải thiện

Rất cao.

---

# Roadmap Đề Xuất

## Giai đoạn 1

1. Candidate Move Generation
2. Move Ordering
3. Pattern Evaluation

## Giai đoạn 2

4. Killer Move
5. History Heuristic
6. Quiescence Search

## Giai đoạn 3

7. Principal Variation Search
8. Aspiration Window
9. Enhanced Transposition Table

## Giai đoạn 4

10. Threat Space Search
11. Parallel Search

---

# Đánh Giá Tác Động

| Kỹ thuật | Độ khó | Hiệu quả |
|-----------|---------|-----------|
| Candidate Move Generation | Thấp | Rất cao |
| Move Ordering | Thấp | Rất cao |
| Pattern Evaluation | Trung bình | Rất cao |
| Threat Search | Trung bình | Rất cao |
| Enhanced TT | Trung bình | Cao |
| Killer Move | Thấp | Trung bình |
| History Heuristic | Thấp | Trung bình |
| Quiescence Search | Trung bình | Cao |
| PVS | Trung bình | Cao |
| Aspiration Window | Trung bình | Trung bình |
| Parallel Search | Cao | Cao |

# Khuyến Nghị

Nếu chỉ được chọn 3 cải tiến:

1. Candidate Move Generation
2. Pattern-Based Evaluation Function
3. Threat-Based Search

Ba kỹ thuật này thường mang lại hiệu quả cao nhất cho AI Gomoku 15x15 sử dụng Minimax/Alpha-Beta.
