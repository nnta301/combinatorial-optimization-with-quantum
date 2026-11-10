# B-07. So sánh công bằng với solver cổ điển, và tài liệu đọc thêm

Mở rộng cho [Phần A, Mục 7](../A-translation/07-discussion.md). Bài báo gốc kết luận rằng chưa rõ máy tính lượng tử có tối ưu nhanh hơn máy tính cổ điển trong thực tế hay không. Với người làm tối ưu tổ hợp, đây là chương thực dụng nhất: **làm thế nào để trả lời câu hỏi đó cho bài toán của chính bạn mà không tự đánh lừa mình.** Notebook minh họa cách đếm chi phí: [B5](../../notebooks/B-extensions/05-benchmarking-toy.ipynb).

> **Cảnh báo:** thí nghiệm ở notebook B5 là một **ví dụ đồ chơi** ($n = 10$ spin, mô phỏng không nhiễu) để minh họa *cách đếm*, không phải bằng chứng cho bất kỳ bên nào. Không rút kết luận nào về hiệu năng từ các con số trong đó.

## 1. Các đại lượng cần đo

**Xác suất thành công mỗi lần chạy** $p_s$: xác suất một lần chạy (một lần ủ, một shot) cho ra nghiệm tối ưu (hoặc nghiệm đạt ngưỡng chất lượng đặt trước).

**Số lần chạy cần để chắc chắn.** Để có xác suất thành công tích lũy $\ge 99\%$ cần
$$R_{99} = \left\lceil \frac{\ln(1 - 0.99)}{\ln(1 - p_s)} \right\rceil .$$

Một vài giá trị: $p_s = 0{,}1 \to 44$ lần chạy; $0{,}3 \to 13$; $0{,}5 \to 7$; $0{,}9 \to 2$; $0{,}99 \to 1$.

**Thời gian-tới-lời-giải (time-to-solution, TTS):** $\mathrm{TTS}_{99} = R_{99} \times t_{\text{lần chạy}}$. Cần tính cho *từng* thể hiện rồi lấy thống kê (trung vị, phân vị), vì độ khó giữa các thể hiện chênh nhau nhiều bậc.

Khi bài toán quá lớn để biết nghiệm tối ưu, dùng **thời gian-tới-chất lượng đích** (time-to-target): thời gian để đạt giá trị mục tiêu cố định (ví dụ tốt nhất đã biết cộng một dung sai).

## 2. Mười nguyên tắc so sánh công bằng

1. **Chọn baseline mạnh nhất cho lớp bài toán**, không phải baseline dễ thắng. Với tối ưu tổ hợp, tập baseline hợp lý gồm: solver chính xác (MIP, CP-SAT) khi thể hiện đủ nhỏ; metaheuristic mạnh (simulated annealing tinh chỉnh, tabu search, parallel tempering); và solver chuyên cho lớp bài toán (ví dụ cho Max-Cut hay QUBO). Benchmark ở [B-01](01-quantum-advantage.md) ghi nhận rằng parallel tempering cải tiến và bộ giải ABS3 chạy GPU ngang hoặc hơn bộ giải lượng tử, còn SA đơn giản thì không bằng.
2. **Cùng thể hiện, cùng hàm mục tiêu, cùng tiêu chí thành công.** Cả hai bên phải giải *cùng bài toán đã được mô hình hóa*, và cùng định nghĩa "thành công".
3. **Đo thời gian đầu-cuối, không chỉ thời gian QPU.** Tính cả chuyển đổi sang QUBO, giảm bậc, minor-embedding, tối ưu tham số (QAOA), hàng đợi, truyền dữ liệu, hậu xử lý (giải mã, sửa chain đứt, kiểm tra khả thi).
4. **Cùng ngân sách tinh chỉnh.** Nếu phía lượng tử được quét `chain_strength`, hằng số phạt, độ sâu $p$, thì phía cổ điển cũng phải được quét lịch nhiệt độ, số sweep, số lần khởi động lại, với công sức tương đương.
5. **Tương đương phần cứng.** So một QPU với một lõi CPU là không công bằng với CPU; so một QPU với cụm GPU là không công bằng với QPU. Báo cáo rõ cấu hình (số lõi, GPU) và ước lượng chi phí (tiền, năng lượng) khi có thể.
6. **Xu hướng theo kích thước, không phải một điểm.** Một con số ở $n = 20$ không nói gì về $n = 200$. Hãy quét kích thước và báo cáo cách TTS tăng theo $n$.
7. **Nhiều thể hiện, báo cáo phân bố.** Không chọn thể hiện đẹp. Báo cáo cả thể hiện khó và tỉ lệ thất bại.
8. **Không so với hộp đen không rõ.** Công bố mã, tham số, hạt giống, thể hiện để người khác tái lập.
9. **Phân biệt mô phỏng và phần cứng.** Kết quả trên trình mô phỏng không nhiễu không nói về hiệu năng trên máy thật. Mô phỏng chính xác chỉ làm được ở $n$ nhỏ, nên thường cần ngoại suy, mà ngoại suy là điểm yếu nhất.
10. **Báo cáo cả khi lượng tử không thắng.** Kết quả âm có giá trị khoa học tương đương.

## 3. Chi phí ẩn của QAOA: vòng tối ưu tham số

Khi tính chi phí của QAOA, người ta hay chỉ tính $R_{99}$ shots lấy mẫu cuối với tham số đã tối ưu, và quên phần tìm tham số. Notebook B5 minh họa trên $n = 10$ spin, 12 thể hiện Ising ngẫu nhiên với $J_{ij}$ chuẩn hóa chuẩn tắc, giả định 1000 shots mỗi lần đánh giá hàm mục tiêu trên phần cứng:

| Phương pháp | $p_s$ trung vị | $R_{99}$ | Chi phí lấy mẫu cuối | Chi phí vòng tối ưu tham số |
|---|---:|---:|---|---|
| SA, 50 sweep (cổ điển) | 0,757 | 4 | 2000 lần cập nhật spin | không có |
| QAOA, $p = 1$ | 0,034 | 135 | 135 shots | ~160 500 shots (160 lần gọi) |
| QAOA, $p = 2$ | 0,074 | 60 | 60 shots | ~495 000 shots (495 lần gọi) |
| QAOA, $p = 3$ | 0,116 | 38 | 38 shots | ~1 256 500 shots (1256 lần gọi) |

Quan sát:

- Chi phí **vòng tối ưu tham số lớn hơn chi phí lấy mẫu cuối hàng nghìn lần**. Nếu chỉ báo cáo $R_{99}$ sẽ đánh giá thấp chi phí thực của QAOA rất nhiều.
- Số lần gọi hàm mục tiêu phụ thuộc bộ tối ưu: BFGS ước lượng gradient bằng sai phân hữu hạn nên tốn $2p + 1$ lần gọi cho mỗi bước. Bộ tối ưu không dùng gradient (COBYLA) hay kỹ thuật khởi tạo thông minh cho số khác, nhưng thường vẫn cỡ hàng trăm đến hàng nghìn lần gọi. Cả SA lẫn QAOA ở đây đều chưa được tinh chỉnh.
- Đơn vị chi phí không so sánh trực tiếp được: "lần cập nhật spin" trên CPU và "shot" trên QPU có thời gian thực khác nhau nhiều bậc. So sánh nghiêm túc cần **thời gian thực đầu-cuối** trên phần cứng cụ thể.
- Ở $n = 10$ SA rất dễ; không suy ra gì cho bài lớn.

## 4. Một quy trình đề xuất cho bài toán của bạn

1. Định nghĩa **tiêu chí thành công** (nghiệm tối ưu? trong vòng $x\%$ của tốt nhất đã biết?) và **ngân sách thời gian** thực tế của ứng dụng.
2. Chọn tập thể hiện đại diện, kèm vài thể hiện lớn để xem xu hướng.
3. Cài đặt tối thiểu ba baseline cổ điển, trong đó có một solver mạnh, và tinh chỉnh chúng với ngân sách tương đương.
4. Mô hình hóa sang QUBO theo [Phần A](../A-translation/04-problem-transformation.md), chọn $P$ cẩn thận ([B-04](04-penalties-and-encodings.md)), kiểm tra tính đúng trên thể hiện nhỏ.
5. Kiểm tra khả năng nhúng ([B-05](05-embedding-and-chains.md)) hoặc độ sâu mạch sau transpile ([B-06](06-qaoa-landscape.md), [Phần C](../C-hardware/ibm-quantum.md)).
6. Đo $p_s$, $R_{99}$, TTS đầu-cuối cho mọi phương pháp, báo cáo phân bố.
7. Báo cáo kết quả, kể cả khi âm.

## 5. Tài liệu đọc thêm

Danh sách do người biên soạn tập hợp từ các nguồn đã dùng trong tài liệu này và từ hiểu biết chung về lĩnh vực. **Hãy kiểm tra lại thông tin xuất bản trước khi trích dẫn.**

**Nền tảng (đã trích trong bài báo gốc):**

- Albash, T., Lidar, D. A. *Adiabatic quantum computation.* Reviews of Modern Physics 90, 015002 (2018). Tổng quan về tính toán lượng tử đoạn nhiệt (tài liệu [1] của bài báo).
- Farhi, E., Goldstone, J., Gutmann, S. *A Quantum Approximate Optimization Algorithm.* arXiv:1411.4028 (2014). Bài báo đầu tiên đề xuất QAOA.
- Kadowaki, T., Nishimori, H. *Quantum annealing in the transverse Ising model.* (1998), tài liệu [27] của bài báo.
- Dattani, N. *Quadratization in discrete optimization and quantum mechanics.* arXiv:1901.04405 (2019). Tổng hợp các kỹ thuật giảm bậc mà bài báo nhắc tới ở Mục 5.1.

**Mô hình hóa QUBO và Ising (thêm):**

- Lucas, A. *Ising formulations of many NP problems.* Frontiers in Physics 2, 5 (2014). Danh mục công thức Ising cho nhiều bài toán NP kinh điển (tô màu đồ thị, TSP, phủ đỉnh, ...).
- Glover, F., Kochenberger, G., Du, Y. *Quantum Bridge Analytics I: a tutorial on formulating and using QUBO models.* 4OR 17 (2019). Hướng dẫn mô hình hóa QUBO từ góc nhìn của người làm vận trù học.

**Tổng quan hiện đại (thêm):**

- Hauke, P., Katzgraber, H. G., Lechner, W., Nishimori, H., Oliver, W. D. *Perspectives of quantum annealing: methods and implementations.* Reports on Progress in Physics 83, 054401 (2020).
- Blekos, K. và cộng sự. *A review on Quantum Approximate Optimization Algorithm and its variants.* Physics Reports (2024).

**Benchmark (đã dùng ở B-01):**

- Chandarana, P. và cộng sự. *The Quest for Quantum Advantage in Combinatorial Optimization: End-to-end Benchmarking of Quantum Solvers vs. Multi-core Classical Solvers.* [arXiv:2603.13607](https://arxiv.org/abs/2603.13607) (2026).

## Bài tập

**Bài 1.** Một thuật toán có $p_s = 0{,}02$ mỗi lần chạy và mỗi lần chạy mất 5 ms. Tính $R_{99}$ và $\mathrm{TTS}_{99}$.

<details>
<summary>Lời giải</summary>

$R_{99} = \lceil \ln 0{,}01 / \ln 0{,}98 \rceil = \lceil -4{,}605 / -0{,}0202 \rceil = \lceil 227{,}9 \rceil = 228$. $\mathrm{TTS}_{99} = 228 \times 5\ \text{ms} = 1{,}14\ \text{s}$.
</details>

**Bài 2.** Phương pháp A có $p_s = 0{,}5$ và mỗi lần chạy mất 100 ms. Phương pháp B có $p_s = 0{,}05$ và mỗi lần chạy mất 5 ms. Phương pháp nào có $\mathrm{TTS}_{99}$ tốt hơn?

<details>
<summary>Lời giải</summary>

A: $R_{99} = \lceil \ln 0{,}01 / \ln 0{,}5 \rceil = \lceil 6{,}64 \rceil = 7$, nên $\mathrm{TTS} = 7 \times 100 = 700$ ms. B: $R_{99} = \lceil \ln 0{,}01 / \ln 0{,}95 \rceil = \lceil 89{,}8 \rceil = 90$, nên $\mathrm{TTS} = 90 \times 5 = 450$ ms. B tốt hơn dù $p_s$ thấp hơn mười lần, vì mỗi lần chạy nhanh hơn hai mươi lần. Bài học: chỉ nhìn $p_s$ hoặc chỉ nhìn thời gian mỗi lần chạy đều dẫn đến kết luận sai; phải nhìn TTS.
</details>

**Bài 3.** QAOA cần 300 lần gọi hàm mục tiêu để tối ưu tham số (1000 shots mỗi lần gọi), rồi 40 shots lấy mẫu cuối. Mỗi shot mất 0,1 ms trên phần cứng. Tổng thời gian QPU là bao nhiêu và phần tối ưu tham số chiếm bao nhiêu phần trăm?

<details>
<summary>Lời giải</summary>

Tối ưu: $300 \times 1000 = 300\,000$ shots; lấy mẫu cuối: 40 shots; tổng $300\,040$ shots, mỗi shot 0,1 ms nên $30{,}004$ s $\approx 30$ s. Phần tối ưu chiếm $300\,000 / 300\,040 \approx 99{,}99\%$. (Chưa tính thời gian hàng đợi, nạp mạch và overhead mỗi job, vốn thường làm tổng thực lớn hơn nhiều.)
</details>
