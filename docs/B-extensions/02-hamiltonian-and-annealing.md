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

Cùng bảng đó, viết bằng toán tử Pauli-Z, là $H_P = -2Z_1 - \tfrac52 Z_2 - \tfrac92 Z_1 Z_2 Z_3$ (phương trình (43)). Hai cách viết cho cùng một ma trận; notebook B1 kiểm tra điều này.

**Ý nghĩa với bài toán tối ưu:** *tìm trạng thái có năng lượng thấp nhất* của $H_P$ chính là tìm $\arg\min f$. Nếu có quyền đọc cả bảng thì trivial; khó khăn là bảng có $2^n$ dòng. Máy lượng tử không "đọc bảng"; nó làm một quá trình vật lý (ủ) hoặc một dãy cổng (QAOA) có xu hướng đưa trạng thái về vùng năng lượng thấp.

**Bậc của hàm quyết định cấu trúc Hamiltonian.** Hệ số của tích $\bigotimes_{j \in S} Z_j$ là biến đổi Walsh–Hadamard của bảng giá trị ([B-02a](02-math-and-qubo-ising.md)). Hàm bậc $k$ cho Hamiltonian có các số hạng chạm nhiều nhất $k$ qubit. Máy ủ chỉ hỗ trợ số hạng một và hai qubit (nên phải giảm bậc, Mục 5.1), trong khi mạch gate-based hiện thực được số hạng nhiều qubit bằng chuỗi CNOT (Mục 6).

## 2. Hai quá trình ủ

| | Simulated annealing (SA) | Quantum annealing (QA) |
|---|---|---|
| Hệ ở đâu | Một lời giải $x$ cụ thể tại mỗi thời điểm | Một trạng thái lượng tử (chồng chập các lời giải) |
| Cái gì "nóng" | Nhiệt độ $T$: xác suất chấp nhận bước xấu | Trường ngang (transverse field) $H_0 = -\sum X_j$ trộn các lời giải |
| Lịch trình | $T$ giảm từ cao xuống thấp | $H(s) = (1-s)H_0 + sH_P$, $s: 0 \to 1$ |
| Cách vượt rào năng lượng | Nhảy nhiệt (thermal hop): cần đủ nhiệt để leo qua | Hiệu ứng đường hầm (quantum tunneling) và giao thoa |
| Đảm bảo lý thuyết | Với lịch làm nguội đủ chậm (logarit) hội tụ về nghiệm tối ưu | Adiabatic theorem: nếu đủ chậm, ở lại trạng thái cơ bản |
| Điều kiện "đủ chậm" | Rất chậm theo cỡ bài toán trong trường hợp xấu | $T \gg 1/\Delta_{\min}^2$, với $\Delta_{\min}$ là energy gap nhỏ nhất |
| Thực tế | Chạy trên CPU, rẻ, dễ tinh chỉnh | Chạy trên phần cứng chuyên dụng; hệ hở, có nhiễu, không thật sự đoạn nhiệt |

Điểm chung: cả hai đều bắt đầu từ trạng thái "lộn xộn" (nhiệt độ cao hoặc chồng chập đều) rồi dần "đóng băng" vào vùng năng lượng thấp.

Về lợi thế của đường hầm: trực giác là QA có thể vượt qua các rào năng lượng *cao nhưng mỏng* mà SA phải leo qua. Điều này đúng về mặt khái niệm, nhưng nó phụ thuộc cấu trúc của địa hình năng lượng, và chưa có bằng chứng chung rằng nó mang lại lợi thế cho các bài toán tối ưu tổ hợp thông thường (xem [B-01](01-quantum-advantage.md)).

## 3. Mô phỏng chính xác trên bài toán 3 qubit

Với 3 qubit, ta có thể tiến hóa chính xác phương trình Schrödinger dưới $H(s) = (1-s)H_0 + sH_P$ với $s = t/T$ và đo xác suất ở nghiệm tối ưu $\lvert 000\rangle$ ($f = -9$).

**Phổ năng lượng.** Energy gap giữa mức thấp nhất và mức kế tiếp đạt nhỏ nhất **1,148 tại $s \approx 0{,}258$**, và bằng 4 ở $s = 1$ (khoảng cách từ $-9$ đến $-5$). Vùng gap nhỏ là nơi quá trình ủ dễ "nhảy" sang trạng thái kích thích nếu chạy quá nhanh.

**Xác suất đo được nghiệm tối ưu theo thời gian ủ $T$:**

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

1. **Ủ nhanh vẫn tốt hơn ngẫu nhiên.** Ngay $T = 1$ (rất không đoạn nhiệt) đã cho $P = 0{,}26$, gấp đôi ngẫu nhiên. Điều này khớp với nhận xét ở Mục 2.2 của bài báo: quantum annealer không bắt buộc phải ở trạng thái cơ bản trong suốt quá trình.
2. **Cần $T$ khá lớn để gần như chắc chắn.** $P > 0{,}98$ khi $T \approx 16$, cỡ hai chục lần $1/\Delta_{\min}$ (với $\Delta_{\min} \approx 1{,}15$). Với bài toán lớn hơn, nơi $\Delta_{\min}$ có thể đóng rất nhanh theo kích thước, thời gian cần thiết có thể tăng mạnh; đó là điều adiabatic theorem nói và là điểm yếu tiềm tàng của cách tiếp cận này.
3. **Thang năng lượng quan trọng.** Giá trị tuyệt đối của $T$ chỉ có nghĩa trong đơn vị năng lượng đang dùng: nhân **cả** $H_0$ **và** $H_P$ với $\lambda$ tương đương nhân $T$ với $\lambda$ (chỉ tích năng lượng × thời gian mới quan trọng).

## 4. Từ phần cứng thật trở lại lý thuyết

Máy ủ thật (D-Wave) khác mô hình trên ở nhiều điểm: hệ tương tác với môi trường ở nhiệt độ hữu hạn (hệ hở), không thật sự đoạn nhiệt, và $H_0$, $H_P$ có thang năng lượng cố định bởi phần cứng nên hệ số của bài toán phải được co giãn vào dải cho phép. Hậu quả: **dải hệ số rộng làm giảm độ phân giải hiệu dụng** của phần mục tiêu, đó là một trong những lý do hằng số phạt $P$ lớn gây hại ([B-04](04-penalties-and-encodings.md)).

## Bài tập

**Bài 1.** Một qubit, $H(s) = -(1-s)X - sZ$. Tìm energy gap giữa hai mức theo $s$ và vị trí nó nhỏ nhất.

<details>
<summary>Lời giải</summary>

$H(s) = -aX - bZ$ với $a = 1-s$, $b = s$ có hai trị riêng $\pm\sqrt{a^2 + b^2}$ (vì $(aX + bZ)^2 = (a^2 + b^2)I$). Gap $= 2\sqrt{(1-s)^2 + s^2}$. Hàm $(1-s)^2 + s^2$ đạt nhỏ nhất ở $s = \tfrac12$, giá trị $\tfrac12$, nên gap nhỏ nhất $= 2\sqrt{1/2} = \sqrt2 \approx 1{,}414$ tại $s = 0{,}5$. Bài toán một qubit này không có chỗ nào gap đóng, nên ủ dễ dàng.
</details>

**Bài 2.** Vì sao thuật toán ủ lượng tử đòi hỏi trạng thái ban đầu là trạng thái cơ bản của $H_0 = -\sum_j X_j$ (chồng chập đều), chứ không phải một trạng thái ngẫu nhiên?

<details>
<summary>Lời giải</summary>

Adiabatic theorem đảm bảo hệ ở lại trạng thái cơ bản *tức thời* của $H(s)$ nếu ban đầu nó ở trạng thái cơ bản của $H(0) = H_0$. Trạng thái cơ bản của $-\sum_j X_j$ là $\lvert{+}\rangle^{\otimes n}$ (chồng chập đều của mọi lời giải), dễ chuẩn bị (một lớp cổng Hadamard). Nếu bắt đầu từ trạng thái khác, ta không còn đảm bảo nào về trạng thái cuối. (Lưu ý bài báo nói máy ủ thực tế "không bắt buộc" ở trạng thái cơ bản trong suốt quá trình, nhưng đảm bảo lý thuyết thì cần điều đó.)
</details>
