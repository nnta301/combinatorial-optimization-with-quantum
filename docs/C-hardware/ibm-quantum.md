# Chạy trên IBM Quantum

Hướng dẫn chạy mạch QAOA của [Phần A, Mục 6](../A-translation/06-gate-based.md) (Hình 9, Ví dụ 10) trên máy tính lượng tử gate-based của IBM. Notebook đi kèm: [notebooks/C-hardware/02-ibm-quantum-qaoa.ipynb](../../notebooks/C-hardware/02-ibm-quantum-qaoa.ipynb).

> **Notebook chạy được ngay cả khi bạn không có tài khoản.** Nếu không kết nối được IBM Quantum, nó dùng `FakeKingston`, một mô hình noise mô phỏng chip Heron r2 156 qubit, chạy hoàn toàn trên máy bạn. Giao diện giống hệt khi chạy máy thật.

## 0. Gói miễn phí và giới hạn

Theo [trang giá của IBM Quantum](https://www.ibm.com/quantum/pricing), **Open Plan** cho phép dùng miễn phí các máy tính lượng tử của IBM **tối đa 10 phút thời gian chạy mỗi tháng**; người dùng tích cực có thể được xin thêm. Các gói trả phí: Pay-As-You-Go (từ 96 USD/phút), Flex (từ 72 USD/phút), Premium (từ 48 USD/phút), và On-Prem.

Một số điểm cần biết:

- **"Thời gian" ở đây là thời gian mạch thực sự chạy trên chip**, không tính thời gian chờ trong hàng đợi. Mạch ba qubit của ta chạy 1000 shots chỉ tốn vài giây QPU.
- Một số nguồn ghi chu kỳ tính là 28 ngày thay vì tháng lịch, và có đợt khuyến mãi tặng thêm thời gian trong một khoảng đăng ký nhất định. Các chi tiết này thay đổi; hãy xem [Open Plan trên trang tài liệu của IBM](https://quantum.cloud.ibm.com/docs/en/guides/plans-overview) (mình chưa mở được trang này tự động để xác minh).
- Trình mô phỏng cục bộ (`AerSimulator`) không bị giới hạn.

## 1. Cảnh báo về mã cũ trên mạng

Nền tảng IBM Quantum đã được nâng cấp, nên nhiều hướng dẫn cũ không còn chạy:

- Tham số `channel="ibm_quantum"` **không còn hợp lệ**. Phiên bản `qiskit-ibm-runtime` 0.52.0 mà mình dùng để kiểm tra báo `ValueError: 'channel' can only be 'ibm_cloud', or 'ibm_quantum_platform'`. Hãy dùng `ibm_quantum_platform`.
- `IBMQ.load_account()` và `execute()` của Qiskit cũ không còn dùng được. Dùng `QiskitRuntimeService`, `SamplerV2` và `EstimatorV2` từ `qiskit_ibm_runtime`, xem [tài liệu IBM Quantum](https://quantum.cloud.ibm.com/docs) (tìm hướng dẫn chuyển đổi, "migration guide", từ nền tảng cũ sang nền tảng mới).

## 2. Tạo tài khoản và lấy thông tin truy cập

1. Tạo tài khoản tại <https://quantum.cloud.ibm.com/>.
2. Lấy **API key** và thông tin **instance** (tên hoặc CRN) từ trang tài khoản. Open Plan thường có sẵn một instance miễn phí; chi tiết cách hiển thị trên giao diện có thể thay đổi nên mình không mô tả từng nút bấm.

## 3. Cài đặt và lưu thông tin đăng nhập

```bash
pip install qiskit qiskit-aer qiskit-ibm-runtime
```

Lưu thông tin một lần trên máy cá nhân (lưu vào `~/.qiskit/qiskit-ibm.json`):

```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="<api-key-cua-ban>",
    instance="<ten-hoac-CRN-cua-instance>",
    set_as_default=True,
    overwrite=True,
)
```

Hoặc dùng biến môi trường (SDK đọc `QISKIT_IBM_TOKEN`, `QISKIT_IBM_INSTANCE`, `QISKIT_IBM_CHANNEL`, `QISKIT_IBM_URL`):

```bash
export QISKIT_IBM_CHANNEL="ibm_quantum_platform"
export QISKIT_IBM_TOKEN="<api-key-cua-ban>"
export QISKIT_IBM_INSTANCE="<ten-hoac-CRN-cua-instance>"
```

> **Bảo mật:** chỉ dùng `save_account` trên máy bạn tin tưởng. Không dán API key vào notebook hoặc mã nguồn, và không commit file cấu hình vào git.

Kiểm tra kết nối:

```python
service = QiskitRuntimeService()
print([b.name for b in service.backends(operational=True, simulator=False)])
```

Nếu chưa lưu tài khoản, `QiskitRuntimeService()` báo `AccountNotFoundError`.

## 4. Quy trình chạy QAOA, và cách tiết kiệm thời gian QPU

Gói miễn phí chỉ có 10 phút, nên làm theo thứ tự sau:

1. **Tối ưu tham số $\gamma, \beta$ trên trình mô phỏng lý tưởng** (`AerSimulator`, miễn phí). Vòng tối ưu COBYLA cần hàng chục lần chạy mạch, nếu chạy trên máy thật sẽ tốn thời gian và hàng đợi.
2. **Chỉ chạy mạch cuối cùng trên máy thật**, với số shots vừa đủ.
3. **So sánh** kết quả máy thật với mô phỏng lý tưởng.

```python
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

service = QiskitRuntimeService()
backend = service.least_busy(min_num_qubits=3, operational=True, simulator=False)

# `logical` là mạch build_ansatz(theta) đã tối ưu (xem notebook)
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa = pm.run(logical)                       # chuyển sang tập native gate và sơ đồ nối của chip

sampler = Sampler(mode=backend)             # job mode: mỗi lần chạy là một job độc lập
job = sampler.run([isa], shots=1000)
counts = job.result()[0].data.meas.get_counts()
```

Ghi chú:

- **Transpile là bắt buộc.** Máy thật chỉ chạy các native gate (với chip Heron: `rz`, `sx`, `x`, `cz`) và chỉ cho phép two-qubit gate giữa các qubit nối vật lý với nhau. Mạch 16 lớp gate của ta nở thành khoảng 46 lớp sau transpile (xem notebook).
- **Tên thanh ghi.** `circuit.measure_all()` tạo thanh ghi tên `meas`, nên kết quả đọc ở `data.meas`. Nếu bạn tự tạo thanh ghi cổ điển với tên khác thì đổi tên tương ứng.
- **Job mode.** Mình dùng `Sampler(mode=backend)`. Theo hiểu biết của mình, Open Plan không dùng session; hãy xem tài liệu hiện hành của IBM nếu bạn muốn dùng `Session`.
- **Job có thể phải chờ hàng đợi** từ vài phút đến hàng giờ. `job.job_id()` cho mã để lấy lại kết quả sau bằng `service.job(job_id)`.

## 5. Theo dõi mức sử dụng

```python
print(job.usage())        # thời gian QPU của job (giây); có thể là 0 cho đến khi IBM tính xong
print(service.usage())    # mức sử dụng của gói hiện tại
```

## 6. Đọc kết quả

Ví dụ kết quả của notebook ở chế độ mô phỏng noise (`FakeKingston`, 1000 shots, cùng tham số tối ưu):

| Khóa | $(x_1,x_2,x_3)$ | $f$ | Lý tưởng | Có noise |
|:-:|:-:|:-:|:-:|:-:|
| 000 | (0,0,0) | −9 | 312 | 269 |
| 110 | (0,1,1) | −4 | 285 | 223 |
| 101 | (1,0,1) | −5 | 166 | 161 |
| 011 | (1,1,0) | 0 | 147 | 111 |
| 010 | (0,1,0) | 5 | 41 | 87 |
| 100 | (0,0,1) | 0 | 27 | 76 |
| 001 | (1,0,0) | 4 | 16 | 36 |
| 111 | (1,1,1) | 9 | 6 | 37 |

Giá trị trung bình của $f$ xấu đi từ khoảng −4,5 (lý tưởng) lên khoảng −3,2 (có noise), và measurement probability được solution tối ưu `000` giảm từ 31% xuống 27%. Đây là bảng của **mô hình noise cục bộ**, không phải kết quả đo trên máy thật. Cả mô hình noise lẫn máy thật đều sampling ngẫu nhiên nên số liệu của bạn sẽ khác một chút giữa các lần chạy (cột "Lý tưởng" thì cố định vì dùng hạt giống cố định).

Khóa của Qiskit có dạng `q2 q1 q0`, nên $(x_1, x_2, x_3)$ là chuỗi bit đọc ngược (xem ghi chú về thứ tự bit ở Mục 6 Phần A).

## 7. Noise làm hỏng điều gì?

- Mỗi two-qubit gate (`cz`) có sai số lớn hơn nhiều so với single-qubit gate. Mạch của ta có 8 gate `cz` sau transpile.
- Depth mạch càng lớn thì qubit càng bị decoherence trước khi đo xong.
- Hệ quả thực tế: tăng số layer $p$ của QAOA có thể cải thiện chất lượng trên giấy nhưng làm kết quả trên máy thật **tệ đi**. Đây chính là hạn chế của kỷ nguyên NISQ đã nhắc ở Mục 1 của bài báo.

## 8. Xử lý sự cố

| Triệu chứng | Nguyên nhân thường gặp |
|---|---|
| `ValueError: 'channel' can only be ...` | Dùng `channel="ibm_quantum"` cũ. Đổi thành `ibm_quantum_platform` |
| `AccountNotFoundError` | Chưa `save_account` hoặc chưa đặt biến môi trường |
| Lỗi mạch không được hỗ trợ | Quên transpile bằng `generate_preset_pass_manager(backend=backend)` |
| Job chờ rất lâu | Hàng đợi dài; thử backend khác hoặc chạy vào giờ ít người dùng |
| Hết thời gian QPU | Đã dùng hết 10 phút của kỳ hiện tại; chuyển sang mô phỏng hoặc chờ kỳ sau |

## Tài liệu tham khảo

- Bài báo gốc, Mục 6: <https://arxiv.org/abs/2412.15778>
- Tài liệu IBM Quantum: <https://quantum.cloud.ibm.com/docs>
