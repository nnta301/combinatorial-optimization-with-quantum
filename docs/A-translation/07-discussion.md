# 7 Thảo luận và hướng phát triển (Discussion and Future Directions)

Trong bài báo này, chúng tôi đã trình bày cách giải các bài toán tối ưu tổ hợp bằng tính toán lượng tử. Chúng tôi đã đưa ra một cách tiếp cận tổng quát và có hệ thống để biến bài toán ban đầu thành một bài toán tương đương, sẵn sàng được tối ưu bởi các máy tính lượng tử hiện nay. Khi giải một bài toán cụ thể, có thể tập trung vào một số tính chất của bài toán để đơn giản hóa các bước, giảm số biến được thêm vào hoặc ước lượng các hằng số phạt [23]. Cần có thêm nghiên cứu để hiểu cách chọn các hằng số phạt và cách giảm thiểu số biến mà ta cần thêm vào để bậc hai hóa (quadratize) hàm mục tiêu [17].

Có nhiều cách khác nhau để biến một bài toán tối ưu tổ hợp, và các cách biến đổi khác nhau có thể cho hiệu năng khác nhau. Tài liệu gần đây có những ví dụ về tác động này [38]. Việc cách biến đổi nào là phù hợp nhất cho một bài toán cho trước vẫn là một câu hỏi mở.

Xuyên suốt bài báo, chúng tôi giả định rằng ta có một biểu thức toán học của hàm mục tiêu. Điều này không phải lúc nào cũng đúng. Hàm mục tiêu có thể là một mô phỏng trên máy tính cổ điển, khiến việc biến bài toán thành biểu thức toán học trở nên khó khăn (hoặc không thể). Có những đề xuất như AutoQUBO [32, 34] để tìm QUBO ứng với một hàm mục tiêu hộp đen (black-box) tùy ý.

Trong khi ở đây chúng tôi tập trung vào tối ưu đơn mục tiêu, ta cũng có thể tìm thấy một vài ví dụ trong tài liệu mà mục tiêu là tối ưu đa mục tiêu, dùng quantum annealer [4] hoặc máy tính gate-based [15]. Tại thời điểm viết bài, có ít hơn 5 bài báo về chủ đề này trong tài liệu hiện tại, nên có thể nói rằng tối ưu đa mục tiêu bằng máy tính lượng tử là một lĩnh vực nghiên cứu mới nổi.

Cuối cùng, nếu tập trung vào các khía cạnh cơ bản hơn của tối ưu lượng tử, vẫn chưa rõ liệu máy tính lượng tử có thể tối ưu các hàm nhanh hơn máy tính cổ điển trong thực tế hay không. Thực ra, có một số công trình chứng minh rằng có thể đánh giá hiệu quả giá trị trung bình của hàm mục tiêu cho các lời giải được sinh bằng ansatz của QAOA trên một máy cổ điển [11]. Tất nhiên, điều này không phải là giải bài toán, nhưng nó gợi ý rằng việc điều chỉnh tham số của ansatz trong QAOA có thể được thực hiện trên máy cổ điển nếu số lớp $p$ đủ thấp; chỉ dùng máy tính lượng tử ở lần lấy mẫu cuối cùng của QAOA để thu các lời giải. Chính công trình đó cũng đề xuất một thuật toán lấy cảm hứng từ lượng tử (quantum-inspired) dựa trên kết quả này. Điều này đặt ra câu hỏi liệu QAOA có thể tối ưu các bài toán nhanh hơn các thuật toán cổ điển hay không, và câu hỏi đó vẫn chưa có lời đáp. Hơn nữa, trong một bài báo gần đây [24], các tác giả kết luận rằng các máy tính lượng tử gate-based hiện nay không thể cạnh tranh với GPU và mức tăng tốc bậc hai do thuật toán Grover và khuếch đại biên độ (amplitude amplification) mang lại không đủ để giải các bài toán tìm kiếm và tối ưu nhanh hơn phần cứng cổ điển hiện tại. Điều này nghĩa là ta cần những cách tiếp cận thuật toán mới. Mức tăng tốc bậc hai là mức tăng tốc tối đa ta có thể đạt được khi dùng cách tiếp cận hộp đen cho bài toán tối ưu [8]. Điều này nghĩa là ta cần dùng các cách tiếp cận *gray-box* [12] và *white-box* để đạt được ưu thế lượng tử (quantum supremacy) trong tối ưu.

> **Ghi chú người dịch:** Đoạn cuối của §7 là phần gần nhất với câu hỏi mà người làm tối ưu tổ hợp quan tâm nhất: *khi nào thì lượng tử thực sự có lợi*. Bài gốc chỉ dành một đoạn cho chủ đề này; Phần B mở rộng ở [B-01](../B-extensions/01-quantum-advantage.md) và [B-07](../B-extensions/07-benchmarking.md), gồm cách so sánh công bằng với solver cổ điển. Xem [B-extensions/](../B-extensions/).

---

## Lời cảm ơn (Acknowledgements)

Nghiên cứu này được tài trợ một phần bởi dự án PID 2020-116727RB-I00 (HUmove) do MCIN/AEI/10.13039/501100011033 tài trợ; mạng lưới TAILOR ICT-48 (số 952215) do chương trình nghiên cứu và đổi mới Horizon 2020 của EU tài trợ; Junta de Andalucía, Tây Ban Nha, theo hợp đồng QUAL21 010UMA; và Đại học Málaga (PAR 4/2023).

## Tài liệu tham khảo (References)

Danh sách 38 tài liệu tham khảo [1]–[38] được giữ nguyên như bài gốc; xem trang 29–31 của [references/2412.15778v2.pdf](../../references/2412.15778v2.pdf).
