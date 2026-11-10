# B-05. Minor-embedding và chain: bài toán của bạn có vừa với máy không?

Mở rộng cho [Phần A, Mục 5.2](../A-translation/05-quantum-annealer.md). Bài báo nói minor-embedding là NP-hard và giới thiệu khái niệm chain, nhưng chỉ trên ví dụ nhỏ. Chương này đo bằng số: **cấu trúc đồ thị của QUBO, không chỉ số biến, quyết định bài toán có vừa với máy hay không.** Notebook: [B4](../../notebooks/B-extensions/04-embedding-scaling.ipynb) (chạy cục bộ, không cần tài khoản D-Wave).

## 1. Nhắc lại vấn đề

- QUBO có đồ thị bài toán: mỗi biến là một đỉnh, hai biến nối với nhau nếu có số hạng bậc hai chứa cả hai.
- Phần cứng có đồ thị topology: qubit vật lý và các coupler cố định giữa chúng.
- Cần ánh xạ mỗi biến logic vào một **chain** (tập các qubit vật lý liên thông), sao cho nếu hai biến có tương tác thì hai chain tương ứng có ít nhất một coupler nối. Đây là **minor-embedding**.
- Coupling nội bộ chain phải đủ mạnh (`chain_strength`) để các qubit trong chain cùng giá trị. Nếu không, chain **bị đứt** và biến logic không có giá trị xác định.

Ba topology của D-Wave (Hình 3 bài báo): **Chimera** (mỗi qubit tối đa 6 láng giềng), **Pegasus** (tối đa 15) và **Zephyr** (tối đa 20). Notebook dùng các bản cỡ thật: Chimera C16 (2048 qubit), Pegasus P16 (5640 qubit), Zephyr Z12 (4800 qubit).

## 2. Đồ thị đầy đủ $K_n$ (QUBO dày)

Mỗi ô là (tổng số qubit vật lý, chain dài nhất):

| | $K_8$ | $K_{16}$ | $K_{24}$ | $K_{32}$ |
|---|---|---|---|---|
| Chimera C16 | (22, 3) | (80, 6) | (188, 10) | (339, 13) |
| Pegasus P16 | (12, 2) | (38, 3) | (80, 4) | (140, 6) |
| Zephyr Z12 | (12, 2) | (37, 3) | (63, 3) | (110, 5) |

Nhận xét:

- Số qubit vật lý tăng nhanh hơn tuyến tính theo $n$ (trên Chimera, từ 22 lên 339 khi $n$ từ 8 lên 32, tức tăng gấp 4 lần $n$ mà qubit tăng hơn 15 lần).
- Topology kết nối dày hơn (Pegasus, Zephyr) cần ít qubit và chain ngắn hơn nhiều: cùng $K_{32}$ cần 339 qubit trên Chimera nhưng chỉ khoảng 110–140 trên Zephyr/Pegasus.
- Kể cả trên máy có hơn 5000 qubit, một QUBO *dày* chỉ vừa vài chục biến logic.

## 3. Đồ thị thưa: 3-regular ngẫu nhiên

| | $n = 32$ | $n = 64$ | $n = 128$ | $n = 256$ |
|---|---|---|---|---|
| Chimera C16 | (63, 3) | (147, 4) | (389, 8) | (1205, 15) |
| Pegasus P16 | (33, 2) | (72, 2) | (175, 3) | (497, 5) |
| Zephyr Z12 | (32, 1) | (70, 2) | (149, 2) | (469, 5) |

Đồ thị thưa với hàng trăm biến vẫn nhúng được, với tổng số qubit chỉ gấp khoảng 2 đến 4,7 lần số biến. So với $K_{32}$ cần hàng trăm qubit, một đồ thị 3-regular 256 biến chỉ cần khoảng 500 qubit trên Pegasus.

## 4. TSP: đồ thị dày xuất hiện từ ràng buộc one-hot

TSP với $n$ thành phố có $n^2$ biến $x_{a,j}$. Hai ràng buộc hoán vị tạo tương tác giữa mọi cặp cùng hàng và cùng cột, và chi phí quãng đường nối mọi cặp ở hai vị trí kề nhau. Kết quả: mỗi biến có bậc $4(n-1)$ (12, 20, 28, 36, 44 khi $n = 4, 6, 8, 10, 12$), vượt xa bậc của qubit.

| $n$ | Biến logic | Bậc tối đa | Chimera C16 | Pegasus P16 | Zephyr Z12 |
|---:|---:|---:|---|---|---|
| 4 | 16 | 12 | 75 qubit, chain ≤ 6 | 34, chain ≤ 3 | 32, chain ≤ 3 |
| 6 | 36 | 20 | 359, chain ≤ 14 | 154, chain ≤ 6 | 123, chain ≤ 5 |
| 8 | 64 | 28 | 1084, chain ≤ 26 | 445, chain ≤ 10 | 367, chain ≤ 8 |
| 10 | 100 | 36 | không tìm được | 1183, chain ≤ 20 | 900, chain ≤ 14 |
| 12 | 144 | 44 | không tìm được | 2269, chain ≤ 24 | 1894, chain ≤ 23 |

("Không tìm được" nghĩa là heuristic `minorminer` thất bại trong thời hạn 30 giây, chưa phải chứng minh không tồn tại nhúng. Mỗi lần chạy heuristic ngẫu nhiên có thể cho số hơi khác.)

Đọc kết quả:

- Số qubit vật lý tăng rất nhanh: từ 34 (với $n=4$) lên 2269 (với $n=12$) trên Pegasus, trong khi số biến logic chỉ tăng từ 16 lên 144.
- Chain dài tới 20+ qubit. Chain dài rất dễ bị đứt.
- $n = 12$ đã chiếm khoảng 40% tổng số qubit của một chip Pegasus P16 (2269/5640). Ngoại suy thô cho thấy TSP cỡ vài chục thành phố sẽ vượt quá khả năng một chip nếu mã hóa trực tiếp theo cách này; đây là ngoại suy từ các điểm $n \le 12$, không phải phép đo.

## 5. Hệ quả cho người mô hình hóa

1. **Giữ đồ thị bài toán thưa.** Khi có lựa chọn giữa hai mô hình QUBO, ưu tiên mô hình có ít cặp tương tác hơn, kể cả khi phải thêm biến phụ.
2. **Cân nhắc lại ràng buộc dày.** Mỗi ràng buộc "tổng của nhiều biến bằng hằng số" bình phương lên tạo clique trong đồ thị. Các cách mã hóa khác (ví dụ ràng buộc cục bộ trên nhóm nhỏ) có thể thưa hơn.
3. **Kiểm tra khả năng nhúng sớm.** Chạy `minorminer.find_embedding` lên topology mục tiêu trước khi đầu tư vào tinh chỉnh tham số. Notebook B4 là khuôn mẫu.
4. **Số qubit quảng cáo không phải số biến dùng được.** Số biến logic nhúng được phụ thuộc cấu trúc đồ thị, và có thể nhỏ hơn tổng số qubit hàng chục lần.
5. **Phân rã bài toán.** Nếu QUBO quá lớn, các cách tiếp cận lai (chia nhỏ bài toán, giải từng phần trên QPU, ghép lại bằng solver cổ điển) là hướng thực tế; chi tiết nằm ngoài phạm vi tài liệu này.

## 6. Về chain strength và chain đứt

- **Quá yếu:** chain đứt, biến logic nhận các giá trị mâu thuẫn trong các qubit của nó. Phần mềm (như `EmbeddingComposite` của Ocean) giải quyết bằng một phương pháp hậu xử lý, thường là bỏ phiếu theo đa số; cách này làm mất thông tin và có thể cho nghiệm kém.
- **Quá mạnh:** các qubit trong chain bị "khóa" với nhau nhưng độ mạnh đó chiếm dải hệ số cho phép của phần cứng, ép các hệ số của bài toán thật xuống phần nhỏ của dải và làm chúng mất độ phân giải (cùng hiệu ứng với $P$ lớn ở [B-04](04-penalties-and-encodings.md)).
- Do đó `chain_strength` là một siêu tham số cần quét, như ở ô cuối của [notebook C1](../../notebooks/C-hardware/01-dwave-leap-maxsat.ipynb) (chỉ chạy trên QPU).

## Bài tập

**Bài 1.** Một QUBO có đồ thị là một chu trình $C_n$ (mỗi biến nối với đúng hai biến khác). Dự đoán độ dài chain cần thiết trên Chimera, và giải thích.

<details>
<summary>Lời giải</summary>

Câu trả lời phụ thuộc tính chẵn lẻ của $n$. Đồ thị Chimera là **đồ thị hai phía** (bipartite), nên nó chỉ chứa các chu trình độ dài chẵn.

- **$n$ chẵn:** chu trình $C_n$ nhúng được như một chu trình có sẵn trong Chimera, mỗi biến dùng đúng một qubit, nên chain có độ dài 1.
- **$n$ lẻ:** Chimera không chứa chu trình lẻ, nên không thể nhúng với mọi chain độ dài 1. Cần ít nhất một chain có 2 qubit (thêm một qubit để "sửa chẵn lẻ").

Kết quả này đã được kiểm tra bằng `minorminer` trên Chimera $C_4$: $C_6, C_8, C_{20}$ cho chain tối đa 1 và tổng số qubit bằng $n$; $C_7, C_9, C_{21}$ cho chain tối đa 2 và tổng số qubit bằng $n + 1$. Nhìn chung, đồ thị bài toán thưa và có cấu trúc giống đồ thị phần cứng thì nhúng gần như không tốn thêm qubit; đó là lý do các bài toán thưa như Max-Cut trên đồ thị bậc thấp hợp với máy ủ hơn nhiều bài toán dày.
</details>

**Bài 2.** Vì sao TSP mã hóa one-hot có bậc đỉnh $4(n-1)$? Đếm các loại tương tác của $x_{a,j}$.

<details>
<summary>Lời giải</summary>

Biến $x_{a,j}$ (thành phố $a$ ở vị trí $j$) tương tác với: (i) $n - 1$ biến cùng vị trí $j$ nhưng thành phố khác (ràng buộc mỗi vị trí đúng một thành phố); (ii) $n - 1$ biến cùng thành phố $a$ nhưng vị trí khác (ràng buộc mỗi thành phố đúng một vị trí); (iii) $n - 1$ biến $x_{b,j+1}$ với $b \ne a$ (chi phí đi từ $a$ sang $b$); (iv) $n - 1$ biến $x_{b,j-1}$ với $b \ne a$ (chi phí đi từ $b$ sang $a$). Tổng cộng $4(n-1)$, khớp với số liệu (12 khi $n = 4$, 44 khi $n = 12$).
</details>
