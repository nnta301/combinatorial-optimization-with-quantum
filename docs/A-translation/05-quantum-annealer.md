# 5 Giải bài toán trên quantum annealer (Solving the problem in the Quantum Annealer)

Các quantum annealer (xem Mục 2.2) có khả năng tìm trạng thái có năng lượng cực tiểu của một Hamiltonian chứa các số hạng tuyến tính phụ thuộc vào từng qubit và các tương tác cặp giữa chúng. Để dùng quantum annealer, ta cần biểu diễn hàm mục tiêu dưới dạng một mô hình Ising với các tương tác cặp. Thường dễ hơn nếu trước hết biến bài toán ban đầu thành QUBO rồi biến QUBO thành mô hình Ising bằng các công thức đã thấy ở Mục 2.1. Ở Mục 4 ta đã thấy cách biến bài toán tối ưu thành một đa thức pseudo-Boolean không ràng buộc. Trong mục này, chúng tôi sẽ mô tả cách thu được một QUBO từ đa thức pseudo-Boolean đó và cách giải QUBO trên một quantum annealer.

## 5.1 Giảm bậc (Order Reduction)

Quantum annealer đòi hỏi đa thức pseudo-Boolean phải có bậc hai. Các số hạng bậc hai và bậc một đã có sẵn trong đa thức không cần thay đổi. Ta sẽ tập trung vào các số hạng bậc cao. Trong tài liệu có thể nhận ra hai chiến lược để giảm bậc của một đa thức pseudo-Boolean. Chiến lược thứ nhất là thay các tích của hai biến $xy$ bằng một biến mới $z$. Nếu làm điều này ở mọi số hạng chứa các biến $x$ và $y$, ta giảm bậc của các số hạng đó đi một. Để giữ cho giá trị của $z$ bằng tích của $x$ và $y$, ta đưa vào một biểu thức phạt của Rosenberg [35]: $P(xy - 2xz - 2yz + 3z)$. Người đọc có thể dễ dàng kiểm tra rằng khi $z = xy$ thì biểu thức bằng không, nhưng nếu $z \neq xy$ thì biểu thức bằng $P$ (khi $xy = 1$ và $z = 0$) hoặc ít nhất $P$ (khi $xy = 0$ và $z = 1$: bằng $P$ nếu đúng một trong hai biến $x$, $y$ bằng 1, và bằng $3P$ nếu $x = y = 0$). Biểu thức phạt này được cộng vào đa thức như bất kỳ ràng buộc nào khác của bài toán. Áp dụng thủ tục này lặp đi lặp lại cho từng đơn thức có ba biến trở lên, cuối cùng ta thu được một biểu thức bậc hai. Kiểu biến đổi này được gọi là *toàn cục* (global), vì mỗi lần xuất hiện của tích các biến có thể được thay bằng biến mới và một số hạng phạt toàn cục được cộng vào đa thức pseudo-Boolean cuối cùng.

> **Đã sửa so với bài gốc:** Bài gốc viết rằng khi $xy = 0$ và $z = 1$ thì biểu thức bằng $3P$. Điều này chỉ đúng khi $x = y = 0$ (giá trị $0 - 0 - 0 + 3 = 3$). Nếu đúng một trong hai biến bằng 1 thì giá trị là $P$ (ví dụ $x = 1$, $y = 0$, $z = 1$: $0 - 2 - 0 + 3 = 1$). Bản dịch đã viết lại câu này cho chính xác. Điều cần thiết không đổi: mọi trường hợp $z \neq xy$ đều cho giá trị **ít nhất là $P > 0$**.

**Ví dụ 15.** Xét thể hiện MAX-SAT ở Ví dụ 2. Hàm mục tiêu, được tính ở Ví dụ 9, là $x_1 x_2 x_3 - 2x_2 x_3 - x_1 x_3 + x_2 + x_3$. Có một số hạng bậc ba trong biểu thức đó mà ta sẽ loại bỏ nhờ biểu thức phạt của Rosenberg. Ta đưa vào biến $z = x_2 x_3$. Hàm mục tiêu cuối cùng là

$$f(x, z) = x_1 z - 2z - x_1 x_3 + x_2 + x_3 + P\,(x_2 x_3 - 2x_2 z - 2x_3 z + 3z), \tag{39}$$

trong đó hằng số phạt $P$ có thể được tính bằng biểu thức cho ở phương trình (36). Lưu ý rằng phương trình (39) là một QUBO. $\square$

Chiến lược thứ hai để giảm bậc là áp dụng một biến đổi *cục bộ* (local) cho từng đơn thức bậc cao. Biến đổi này thay đơn thức bằng một biểu thức bậc hai có cùng lời giải tối ưu. Một ví dụ về các biến đổi cục bộ trong bài toán cực tiểu hóa là thay một đơn thức có hệ số âm $a \prod_{j \in S} x_j$, với $a < 0$, bằng biểu thức bậc hai $a\left(\sum_{j \in S} x_j - |S| + 1\right) t$, trong đó $t$ là một biến mới. Nếu có nhiều đơn thức bậc cao, mỗi đơn thức sẽ cần một biến $t$ mới; đó là lý do các biến đổi này được gọi là cục bộ. Cách tiếp cận này có thể cần nhiều biến mới, nhưng ưu điểm là ta không phải đưa ra hằng số phạt $P$.

**Ví dụ 16.** Hãy hình dung ta muốn cực đại hóa hàm mục tiêu ở Ví dụ 10. Ta có thể chuyển bài toán về cực tiểu hóa bằng cách nhân hàm mục tiêu với $-1$. Số hạng bậc ba duy nhất trong biểu thức của $-f(x)$ là $-36x_1 x_2 x_3$, có hệ số âm. Do đó ta có thể áp dụng biến đổi cục bộ $-36x_1 x_2 x_3 \to -36(x_1 + x_2 + x_3 - 2)\,t$. Hàm mục tiêu cuối cùng cần cực tiểu hóa là

$$f'(x, t) = 9 - 13x_1 - 14x_2 - 9x_3 + 18x_1 x_2 + 18x_1 x_3 + 18x_2 x_3 - 36\,(x_1 + x_2 + x_3 - 2)\,t, \tag{40}$$

trong đó $t$ là một biến nhị phân mới. $\square$

Chúng tôi chỉ nêu một ví dụ về biến đổi cục bộ, hợp lệ khi hệ số của đơn thức là âm trong bài toán cực tiểu hóa (hoặc dương trong bài toán cực đại hóa). Người đọc quan tâm đến các biến đổi cục bộ có thể tham khảo bản tổng hợp của Nike Dattani [16].

> **Đã sửa so với bài gốc (Ví dụ 16 và đoạn ngay sau):**
> - **Phương trình (40):** bài gốc in số hạng cuối là $(x_2 + x_2 + x_3 - 2)\,t$, một lỗi đánh máy. Đúng ra là $(x_1 + x_2 + x_3 - 2)\,t$, khớp với biến đổi $-36x_1 x_2 x_3 \to -36(x_1 + x_2 + x_3 - 2)\,t$ viết ngay phía trên. Bản dịch đã sửa thành $x_1$.
> - **Câu về điều kiện áp dụng biến đổi cục bộ:** bài gốc viết "hợp lệ khi hệ số của đơn thức là dương trong âm trong bài toán cực tiểu hóa", bị lặp chữ. Ý đúng là: hợp lệ khi hệ số là **âm** trong bài toán cực tiểu hóa (hoặc dương trong bài toán cực đại hóa), khớp với điều kiện $a < 0$ ở đoạn trên. Bản dịch đã sửa thành "âm".
>
> Để thấy biến đổi cục bộ là đúng: nếu mọi $x_j = 1$ thì $\sum x_j - |S| + 1 = 1$, và việc cực tiểu hóa theo $t$ cho $t = 1$, giá trị $a$; nếu có ít nhất một $x_j = 0$ thì hệ số của $t$ là $a \cdot (\text{số} \le 0) \ge 0$ và $t = 0$ cho giá trị 0. Cả hai trường hợp khớp với đơn thức gốc $a \prod x_j$.

---

## 5.2 Sử dụng quantum annealer (Using the quantum annealer)

Các quantum annealer chuyên dụng để cực tiểu hóa các mô hình Ising. Khi đã có một QUBO, ta có thể biến nó thành mô hình Ising bằng các phương trình (8) đến (11). Trong mô hình Ising cuối cùng, ta có thể bỏ số hạng hằng, vì nó chỉ làm dịch hàm mục tiêu mà không đổi cực tiểu toàn cục. Do đó ta có thể đặt $J_{j,j} = 0$ với mọi $j$. Khi hai biến $s_j$ và $s_k$ được ánh xạ vào hai qubit trong quantum annealer, hệ số $J_{j,k}$ được gọi là *coupling* giữa hai qubit.

Các quantum annealer hiện đại không cho phép có coupling giữa một cặp qubit bất kỳ; tương tác bị giới hạn ở một số cặp được xác định bởi topology của quantum annealer. Ở Hình 3, chúng tôi trình bày ba topology kết nối khác nhau của các máy D-Wave: *Chimera*, *Pegasus* và *Zephyr*. Trong thực tế, ràng buộc do topology áp đặt nghĩa là ta không thể đặt giá trị khác không cho một hệ số $J_{j,k}$ bất kỳ trong mô hình Ising. Để giải quyết vấn đề này, thay vì ánh xạ một biến $s_j$ vào một qubit đơn, ta cần biểu diễn một biến bằng một tập các qubit được nối với nhau trong quantum annealer, còn gọi là một *chain*. Coupling giữa các qubit trong chain phải âm và có giá trị tuyệt đối lớn để tránh việc các qubit khác nhau của chain nhận các giá trị khác nhau. Khi có một qubit trong chain có giá trị khác với các qubit còn lại ở trạng thái lượng tử cuối cùng, biến được chain biểu diễn không có giá trị xác định trong trạng thái lượng tử đó. Bài toán ánh xạ mô hình Ising lên topology của một máy lượng tử cụ thể được gọi là *minor-embedding*, và là bài toán NP-hard [30].

> **Hình 3** *(Topology đồ thị của các máy D-Wave: (a) Chimera, (b) Pegasus, (c) Zephyr)*. Hình này trong bài gốc là tài liệu chính thức của D-Wave được tái bản với sự cho phép, nên bản dịch này không sao chép lại. Xem các hình tương ứng trong bài gốc (trang 21 của [references/2412.15778v2.pdf](../../references/2412.15778v2.pdf)) hoặc trong tài liệu chính thức của D-Wave.

Các công cụ phần mềm hiện nay để dùng quantum annealer giúp người dùng thực hiện tự động một số bước trên. Ví dụ, thường không cần biến QUBO thành mô hình Ising. Cũng không cần tìm các hằng số cho biểu thức phạt, vì chúng tự tính giá trị phù hợp từ chính các ràng buộc. Một ví dụ nổi bật về SDK mã nguồn mở để giải các bài toán tối ưu tổ hợp bằng quantum annealer là D-Wave Ocean.<sup>5</sup> Hình 4 trình bày một đoạn mã Python đơn giản dùng D-Wave Ocean SDK để giải thể hiện MAX-SAT ở Ví dụ 2, dùng hàm fitness đã tính ở Ví dụ 15 với hằng số phạt $P = 7$. Kết quả thu được khi chạy trên hệ Advantage 4.1 của D-Wave được trình bày ở Bảng 2. Mỗi hàng biểu diễn một tổ hợp khác nhau của các biến nhị phân ở cuối quá trình annealing, thu được qua 1000 lần chạy. Ta có thể quan sát thấy các phép gán thỏa mọi clause (Energy bằng 0) xuất hiện thường xuyên hơn các tổ hợp khác. Lưu ý: Bảng 2 là kết quả gốc của tác giả, thu được với phiên bản mã chưa có số hạng $-2x_3 z$ trong biểu thức phạt (xem ghi chú bên dưới Bảng 2), nên chỉ có ba trong năm phép gán thỏa mọi clause xuất hiện.

<sup>5</sup> <https://www.dwavesys.com/solutions-and-products/ocean/>

```python
from dimod import Binary, ExactSolver
from dwave.system import DWaveSampler, EmbeddingComposite
qubo = Binary('x1') * Binary('z') - 2 * Binary('z') \
  - Binary('x1') * Binary('x3') + Binary('x2') + Binary('x3') \
  + 7*(Binary('x2')*Binary('x3') - 2 * Binary('x2') * Binary('z') - 2 * Binary('x3') * Binary('z') + 3 * Binary('z'))
sampler = EmbeddingComposite(DWaveSampler())
result=sampler.sample(qubo, num_reads=1000)
print(result)
```

*Hình 4: Mã dùng D-Wave Ocean SDK để giải Ví dụ 15. (Đã sửa: thêm số hạng `- 2 * Binary('x3') * Binary('z')` ở dòng 5; xem ghi chú bên dưới Bảng 2.)*

*Bảng 2: Kết quả gốc của tác giả, thu được sau khi chạy mã ở Hình 4 **trước khi sửa** (chưa có số hạng $-2x_3 z$). Energy là giá trị của hàm mục tiêu (số clause không được thỏa) ứng với mỗi tổ hợp biến, và cột cuối cho biết số lần tổ hợp ở hàng đó xuất hiện trong các lần chạy.*

| $x_1$ | $x_2$ | $x_3$ | $z$ | Energy | Occurrences |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | 0 | 0 | 0 | 0.0 | 371 |
| 1 | 0 | 1 | 0 | 0.0 | 320 |
| 0 | 0 | 0 | 0 | 0.0 | 270 |
| 1 | 1 | 0 | 0 | 1.0 | 16 |
| 0 | 0 | 1 | 0 | 1.0 | 15 |
| 0 | 1 | 0 | 0 | 1.0 | 8 |

> **Đã sửa so với bài gốc (Hình 4, Bảng 2 và câu mô tả kết quả):**
> - **Lỗi trong mã gốc.** Dòng 5 của Hình 4 trong bài gốc là `7*(x2*x3 - 2*x2*z + 3*z)`, thiếu số hạng $-2x_3 z$ so với phương trình (39), $P(x_2 x_3 - 2x_2 z - 2x_3 z + 3z)$. Bản dịch đã thêm số hạng này vào mã (`- 2 * Binary('x3') * Binary('z')`).
> - **Vì sao thiếu số hạng này là lỗi.** Khi thiếu, tổ hợp $z = x_2 x_3 = 1$ bị phạt sai (với $x_2 = x_3 = z = 1$, phạt trong mã gốc bằng $2P$ thay vì 0), nên QUBO trong mã gốc không còn tương đương với bài toán MAX-SAT ban đầu.
> - **Số phép gán thỏa mọi clause.** Thể hiện MAX-SAT ở Ví dụ 2 có **5** phép gán thỏa mọi clause: $(x_1, x_2, x_3) \in \{000,\ 011,\ 100,\ 101,\ 111\}$. Phương trình (39) và mã đã sửa có đúng 5 cực tiểu (hai trong số đó, $011$ và $111$, có $z = 1$). QUBO trong mã gốc chỉ còn 3 cực tiểu ($000$, $100$, $101$), chính là ba hàng đầu của Bảng 2. Các phép gán $011$ và $111$ bị loại oan. Kết quả này đã được kiểm tra bằng cách duyệt vét cạn cả 16 tổ hợp của $(x_1, x_2, x_3, z)$.
> - **Bảng 2 được giữ nguyên.** Bảng 2 là dữ liệu thực nghiệm mà tác giả thu được trên máy D-Wave Advantage 4.1 bằng mã gốc (thiếu số hạng), nên bản dịch không thay số liệu. Câu mô tả kết quả ("ba phép gán thỏa mọi clause") đã được viết lại để nói rõ điều này. Chạy lại bằng mã đã sửa sẽ cho ra các tổ hợp $011$ và $111$ cùng $z = 1$ với Energy bằng 0; bạn có thể tự kiểm tra bằng [notebooks/A-examples/04-quantum-annealer-maxsat.ipynb](../../notebooks/A-examples/04-quantum-annealer-maxsat.ipynb) (chạy không cần tài khoản D-Wave). Hướng dẫn chạy trên máy thật sẽ có ở Phần C.
