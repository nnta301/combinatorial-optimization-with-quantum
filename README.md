# Tối ưu tổ hợp với máy tính lượng tử

Tài liệu tiếng Việt dành cho những người đã có nền tảng về **tối ưu tổ hợp (combinatorial optimization)** và muốn tiếp cận hướng giải bằng **máy tính lượng tử**.

Tài liệu dựa trên bài tutorial:

> F. Chicano, G. Luque, Z. A. Dahi, R. Gil-Merino. *Combinatorial Optimization with Quantum Computers*. arXiv:2412.15778v2 (2025). Bản đã đăng: <https://doi.org/10.1080/0305215X.2024.2435538>

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

## Trạng thái

Đang xây dựng. Hiện đã có khung thư mục và bảng thuật ngữ nháp.
