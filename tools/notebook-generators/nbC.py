import nbformat as nbf

def md(s): return nbf.v4.new_markdown_cell(s.strip("\n"))
def code(s): return nbf.v4.new_code_cell(s.strip("\n"))

def save(cells, path):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nbf.write(nb, path)

# ------------------------------------------------------------------ C1: D-Wave
nb1 = [
md(r"""
# Notebook C1: Chạy MAX-SAT trên D-Wave (Hình 4 trên máy thật)

Đi kèm [docs/C-hardware/dwave-leap.md](../../docs/C-hardware/dwave-leap.md) và [Phần A, Mục 5](../../docs/A-translation/05-quantum-annealer.md).

**Notebook chạy được dù bạn có hay không có tài khoản D-Wave.** Ô cấu hình bên dưới thử kết nối tới máy QPU thật; nếu không có API token (hoặc kết nối thất bại), nó tự chuyển sang `SimulatedAnnealingSampler` chạy trên máy bạn. Mọi ô phụ thuộc vào QPU đều được ghi chú rõ và tự bỏ qua trong chế độ mô phỏng.
"""),
code(r"""
import itertools, os, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import dimod, minorminer
import dwave_networkx as dnx
from dimod import Binary, SimulatedAnnealingSampler
from dwave.system import DWaveSampler, EmbeddingComposite

# Đặt USE_QPU=0 trong môi trường nếu muốn ép dùng trình mô phỏng.
USE_QPU = os.environ.get("USE_QPU", "1") == "1"
try:
    if not USE_QPU:
        raise RuntimeError("USE_QPU=0")
    qpu = DWaveSampler()                       # đọc token từ file cấu hình (dwave config create) hoặc biến DWAVE_API_TOKEN
    sampler = EmbeddingComposite(qpu)
    ON_QPU = True
    print("Đang dùng QPU:", qpu.solver.name, "| topology:", qpu.properties["topology"]["type"])
except Exception as e:
    sampler = SimulatedAnnealingSampler()
    ON_QPU = False
    print(f"Không dùng được QPU ({type(e).__name__}: {str(e)[:80]}).")
    print("-> Chuyển sang SimulatedAnnealingSampler (chạy cục bộ, không cần tài khoản).")
"""),
md(r"""
## 1. Mô hình: phương trình (39) với $P = 7$ (bản đã sửa)

Đây là QUBO đúng của Ví dụ 15, có đủ số hạng $-2x_3 z$. (Hình 4 trong bài gốc thiếu số hạng này; xem ghi chú ở Mục 5 của Phần A.)
"""),
code(r"""
x1, x2, x3, z = (Binary(v) for v in ("x1", "x2", "x3", "z"))
P = 7
model = x1*z - 2*z - x1*x3 + x2 + x3 + P*(x2*x3 - 2*x2*z - 2*x3*z + 3*z)

def count_unsat(a, b, c):
    clauses = [(a or (not b) or c), (a or b or (not c)), ((not a) or (not b) or c)]
    return sum(1 for cl in clauses if not cl)
satisfying = [t for t in itertools.product((0, 1), repeat=3) if count_unsat(*t) == 0]
print("Các phép gán thỏa mọi clause (đáp án đúng):", satisfying)
"""),
md(r"""
## 2. Minor-embedding: bài toán trông thế nào trên từng topology?

Máy D-Wave không cho phép coupling giữa hai qubit bất kỳ (Mục 5.2). Ta có thể thấy điều này **mà không cần máy thật**: dùng `minorminer` để nhúng đồ thị của QUBO lên các topology Chimera, Pegasus và Zephyr (bản nhỏ), rồi xem mỗi biến logic cần bao nhiêu qubit vật lý (độ dài chain).
"""),
code(r"""
bqm = dimod.BinaryQuadraticModel(model)
logical_edges = list(bqm.quadratic)
print("Các cạnh của đồ thị bài toán:", logical_edges)
print()
for name, G in (("Chimera (C2)", dnx.chimera_graph(2)),
                ("Pegasus (P2)", dnx.pegasus_graph(2)),
                ("Zephyr (Z1)", dnx.zephyr_graph(1))):
    emb = minorminer.find_embedding(logical_edges, G.edges, random_seed=1)
    chains = {v: len(q) for v, q in sorted(emb.items())}
    max_deg = max(d for _, d in G.degree())
    print(f"{name:13s} bậc tối đa mỗi qubit = {max_deg:2d} | độ dài chain của từng biến: {chains}")
"""),
md(r"""
Chimera mỗi qubit chỉ nối tối đa 5 qubit khác, nên biến $x_3$ (nối tới 3 biến khác trong đồ thị bài toán, trong đó có cặp khó đặt cạnh nhau) phải dùng một chain 2 qubit. Pegasus và Zephyr có độ kết nối cao hơn nên bài toán nhỏ này nhúng được mà không cần chain. Chain càng dài thì càng dễ bị "đứt" (qubit trong chain nhận giá trị khác nhau), như đã nói ở Mục 5.2.
"""),
md(r"""
## 3. Chạy và đọc kết quả

Giống Hình 4 của bài báo: 1000 lần chạy (`num_reads=1000`). Cột `unsat` là số clause không được thỏa, `occ` là số lần xuất hiện.
"""),
code(r"""
kwargs = dict(num_reads=1000)
if ON_QPU:
    kwargs["label"] = "co-quantum maxsat ex15"      # nhãn để tìm lại job trên Leap dashboard
sampleset = sampler.sample(model, **kwargs)

agg = sampleset.aggregate()
print("  x1 x2 x3 z  energy  unsat  occ")
for rec in sorted(agg.data(["sample", "energy", "num_occurrences"]), key=lambda r: (r.energy, -r.num_occurrences)):
    s = rec.sample
    a, b, c, d = (int(s[v]) for v in ("x1", "x2", "x3", "z"))
    print(f"   {a}  {b}  {c}  {d}  {rec.energy:6.1f}  {count_unsat(a, b, c):5d}  {rec.num_occurrences:4d}")

found = {(int(r.sample["x1"]), int(r.sample["x2"]), int(r.sample["x3"]))
         for r in agg.data(["sample", "energy"]) if r.energy == 0}
print("\nCác phép gán Energy = 0 tìm được:", sorted(found))
print("Đủ cả 5 phép gán thỏa mọi clause?", found == set(satisfying))
"""),
md(r"""
Với QUBO đã sửa, ta kỳ vọng thấy **cả 5** phép gán `000`, `011`, `100`, `101`, `111` có Energy bằng 0 (khác với Bảng 2 của bài gốc, vốn chỉ có 3). Trên máy thật, vài trạng thái Energy 1 hoặc cao hơn cũng xuất hiện do nhiễu và do chain bị đứt; số lần xuất hiện cụ thể thay đổi giữa các lần chạy.
"""),
code(r"""
if ON_QPU:
    names = sampleset.record.dtype.names
    if "chain_break_fraction" in names:
        print("Tỉ lệ chain bị đứt trung bình:", float(sampleset.record.chain_break_fraction.mean()))
    timing = sampleset.info.get("timing", {})
    print("Thời gian QPU tính phí (qpu_access_time, micro giây):", timing.get("qpu_access_time"))
    print("Embedding dùng:", sampleset.info.get("embedding_context", {}).get("embedding"))
else:
    print("(Chế độ mô phỏng: không có thông tin chain hay thời gian QPU.)")
"""),
md(r"""
## 4. Ảnh hưởng của `chain_strength` (chỉ chạy khi có QPU)

Coupling trong chain phải đủ mạnh để các qubit của chain đồng ý với nhau, nhưng quá mạnh thì "lấn át" phần bài toán thật. Ô dưới đây quét vài giá trị và đo tỉ lệ chain đứt cùng tỉ lệ lần chạy rơi vào một phép gán đúng. **Ô này tiêu tốn thời gian QPU** (mỗi giá trị 200 lần chạy), nên chỉ chạy khi `ON_QPU` là đúng.
"""),
code(r"""
def correct_fraction(ss):
    # tỉ lệ lần chạy cho ra một phép gán thỏa mọi clause (số clause không thỏa = 0)
    total = good = 0
    for rec in ss.aggregate().data(["sample", "num_occurrences"]):
        s = rec.sample
        total += int(rec.num_occurrences)
        if count_unsat(int(s["x1"]), int(s["x2"]), int(s["x3"])) == 0:
            good += int(rec.num_occurrences)
    return good / total

# Kiểm tra hàm bằng sampleset đã có ở trên (chạy được cả khi không có QPU):
print("tỉ lệ đúng của lần chạy ở Mục 3:", correct_fraction(sampleset))

if ON_QPU:
    for cs in (1, 2, 4, 8, 16):
        ss = sampler.sample(model, num_reads=200, chain_strength=cs, label=f"chain_strength={cs}")
        names = ss.record.dtype.names
        broken = float(ss.record.chain_break_fraction.mean()) if "chain_break_fraction" in names else float("nan")
        print(f"chain_strength={cs:2d}  chain đứt={broken:.3f}  tỉ lệ đúng={correct_fraction(ss):.2f}")
else:
    print("Bỏ qua phần quét chain_strength: cần QPU. Xem docs/C-hardware/dwave-leap.md để tạo tài khoản và lấy token.")
"""),
]
save(nb1, "01-dwave-leap-maxsat.ipynb")

# ------------------------------------------------------------------ C2: IBM
nb2 = [
md(r"""
# Notebook C2: Chạy QAOA trên IBM Quantum

Đi kèm [docs/C-hardware/ibm-quantum.md](../../docs/C-hardware/ibm-quantum.md) và [Phần A, Mục 6](../../docs/A-translation/06-gate-based.md).

**Notebook chạy được dù bạn có hay không có tài khoản IBM Quantum.** Nếu không kết nối được, nó dùng `FakeKingston`: một mô hình nhiễu mô phỏng chip Heron r2 156 qubit của IBM, chạy hoàn toàn trên máy bạn. Giao diện (`generate_preset_pass_manager`, `SamplerV2`) giống hệt khi chạy máy thật, nên ta thấy được tác động của nhiễu và quá trình transpile.

Chiến lược quan trọng để tiết kiệm thời gian QPU (gói miễn phí giới hạn rất ít): **tối ưu tham số trên trình mô phỏng lý tưởng trước, chỉ chạy mạch cuối cùng trên máy thật.**
"""),
code(r"""
import os, warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import minimize
from qiskit.circuit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeKingston

def f(x):                                      # hàm mục tiêu của Ví dụ 10
    return (-9 + 13*x[0] + 14*x[1] + 9*x[2]
            - 18*x[0]*x[1] - 18*x[0]*x[2] - 18*x[1]*x[2] + 36*x[0]*x[1]*x[2])

def build_ansatz(theta):                       # Hình 9 của bài báo
    qaoa_depth = len(theta) // 2
    gamma, beta = theta[:qaoa_depth], theta[qaoa_depth:]
    circuit = QuantumCircuit(3)
    for i in range(3):
        circuit.h(i)
    for i in range(qaoa_depth):
        circuit.rz(-4 * gamma[i], 0)
        circuit.rz(-5 * gamma[i], 1)
        circuit.cx(0, 1)
        circuit.cx(1, 2)
        circuit.rz(-9 * gamma[i], 2)
        circuit.cx(1, 2)
        circuit.cx(0, 1)
        for q in range(3):
            circuit.rx(2 * beta[i], q)
    circuit.measure_all()
    return circuit

def mean_f(counts):
    total = sum(counts.values())
    return sum(f([int(v) for v in k[::-1]]) * n for k, n in counts.items()) / total
"""),
md(r"""
## 1. Tối ưu tham số trên trình mô phỏng lý tưởng (miễn phí)

Dùng hàm mục tiêu đã sửa (`value +=`) như ở [Notebook 5](../A-examples/05-qaoa-integer-function.ipynb), cùng hạt giống nên tham số tìm được giống nhau.
"""),
code(r"""
ideal = AerSimulator()
SEED = 7

def objective(theta, shots=1000):
    counts = ideal.run(build_ansatz(theta), shots=shots, seed_simulator=SEED).result().get_counts()
    return mean_f(counts)

res = minimize(objective, [0.1, 0.1, 0.1, 0.1], method="COBYLA")
theta = res.x
print("tham số tối ưu (gamma1, gamma2, beta1, beta2):", np.round(theta, 3))
print("giá trị trung bình của f khi lấy mẫu:", round(res.fun, 3))
"""),
md(r"""
## 2. Chọn backend

- Có tài khoản: `QiskitRuntimeService()` đọc thông tin đã lưu bằng `save_account` (hoặc các biến môi trường `QISKIT_IBM_TOKEN`, `QISKIT_IBM_INSTANCE`), rồi `least_busy` chọn máy ít hàng đợi nhất.
- Không có tài khoản: dùng `FakeKingston()`.
"""),
code(r"""
USE_REAL = os.environ.get("USE_REAL_IBM", "1") == "1"
try:
    if not USE_REAL:
        raise RuntimeError("USE_REAL_IBM=0")
    service = QiskitRuntimeService()
    backend = service.least_busy(min_num_qubits=3, operational=True, simulator=False)
    ON_REAL = True
    print("Đang dùng máy thật:", backend.name, "|", backend.num_qubits, "qubit")
except Exception as e:
    backend = FakeKingston()
    ON_REAL = False
    print(f"Không kết nối được IBM Quantum ({type(e).__name__}).")
    print("-> Dùng FakeKingston (mô phỏng nhiễu cục bộ):", backend.name, "|", backend.num_qubits, "qubit")
"""),
md(r"""
## 3. Transpile

Máy thật chỉ hiểu một tập cổng gốc (với chip Heron: `rz`, `sx`, `x`, `cz`) và chỉ cho phép CNOT/CZ giữa các qubit nối vật lý với nhau. Bước transpile biến mạch của ta thành mạch "ISA" tương thích. Mạch ba qubit nhỏ của ta nở ra khá nhiều.
"""),
code(r"""
logical = build_ansatz(theta)
pm = generate_preset_pass_manager(backend=backend, optimization_level=1, seed_transpiler=1)
isa = pm.run(logical)
print("mạch gốc  : độ sâu", logical.depth(), "| số cổng:", dict(logical.count_ops()))
print("mạch ISA  : độ sâu", isa.depth(), "| số cổng:", dict(isa.count_ops()))
"""),
md(r"""
## 4. Chạy và so sánh với trình mô phỏng lý tưởng

Ta lấy 1000 mẫu từ backend rồi so với 1000 mẫu từ mô phỏng lý tưởng (cùng tham số). Trên máy thật hoặc mô hình nhiễu, các lời giải xấu như `111` ($f = 9$) xuất hiện nhiều hơn.
"""),
code(r"""
SHOTS = 1000
sampler = Sampler(mode=backend)                # job mode: mỗi lần chạy là một job độc lập
job = sampler.run([isa], shots=SHOTS)
if ON_REAL:
    print("job id:", job.job_id(), "| trạng thái:", job.status())
noisy = job.result()[0].data.meas.get_counts()      # thanh ghi tên 'meas' do measure_all() tạo ra

clean = ideal.run(logical, shots=SHOTS, seed_simulator=11).result().get_counts()

print("Khóa | (x1,x2,x3) |  f  | lý tưởng | backend")
for key in sorted(clean, key=lambda k: -clean[k]):
    x = tuple(int(v) for v in key[::-1])
    print(f" {key} | {x} | {f(x):3d} | {clean[key]:8d} | {noisy.get(key, 0):7d}")
print()
print("giá trị trung bình của f -> lý tưởng:", round(mean_f(clean), 2), "| backend:", round(mean_f(noisy), 2))
print("xác suất đo được lời giải tối ưu 000 -> lý tưởng:", clean.get("000", 0) / SHOTS, "| backend:", noisy.get("000", 0) / SHOTS)
"""),
code(r"""
if ON_REAL:
    # job.usage() trả về 0 cho đến khi IBM tính xong; nếu thấy 0 hãy gọi lại sau ít phút
    print("Thời gian QPU job này đã dùng (giây):", job.usage())
    print("Mức sử dụng của gói hiện tại:", service.usage())
else:
    print("(Chế độ mô phỏng: không có thông tin sử dụng QPU.)")
"""),
md(r"""
Nhận xét: nhiễu làm giảm xác suất của lời giải tối ưu và nâng xác suất của các lời giải xấu so với mô phỏng lý tưởng. Đây là điều đã đề cập ở Mục 1 của bài báo (kỷ nguyên NISQ). Với mạch lớn hơn hoặc nhiều lớp $p$ hơn, mạch ISA càng sâu và nhiễu càng nặng, nên số lớp $p$ lớn không phải lúc nào cũng tốt hơn trên máy thật.
"""),
]
save(nb2, "02-ibm-quantum-qaoa.ipynb")
