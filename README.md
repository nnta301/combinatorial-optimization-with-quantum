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

Các notebook chạy được bằng trình mô phỏng, không cần tài khoản. Phần chạy trên máy thật cần tài khoản D-Wave Leap hoặc IBM Quantum (xem Phần C).

## Notebook cho Phần A

Các notebook trong [notebooks/A-examples/](notebooks/A-examples/) tái hiện và kiểm chứng các ví dụ của bài báo bằng tính toán (duyệt vét cạn, mô phỏng). Mã dùng chung nằm trong [code/qco_utils.py](code/qco_utils.py).

| Notebook | Nội dung |
|---|---|
| [01-qubo-and-ising](notebooks/A-examples/01-qubo-and-ising.ipynb) | Chuyển QUBO sang Ising, phương trình (8)–(11) |
| [02-binary-encoding-and-objective](notebooks/A-examples/02-binary-encoding-and-objective.ipynb) | Ví dụ 4–6, 9–11: biểu diễn nhị phân, hàm mục tiêu |
| [03-constraints-and-penalty](notebooks/A-examples/03-constraints-and-penalty.ipynb) | Ví dụ 13–14: slack, hằng số phạt |
| [04-quantum-annealer-maxsat](notebooks/A-examples/04-quantum-annealer-maxsat.ipynb) | Ví dụ 15–16, Hình 4, Bảng 2 (không cần tài khoản D-Wave) |
| [05-qaoa-integer-function](notebooks/A-examples/05-qaoa-integer-function.ipynb) | Ví dụ 17–19, Hình 8–10, Bảng 3 (trình mô phỏng Qiskit Aer) |

## Phần C: chạy trên phần cứng thật

| Hướng dẫn | Notebook |
|---|---|
| [D-Wave Leap](docs/C-hardware/dwave-leap.md) | [01-dwave-leap-maxsat](notebooks/C-hardware/01-dwave-leap-maxsat.ipynb) |
| [IBM Quantum](docs/C-hardware/ibm-quantum.md) | [02-ibm-quantum-qaoa](notebooks/C-hardware/02-ibm-quantum-qaoa.ipynb) |

Hai notebook này tự chuyển sang trình mô phỏng khi không tìm thấy tài khoản, nên chạy được ngay cả khi bạn chưa đăng ký. Lưu ý chính sách gói miễn phí của D-Wave và IBM thay đổi thường xuyên; đọc phần "Lưu ý" ở đầu mỗi hướng dẫn trước khi đăng ký.

## Trạng thái

Đang xây dựng. Đã xong: bản dịch Phần A (§1–§7), 5 notebook cho Phần A, hướng dẫn và notebook Phần C. Chưa có: Phần B (mở rộng). Các notebook Phần C mới được chạy ở chế độ mô phỏng; phần chạy trên máy thật chưa được kiểm chứng bằng tài khoản thật.
