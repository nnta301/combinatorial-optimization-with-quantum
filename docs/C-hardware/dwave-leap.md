# Chạy trên D-Wave Leap

Hướng dẫn chạy bài toán MAX-SAT của [Phần A, Mục 5](../A-translation/05-quantum-annealer.md) (Hình 4, Ví dụ 15) trên máy quantum annealer D-Wave thật. Notebook đi kèm: [notebooks/C-hardware/01-dwave-leap-maxsat.ipynb](../../notebooks/C-hardware/01-dwave-leap-maxsat.ipynb).

> **Notebook chạy được ngay cả khi bạn không có tài khoản.** Nếu không tìm thấy API token, nó tự chuyển sang trình mô phỏng cục bộ. Vì vậy bạn có thể đọc và chạy thử trước, rồi quyết định có cần máy thật hay không.

## 0. Lưu ý quan trọng về quyền truy cập (kiểm tra lại trước khi bắt đầu)

Chính sách gói miễn phí của D-Wave đã thay đổi và **các nguồn hiện có mâu thuẫn nhau**. Tình trạng tìm được khi viết tài liệu này (tháng 11/2026):

- Theo [trang hỗ trợ của D-Wave](https://support.dwavesys.com/hc/en-us/articles/360003718773-What-Leap-Customer-Plans-Are-Available), khi đăng ký Leap bạn nhận **Trial Plan**, cho phép chạy một số demo; để dùng các solver lượng tử và lai cho ứng dụng của riêng mình, D-Wave hướng tới chương trình [Leap Quantum LaunchPad](https://www.businesswire.com/news/home/20250122232294/en/D-Wave-Announces-New-Leap-Quantum-LaunchPad%E2%84%A2-Program-to-Fast-track-Deployment-of-Quantum-Computing-Applications) (dùng thử 3 tháng cho người tham gia được chọn).
- Theo các [trả lời của hỗ trợ D-Wave trên cộng đồng](https://support.dwavesys.com/hc/en-us/community/posts/32226980341911-why-individual-application-could-not-be-passed-to-use-free-token), từ 22/1/2025 một số gói, trong đó có Trial, **không còn cấp API token**; tài khoản tự đăng ký không thể gửi job tùy ý từ chương trình của bạn.
- Một số nguồn bên thứ ba (và các tài liệu cũ) vẫn nói về mức miễn phí khoảng 1 phút thời gian QPU mỗi tháng. Những thông tin này có thể đã lỗi thời.

Mình **chưa xác minh được trang gói chính thức ở thời điểm hiện tại** (trang hỗ trợ chặn truy cập tự động). Hãy xem trang [What Leap Customer Plans Are Available?](https://support.dwavesys.com/hc/en-us/articles/360003718773-What-Leap-Customer-Plans-Are-Available) và [How Do I Get an API Token?](https://support.dwavesys.com/hc/en-us/articles/360003682634-How-Do-I-Get-an-API-Token) để biết gói của bạn có token hay không.

**Nếu tài khoản của bạn không có API token**, bạn vẫn học được toàn bộ nội dung bằng chế độ mô phỏng của notebook (gồm cả phần minor-embedding lên các topology Chimera, Pegasus, Zephyr, chạy hoàn toàn cục bộ), hoặc làm việc với D-Wave qua chương trình LaunchPad nếu đủ điều kiện.

## 1. Tạo tài khoản

1. Đăng ký tại <https://cloud.dwavesys.com/leap/signup>.
2. Vào Leap dashboard. Nếu gói của bạn có API token, nó hiển thị ở cột bên trái; bấm **COPY** để sao chép. Nếu token bị lộ, bấm **RESET** để tạo token mới.

## 2. Cài đặt Ocean SDK

```bash
pip install dwave-ocean-sdk
```

Bản đã dùng để kiểm tra các lệnh trong tài liệu này: `dwave-system` 1.36.0, `dimod` 0.12.23 (tháng 11/2026).

## 3. Cấu hình token

Có ba cách, chọn một:

**a) Lệnh cấu hình tương tác** (lưu token vào file cấu hình của bạn):

```bash
dwave setup          # hoặc: dwave config create
```

**b) Đăng nhập Leap rồi để SDK lấy token giúp:**

```bash
dwave auth login
dwave config create --auto-token
```

**c) Biến môi trường** (không lưu vào file; tiện cho CI hoặc máy dùng chung):

```bash
# Linux / macOS
export DWAVE_API_TOKEN="<token-cua-ban>"
# Windows PowerShell
$env:DWAVE_API_TOKEN = "<token-cua-ban>"
```

> **Bảo mật:** token tương đương mật khẩu. Không dán token vào notebook hoặc mã nguồn, và không commit file cấu hình vào git.

Kiểm tra cấu hình bằng các lệnh có sẵn của SDK:

```bash
dwave solvers        # liệt kê các solver bạn dùng được
dwave ping           # gửi một bài toán 1 qubit tới một QPU để thử kết nối
```

Nếu chưa có token, `DWaveSampler()` báo `ValueError: API token not defined`; nếu token sai, nó báo `SolverAuthenticationError`.

## 4. Chạy MAX-SAT trên QPU

Đây là Hình 4 của bài báo, **đã sửa** (thêm số hạng `- 2 * Binary('x3') * Binary('z')`; xem ghi chú ở Mục 5 Phần A):

```python
from dimod import Binary
from dwave.system import DWaveSampler, EmbeddingComposite

x1, x2, x3, z = (Binary(v) for v in ("x1", "x2", "x3", "z"))
P = 7
qubo = x1*z - 2*z - x1*x3 + x2 + x3 + P*(x2*x3 - 2*x2*z - 2*x3*z + 3*z)

sampler = EmbeddingComposite(DWaveSampler())
result = sampler.sample(qubo, num_reads=1000, label="co-quantum maxsat ex15")
print(result.aggregate())
```

`EmbeddingComposite` tự làm minor-embedding và chọn `chain_strength` mặc định. Tham số `label` giúp bạn tìm lại job trên Leap dashboard.

## 5. Đọc kết quả

`result.aggregate()` gộp các lần chạy giống nhau. Các cột quan trọng:

| Cột | Ý nghĩa |
|---|---|
| `x1 x2 x3 z` | Giá trị các biến của mẫu |
| `energy` | Giá trị hàm QUBO của mẫu. Với $z = x_2 x_3$ (tức hàm phạt bằng 0), nó bằng số clause không được thỏa |
| `num_occurrences` | Số lần mẫu này xuất hiện trong `num_reads` lần chạy |
| `chain_break_fraction` | Tỉ lệ chain bị đứt (xem `result.record.chain_break_fraction`) |

Thông tin thêm: `result.info["timing"]["qpu_access_time"]` là thời gian QPU được tính (micro giây), tiện để theo dõi mức tiêu thụ.

**Điều cần quan sát:** với QUBO đã sửa, cả **5** phép gán thỏa mọi clause (`000`, `011`, `100`, `101`, `111`) nên có Energy bằng 0. Bảng 2 của bài gốc chỉ có 3 vì mã gốc thiếu số hạng phạt. Một số mẫu có Energy 1 hoặc cao hơn vẫn xuất hiện do nhiễu, và vì chain bị đứt.

## 6. Các tham số nên thử

| Tham số | Tác dụng |
|---|---|
| `num_reads` | Số lần chạy. Tăng lên để thấy rõ phân bố, nhưng tốn thời gian QPU hơn |
| `chain_strength` | Độ mạnh coupling trong chain (Mục 5.2 Phần A). Quá nhỏ thì chain đứt; quá lớn thì lấn át phần bài toán thật. Notebook có ô quét vài giá trị |
| `annealing_time` | Thời gian mỗi lần annealing (micro giây). Dài hơn làm quá trình gần với "đoạn nhiệt" hơn, nhưng có giới hạn tùy máy |
| `label` | Nhãn job |

Các giá trị cụ thể hợp lệ phụ thuộc từng máy; xem `qpu.properties` hoặc tài liệu Ocean.

## 7. Máy thật khác trình mô phỏng ở đâu?

- Trình mô phỏng (`ExactSolver`, `SimulatedAnnealingSampler`) hoạt động trên biến logic, không có chain, không có nhiễu phần cứng.
- Trên QPU, đồ thị bài toán phải được nhúng vào topology của máy. Chạy Mục 2 của notebook để thấy: với bài toán nhỏ này, topology Chimera cần một chain 2 qubit cho biến $x_3$, trong khi Pegasus và Zephyr nhúng được mà không cần chain.
- Kết quả trên QPU thay đổi giữa các lần chạy; đừng kỳ vọng số lần xuất hiện giống Bảng 2.

## 8. Xử lý sự cố

| Triệu chứng | Nguyên nhân thường gặp |
|---|---|
| `ValueError: API token not defined` | Chưa cấu hình token. Làm lại Mục 3 |
| `SolverAuthenticationError` | Token sai, hết hạn, hoặc gói của bạn không có quyền dùng solver đó |
| Chạy rất lâu hoặc bị từ chối | Hết thời gian QPU của gói. Xem Leap dashboard |
| Nhiều chain bị đứt | Tăng `chain_strength` hoặc chọn máy có topology kết nối dày hơn |

## Tài liệu tham khảo

- Bài báo gốc, Mục 5: <https://arxiv.org/abs/2412.15778>
- Trang hỗ trợ D-Wave: <https://support.dwavesys.com/hc/en-us>
