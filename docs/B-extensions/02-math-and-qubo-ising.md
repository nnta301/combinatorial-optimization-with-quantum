# B-02a. Toán học nền: ký hiệu Dirac, tensor product và dẫn công thức QUBO ↔ Ising

Mở rộng cho [Phần A, Mục 2.1](../A-translation/02-background.md). Bài báo gốc nén toàn bộ nền toán vào hai trang. Chương này giải thích trực giác cho người đã quen đại số tuyến tính và tối ưu, rồi **dẫn từng bước** các công thức (8)–(11) mà bài báo chỉ phát biểu kết quả. Notebook kiểm chứng: [01-qubo-and-ising](../../notebooks/A-examples/01-qubo-and-ising.ipynb).

## 1. Ký hiệu Dirac nhìn như đại số tuyến tính bình thường

Không có gì huyền bí: ký hiệu Dirac chỉ là cách viết gọn cho vector và ma trận.

| Ký hiệu Dirac | Nghĩa trong đại số tuyến tính |
|---|---|
| $\lvert x\rangle$ | Một vector (cột) |
| $\langle x\rvert$ | Vector hàng liên hợp phức của $\lvert x\rangle$ |
| $\langle x\vert y\rangle$ | Tích vô hướng (có liên hợp phức) |
| $\lvert 0\rangle, \lvert 1\rangle$ | Hai vector đơn vị của $\mathbb{C}^2$: $(1,0)^T$ và $(0,1)^T$ |
| $\lvert w\rangle$ với $w \in \{0,1\}^n$ | Vector đơn vị thứ $w$ của $\mathbb{C}^{2^n}$ (chỉ có một phần tử bằng 1) |
| $A\lvert\psi\rangle$ | Nhân ma trận với vector |
| $\langle\psi\rvert A\lvert\psi\rangle$ | Dạng toàn phương $\psi^\dagger A \psi$ |

**State của $n$ qubit** là một vector $\lvert\psi\rangle = \sum_{w} a_w \lvert w\rangle$ trong $\mathbb{C}^{2^n}$ với $\sum_w |a_w|^2 = 1$. Đối với người làm tối ưu, có thể nghĩ nó như **một "distribution xác suất" trên tất cả solution $\{0,1\}^n$, nhưng lưu trữ ở dạng amplitude phức** $a_w$ thay vì xác suất. Measurement probability được $w$ là $|a_w|^2$. Điểm khác biệt quyết định là amplitude có thể **triệt tiêu nhau** (giao thoa), còn xác suất thì không; đó là thứ thuật toán lượng tử khai thác.

**Số $2^n$:** để mô tả một state tổng quát của $n$ qubit cần $2^n$ số phức. Đây là lý do mô phỏng cổ điển trở nên bất feasible ở $n$ cỡ vài chục, và cũng là lý do ta chỉ mô phỏng được các ví dụ nhỏ (3 đến vài chục qubit) trong các notebook.

## 2. Tensor product: cách ghép các hệ

Tensor product $A \otimes B$ (phương trình (3)) chính là **tích Kronecker** của hai ma trận. Hai hệ qubit riêng $\lvert\psi\rangle$ và $\lvert\varphi\rangle$ ghép lại thành $\lvert\psi\rangle \otimes \lvert\varphi\rangle$ (vector có kích thước nhân lên). Viết $\lvert 01 \rangle$ là viết tắt của $\lvert 0\rangle \otimes \lvert 1\rangle$.

Hai quy tắc đủ dùng:

- $(A \otimes B)(\lvert\psi\rangle \otimes \lvert\varphi\rangle) = (A\lvert\psi\rangle) \otimes (B\lvert\varphi\rangle)$: mỗi operator tác dụng lên phần của mình.
- Một operator chỉ tác dụng lên qubit $j$ được viết $I \otimes \dots \otimes A \otimes \dots \otimes I$. Trong tài liệu này $Z_j$ có nghĩa đó. Tích $Z_1 \otimes Z_2 \otimes Z_3$ là ma trận $8 \times 8$ đường chéo.

**Quy ước thứ tự bit (cẩn thận khi dùng Qiskit):** Qiskit xếp qubit 0 là bit ít quan trọng nhất, nên $\lvert q_2 q_1 q_0\rangle$ viết từ trái sang phải. Trong tài liệu này $x_1$ ứng với qubit 0. Xem ghi chú ở [Phần A, Mục 6](../A-translation/06-gate-based.md).

## 3. Tại sao Z gate "là" hàm mục tiêu

$Z = \mathrm{diag}(1, -1)$ nên $Z\lvert x\rangle = (-1)^x \lvert x\rangle$: tác dụng lên computational basis chỉ **nhân với $\pm 1$**, không làm thay đổi state. Vì $Z_j$ và mọi tích của chúng đều đường chéo, nên mọi tổ hợp tuyến tính của chúng cũng đường chéo, và chiều ngược lại cũng đúng: *mọi* diagonal matrix $2^n \times 2^n$ viết được như tổ hợp tuyến tính của các tích $\bigotimes_{j \in S} Z_j$ (có $2^n$ tập $S$, đủ để biểu diễn $2^n$ giá trị tùy ý). Coefficient $a_S$ ở phương trình (44) chính là **biến đổi Walsh–Hadamard** của bảng giá trị hàm mục tiêu. Hệ quả: hàm bậc $k$ (chỉ có term $|S| \le k$) tương ứng Hamiltonian chỉ chứa tích Z tối đa $k$ qubit. Xem [B-02b](02-hamiltonian-and-annealing.md) và [notebook B1](../../notebooks/B-extensions/01-hamiltonian-and-annealing.ipynb).

## 4. Dẫn công thức (8)–(11)

**Mục tiêu:** từ $f(x) = \sum_{j,k} Q_{j,k}\, x_j x_k + c$ với $Q$ đối xứng, thế $x_j = (1 - s_j)/2$ và viết lại thành $f(s) = \sum_{j,k} J_{j,k}\, s_j s_k + \sum_j h_j s_j$.

**Bước 1: thế một tích hai biến.**
$$x_j x_k = \frac{(1 - s_j)(1 - s_k)}{4} = \frac{1 - s_j - s_k + s_j s_k}{4}.$$

Công thức này đúng cả khi $j = k$: khi đó $x_j x_j = x_j = (1-s_j)/2$, và vế phải cho $(1 - 2s_j + s_j^2)/4 = (2 - 2s_j)/4 = (1 - s_j)/2$ vì $s_j^2 = 1$. Nên ta có thể dùng cùng một công thức cho toàn bộ các term, kể cả đường chéo.

**Bước 2: cộng theo mọi cặp $(j,k)$.**
$$\sum_{j,k} Q_{j,k}\, x_j x_k = \frac14 \sum_{j,k} Q_{j,k} \;-\; \frac14 \sum_{j,k} Q_{j,k}(s_j + s_k) \;+\; \frac14 \sum_{j,k} Q_{j,k}\, s_j s_k.$$

**Bước 3: term tuyến tính.** Vì $Q$ đối xứng, $\sum_{j,k} Q_{j,k} s_k = \sum_{j,k} Q_{k,j} s_j = \sum_{j,k} Q_{j,k} s_j$. Do đó
$$-\frac14 \sum_{j,k} Q_{j,k}(s_j + s_k) = -\frac12 \sum_{j} \Big(\sum_k Q_{j,k}\Big) s_j \quad\Longrightarrow\quad h_j = -\frac12 \sum_{k=1}^{n} Q_{j,k}. \qquad \text{(11)}$$

**Bước 4: term bậc hai.** Tách tổng $\sum_{j,k} Q_{j,k}\, s_j s_k$ thành phần $j \ne k$ và phần $j = k$:
$$\frac14 \sum_{j \ne k} Q_{j,k}\, s_j s_k + \frac14 \sum_{j} Q_{j,j}\underbrace{s_j^2}_{=1}.$$
Phần $j \ne k$ cho $J_{j,k} = \tfrac14 Q_{j,k}$ (phương trình (8)). Phần $j = k$ là **hằng số** $\tfrac14 \sum_j Q_{j,j}$.

**Bước 5: gom hằng số.** Hằng số tổng cộng là $c + \frac14\sum_{j,k} Q_{j,k} + \frac14 \sum_j Q_{j,j}$. Mọi hằng số có thể đặt vào coefficient của $s_1^2 = 1$, nên bài báo gán nó cho $J_{1,1}$ (phương trình (9)), và đặt $J_{j,j} = 0$ với $j \ge 2$ (phương trình (10)).

### Ví dụ có số

$f(x) = 3x_1 - 2x_2 + 4x_1 x_2$. Ma trận đối xứng: $Q_{1,1} = 3$, $Q_{2,2} = -2$, $Q_{1,2} = Q_{2,1} = 2$ (vì $4x_1x_2 = 2x_1x_2 + 2x_2x_1$), $c = 0$.

- $h_1 = -\tfrac12(3 + 2) = -2{,}5$; $h_2 = -\tfrac12(2 - 2) = 0$.
- $J_{1,2} = J_{2,1} = \tfrac14 \cdot 2 = 0{,}5$ (nên term $s_1 s_2$ có coefficient tổng là 1).
- $J_{1,1} = 0 + \tfrac14(3 + 2 + 2 - 2) + \tfrac14(3 - 2) = \tfrac54 + \tfrac14 = 1{,}5$.

Kết quả: $f(s) = 1{,}5 - 2{,}5\,s_1 + s_1 s_2$. Kiểm tra: tại $x = (1,1)$ ta có $f = 3 - 2 + 4 = 5$ và $s = (-1,-1)$ nên $1{,}5 + 2{,}5 + 1 = 5$ ✓; tại $x = (1,0)$ ta có $f = 3$ và $s = (-1, 1)$ nên $1{,}5 + 2{,}5 - 1 = 3$ ✓. (Các con số này đã được kiểm tra bằng `qubo_to_ising` trong `code/qco_utils.py`.)

## 5. Đọc hiểu mô hình Ising như bài toán đồ thị

Mô hình Ising là hàm trên đồ thị: mỗi biến $s_j$ là một đỉnh, mỗi coefficient $J_{j,k} \ne 0$ là một cạnh có trọng số, và $h_j$ là "trường ngoài" tác dụng lên từng đỉnh. Ví dụ quen thuộc: bài toán **Max-Cut** là Ising không có trường ngoài ($h = 0$) với $J_{j,k} > 0$ trên các cạnh (cực tiểu hóa $\sum J_{j,k} s_j s_k$ ép hai đầu cạnh khác dấu). Đồ thị này chính là thứ phải nhúng lên phần cứng ở [B-05](05-embedding-and-chains.md).

## Bài tập

**Bài 1.** Chuyển $g(x) = x_1 + x_2 + x_3 - 2(x_1 x_2 + x_1 x_3 + x_2 x_3)$ sang mô hình Ising.

<details>
<summary>Solution</summary>

$Q_{j,j} = 1$, $Q_{j,k} = -1$ với $j \ne k$ (vì $-2x_jx_k = -x_jx_k - x_kx_j$), $c = 0$. Khi đó $J_{j,k} = -\tfrac14$ với $j \ne k$, $h_j = -\tfrac12(1 - 1 - 1) = \tfrac12$ cho mọi $j$, và $J_{1,1} = 0 + \tfrac14(3 + 6 \cdot (-1)) + \tfrac14 \cdot 3 = -\tfrac34 + \tfrac34 = 0$. Cộng hai thứ tự $(j,k)$ và $(k,j)$:
$$g(s) = -\tfrac12 (s_1 s_2 + s_1 s_3 + s_2 s_3) + \tfrac12 (s_1 + s_2 + s_3).$$
Kiểm tra: $x = (1,1,1)$ cho $g = 3 - 6 = -3$; $s = (-1,-1,-1)$ cho $-\tfrac12 \cdot 3 + \tfrac12 \cdot (-3) = -3$ ✓.
</details>

**Bài 2.** Giải thích vì sao $J_{j,j}$ (đường chéo) không ảnh hưởng đến optimal solution của mô hình Ising.

<details>
<summary>Solution</summary>

Vì $s_j \in \{-1, 1\}$ nên $s_j^2 = 1$, nên $J_{j,j} s_j^2 = J_{j,j}$ là hằng số không phụ thuộc $s$. Cộng một hằng số vào hàm mục tiêu không đổi nghiệm cực tiểu, chỉ dịch giá trị tối ưu.
</details>

**Bài 3.** Ma trận $Q$ không đối xứng có thể được đối xứng hóa mà không đổi hàm $f$ không? Bằng cách nào?

<details>
<summary>Solution</summary>

Có. $\sum_{j,k} Q_{j,k} x_j x_k$ chỉ phụ thuộc $Q_{j,k} + Q_{k,j}$ (coefficient của $x_j x_k$ với $j \ne k$). Thay $Q$ bằng $Q' = (Q + Q^T)/2$ cho cùng hàm $f$, vì $Q'_{j,k} + Q'_{k,j} = Q_{j,k} + Q_{k,j}$ và đường chéo không đổi.
</details>
