# B-04. Penalty function và cách mã hóa

Mở rộng cho [Phần A, Mục 4](../A-translation/04-problem-transformation.md). Đây là phần mà người làm tối ưu tổ hợp có nhiều kinh nghiệm nhất, và cũng là phần quyết định chất lượng của QUBO. Chương này (1) liên hệ penalty function với phương pháp penalty quen thuộc, (2) chỉ ra công thức chọn $P$ của bài báo an toàn nhưng rất thận trọng, và (3) so sánh các cách mã hóa. Notebook: [B3](../../notebooks/B-extensions/03-penalty-and-encodings.ipynb).

## 1. Liên hệ với phương pháp penalty cổ điển

Biến $\min f(x)$ s.t. $h(x) = 0$ thành $\min f(x) + P\,h(x)^2$ chính là **phương pháp penalty function bình phương** (quadratic penalty) trong tối ưu cổ điển. Hai điểm khác biệt quan trọng khi làm với QUBO:

| | Penalty cổ điển (liên tục) | Penalty trong QUBO (rời rạc) |
|---|---|---|
| Penalty constant | Thường tăng dần $P_k \to \infty$ qua các vòng lặp | Phải cố định trước khi sampling; tăng $P$ giữa chừng nghĩa là phải chạy lại |
| Tính chính xác | Cần $P \to \infty$ để thỏa ràng buộc | Với bài toán nguyên/rời rạc, một $P$ **hữu hạn** là đủ (penalty function "chính xác") |
| Chi phí của $P$ lớn | Điều kiện hóa kém (ill-conditioning) | Dải coefficient rộng, địa hình khó cho annealer, mất độ phân giải trên phần cứng |
| Thay thế | Lagrangian/augmented Lagrangian cập nhật nhân tử | Có thể lặp: chạy, kiểm tra vi phạm, tăng coefficient các ràng buộc bị vi phạm |

Điểm thứ hai là ý chính: vì biến rời rạc, tồn tại một **ngưỡng $P^*$ hữu hạn** sao cho với mọi $P > P^*$ optimal solution của QUBO trùng optimal solution của bài toán có ràng buộc. Câu hỏi thực tế là $P^*$ bằng bao nhiêu và việc chọn $P \gg P^*$ có hại không.

## 2. Công thức (36) an toàn nhưng rất thận trọng

Bài báo đề xuất $P = ub(f) - lb(f) + 1 = 1 + \sum_{S \ne \emptyset} |a_S|$. Công thức này chỉ nhìn vào coefficient của hàm mục tiêu, nên luôn đúng nhưng không tận dụng cấu trúc ràng buộc.

**Một bài knapsack nhỏ.** Tám vật với giá trị $[13, 4, 5, 6, 5, 13, 14, 10]$, trọng lượng $[2, 2, 4, 5, 6, 5, 4, 3]$, sức chứa $W = 20$, tối ưu bằng 59. Ràng buộc $\sum w_i x_i \le W$ được đưa vào bằng 5 biến slack nhị phân, rồi phạt bình phương (notebook B3). Duyệt vét cạn $2^{13}$ state cho:

| Đại lượng | Giá trị |
|---|---|
| $P$ theo công thức (36) (áp dụng cho phần mục tiêu) | **71** |
| $P^*$ thực nhỏ nhất làm mọi nghiệm cực tiểu đều feasible và tối ưu | **khoảng 1,1** |

Công thức (36) lớn hơn ngưỡng thực khoảng 65 lần. Điều này không có nghĩa (36) sai. Nó nghĩa là (36) là một cận *đảm bảo* cho mọi bài toán, còn ngưỡng thực phụ thuộc vào cấu trúc cụ thể của thể hiện và có thể thấp hơn rất nhiều.

## 3. $P$ lớn không miễn phí

Dùng simulated annealing với lịch nhiệt độ tự co giãn theo thang energy của QUBO (cách các solver thật làm), ta đo hai tỉ lệ trên 2000 lần chạy:

| $P$ | Feasible (400 sweep) | Feasible và tối ưu (400 sweep) |
|---:|---:|---:|
| 0,5 | 0,46 | 0,45 |
| 1 | 0,59 | 0,39 |
| 2 | 0,81 | 0,18 |
| 4 | 0,92 | 0,06 |
| 8 | 0,97 | 0,02 |
| 16 | 0,99 | 0,01 |
| 71 | 0,99 | 0,00 |
| 1000 | 0,99 | 0,00 |

Hai xu hướng ngược nhau:

- **Tỉ lệ feasible tăng theo $P$.** Ràng buộc phạt nặng thì được tuân thủ.
- **Tỉ lệ feasible *và tối ưu* giảm đơn điệu theo $P$.** Khi $P$ lớn, annealer tốn nhiệt độ vào vùng quá nóng so với phần mục tiêu thật (lịch nhiệt độ bị kéo bởi coefficient lớn), và các nghiệm feasible bị ngăn cách bởi rào energy rất cao nên khó chuyển từ nghiệm kém sang nghiệm tốt hơn.

Điểm tốt nhất nằm **gần ngưỡng $P^*$**, thậm chí hơi dưới ngưỡng (một số shots không cần QUBO đúng để cho nghiệm feasible tốt). Giá trị $P = 71$ theo (36) cho gần như 0% thành công dù QUBO tương ứng đúng hoàn toàn về mặt toán học. Đây là một thể hiện nhỏ và một sampler cổ điển, nên số cụ thể sẽ khác trên phần cứng và bài toán khác; điều đáng mang đi là **bản chất đánh đổi** và việc (36) là cận an toàn về tính đúng đắn, không phải lựa chọn tốt về hiệu năng.

Trên phần cứng lượng tử còn một lý do nữa: các coefficient phải được co giãn vào dải cho phép và được lập trình với độ chính xác hữu hạn, nên dải coefficient rộng (thang energy tăng tuyến tính theo $P$, từ 32 đến 64000 lần giá trị vật nhỏ nhất trong thí nghiệm trên) làm phần mục tiêu thật bị "chìm" trong noise lập trình.

### Quy trình thực dụng chọn $P$

1. **Bắt đầu từ cận chặt theo bài toán.** Với mỗi ràng buộc, hỏi: lợi ích tối đa trong hàm mục tiêu khi vi phạm nó một đơn vị là bao nhiêu? $P$ chỉ cần lớn hơn đại lượng đó (thường nhỏ hơn rất nhiều so với (36)).
2. **Kiểm tra QUBO đúng trên thể hiện nhỏ** bằng duyệt vét cạn hoặc solver chính xác, như ở notebook B3.
3. **Thăm dò $P$ bằng thực nghiệm**: chạy với vài giá trị, vẽ tỉ lệ feasible và tỉ lệ feasible-và-tối ưu. Chọn $P$ ở vùng feasible đủ cao mà chất lượng chưa giảm nhiều.
4. **Dùng công thức (36) làm cận trên an toàn khi không còn gì khác**, nhưng đừng dùng nó như mặc định.
5. **Tiền xử lý:** chuẩn hóa thang của hàm mục tiêu (chia cho một hằng số) để $P$ và coefficient mục tiêu cùng cỡ.

## 4. Cách mã hóa biến

**Biến nguyên trong $[a, c]$:**

| Cách mã hóa | Số biến nhị phân | Ghi chú |
|---|---|---|
| Nhị phân (phương trình (20)) | $\lceil \log_2(c - a + 1) \rceil$ | Ít biến nhất; một giá trị có thể có nhiều biểu diễn; trọng số lệch nhau nhiều nên mức độ "gần nhau" không giữ được |
| Unary | $c - a$ | Nhiều biến hơn rất nhiều; mỗi biến trọng số 1 nên các bước nhỏ rất tự nhiên (mở rộng với ràng buộc thứ tự) |
| One-hot | $c - a + 1$ | Cần ràng buộc $\sum = 1$ (phạt dày) |

Số biến slack cho ràng buộc $\sum w_i x_i \le W$ (notebook B3): với $W = 20$ cần 5 biến nhị phân so với 20 biến unary; với $W = 1000$ là 10 so với 1000.

**Slack: dùng cận chặt nhất có thể.** Ở [Ví dụ 14](../A-translation/04-problem-transformation.md), cận dưới của $h$ là $-24$ nên slack trong $[0, 24]$ cần 5 biến, nhưng giá trị nhỏ nhất thực của $h$ là $-6$ nên slack trong $[0, 6]$ chỉ cần 3 biến ([notebook 3](../../notebooks/A-examples/03-constraints-and-penalty.ipynb)). Mỗi biến slack tiết kiệm được là một qubit và một lớp tương tác dày.

**Variational loại và hoán vị: one-hot.** Mã hóa one-hot (phương trình (21)–(24)) có hai cái giá:

- Nhiều biến hơn: một variational loại $k$ mức cần $k$ biến, một hoán vị cỡ $n$ cần $n^2$ biến.
- Đồ thị tương tác dày: ràng buộc $\sum_\ell x_\ell = 1$ sau khi bình phương tạo tương tác giữa mọi cặp biến trong nhóm. Với TSP, mỗi biến có bậc cỡ $4(n-1)$, và đó là lý do bài toán khó nhúng lên phần cứng ([B-05](05-embedding-and-chains.md)).

Các cách mã hóa khác (ví dụ domain-wall encoding cho biến có thứ tự) và các ansatz bảo toàn ràng buộc (ví dụ mixer kiểu XY cho one-hot trong QAOA) đã được đề xuất trong tài liệu nghiên cứu để giảm bớt chi phí này. Mình không thẩm định chúng ở đây; hãy xem các tài liệu ở [B-07](07-benchmarking.md) khi cần.

## Bài tập

**Bài 1.** Bài toán: cực đại hóa $3x_1 + 2x_2$ với ràng buộc $2x_1 + 2x_2 \le 3$. Dùng slack $s = t_1 + 2t_2$ (có thể nhận giá trị trong $[0, 3]$) và penalty function $P(2x_1 + 2x_2 + s - 3)^2$. Tìm $P^*$ nhỏ nhất để nghiệm cực tiểu của QUBO là optimal solution feasible.

<details>
<summary>Solution</summary>

Optimal solution feasible là $x = (1, 0)$ (giá trị 3, vì $x = (1,1)$ có trọng lượng 4 > 3 là infeasible). Hàm cần cực tiểu: $-(3x_1 + 2x_2) + P(2x_1 + 2x_2 + s - 3)^2$.

- Tại $x = (1, 0)$ với $s = 1$ ($t_1 = 1$): vi phạm bằng $2 + 0 + 1 - 3 = 0$, nên energy $= -3$.
- Tại $x = (1, 1)$ (infeasible), trọng lượng 4: $h + s = 1 + s$, nhỏ nhất khi $s = 0$ cho $(1)^2 = 1$. Energy $= -5 + P$.

Để nghiệm infeasible không thắng optimal solution cần $-5 + P > -3$, tức $P > 2$. Tại $P = 2$ hai nghiệm hòa nhau; với $P < 2$ nghiệm cực tiểu là $x = (1,1)$ infeasible. Vậy $P^* = 2$ (cần $P > 2$ để chắc chắn). Kết quả này đã được kiểm tra bằng duyệt vét cạn 16 state: với $P = 1$ và $1{,}5$ nghiệm cực tiểu là $(1,1,0,0)$, với $P = 2$ có hai nghiệm cực tiểu, với $P = 2{,}5$ trở lên chỉ còn $(1,0,1,0)$.
</details>

**Bài 2.** Cho biến nguyên $z \in [0, 100]$. So sánh số biến nhị phân giữa mã hóa nhị phân và one-hot, và nêu một ưu điểm của one-hot bất chấp số biến nhiều hơn.

<details>
<summary>Solution</summary>

Nhị phân: $\lceil \log_2 101 \rceil = 7$ biến. One-hot: 101 biến. Ưu điểm của one-hot: hàm của $z$ bất kỳ (kể cả hàm không đơn điệu, phi tuyến) trở thành hàm *tuyến tính* của các biến one-hot (mỗi mức một coefficient), không cần khai triển bậc cao như ở Ví dụ 10 với biểu diễn nhị phân; cái giá là ràng buộc $\sum_\ell x_\ell = 1$ và nhiều biến hơn.
</details>
