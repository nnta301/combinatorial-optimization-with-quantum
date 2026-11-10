# B-01. Kỳ vọng thực tế về lợi thế lượng tử

Mở rộng cho [Phần A, Mục 1 và Mục 7](../A-translation/07-discussion.md). Bài báo gốc dành cả Mục 1 để nói về tiềm năng, và chỉ một đoạn cuối Mục 7 để nói về câu hỏi quan trọng nhất với người làm tối ưu tổ hợp: **khi nào thì máy tính lượng tử thực sự giải bài toán tối ưu tốt hơn máy tính cổ điển?** Chương này mở rộng đoạn đó.

> **Về độ tin cậy của chương này.** Lĩnh vực đang thay đổi rất nhanh. Các kết quả thực nghiệm dưới đây được tra cứu vào **tháng 11/2026**; với một số bài mình chỉ đọc được phần tóm tắt chứ chưa đọc toàn văn, và sẽ ghi rõ. Hãy coi đây là bản đồ để bạn tự kiểm chứng, không phải kết luận cuối cùng.

## 1. "Nhanh hơn" nghĩa là gì?

Trước khi đánh giá, cần tách các câu hỏi khác nhau thường bị trộn lẫn:

| Câu hỏi | Ví dụ |
|---|---|
| **Về lý thuyết**, có thuật toán lượng tử nào chứng minh được nhanh hơn *mọi* thuật toán cổ điển (hoặc nhanh hơn thuật toán cổ điển tốt nhất đã biết) không? | Thuật toán Shor cho phân tích số nguyên (không phải tối ưu tổ hợp NP-hard) |
| **Tăng tốc theo hàm mũ, đa thức, hay bậc hai?** | Grover: bậc hai |
| **Trên bài toán nào?** Bài toán tối ưu NP-hard tổng quát hay một lớp có cấu trúc? | Max-Cut tổng quát so với bài toán có cấu trúc đại số |
| **So với thuật toán cổ điển nào?** Một baseline yếu, hay solver mạnh đã được tinh chỉnh? | Simulated annealing "ngây thơ" so với parallel tempering |
| **Đo cái gì?** Chất lượng nghiệm, thời gian tới nghiệm tối ưu, hay thời gian cả quy trình từ đầu đến cuối? | Chỉ thời gian chạy QPU so với cả chuyển đổi bài toán, nhúng, hàng đợi |

Một tuyên bố nghe rất mạnh thường chỉ đúng với một tổ hợp rất hẹp của các câu trả lời trên.

## 2. Điều đã biết về mặt lý thuyết

**a) Chồng chập không có nghĩa là thử mọi lời giải cùng lúc rồi chọn cái tốt nhất.** Phần Tóm tắt của bài báo nói máy lượng tử tính toán "dường như song song". Nhưng phép đo (measurement) chỉ trả về *một* chuỗi bit ngẫu nhiên theo phân phối xác suất $|a_w|^2$. Thuật toán lượng tử chỉ hữu ích nếu nó làm xác suất của lời giải tốt tăng lên (nhờ giao thoa), và đó là phần khó.

**b) Với bài toán "hộp đen", mức tăng tốc tối đa là bậc hai.** Thuật toán Grover và khuếch đại biên độ (amplitude amplification) cho tăng tốc bậc hai khi tìm kiếm không cấu trúc, và có kết quả cận dưới cho thấy không thể tốt hơn nếu chỉ truy cập hàm mục tiêu như hộp đen. Bài báo gốc nói điều này ở Mục 7, trích [8] và [24]: mức tăng tốc bậc hai là tối đa với cách tiếp cận hộp đen, nên để có ưu thế lớn hơn ta cần khai thác *cấu trúc* của bài toán (gray-box, white-box). Bài báo cũng trích [24] kết luận rằng với phần cứng gate-based hiện nay, tăng tốc bậc hai chưa đủ để thắng GPU.

**c) Tăng tốc bậc hai bị "ăn" bởi chi phí.** Một lợi thế bậc hai chỉ có ý nghĩa nếu mỗi bước của thuật toán lượng tử không chậm hơn bước cổ điển quá nhiều. Với tần số xung nhịp và độ tin cậy của cổng hiện nay, hằng số này rất bất lợi. Đây là lý do mức tăng tốc bậc hai riêng lẻ thường chưa đủ trong thực tế.

**d) Với bài toán NP-hard tổng quát, không có thuật toán lượng tử thời gian đa thức nào được biết, và người ta cũng không tin có.** Giả thuyết chung là các bài toán NP-hard nằm ngoài lớp BQP. Đây là giả thuyết, chưa phải định lý, nhưng nó có nghĩa là đừng kỳ vọng một thuật toán lượng tử giải được mọi thể hiện của bài toán NP-hard một cách hiệu quả. Hy vọng thực tế nằm ở **một số lớp thể hiện có cấu trúc** hoặc ở **chất lượng xấp xỉ**.

## 3. Điều đã quan sát về mặt thực nghiệm (tính đến 11/2026)

Bức tranh khá lẫn lộn và có nhiều tranh cãi. Bốn điểm sau đại diện cho các hướng chính.

**Máy ủ lượng tử D-Wave.** Năm 2025, D-Wave cùng cộng sự công bố trên *Science* rằng một máy Advantage2 mô phỏng động lực học của vật liệu từ (spin glass lượng tử) nhanh hơn siêu máy tính cổ điển rất nhiều. Hai điều cần lưu ý. Thứ nhất, đây là bài toán **mô phỏng hệ lượng tử**, không phải tối ưu tổ hợp, nên không suy ra được gì trực tiếp cho tối ưu. Thứ hai, kết quả bị phản biện: các nhóm khác (xem [HPCwire](https://www.hpcwire.com/2025/03/13/d-wave-reports-quantum-supremacy-stirs-immediate-challenge-and-rebuttal/) và bài [arXiv:2503.08247](https://arxiv.org/abs/2503.08247)) cho rằng các phương pháp mô phỏng cổ điển có thể tái tạo một phần kết quả, còn D-Wave phản bác rằng các mô phỏng đó không tính cùng các đại lượng và cấu hình. Theo các nguồn mình đọc, ranh giới vẫn đang được vẽ lại.

**QAOA trong mô phỏng.** Một nghiên cứu đăng ở [*Science Advances*](https://www.science.org/doi/10.1126/sciadv.adm6761) báo cáo bằng chứng về "tăng tốc theo quy mô" của QAOA so với một số thuật toán cổ điển (branch-and-bound) trên bài toán LABS, qua mô phỏng không nhiễu tới 40 qubit. Đây là kết quả **mô phỏng ở kích thước nhỏ, ngoại suy lên**, và lập luận dựa trên giả định máy lượng tử chịu lỗi lý tưởng. Mình chưa đọc toàn văn.

**Thuật toán DQI.** *Decoded quantum interferometry* ([Nature, 2025](https://www.nature.com/articles/s41586-025-09527-5)) là một đề xuất thuật toán dùng biến đổi Fourier lượng tử để đưa một số bài toán tối ưu về bài toán giải mã. Theo phần tóm tắt các kết quả tìm kiếm mình đọc được, lợi thế dự kiến là **lý thuyết hoặc trong mô hình oracle**, phụ thuộc vào cấu trúc bài toán và vào việc dựng được mạch lượng tử đa thức hiệu quả, và một solver cổ điển được thiết kế riêng vẫn có thể thắng trên thể hiện được khảo sát. Một số công trình năm 2026 tiếp tục khảo sát cả hai chiều (tìm điều kiện có lợi thế và chỉ ra giới hạn); mình chỉ đọc tiêu đề các bài đó.

**Benchmark đầu-cuối trên IBM Heron.** Bài [arXiv:2603.13607](https://arxiv.org/abs/2603.13607) (Chandarana và cộng sự, 3/2026) so sánh một bộ giải lai lượng tử–cổ điển cho bài toán HUBO (tối ưu nhị phân bậc cao) chạy trên chip IBM Heron r3 với các solver cổ điển mạnh, trên 20 thể hiện, tính **toàn bộ quy trình từ tiền xử lý đến hậu xử lý**. Theo tóm tắt của bài: một lần chạy lai tìm được nghiệm chất lượng cao trong chưa đầy một giây và đạt năng lượng nền trong 14/20 thể hiện; với cùng thời gian chạy, simulated annealing, memetic tabu search và EasySolve **không** đạt chất lượng nghiệm đó, nhưng một phương pháp parallel tempering cải tiến và bộ giải ABS3 chạy GPU **ngang bằng hoặc tốt hơn**. Các tác giả kết luận bộ giải lượng tử "cạnh tranh được với các solver cổ điển mạnh", không phải "thắng".

**Tóm lại:** chưa có bằng chứng được chấp nhận rộng rãi về lợi thế *thực tế* của máy tính lượng tử cho tối ưu tổ hợp so với các solver cổ điển mạnh đã được tinh chỉnh. Có những kết quả đáng chú ý (đặc biệt benchmark đầu-cuối ở trên cho thấy khoảng cách đang thu hẹp), nhưng cũng nhiều tuyên bố bị phản biện hoặc chỉ đúng trong điều kiện hẹp.

## 4. Cách đọc một tuyên bố "lợi thế lượng tử"

Khi gặp một tiêu đề kiểu "máy lượng tử nhanh hơn X lần", hãy hỏi:

1. **Bài toán gì?** Tối ưu tổ hợp, hay mô phỏng vật lý, hay một bài toán nhân tạo được thiết kế cho máy lượng tử?
2. **Baseline là gì?** Có phải solver cổ điển mạnh nhất cho lớp bài toán đó, được tinh chỉnh tương đương công sức bỏ ra cho phía lượng tử không? Có dùng cùng phần cứng song song (nhiều lõi, GPU) không?
3. **Thước đo là gì?** Thời gian tới nghiệm tối ưu, hay chất lượng nghiệm trong thời gian cố định? Có tính cả thời gian chuyển bài toán sang QUBO, nhúng, tối ưu tham số (với QAOA), hàng đợi không? ([B-07](07-benchmarking.md))
4. **Kích thước nào?** Một kích thước cố định hay xu hướng theo quy mô? Có ngoại suy từ mô phỏng nhỏ không?
5. **Oracle hay đầu-cuối?** Lợi thế được chứng minh trong mô hình lý tưởng (oracle, chịu lỗi), hay đo trên phần cứng có nhiễu hiện nay?
6. **Có tái lập được không?** Mã, dữ liệu, thể hiện có công khai không?

## 5. Chi phí ẩn của việc đưa bài toán lên máy lượng tử

Phần A cho thấy mỗi bước chuyển đổi đều có cái giá, và các chi phí này trừ thẳng vào lợi thế (nếu có):

| Bước (Phần A) | Chi phí | Ví dụ định lượng trong tài liệu này |
|---|---|---|
| Biến nguyên → nhị phân (4.1) | Thêm biến | Ví dụ 6: 1 biến nguyên thành 3 biến nhị phân |
| Ràng buộc → hàm phạt, biến slack (4.3) | Thêm biến, dải hệ số rộng | Ví dụ 14: thêm 5 biến slack (chỉ cần 3 nếu dùng cận chặt) ([notebook 3](../../notebooks/A-examples/03-constraints-and-penalty.ipynb)) |
| Hằng số phạt $P$ (4.3) | $P$ lớn làm bài toán khó hơn | [B-04](04-penalties-and-encodings.md): $P$ theo (36) là 71, ngưỡng thực chỉ khoảng 1,1 trong bài knapsack |
| Giảm bậc (5.1) | Thêm biến, thêm số hạng | [B-06](06-qaoa-landscape.md): khử bậc ba tốn 4 qubit và ~12 CNOT thay vì 3 qubit và 4 CNOT |
| Nhúng lên topology (5.2) | Chain, tổng qubit vật lý tăng nhanh | [B-05](05-embedding-and-chains.md): TSP 10 thành phố (100 biến logic) cần khoảng 900 đến 1200 qubit vật lý |
| Nhiễu phần cứng (Mục 1, [Phần C](../C-hardware/ibm-quantum.md)) | Giảm xác suất nghiệm tốt | Mạch QAOA 3 qubit nở từ độ sâu 16 lên 46 sau transpile |
| Vòng tối ưu tham số (Mục 6) | Hàng trăm nghìn shots | [B-07](07-benchmarking.md) |

## 6. Vậy người làm tối ưu tổ hợp nên làm gì?

- **Học cách mô hình hóa QUBO.** Kỹ năng này, vốn là phần lõi của bài báo, dùng được cho cả máy lượng tử lẫn các solver QUBO cổ điển và "lấy cảm hứng từ lượng tử". Nó có giá trị ngay cả khi máy lượng tử chưa thắng.
- **Luôn có baseline cổ điển mạnh.** Mọi thí nghiệm lượng tử nên đi kèm so sánh công bằng ([B-07](07-benchmarking.md)).
- **Tìm bài toán có cấu trúc phù hợp.** Hy vọng lý thuyết nằm ở các lớp có cấu trúc, không phải ở "mọi bài toán NP-hard".
- **Theo dõi benchmark đầu-cuối** hơn là tiêu đề báo chí.

## Bài tập

**Bài 1.** Một tác giả báo cáo: "bộ ủ lượng tử của chúng tôi tìm được nghiệm tốt hơn simulated annealing 100 lần nhanh hơn." Hãy liệt kê ít nhất bốn câu hỏi bạn sẽ đặt ra trước khi tin điều này.

<details>
<summary>Gợi ý lời giải</summary>

Các câu hỏi hợp lý: (1) Simulated annealing nào, được tinh chỉnh ra sao (lịch nhiệt độ, số sweep, cài đặt), chạy trên phần cứng gì? (2) Có so với solver mạnh hơn SA (parallel tempering, tabu, solver chuyên biệt, MIP) không? (3) "Nhanh hơn 100 lần" tính theo thời gian QPU hay thời gian cả quy trình, gồm nhúng, hàng đợi, và tinh chỉnh tham số như `chain_strength`? (4) Trên bao nhiêu thể hiện, kích thước bao nhiêu, và xu hướng theo kích thước? (5) "Tốt hơn" là chất lượng nghiệm trung bình hay xác suất tìm nghiệm tối ưu? (6) Cả hai bên có cùng ngân sách công sức tinh chỉnh không?
</details>

**Bài 2.** Giả sử một thuật toán lượng tử cho tăng tốc bậc hai: giải một bài toán trong $\sqrt{N}$ bước thay vì $N$ bước. Mỗi bước lượng tử chậm hơn mỗi bước cổ điển $c$ lần. Với $c = 10^6$, kích thước $N$ tối thiểu để thuật toán lượng tử nhanh hơn là bao nhiêu?

<details>
<summary>Lời giải</summary>

Thời gian lượng tử $= c\sqrt{N}$, thời gian cổ điển $= N$. Lượng tử nhanh hơn khi $c\sqrt{N} < N$, tức $\sqrt{N} > c$, tức $N > c^2 = 10^{12}$. Với hằng số bất lợi $10^6$, bài toán phải có cỡ hơn một nghìn tỉ bước cổ điển thì mức tăng tốc bậc hai mới bắt đầu có ý nghĩa. Đây là lý do tăng tốc bậc hai riêng lẻ thường chưa đủ trong thực tế.
</details>
