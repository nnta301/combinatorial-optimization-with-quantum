# 3 Các bài toán mẫu (Running Examples)

Trong mục này, chúng tôi giới thiệu hai bài toán tối ưu NP-hard sẽ được dùng ở các mục còn lại để minh họa các bước cần thiết khi dùng máy tính lượng tử giải bài toán tối ưu. Bài toán tối ưu thứ nhất là một hàm số nguyên có ràng buộc. Đây là một họ bài toán khá tổng quát, hữu ích để mô hình hóa cách xử lý các ràng buộc trong tối ưu lượng tử. Bài toán tối ưu thứ hai là *maximum satisfiability* (MAX-SAT) [7], một bài toán tối ưu nổi tiếng không có ràng buộc, nằm ở lõi của nhiều công cụ và rất được quan tâm trong khoa học máy tính.

## 3.1 Tối ưu số nguyên có ràng buộc (Constrained Integer Optimization)

Một *hàm số nguyên* (integer function) là hàm có đầu vào là một vector số nguyên và đầu ra là một giá trị nguyên, tức là $f : \mathbb{Z}^n \to \mathbb{Z}$. Trong công trình này, ta giả sử mình làm việc với các hàm số nguyên có thể viết dưới dạng polynomial có bậc tối đa $k$ (một hằng số). Điều này đảm bảo số term tối đa trong biểu diễn polynomial của các hàm số nguyên là $O(n^k)$. Các polynomial này có thể viết dưới dạng gọn:

$$p(z) = \sum_{\substack{w \in \mathbb{Z}^n \\ |w| \le k}} a_w \prod_{j=1}^{n} z_j^{w_j}, \tag{12}$$

trong đó $z_j$ là biến nguyên thứ $j$, và các hằng số $a_w$ là các coefficient của polynomial.

Trong *tối ưu số nguyên có ràng buộc* (constrained integer optimization), mục tiêu là cực tiểu hóa một polynomial nguyên $p(z)$ thỏa một số ràng buộc dựa trên $m$ polynomial nguyên khác $q_j(z)$. Một cách hình thức, ta phát biểu bài toán như sau:

$$\min\; p(z) \tag{13}$$

với điều kiện:

$$q_j(z) \le 0 \quad \forall j \in [m], \tag{14}$$

$$z \in \mathbb{Z}^n. \tag{15}$$

Vì lý do thực tiễn, ta sẽ cần giới hạn miền giá trị của các biến nguyên trong một khoảng $[a, b] \subseteq \mathbb{Z}$.

**Ví dụ 1.** Một thể hiện bài toán có năm biến và sáu ràng buộc như sau:

$$\min\; 5z_1^3 z_2 - 3 z_2 z_4^3 z_5 + 2 z_3$$

với điều kiện:

$$z_4 z_1 + z_2 z_3^2 - 1 \le 0,$$
$$-5 \le z_j \le 5 \quad \forall j \in [5]$$

$\square$

> **Ghi chú người dịch:** Bài gốc nói "sáu ràng buộc" nhưng chỉ viết một bất đẳng thức polynomial và một dòng chặn miền cho cả năm biến. Con số sáu có thể hiểu là 1 ràng buộc polynomial cộng với 5 ràng buộc chặn miền (mỗi biến một ràng buộc dạng $-5 \le z_j \le 5$). Ví dụ này không được dùng lại ở các mục sau; các mục sau dùng Ví dụ 10 và 13–14.

## 3.2 Maximum Satisfiability (MAX-SAT)

Bài toán MAX-SAT [7] là một bài toán nổi tiếng liên quan đến tính thỏa được của các công thức Boolean. Một *literal* là một biến Boolean $x_j$ hoặc một biến Boolean bị phủ định $\neg x_j$. Một literal dương $x_j$ được thỏa khi biến Boolean là đúng, và một literal âm $\neg x_j$ được thỏa khi biến Boolean là sai. Một *clause* là một phép tuyển (disjunction) của các literal (ví dụ $x_1 \lor \neg x_2 \lor x_3$), và được thỏa khi và chỉ khi có ít nhất một literal được thỏa. Một thể hiện MAX-SAT gồm một tập các clause $C$. Bài toán MAX-SAT là tìm một phép gán giá trị Boolean cho các biến sao cho số clause được thỏa là lớn nhất, hay tương đương, số clause không được thỏa là nhỏ nhất. Hàm mục tiêu của MAX-SAT cần cực tiểu hóa được định nghĩa là

$$f(x) = \sum_{c \in C} f_c(x), \tag{16}$$

trong đó

$$f_c(x) = \begin{cases} 1 & \text{nếu } c \text{ không được thỏa với phép gán } x, \\ 0 & \text{ngược lại.} \end{cases} \tag{17}$$

**Ví dụ 2.** Một thể hiện MAX-SAT với ba biến như sau:

$$C = \{\, x_1 \lor \neg x_2 \lor x_3,\;\; x_1 \lor x_2 \lor \neg x_3,\;\; \neg x_1 \lor \neg x_2 \lor x_3 \,\}.$$

$\square$
