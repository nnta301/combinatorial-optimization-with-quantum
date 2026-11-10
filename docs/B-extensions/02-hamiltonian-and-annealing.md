# B-02b. Hamiltonian, quantum annealing và simulated annealing

Mở rộng cho [Phần A, Mục 2.2 và 2.3](../A-translation/02-background.md). Chương này (1) giải thích Hamiltonian của bài toán chính là một "bảng giá trị", và (2) đặt quantum annealing cạnh simulated annealing quen thuộc, kèm mô phỏng chính xác trên một bài toán nhỏ. Notebook: [B1](../../notebooks/B-extensions/01-hamiltonian-and-annealing.ipynb).

## 1. Hamiltonian của bài toán là bảng giá trị của hàm mục tiêu

Với bài toán $n$ biến nhị phân, Hamiltonian $H_P$ là ma trận $2^n \times 2^n$ **đường chéo**, với phần tử đường chéo ứng với $\lvert x\rangle$ bằng $f(x)$: $H_P \lvert x\rangle = f(x)\lvert x\rangle$ (như bài báo nói ở Mục 6). Với bài toán Ví dụ 10:

| $i$ | $x_1 x_2 x_3$ | $f(x)$ |
|:-:|:-:|:-:|
| 0 | 000 | −9 |
| 1 | 100 | 4 |
| 2 | 010 | 5 |
| 3 | 110 | 0 |
| 4 | 001 | 0 |
| 5 | 101 | −5 |
| 6 | 011 | −4 |
| 7 | 111 | 9 |

Cùng bảng đó, viết bằng operator Pauli-Z, là $H_P = -2Z_1 - \tfrac52 Z_2 - \tfrac92 Z_1 Z_2 Z_3$ (phương trình (43)). Hai cách viết cho cùng một ma trận; notebook B1 kiểm tra điều này.

**Ý nghĩa với bài toán tối ưu:** *tìm state có energy thấp nhất* của $H_P$ chính là tìm $\arg\min f$. Nếu có quyền đọc cả bảng thì trivial; khó khăn là bảng có $2^n$ dòng. Máy lượng tử không "đọc bảng"; nó làm một quá trình vật lý (ủ) hoặc một dãy gate (QAOA) có xu hướng đưa state về vùng energy thấp.

**Bậc của hàm quyết định cấu trúc Hamiltonian.** Coefficient của tích $\bigotimes_{j \in S} Z_j$ là biến đổi Walsh–Hadamard của bảng giá trị ([B-02a](02-math-and-qubo-ising.md)). Hàm bậc $k$ cho Hamiltonian có các term chạm nhiều nhất $k$ qubit. Annealer chỉ hỗ trợ term một và hai qubit (nên phải order reduction, Mục 5.1), trong khi mạch gate-based hiện thực được term nhiều qubit bằng chuỗi CNOT (Mục 6).

## 2. Hai quá trình ủ

| | Simulated annealing (SA) | Quantum annealing (QA) |
|---|---|---|
| Hệ ở đâu | Một solution $x$ cụ thể tại mỗi thời điểm | Một state lượng tử (superposition các solution) |
| Cái gì "nóng" | Nhiệt độ $T$: xác suất chấp nhận bước xấu | Trường ngang (transverse field) $H_0 = -\sum X_j$ trộn các solution |
| Lịch trình | $T$ giảm từ cao xuống thấp | $H(s) = (1-s)H_0 + sH_P$, $s: 0 \to 1$ |
| Cách vượt rào energy | Nhảy nhiệt (thermal hop): cần đủ nhiệt để leo qua | Tunneling (quantum tunneling) và giao thoa |
| Đảm bảo lý thuyết | Với lịch làm nguội đủ chậm (logarit) hội tụ về optimal solution | Adiabatic theorem: nếu đủ chậm, ở lại ground state |
| Điều kiện "đủ chậm" | Rất chậm theo cỡ bài toán trong trường hợp xấu | $T \gg 1/\Delta_{\min}^2$, với $\Delta_{\min}$ là energy gap nhỏ nhất |
| Thực tế | Chạy trên CPU, rẻ, dễ tinh chỉnh | Chạy trên phần cứng chuyên dụng; hệ hở, có noise, không thật sự adiabatic |

Điểm chung: cả hai đều bắt đầu từ state "lộn xộn" (nhiệt độ cao hoặc superposition đều) rồi dần "đóng băng" vào vùng energy thấp.

Về lợi thế của đường hầm: trực giác là QA có thể vượt qua các rào energy *cao nhưng mỏng* mà SA phải leo qua. Điều này đúng về mặt khái niệm, nhưng nó phụ thuộc cấu trúc của địa hình energy, và chưa có bằng chứng chung rằng nó mang lại lợi thế cho các bài toán tối ưu tổ hợp thông thường (xem [B-01](01-quantum-advantage.md)).

## 3. Mô phỏng chính xác trên bài toán 3 qubit

Với 3 qubit, ta có thể tiến hóa chính xác phương trình Schrödinger dưới $H(s) = (1-s)H_0 + sH_P$ với $s = t/T$ và đo xác suất ở optimal solution $\lvert 000\rangle$ ($f = -9$).

**Phổ energy.** Energy gap giữa mức thấp nhất và mức kế tiếp đạt nhỏ nhất **1,148 tại $s \approx 0{,}258$**, và bằng 4 ở $s = 1$ (khoảng cách từ $-9$ đến $-5$). Vùng gap nhỏ là nơi quá trình ủ dễ "nhảy" sang excited state nếu chạy quá nhanh.

**Measurement probability được optimal solution theo thời gian ủ $T$:**

| $T$ | $P(000)$ | $E$ trung bình |
|---:|---:|---:|
| 0,25 | 0,146 | −0,67 |
| 0,5 | 0,191 | −2,06 |
| 1 | 0,259 | −3,87 |
| 2 | 0,371 | −5,34 |
| 4 | 0,586 | −6,86 |
| 8 | 0,874 | −8,42 |
| 16 | 0,986 | −8,93 |
| 32 | 0,999 | −9,00 |
| 64 | 1,000 | −9,00 |

(Chọn ngẫu nhiên đều cho $P = 0{,}125$ và $E = 0$.)

Các quan sát:

1. **Ủ nhanh vẫn tốt hơn ngẫu nhiên.** Ngay $T = 1$ (rất không adiabatic) đã cho $P = 0{,}26$, gấp đôi ngẫu nhiên. Điều này khớp với nhận xét ở Mục 2.2 của bài báo: quantum annealer không bắt buộc phải ở ground state trong suốt quá trình.
2. **Cần $T$ khá lớn để gần như chắc chắn.** $P > 0{,}98$ khi $T \approx 16$, cỡ hai chục lần $1/\Delta_{\min}$ (với $\Delta_{\min} \approx 1{,}15$). Với bài toán lớn hơn, nơi $\Delta_{\min}$ có thể đóng rất nhanh theo kích thước, thời gian cần thiết có thể tăng mạnh; đó là điều adiabatic theorem nói và là điểm yếu tiềm tàng của cách tiếp cận này.
3. **Thang energy quan trọng.** Giá trị tuyệt đối của $T$ chỉ có nghĩa trong đơn vị energy đang dùng: nhân **cả** $H_0$ **và** $H_P$ với $\lambda$ tương đương nhân $T$ với $\lambda$ (chỉ tích energy × thời gian mới quan trọng).

## 4. Từ phần cứng thật trở lại lý thuyết

Annealer thật (D-Wave) khác mô hình trên ở nhiều điểm: hệ tương tác với môi trường ở nhiệt độ hữu hạn (hệ hở), không thật sự adiabatic, và $H_0$, $H_P$ có thang energy cố định bởi phần cứng nên coefficient của bài toán phải được co giãn vào dải cho phép. Hậu quả: **dải coefficient rộng làm giảm độ phân giải hiệu dụng** của phần mục tiêu, đó là một trong những lý do penalty constant $P$ lớn gây hại ([B-04](04-penalties-and-encodings.md)).

## Bài tập

**Bài 1.** Một qubit, $H(s) = -(1-s)X - sZ$. Tìm energy gap giữa hai mức theo $s$ và vị trí nó nhỏ nhất.

<details>
<summary>Solution</summary>

$H(s) = -aX - bZ$ với $a = 1-s$, $b = s$ có hai eigenvalue $\pm\sqrt{a^2 + b^2}$ (vì $(aX + bZ)^2 = (a^2 + b^2)I$). Gap $= 2\sqrt{(1-s)^2 + s^2}$. Hàm $(1-s)^2 + s^2$ đạt nhỏ nhất ở $s = \tfrac12$, giá trị $\tfrac12$, nên gap nhỏ nhất $= 2\sqrt{1/2} = \sqrt2 \approx 1{,}414$ tại $s = 0{,}5$. Bài toán một qubit này không có chỗ nào gap đóng, nên ủ dễ dàng.
</details>

**Bài 2.** Vì sao thuật toán quantum annealing đòi hỏi state ban đầu là ground state của $H_0 = -\sum_j X_j$ (superposition đều), chứ không phải một state ngẫu nhiên?

<details>
<summary>Solution</summary>

Adiabatic theorem đảm bảo hệ ở lại ground state *tức thời* của $H(s)$ nếu ban đầu nó ở ground state của $H(0) = H_0$. Ground state của $-\sum_j X_j$ là $\lvert{+}\rangle^{\otimes n}$ (superposition đều của mọi solution), dễ chuẩn bị (một lớp Hadamard gate). Nếu bắt đầu từ state khác, ta không còn đảm bảo nào về state cuối. (Lưu ý bài báo nói annealer thực tế "không bắt buộc" ở ground state trong suốt quá trình, nhưng đảm bảo lý thuyết thì cần điều đó.)
</details>
