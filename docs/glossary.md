# Bảng thuật ngữ

**Quy ước:** các thuật ngữ chuyên ngành dưới đây được **giữ nguyên tiếng Anh** xuyên suốt tài liệu. Cột bên phải chỉ để giải nghĩa. Những từ thông dụng như "máy tính lượng tử", "tối ưu tổ hợp", "hàm mục tiêu", "ràng buộc" vẫn viết bằng tiếng Việt.

## Lượng tử

| Thuật ngữ | Giải nghĩa |
|---|---|
| qubit | bit lượng tử |
| superposition | chồng chập: hệ ở nhiều trạng thái cùng lúc cho đến khi bị đo |
| entanglement | rối lượng tử (còn gọi vướng víu, liên đới lượng tử): các hạt tương quan với nhau dù cách xa |
| measurement | phép đo: làm trạng thái sụp về một chuỗi bit cổ điển |
| quantum gate | cổng lượng tử |
| quantum circuit | mạch lượng tử |
| gate-based | mô hình tính toán dựa trên cổng |
| adiabatic | đoạn nhiệt: mô hình tính toán dựa trên việc Hamiltonian thay đổi chậm |
| adiabatic theorem | định lý đoạn nhiệt |
| quantum annealing | ủ lượng tử |
| quantum annealer | máy ủ lượng tử |
| quantum tunneling | hiệu ứng đường hầm lượng tử |
| Hamiltonian | toán tử mô tả năng lượng của hệ |
| ground state | trạng thái cơ bản: trạng thái có năng lượng thấp nhất |
| energy gap | khe năng lượng: chênh lệch giữa mức năng lượng thấp nhất và mức kích thích thấp nhất của Hamiltonian (không phải band gap của chất rắn) |
| Bloch sphere | mặt cầu Bloch |
| Hadamard gate | cổng Hadamard |
| Pauli-X / Pauli-Y / Pauli-Z gate | cổng Pauli-X / Y / Z |
| CNOT | cổng NOT có điều khiển |
| unitary | unita: phép biến đổi bảo toàn chuẩn |
| tensor product | tích tensor |
| computational basis | cơ sở tính toán: {\|0⟩, \|1⟩} |
| decoherence | mất kết hợp: hệ mất tính chất lượng tử do tương tác với môi trường |
| NISQ | Noisy Intermediate Scale Quantum: kỷ nguyên máy lượng tử quy mô trung gian, có nhiễu 
| state / state vector | trạng thái / vector trạng thái của hệ |
| excited state | trạng thái kích thích: trạng thái có năng lượng cao hơn ground state |
| energy | năng lượng: giá trị của Hamiltonian trên một state |
| operator | toán tử |
| eigenvalue / eigenvector | trị riêng / vector riêng |
| amplitude | biên độ (số phức) của một state trong superposition |
| diagonal matrix | ma trận đường chéo |
| expectation value | giá trị kỳ vọng của một đại lượng đo được |
| measurement probability | xác suất đo được một kết quả |
| noise | nhiễu |
| native gate | gate gốc mà phần cứng thực thi trực tiếp |
| annealing schedule | lịch ủ: cách tham số s thay đổi theo thời gian |
| periodic | tuần hoàn |

## Tối ưu

| Thuật ngữ | Giải nghĩa |
|---|---|
| feasible / infeasible | khả thi / không khả thi (thỏa / không thỏa mọi ràng buộc) |
| penalty | hàm phạt cộng vào hàm mục tiêu khi vi phạm ràng buộc |
| slack variable | biến bù, dùng để đổi bất đẳng thức thành đẳng thức |
| pseudo-Boolean function | hàm có biến nhị phân và giá trị thực |
| QUBO | Quadratic Unconstrained Binary Optimization: tối ưu nhị phân bậc hai không ràng buộc |
| Ising model | mô hình Ising: hàm bậc hai trên các biến nhận giá trị −1 hoặc 1 |
| Iverson bracket | ngoặc Iverson: đổi mệnh đề đúng/sai thành 1/0 |
| order reduction (quadratization) | giảm bậc: đưa đa thức bậc cao về bậc hai nhờ biến phụ. Chỉ bắt buộc với quantum annealer; QAOA xử lý được số hạng bậc cao |
| minor-embedding | ánh xạ đồ thị của bài toán lên topology của máy |
| chain | chuỗi các qubit vật lý biểu diễn một biến |
| coupling | ghép nối: hệ số J<sub>j,k</sub> là hệ số ghép nối giữa hai qubit |
| local minimum | cực tiểu địa phương |
| simulated annealing | ủ mô phỏng (thuật toán cổ điển) 
| solution | lời giải / nghiệm của bài toán |
| optimal solution | nghiệm tối ưu |
| term | số hạng của đa thức hoặc Hamiltonian |
| coefficient | hệ số |
| polynomial | đa thức |
| auxiliary variable | biến phụ |
| penalty function / penalty constant | hàm phạt / hằng số phạt |
| landscape | cảnh quan: đồ thị giá trị hàm theo tham số |
| optimizer | bộ tối ưu |
| sampling | lấy mẫu |
| grid | lưới |

## Thuật toán

| Thuật ngữ | Giải nghĩa |
|---|---|
| QAOA | Quantum Approximate Optimization Algorithm |
| VQE | Variational Quantum Eigensolver |
| VQA | Variational Quantum Algorithms: họ thuật toán biến phân, gồm QAOA và VQE |
| ansatz | mạch lượng tử có tham số, dạng tham số hóa của trạng thái thử |
| mixer Hamiltonian | Hamiltonian trộn trong QAOA |
| layer / depth | lớp / độ sâu của ansatz (số lớp p) |
| hybrid algorithm | thuật toán lai lượng tử – cổ điển |
| variational | biến phân: tối ưu tham số của mạch lượng tử bằng vòng lặp cổ điển |
| simulator | bộ mô phỏng |
| distribution | phân phối |
| shots | số lần chạy mạch và đo lặp lại |
