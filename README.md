# Tối ưu tổ hợp với máy tính lượng tử

Tài liệu tiếng Việt dành cho những người đã có nền tảng về **tối ưu tổ hợp (combinatorial optimization)** và muốn tiếp cận hướng giải bằng **máy tính lượng tử**.

Tài liệu dựa trên bài tutorial:

> F. Chicano, G. Luque, Z. A. Dahi, R. Gil-Merino. *Combinatorial Optimization with Quantum Computers*. arXiv:2412.15778v2 (2025). <https://arxiv.org/abs/2412.15778>

Bản PDF gốc nằm ở [references/2412.15778v2.pdf](references/2412.15778v2.pdf).

## Cấu trúc

| Phần | Thư mục | Nội dung |
|---|---|---|
| A | [docs/A-translation/](docs/A-translation/) | Bản dịch bám sát bài báo, giữ nguyên số mục, phương trình, ví dụ, hình |
| B | [docs/B-extensions/](docs/B-extensions/) | Phần mở rộng: giải thích thêm, so sánh, bài tập |
| C | [docs/C-hardware/](docs/C-hardware/) | Hướng dẫn chạy trên phần cứng thật (D-Wave Leap, IBM Quantum) |

Notebook tương ứng nằm trong [notebooks/](notebooks/); mã dùng chung trong [code/](code/). Bảng thuật ngữ Anh–Việt: [docs/glossary.md](docs/glossary.md).

Quy ước: nội dung trong khung **Ghi chú người dịch** là của người biên soạn, không phải của tác giả gốc. Khung **Đã sửa so với bài gốc** đánh dấu những chỗ bản dịch đã sửa lỗi của bài gốc, kèm giải thích.

## Lộ trình đọc

1. [Lời nói đầu](docs/00-preface.md)
2. Phần A theo thứ tự §1 → §7
3. Phần B tương ứng sau mỗi chương A
4. Phần C khi muốn chạy trên máy thật

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```

Các phiên bản trong [requirements.txt](requirements.txt) được ghim theo bản đã chạy thử với Python 3.14. Các notebook chạy được bằng trình mô phỏng, không cần tài khoản. Phần chạy trên máy thật cần tài khoản D-Wave Leap hoặc IBM Quantum (xem Phần C).

Nếu muốn sinh lại hoặc chạy hàng loạt notebook, xem [tools/notebook-generators/README.md](tools/notebook-generators/README.md).

## Notebook cho Phần A

Các notebook trong [notebooks/A-examples/](notebooks/A-examples/) tái hiện và kiểm chứng các ví dụ của bài báo bằng tính toán (duyệt vét cạn, mô phỏng). Mã dùng chung nằm trong [code/qco_utils.py](code/qco_utils.py).

| Notebook | Nội dung |
|---|---|
| [01-qubo-and-ising](notebooks/A-examples/01-qubo-and-ising.ipynb) | Chuyển QUBO sang Ising, phương trình (8)–(11) |
| [02-binary-encoding-and-objective](notebooks/A-examples/02-binary-encoding-and-objective.ipynb) | Ví dụ 4–6, 9–11: biểu diễn nhị phân, hàm mục tiêu |
| [03-constraints-and-penalty](notebooks/A-examples/03-constraints-and-penalty.ipynb) | Ví dụ 13–14: slack, penalty constant |
| [04-quantum-annealer-maxsat](notebooks/A-examples/04-quantum-annealer-maxsat.ipynb) | Ví dụ 15–16, Hình 4, Bảng 2 (không cần tài khoản D-Wave) |
| [05-qaoa-integer-function](notebooks/A-examples/05-qaoa-integer-function.ipynb) | Ví dụ 17–19, Hình 8–10, Bảng 3 (trình mô phỏng Qiskit Aer) |

## Phần B: mở rộng

Mỗi chương B bám theo một chương A, bổ sung giải thích, thí nghiệm bằng số và bài tập có solution.

| Chương | Mở rộng cho | Notebook |
|---|---|---|
| [B-01: Expectation thực tế về lợi thế lượng tử](docs/B-extensions/01-quantum-advantage.md) | §1, §7 | |
| [B-02a: Toán nền và dẫn công thức QUBO ↔ Ising](docs/B-extensions/02-math-and-qubo-ising.md) | §2.1 | [A-01](notebooks/A-examples/01-qubo-and-ising.ipynb) |
| [B-02b: Hamiltonian, quantum annealing và simulated annealing](docs/B-extensions/02-hamiltonian-and-annealing.md) | §2.2, §2.3 | [B1](notebooks/B-extensions/01-hamiltonian-and-annealing.ipynb) |
| [B-04: Penalty function và cách mã hóa](docs/B-extensions/04-penalties-and-encodings.md) | §4 | [B3](notebooks/B-extensions/03-penalty-and-encodings.ipynb) |
| [B-05: Minor-embedding và chain](docs/B-extensions/05-embedding-and-chains.md) | §5 | [B4](notebooks/B-extensions/04-embedding-scaling.ipynb) |
| [B-06: QAOA, landscape và depth](docs/B-extensions/06-qaoa-landscape.md) | §6 | [B2](notebooks/B-extensions/02-qaoa-landscape.ipynb) |
| [B-07: So sánh công bằng và tài liệu đọc thêm](docs/B-extensions/07-benchmarking.md) | §7 | [B5](notebooks/B-extensions/05-benchmarking-toy.ipynb) |

## Phần C: chạy trên phần cứng thật

| Hướng dẫn | Notebook |
|---|---|
| [D-Wave Leap](docs/C-hardware/dwave-leap.md) | [01-dwave-leap-maxsat](notebooks/C-hardware/01-dwave-leap-maxsat.ipynb) |
| [IBM Quantum](docs/C-hardware/ibm-quantum.md) | [02-ibm-quantum-qaoa](notebooks/C-hardware/02-ibm-quantum-qaoa.ipynb) |

Hai notebook này tự chuyển sang trình mô phỏng khi không tìm thấy tài khoản, nên chạy được ngay cả khi bạn chưa đăng ký. Lưu ý chính sách gói miễn phí của D-Wave và IBM thay đổi thường xuyên; đọc phần "Lưu ý" ở đầu mỗi hướng dẫn trước khi đăng ký.

## Giấy phép và ghi nguồn

- **Bài báo gốc** (F. Chicano, G. Luque, Z. A. Dahi, R. Gil-Merino, arXiv:2412.15778) được distribution theo giấy phép [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Bản PDF trong [references/](references/) và bản dịch ở Phần A được phép theo giấy phép đó.
- **Phần A là bản dịch có chỉnh sửa**, tức tác phẩm phái sinh của bài gốc. Các thay đổi so với bài gốc gồm: dịch sang tiếng Việt, vẽ lại các hình (trừ Hình 3, chỉ dẫn link), sửa các lỗi của bài gốc (mỗi chỗ nằm trong khung **Đã sửa so với bài gốc** kèm giải thích), và thêm các khung **Ghi chú người dịch**. Bản dịch không do các tác giả gốc xác nhận hay tài trợ.
- **Văn bản tài liệu do người biên soạn viết** (Phần B, Phần C, lời nói đầu, chữ trong notebook): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- **Mã nguồn** ([code/](code/), [tools/](tools/) và các ô mã trong notebook): giấy phép MIT, xem [LICENSE](LICENSE).

## State

Bản đầu tiên của cả ba phần đã hoàn thành:

- **Phần A:** bản dịch §1–§7 và 5 notebook. Đã sửa các lỗi tìm thấy trong bài gốc, mỗi chỗ có giải thích.
- **Phần B:** 7 chương mở rộng và 5 notebook.
- **Phần C:** hướng dẫn và notebook cho D-Wave Leap và IBM Quantum.

Tất cả notebook đã được chạy ở chế độ mô phỏng. Phần chạy trên máy thật ở Phần C chưa được kiểm chứng bằng tài khoản thật. Nội dung về thực nghiệm lượng tử (B-01) phản ánh tình hình tháng 11/2026 và có thể lỗi thời nhanh.
