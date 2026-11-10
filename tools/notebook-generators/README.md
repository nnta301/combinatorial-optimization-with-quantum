# Script sinh và chạy notebook

Các notebook trong [notebooks/](../../notebooks/) được sinh từ các script Python ở đây (bằng `nbformat`), rồi chạy bằng `nbclient` để lưu kèm kết quả. Lý do dùng script: mọi chỗ cần sửa văn bản hay mã đều nằm ở một nơi, và có thể sinh lại toàn bộ notebook cho nhất quán.

> **Lưu ý:** nếu bạn sửa nội dung một notebook, hãy sửa **cả script tương ứng**. Nếu chỉ sửa file `.ipynb` thì lần sinh lại sau sẽ ghi đè thay đổi của bạn.

## Cài đặt

```bash
pip install -r requirements-dev.txt
```

## Sinh và chạy lại

Mỗi script ghi file `.ipynb` vào **thư mục hiện tại**, nên cần chạy từ đúng thư mục notebook (để các đường dẫn tương đối như `../../code` hoạt động khi chạy notebook).

| Script | Chạy từ thư mục | Sinh ra |
|---|---|---|
| `nb12.py` | `notebooks/A-examples` | Notebook A-01, A-02 |
| `nb345.py` | `notebooks/A-examples` | Notebook A-03, A-04, A-05 |
| `nbB.py` | `notebooks/B-extensions` | Notebook B1 đến B5 |
| `nbC.py` | `notebooks/C-hardware` | Notebook C1, C2 |
| `run_nb.py` | thư mục chứa notebook | Chạy các notebook được liệt kê và ghi đè kết quả vào chính file |

Ví dụ cho Phần A:

```bash
cd notebooks/A-examples
python ../../tools/notebook-generators/nb12.py
python ../../tools/notebook-generators/nb345.py
python ../../tools/notebook-generators/run_nb.py 01-qubo-and-ising.ipynb 02-binary-encoding-and-objective.ipynb 03-constraints-and-penalty.ipynb 04-quantum-annealer-maxsat.ipynb 05-qaoa-integer-function.ipynb
```

Trên Windows, đặt `PYTHONIOENCODING=utf-8` để các lệnh in tiếng Việt không bị lỗi mã hóa.

## Thời gian chạy

Notebook B4 (`04-embedding-scaling.ipynb`) chạy lâu nhất, khoảng 3 đến 6 phút, vì nhúng đồ thị lên topology cỡ thật. Các notebook còn lại chạy trong vài giây đến khoảng một phút.
