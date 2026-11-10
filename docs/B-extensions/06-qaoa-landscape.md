# B-06. QAOA: cảnh quan năng lượng, độ sâu và chi phí mạch

Mở rộng cho [Phần A, Mục 6](../A-translation/06-gate-based.md). Bài báo giải thích cách dựng ansatz của QAOA và chạy một ví dụ. Chương này trả lời các câu hỏi tiếp theo mà người làm tối ưu thường hỏi: cảnh quan của bài toán tối ưu tham số trông thế nào, tăng độ sâu $p$ giúp được bao nhiêu, QAOA liên hệ gì với quantum annealing, và xử lý số hạng bậc cao tốn gì. Notebook: [B2](../../notebooks/B-extensions/02-qaoa-landscape.ipynb), dùng bộ mô phỏng vector trạng thái chính xác `qaoa_state` trong [code/qco_utils.py](../../code/qco_utils.py). Bộ mô phỏng này đã được đối chiếu với mạch Qiskit ở Hình 9 (cho cùng phân phối xác suất).

## 1. Hai khó khăn của QAOA: một về mặt lượng tử, một về mặt tối ưu

QAOA gồm hai phần ([Mục 6](../A-translation/06-gate-based.md)): phần lượng tử (mạch tham số hóa) và phần cổ điển (bộ tối ưu chọn $\gamma, \beta$). Khó khăn nằm ở cả hai:

- **Mạch phải đủ sâu** ($p$ đủ lớn) để biểu diễn trạng thái tốt, nhưng mạch sâu thì nhiễu nặng trên phần cứng ([Phần C](../C-hardware/ibm-quantum.md)).
- **Bộ tối ưu phải tìm được tham số tốt** trên một cảnh quan phức tạp, và mỗi lần đánh giá hàm mục tiêu trên phần cứng là một đợt đo nhiều shots ([B-07](07-benchmarking.md)).

## 2. Cảnh quan khi $p = 1$

Với $p = 1$ chỉ có hai tham số, nên ta vẽ được toàn bộ cảnh quan $E(\gamma, \beta)$ cho bài toán Ví dụ 10. Quan sát trên lưới $241 \times 121$ điểm:

- Giá trị nhỏ nhất trên lưới là $E = -4{,}412$ tại $(\gamma, \beta) \approx (0{,}340;\ 0{,}785)$, xấp xỉ $\beta = \pi/4$.
- $E$ **tuần hoàn** theo $\gamma$ (chu kỳ $2\pi$ vì $f$ nhận giá trị nguyên) và có đối xứng, nên cùng một cực tiểu xuất hiện nhiều lần. Trên lưới có 44 điểm local minimum (tính cả các bản sao do tính tuần hoàn và đối xứng).
- Tối ưu hóa bằng BFGS từ điểm ngẫu nhiên có thể rơi vào bất kỳ "thung lũng" nào, nên kết quả phụ thuộc điểm khởi đầu.

**Ý nghĩa thực tế:** vòng tối ưu cổ điển không phải phần phụ; nó là một bài toán tối ưu phi lồi thực sự. Trên phần cứng nó còn bị nhiễu lấy mẫu làm gợn thêm. Các kỹ thuật như khởi tạo nhiều điểm, khởi tạo thông minh (xem mục 4), hay dùng bộ tối ưu chịu nhiễu đều nhằm giảm khó khăn này.

## 3. Độ sâu $p$ và chất lượng nghiệm

Với mỗi $p$, chạy BFGS từ 12 điểm ngẫu nhiên và lấy kết quả tốt nhất (mô phỏng không nhiễu, bài toán 3 qubit):

| $p$ | $E$ tốt nhất | $P(\text{nghiệm tối ưu})$ |
|---:|---:|---:|
| 1 | −4,432 | 0,492 |
| 2 | −6,986 | 0,629 |
| 3 | −8,540 | 0,955 |
| 4 | −8,774 | 0,972 |
| 5 | −8,942 | 0,993 |
| 6 | −9,000 | 1,000 |

($E = -9$ là tối ưu; chọn ngẫu nhiên đều cho $E = 0$ và $P = 0{,}125$.)

Chất lượng tăng nhanh theo $p$ và đạt tối ưu ở $p = 6$. Ba lưu ý:

1. **Đây là bài 3 qubit, không nhiễu.** Với bài lớn hơn và có nhiễu, bức tranh khác: mỗi lớp thêm vào làm mạch sâu hơn (độ sâu mạch Qiskit đã nở từ 16 lên 46 sau transpile cho $p = 2$, [Phần C](../C-hardware/ibm-quantum.md)) nên nhiễu tăng và lợi ích của $p$ lớn có thể biến mất trên máy thật.
2. **Số tham số là $2p$.** Điều ta quan tâm là phân phối xác suất trên $2^3 = 8$ kết quả đo, tức 7 bậc tự do. Với $p = 6$ ansatz có 12 tham số, nhiều hơn 7, nên về mặt đếm tham số nó đủ linh hoạt để điều khiển toàn bộ phân phối; đây là một gợi ý vì sao $P$ đạt gần đúng 1,000 ở $p = 6$ không quá bất ngờ. Đây chỉ là lập luận đếm tham số, không phải chứng minh: các tham số $\gamma, \beta$ không điều khiển độc lập từng xác suất, nên việc thực sự đạt được xác suất 1 phải do tối ưu số xác nhận, như ở bảng trên.
3. **Tối ưu toàn cục các tham số không được đảm bảo** (bài toán phi lồi); số liệu là tốt nhất trong 12 lần thử.

## 4. QAOA là phiên bản rời rạc hóa của quantum annealing

Nếu đặt $\gamma_k = s_k \Delta t$ và $\beta_k = -(1 - s_k)\Delta t$ với $s_k = (k + \tfrac12)/p$ và $\Delta t = T/p$, thì QAOA độ sâu $p$ chính là xấp xỉ Trotter của quá trình ủ có thời gian $T$ ở [B-02b](02-hamiltonian-and-annealing.md). Khi $p \to \infty$ với $T$ cố định, hai kết quả phải trùng nhau. Mô phỏng xác nhận:

| $T$ | Ủ liên tục | QAOA $p = 8$ | $p = 16$ | $p = 32$ | $p = 64$ | $p = 128$ |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | −6,860 | −6,115 | −6,930 | −6,916 | −6,893 | −6,878 |
| 8 | −8,416 | −0,458 | −7,490 | −8,428 | −8,433 | −8,427 |

Giá trị hội tụ về quá trình ủ liên tục khi $p$ tăng (các dao động nhỏ là sai số Trotter). Quan trọng hơn: **khi để các tham số tối ưu tự do** (Mục 3), $p = 3$ đã đạt $E = -8{,}54$ và $p = 4$ đạt $-8{,}77$, tốt hơn cả quá trình ủ có $T = 8$ ($E = -8{,}42$), với độ sâu mạch nhỏ hơn nhiều so với $p = 32$ cần để QAOA "bắt chước" quá trình ủ đó. Cái giá là phải tối ưu $2p$ tham số.

Hệ quả: tham số đã tối ưu của QAOA không chỉ là "một lịch ủ tốt hơn"; nó có thể thoát khỏi ràng buộc của lịch ủ đơn điệu. Đồng thời, kết quả này chỉ trên một bài 3 qubit, nên không suy ra được gì cho bài lớn.

## 5. Chi phí mạch của số hạng bậc cao: không cần giảm bậc, nhưng không miễn phí

Ở máy ủ, số hạng bậc ba buộc phải giảm bậc (Mục 5.1), thêm biến phụ. Ở gate-based, ta hiện thực trực tiếp số hạng $Z_{j_1} \dots Z_{j_k}$ bằng chuỗi CNOT (phương trình (49)): một số hạng $k$ qubit tốn $2(k-1)$ cổng CNOT và một cổng RZ.

**So sánh trên Ví dụ 10.** Hamiltonian gốc (phương trình (43)) chỉ có ba số hạng Pauli: $Z_1$, $Z_2$ và $Z_1 Z_2 Z_3$. Mỗi lớp $U(H_P, \gamma)$ tốn $2 \times (3 - 1) = 4$ cổng CNOT trên 3 qubit (khớp mạch ở Hình 6).

Nếu thay vào đó khử bậc ba bằng cách đưa $z = x_2 x_3$ với hàm phạt Rosenberg (hằng số phạt 127, như công thức (36)), Hamiltonian trên 4 qubit gồm một hằng số, bốn số hạng một qubit và **sáu số hạng hai qubit** (mọi cặp trong 4 qubit đều có tương tác). Mỗi số hạng $ZZ$ tốn 2 CNOT (phương trình (48)), nên mỗi lớp tốn khoảng $6 \times 2 = 12$ CNOT trên 4 qubit.

| | Qubit | CNOT mỗi lớp |
|---|---:|---:|
| Số hạng bậc ba hiện thực trực tiếp | 3 | 4 |
| Khử bậc bằng biến phụ (Rosenberg) | 4 | 12 |

(Hai con số Pauli ở trên được tính bằng biến đổi Walsh–Hadamard của hàm mục tiêu, như ở [B-02a](02-math-and-qubo-ising.md).) Trong trường hợp này, hiện thực trực tiếp rẻ hơn ba lần số CNOT và ít hơn một qubit. Điều này không đúng với mọi bài toán: nhiều số hạng bậc cao chồng lên nhau cũng làm số CNOT tăng, và độ kết nối giữa các qubit vật lý còn quyết định chi phí thật sau transpile.

Đây là một lợi thế cấu trúc của gate-based so với máy ủ khi bài toán có số hạng bậc cao tự nhiên, nhưng với phần cứng có nhiễu, mỗi CNOT là một nguồn lỗi.

## Bài tập

**Bài 1.** Một số hạng $a\, Z_1 Z_2 Z_3 Z_4$ trong $H_P$. Hiện thực $e^{-i\gamma a Z_1 Z_2 Z_3 Z_4}$ cần bao nhiêu CNOT và RZ theo phương trình (49)?

<details>
<summary>Lời giải</summary>

$|S| = 4$ nên chuỗi CNOT $\mathrm{CNOT}_{S_1,S_2}\mathrm{CNOT}_{S_2,S_3}\mathrm{CNOT}_{S_3,S_4}$ ở trước và chuỗi đảo ở sau: $2(|S| - 1) = 6$ cổng CNOT, và một cổng RZ$(2\gamma a)$ trên qubit cuối $S_4$. Tổng: 6 CNOT, 1 RZ. (Ý tưởng: chuỗi CNOT tính chẵn lẻ của $x_{S_1} \oplus \dots \oplus x_{S_4}$ vào qubit cuối; RZ trên qubit đó nhân pha $e^{\mp i\gamma a}$ tùy chẵn lẻ; chuỗi đảo trả các qubit về lại.)
</details>

**Bài 2.** Vì sao $E(\gamma, \beta)$ khi $p = 1$ tuần hoàn theo $\gamma$ với chu kỳ $2\pi$ trong ví dụ này, nhưng nói chung chỉ tuần hoàn khi các giá trị $f(x)$ đều nguyên?

<details>
<summary>Lời giải</summary>

$U(H_P, \gamma) = e^{-i\gamma H_P}$ là ma trận đường chéo với phần tử $e^{-i\gamma f(x)}$. Nếu mọi $f(x)$ là số nguyên thì $e^{-i(\gamma + 2\pi) f(x)} = e^{-i\gamma f(x)}$ nên $U$ và do đó $E$ tuần hoàn theo $\gamma$ với chu kỳ $2\pi$. Nếu $f(x)$ có giá trị không nguyên (ví dụ hệ số thập phân) thì nói chung không còn chu kỳ chung ngắn như vậy; ngoài ra, nhân hàm mục tiêu với một hằng số làm co giãn trục $\gamma$.
</details>
