import nbformat as nbf

def md(s): return nbf.v4.new_markdown_cell(s.strip("\n"))
def code(s): return nbf.v4.new_code_cell(s.strip("\n"))

def save(cells, path):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nbf.write(nb, path)

F10 = r"""
f_poly = {frozenset(): -9, frozenset({0}): 13, frozenset({1}): 14, frozenset({2}): 9,
          frozenset({0, 1}): -18, frozenset({0, 2}): -18, frozenset({1, 2}): -18, frozenset({0, 1, 2}): 36}
"""

# ------------------------------------------------------------------ B1
nb1 = [
md(r"""
# Notebook B1: Hamiltonian là "bảng giá trị", và mô phỏng quá trình quantum annealing

Đi kèm [B-02: Hamiltonian và quantum annealing](../../docs/B-extensions/02-hamiltonian-and-annealing.md).

Hai việc: (1) thấy tận mắt rằng Hamiltonian của bài toán $H_P$ chỉ là một diagonal matrix chứa các giá trị của hàm mục tiêu; (2) mô phỏng chính xác quá trình ủ $H(s) = (1-s)H_0 + sH_P$ cho bài toán của Ví dụ 10 (3 qubit, optimal solution duy nhất), để thấy vai trò của *energy gap* và thời gian ủ $T$.
"""),
code(r"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
sys.path.insert(0, "../../code")
from qco_utils import cost_vector
""" + F10 + r"""
cost = cost_vector(f_poly, 3)
"""),
md(r"""
## 1. $H_P$ là bảng giá trị của hàm mục tiêu

Với 3 biến nhị phân có $2^3 = 8$ solution. Hamiltonian $H_P$ là ma trận $8 \times 8$ đường chéo, phần tử thứ $i$ là $f(x)$ của solution thứ $i$. Cùng bảng đó có thể viết bằng operator Pauli-Z, như phương trình (43): $H_P = -2Z_1 - \tfrac{5}{2}Z_2 - \tfrac{9}{2}Z_1Z_2Z_3$.
"""),
code(r"""
Z = np.diag([1.0, -1.0]); I2 = np.eye(2)
def on(qubit_ops):                      # qubit 0 = bit ít quan trọng nhất (như Qiskit)
    out = np.array([[1.0]])
    for m in reversed(qubit_ops):
        out = np.kron(out, m)
    return out

HP_pauli = -2*on([Z, I2, I2]) - 2.5*on([I2, Z, I2]) - 4.5*on([Z, Z, Z])
print("H_P (Pauli) có đường chéo trùng bảng f(x):", np.allclose(np.diag(HP_pauli), cost),
      "| ngoài đường chéo bằng 0:", np.allclose(HP_pauli, np.diag(np.diag(HP_pauli))))
print()
print(" i | x1 x2 x3 |  f(x)")
for i in range(8):
    x = [(i >> j) & 1 for j in range(3)]
    print(f" {i} |  {x[0]}  {x[1]}  {x[2]} | {cost[i]:5.0f}")
"""),
md(r"""
Điều này giải thích vì sao các Pauli-Z gate là then chốt: chúng đường chéo trong computational basis, nên tổng và tích của chúng sinh ra đúng các Hamiltonian có dạng "bảng giá trị". Bài toán tối ưu trở thành: *tìm state có energy thấp nhất của một diagonal matrix đã biết trước*. Nếu ta được phép đọc cả bảng thì việc này tầm thường; khó khăn là bảng có $2^n$ dòng.
"""),
md(r"""
## 2. Phổ energy của $H(s) = (1-s)H_0 + sH_P$

$H_0 = -\sum_j X_j$ có ground state là superposition đều $|{+}{+}{+}\rangle$ (dễ chuẩn bị). Khi $s$ tăng từ 0 đến 1, $H(s)$ đi từ $H_0$ đến $H_P$. Ta vẽ 8 mức energy và tìm *energy gap* nhỏ nhất giữa mức thấp nhất và mức kế tiếp.
"""),
code(r"""
X = np.array([[0.0, 1.0], [1.0, 0.0]])
H0 = -sum(on([X if j == q else I2 for j in range(3)]) for q in range(3))
HP = np.diag(cost)

ss = np.linspace(0, 1, 401)
levels = np.array([np.linalg.eigvalsh((1 - s) * H0 + s * HP) for s in ss])
gap = levels[:, 1] - levels[:, 0]
k = gap.argmin()
print(f"energy gap nhỏ nhất = {gap[k]:.3f} tại s = {ss[k]:.3f}   (gap ở s = 1: {gap[-1]:.1f})")

fig, ax = plt.subplots(figsize=(6, 3.6))
ax.plot(ss, levels, lw=1.2)
ax.axvline(ss[k], ls=":", c="gray")
ax.set_xlabel("s"); ax.set_ylabel("energy"); ax.set_title("Phổ energy của H(s)")
plt.tight_layout(); plt.show()
"""),
md(r"""
## 3. Measurement probability được optimal solution theo thời gian ủ $T$

Ta tiến hóa $|\psi\rangle$ dưới $H(s)$ với $s = t/T$, rồi tính xác suất ở state $|000\rangle$ (optimal solution, $f = -9$). $T$ nhỏ là ủ quá nhanh (không còn adiabatic); $T$ lớn thì hệ đi theo ground state.
"""),
code(r"""
def anneal(T, per_unit=60, min_steps=300):
    N = max(min_steps, int(T * per_unit)); dt = T / N
    psi = np.ones(8, complex) / np.sqrt(8)
    for step in range(N):
        s = (step + 0.5) / N
        w, V = eigh((1 - s) * H0 + s * HP)
        psi = V @ (np.exp(-1j * w * dt) * (V.conj().T @ psi))
    return np.abs(psi) ** 2

Ts = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64]
rows = []
for T in Ts:
    p = anneal(T)
    rows.append((T, p[0], p @ cost))
print("   T   P(000)   E trung bình")
for T, p0, e in rows:
    print(f"{T:5.2f}  {p0:6.3f}   {e:7.2f}")
print("tham chiếu: chọn ngẫu nhiên đều cho P = 0.125 và E = 0")

fig, ax = plt.subplots(figsize=(6, 3.4))
ax.semilogx([r[0] for r in rows], [r[1] for r in rows], "o-")
ax.axhline(1/8, ls=":", c="gray"); ax.set_xlabel("thời gian ủ T"); ax.set_ylabel("P(optimal solution)")
plt.tight_layout(); plt.show()
"""),
md(r"""
Quan sát:

- Với $T$ rất nhỏ, xác suất chỉ cao hơn ngẫu nhiên (0,125) một chút. Với $T$ vừa phải đã khá tốt dù chưa "adiabatic" thực sự. Điều này khớp với ghi chú ở Mục 2.2: quantum annealer *không bắt buộc* phải ở ground state suốt quá trình.
- Xác suất đạt gần 1 khi $T$ cỡ hàng chục lần nghịch đảo của gap nhỏ nhất (ở đây gap nhỏ nhất khoảng 1,15). Đây là nội dung thực tế của adiabatic theorem: bài toán nào có gap nhỏ nhất đóng nhanh theo kích thước thì cần $T$ rất lớn.
- Giá trị tuyệt đối của $T$ chỉ có nghĩa trong đơn vị energy đang dùng: nếu nhân **cả** $H_0$ **và** $H_P$ với cùng một hằng số $\lambda$ thì kết quả giống hệt việc nhân $T$ với $\lambda$ (chỉ tích energy × thời gian mới quan trọng). Vì thế khi so sánh các máy hay các bài toán, phải so $T$ theo cùng thang energy.
"""),
]
save(nb1, "01-hamiltonian-and-annealing.ipynb")

# ------------------------------------------------------------------ B2
nb2 = [
md(r"""
# Notebook B2: Landscape energy và depth của QAOA

Đi kèm [B-06: QAOA, landscape và depth](../../docs/B-extensions/06-qaoa-landscape.md). Dùng simulator state vector chính xác `qaoa_state` trong `code/qco_utils.py` (không có noise sampling), cho bài toán Ví dụ 10.

Simulator này đã được đối chiếu với mạch Qiskit của Hình 9 (cùng tham số cho cùng distribution xác suất).
"""),
code(r"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
sys.path.insert(0, "../../code")
from qco_utils import cost_vector, qaoa_state, qaoa_expectation
""" + F10 + r"""
cost = cost_vector(f_poly, 3)
print("bảng f(x):", cost, "| tối ưu:", cost.min(), "tại chỉ số", int(cost.argmin()))
"""),
md(r"""
## 1. Landscape $E(\gamma, \beta)$ khi $p = 1$

Với $p=1$ ansatz chỉ có hai tham số. Ta tính $E(\gamma,\beta)$ trên grid và vẽ bản đồ nhiệt. Vì $f$ nhận giá trị nguyên nên $E$ periodic theo $\gamma$ với chu kỳ $2\pi$.
"""),
code(r"""
gs = np.linspace(0, 2*np.pi, 241)
bs = np.linspace(0, np.pi, 121)
E = np.array([[qaoa_expectation(cost, [g], [b]) for g in gs] for b in bs])
i, j = np.unravel_index(E.argmin(), E.shape)
print(f"cực tiểu trên grid: E = {E[i, j]:.3f} tại gamma = {gs[j]:.3f}, beta = {bs[i]:.3f}")

fig, ax = plt.subplots(figsize=(7, 3.6))
im = ax.imshow(E, origin="lower", aspect="auto", extent=[gs[0], gs[-1], bs[0], bs[-1]], cmap="viridis")
ax.plot(gs[j], bs[i], "r*", ms=12)
ax.set_xlabel("gamma"); ax.set_ylabel("beta"); ax.set_title("E(gamma, beta), p = 1")
fig.colorbar(im, ax=ax, label="E"); plt.tight_layout(); plt.show()
print("số điểm local minimum trên grid (tính cả các bản sao do tính periodic và đối xứng):",
      int(sum(E[a, b] < min(E[a-1, b], E[a+1, b], E[a, b-1], E[a, b+1])
              for a in range(1, E.shape[0]-1) for b in range(1, E.shape[1]-1))))
"""),
md(r"""
Landscape có nhiều "thung lũng" tách biệt, nên optimizer cổ điển (COBYLA, BFGS, ...) phụ thuộc điểm khởi đầu. Đây là khó khăn cốt lõi của các thuật toán variational, thường gọi là vấn đề *tối ưu tham số*.
"""),
md(r"""
## 2. Depth $p$ và chất lượng nghiệm

Với mỗi $p$, ta chạy BFGS từ nhiều điểm khởi đầu ngẫu nhiên rồi lấy kết quả tốt nhất. Cột `P(tối ưu)` là measurement probability được $|000\rangle$.
"""),
code(r"""
rng = np.random.default_rng(0)
def best_over_starts(p, starts=12):
    best_val, best_x = np.inf, None
    for _ in range(starts):
        x0 = np.concatenate([rng.uniform(0, 1.5, p), rng.uniform(0, np.pi/2, p)])
        r = minimize(lambda t: qaoa_expectation(cost, t[:p], t[p:]), x0, method="BFGS")
        if r.fun < best_val:
            best_val, best_x = r.fun, r.x
    return best_val, best_x

table = []
for p in range(1, 7):
    v, x = best_over_starts(p)
    prob = np.abs(qaoa_state(cost, x[:p], x[p:])) ** 2
    table.append((p, v, prob[0]))
print(" p   E tốt nhất   P(tối ưu)")
for p, v, pr in table:
    print(f" {p}    {v:8.3f}     {pr:6.3f}")
print("tham chiếu: E tối ưu = -9, chọn ngẫu nhiên: E = 0 và P = 0.125")
"""),
md(r"""
Chất lượng tăng nhanh theo $p$; ở bài 3 qubit này, $p = 5$–$6$ đã gần như chắc chắn cho optimal solution. Lưu ý đây là bài rất nhỏ và là mô phỏng không noise. Trên máy thật, mỗi lớp thêm vào làm mạch sâu hơn nên noise tăng, như đã thấy ở [Notebook C2](../C-hardware/02-ibm-quantum-qaoa.ipynb).
"""),
md(r"""
## 3. QAOA là phiên bản "rời rạc hóa" của quá trình ủ

Nếu lấy $\gamma_k = s_k\,\Delta t$ và $\beta_k = -(1-s_k)\,\Delta t$ với $s_k = (k + \tfrac12)/p$ và $\Delta t = T/p$, thì QAOA depth $p$ chính là xấp xỉ Trotter của quá trình ủ có thời gian $T$ ở [Notebook B1](01-hamiltonian-and-annealing.ipynb). Khi $p \to \infty$ với $T$ cố định, hai kết quả phải trùng nhau.
"""),
code(r"""
from scipy.linalg import eigh
X = np.array([[0.0, 1.0], [1.0, 0.0]]); I2 = np.eye(2)
def on(ops):
    out = np.array([[1.0]])
    for m in reversed(ops): out = np.kron(out, m)
    return out
H0 = -sum(on([X if j == q else I2 for j in range(3)]) for q in range(3)); HP = np.diag(cost)

def anneal_E(T, N=4000):
    dt = T / N; psi = np.ones(8, complex) / np.sqrt(8)
    for step in range(N):
        s = (step + 0.5) / N
        w, V = eigh((1 - s) * H0 + s * HP)
        psi = V @ (np.exp(-1j * w * dt) * (V.conj().T @ psi))
    return float(np.abs(psi) ** 2 @ cost)

for T in (4, 8):
    ref = anneal_E(T)
    print(f"T = {T}: ủ liên tục E = {ref:.3f}")
    for p in (4, 8, 16, 32, 64, 128):
        dt = T / p; sk = (np.arange(p) + 0.5) / p
        e = qaoa_expectation(cost, sk * dt, -(1 - sk) * dt)
        print(f"    QAOA p = {p:3d} với tham số 'ủ':  E = {e:7.3f}")
"""),
md(r"""
Với $p$ lớn, kết quả hội tụ về giá trị của quá trình ủ liên tục (các dao động nhỏ quanh giá trị đó là sai số Trotter). Còn khi **tối ưu tự do** các tham số (Mục 2), ở lần chạy này $p = 3$ đã đạt $E \approx -8{,}5$ và $p = 4$ đạt $E \approx -8{,}8$, tốt hơn quá trình ủ có $T = 8$ ($E \approx -8{,}4$) với depth mạch nhỏ hơn nhiều so với $p = 32$ cần để QAOA "bắt chước" quá trình ủ đó. Đây là lý do QAOA hấp dẫn, nhưng cái giá là phải tối ưu $2p$ tham số bằng vòng lặp cổ điển (xem [B-07](../../docs/B-extensions/07-benchmarking.md)). Cần nhớ đây chỉ là một bài 3 qubit.
"""),
]
save(nb2, "02-qaoa-landscape.ipynb")

# ------------------------------------------------------------------ B3
nb3 = [
md(r"""
# Notebook B3: Penalty constant $P$ trong bài toán knapsack

Đi kèm [B-04: Penalty function và cách mã hóa](../../docs/B-extensions/04-penalties-and-encodings.md).

Ta lấy bài toán knapsack 8 vật, rồi biến thành QUBO bằng chính quy trình ở Mục 4 của bài báo (biến nhị phân, ràng buộc bất đẳng thức → đẳng thức bằng biến slack, penalty function $P(\cdot)^2$). Sau đó khảo sát: (a) $P$ nhỏ nhất để QUBO còn đúng, (b) $P$ tác động ra sao đến việc tìm nghiệm bằng simulated annealing, (c) so với công thức (36) của bài báo.
"""),
code(r"""
import itertools, sys, warnings
warnings.filterwarnings("ignore")
import numpy as np
import dimod
sys.path.insert(0, "../../code")
from qco_utils import integer_encoding

rng = np.random.default_rng(3)
n = 8
values  = rng.integers(3, 16, n)
weights = rng.integers(2, 10, n)
W = 20
print("giá trị :", values)
print("trọng lượng:", weights, "| sức chứa W =", W)

def feasible(x):  return sum(int(w) * xi for w, xi in zip(weights, x)) <= W
def total_value(x): return sum(int(v) * xi for v, xi in zip(values, x))
opt = max(total_value(x) for x in itertools.product((0, 1), repeat=n) if feasible(x))
print("giá trị tối ưu (vét cạn):", opt)
"""),
md(r"""
## 1. Dựng QUBO

Cực tiểu hóa $-\sum_i v_i x_i + P\left(\sum_i w_i x_i + s - W\right)^2$, với slack $s \in [0, W]$ biểu diễn nhị phân bằng `integer_encoding` (Mục 4.1).
"""),
code(r"""
a, slack_w = integer_encoding(0, W)
print("trọng số của slack:", slack_w, "->", len(slack_w), "auxiliary variable (mã hóa nhị phân)")
xs = [f"x{i}" for i in range(n)]
ts = [f"s{j}" for j in range(len(slack_w))]

def build_qubo(P):
    bqm = dimod.BinaryQuadraticModel("BINARY")
    for i in range(n):
        bqm.add_variable(xs[i], -float(values[i]))
    terms = [(xs[i], float(weights[i])) for i in range(n)] + [(ts[j], float(slack_w[j])) for j in range(len(slack_w))]
    for u, c in terms:
        bqm.add_linear(u, P * (c*c - 2*W*c))
    for (u, c), (v, d) in itertools.combinations(terms, 2):
        bqm.add_quadratic(u, v, 2 * P * c * d)
    bqm.offset += P * W * W
    return bqm

def decode(sample):
    return [int(sample[v]) for v in xs]
"""),
md(r"""
## 2. $P$ nhỏ nhất để QUBO còn đúng

Với từng $P$, ta duyệt vét cạn cả 13 biến nhị phân ($2^{13} = 8192$ state) và kiểm tra: mọi state energy thấp nhất có feasible và có giá trị đúng bằng tối ưu hay không.
"""),
code(r"""
def exact_is_correct(P):
    ss = dimod.ExactSolver().sample(build_qubo(P))
    low = ss.lowest()
    return all(feasible(decode(s)) and total_value(decode(s)) == opt for s in low.samples())

grid = [0.25, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 8, 16, 71, 160]
for P in grid:
    print(f"P = {P:6}: QUBO đúng (mọi nghiệm cực tiểu đều feasible và tối ưu)? {exact_is_correct(P)}")
"""),
code(r"""
for P in np.arange(0.1, 6.0, 0.1):
    if exact_is_correct(P):
        print(f"P nhỏ nhất (grid 0.1) làm QUBO đúng: ~{P:.1f}")
        break
print("P theo công thức (36) áp dụng cho phần mục tiêu:", 1 + int(values.sum()))
"""),
md(r"""
Công thức (36) cho $P = 1 + \sum_i v_i$, lớn hơn rất nhiều so với mức tối thiểu thực tế. Giá trị này đúng (an toàn) nhưng không tối ưu. Câu hỏi tiếp theo là: $P$ lớn có hại không?
"""),
md(r"""
## 3. $P$ tác động thế nào đến việc tìm nghiệm bằng annealing?

Ta dùng một simulated annealing cổ điển tự viết (chạy song song nhiều lần bằng numpy) thay cho phần cứng. Lịch nhiệt độ **tự co giãn theo thang energy của QUBO**, giống cách các solver thật làm: nhiệt độ đầu đủ cao để lật được spin tốn energy lớn nhất, nhiệt độ cuối đủ thấp để phân biệt coefficient nhỏ nhất. Hệ quả: khi $P$ rất lớn, các coefficient lớn kéo nhiệt độ đầu lên cao, và phần lớn thời gian ủ bị lãng phí ở vùng quá nóng đối với phần mục tiêu thật.

Với mỗi $P$, ta đo (a) tỉ lệ lần chạy cho ra solution **feasible**, (b) tỉ lệ cho ra solution **feasible và tối ưu**, cả hai tính trên $x$ đã giải mã (bỏ biến slack).
"""),
code(r"""
coef = np.concatenate([weights, slack_w]).astype(float)
N = n + len(slack_w)

def qubo_arrays(P):
    h = np.zeros(N); h[:n] -= values
    h += P * (coef**2 - 2 * W * coef)
    J = 2 * P * np.outer(coef, coef); np.fill_diagonal(J, 0)      # E = sum_i h_i x_i + sum_{i<j} J_ij x_i x_j (J đối xứng)
    return h, J

def sa_run(P, sweeps, reads=2000, seed=0):
    r = np.random.default_rng(seed)
    h, J = qubo_arrays(P)
    max_dE = (np.abs(h) + np.abs(J).sum(1)).max()
    upper = np.abs(J[np.triu_indices(N, 1)])
    nonzero = np.concatenate([np.abs(h[h != 0]), upper[upper != 0]])
    betas = np.geomspace(np.log(2) / max_dE, np.log(100) / nonzero.min(), sweeps)
    X = r.integers(0, 2, size=(reads, N))
    for beta in betas:
        for i in range(N):
            dE = (1 - 2 * X[:, i]) * (h[i] + X @ J[:, i])
            accept = (dE < 0) | (r.random(reads) < np.exp(-beta * np.clip(dE, 0, None)))
            X[accept, i] ^= 1
    return X

def report(P, sweeps):
    X = sa_run(P, sweeps)
    sel = X[:, :n]
    feas_mask = (sel @ weights) <= W
    good_mask = feas_mask & ((sel @ values) == opt)
    h, J = qubo_arrays(P)
    scale = max(np.abs(h).max(), np.abs(J).max()) / values.min()
    return feas_mask.mean(), good_mask.mean(), scale

for sweeps in (100, 400):
    print(f"sweeps = {sweeps}")
    print("      P    feasible   feasible và tối ưu   thang energy (max|coefficient| / giá trị nhỏ nhất)")
    for P in (0.5, 1, 1.5, 2, 4, 8, 16, 40, 71, 160, 1000):
        f_, g_, sc = report(P, sweeps)
        print(f"  {P:6}     {f_:5.2f}          {g_:5.2f}                 {sc:9.1f}")
"""),
md(r"""
Đọc kết quả (hai mức sweep cho cùng xu hướng):

- **Tỉ lệ feasible tăng theo $P$**: ở $P = 0{,}5$ chưa đến một nửa lần chạy feasible, còn từ $P \approx 8$ trở lên gần như luôn feasible. Ràng buộc càng bị phạt nặng thì càng được tuân thủ.
- **Tỉ lệ "feasible và tối ưu" giảm đơn điệu theo $P$**: từ khoảng 0,25–0,45 ở $P \lesssim 1$ (tùy số sweep) xuống gần 0 từ $P \approx 16$. Lý do: khi $P$ lớn, bộ ủ vừa tốn nhiệt độ vào phần quá nóng, vừa bị giam trong một vùng feasible mà các nghiệm feasible khác nhau cách nhau bởi rào cản energy rất cao, nên khó chuyển từ nghiệm feasible kém sang nghiệm feasible tốt hơn.
- Điểm tốt nhất nằm **gần ngưỡng $P^* \approx 1{,}1$** tìm được ở Mục 2 (thậm chí hơi dưới ngưỡng, vì một số shots không cần QUBO đúng để cho solution feasible tốt). Giá trị $P = 71$ của công thức (36) cho gần như 0% thành công trong thí nghiệm này, dù QUBO tương ứng hoàn toàn đúng về mặt toán học.

Cần lưu ý: đây là một thể hiện knapsack nhỏ và một sampler cổ điển, nên số cụ thể sẽ khác trên phần cứng và bài toán khác. Điều đáng mang đi là **bản chất đánh đổi** (feasible so với chất lượng) và việc công thức (36) là cận an toàn về tính đúng đắn của QUBO, không phải lựa chọn tốt về hiệu năng.
"""),
md(r"""
## 4. Số biến theo cách mã hóa slack

Cùng ràng buộc $\sum w_i x_i \le W$, slack nhị phân dùng ít qubit nhất; cách mã hóa unary (mỗi đơn vị một biến) dùng nhiều hơn nhiều.
"""),
code(r"""
for W_ in (10, 20, 50, 100, 500, 1000):
    a_, w_ = integer_encoding(0, W_)
    print(f"W = {W_:5d}: slack nhị phân cần {len(w_):2d} biến | slack unary cần {W_:5d} biến")
"""),
]
save(nb3, "03-penalty-and-encodings.ipynb")

# ------------------------------------------------------------------ B4
nb4 = [
md(r"""
# Notebook B4: Minor-embedding và độ dài chain

Đi kèm [B-05: Minor-embedding và chain](../../docs/B-extensions/05-embedding-and-chains.md). Notebook dùng `minorminer` để nhúng các đồ thị lên topology cỡ thật của máy D-Wave (Chimera 2048 qubit, Pegasus 5640 qubit, Zephyr 4800 qubit). **Không cần tài khoản D-Wave**, mọi thứ chạy cục bộ.
"""),
code(r"""
import time, warnings
warnings.filterwarnings("ignore")
import networkx as nx
import minorminer
import dwave_networkx as dnx

topologies = {
    "Chimera C16": dnx.chimera_graph(16),
    "Pegasus P16": dnx.pegasus_graph(16),
    "Zephyr Z12":  dnx.zephyr_graph(12),
}
for name, G in topologies.items():
    degs = [d for _, d in G.degree()]
    print(f"{name}: {G.number_of_nodes()} qubit, {G.number_of_edges()} coupler, bậc tối đa {max(degs)}")
"""),
md(r"""
## 1. Đồ thị đầy đủ $K_n$ (QUBO dày)

Một QUBO mà mọi cặp biến đều có tương tác bậc hai (ví dụ bài toán có ràng buộc one-hot dày) có đồ thị $K_n$. Ta nhúng $K_n$ và đếm tổng số qubit vật lý cùng độ dài chain lớn nhất.
"""),
code(r"""
def embed_stats(graph_edges, target, timeout=30, seed=1):
    t = time.time()
    emb = minorminer.find_embedding(graph_edges, target.edges, timeout=timeout, random_seed=seed)
    if not emb:
        return None
    lens = [len(c) for c in emb.values()]
    return sum(lens), max(lens), time.time() - t

print("Nhúng K_n; mỗi ô: (tổng qubit vật lý, chain dài nhất)")
sizes = (8, 16, 24, 32)
print(f"{'':12s}" + "".join(f"K{n:<14d}" for n in sizes))
for name, G in topologies.items():
    cells = []
    for n in sizes:
        r = embed_stats(nx.complete_graph(n).edges, G)
        cells.append("không tìm được" if r is None else f"({r[0]}, {r[1]})")
    print(f"{name:12s}" + "".join(f"{c:<15s}" for c in cells))
"""),
md(r"""
Số qubit vật lý tăng nhanh hơn tuyến tính theo $n$, và chain dài hơn nhiều trên Chimera so với Pegasus/Zephyr vì mỗi qubit chỉ nối được tối đa 6 qubit khác (bậc 6, so với 15 và 20). Đây là lý do độ kết nối của topology quan trọng, và là lý do các bài toán dày bị giới hạn ở kích thước nhỏ hơn rất nhiều so với tổng số qubit.
"""),
md(r"""
## 2. Đồ thị sparse: 3-regular ngẫu nhiên

Nhiều bài toán tối ưu tổ hợp thực tế (ví dụ Max-Cut trên đồ thị sparse) có đồ thị bậc nhỏ, và nhúng dễ hơn nhiều.
"""),
code(r"""
print("Nhúng đồ thị 3-regular ngẫu nhiên; mỗi ô: (tổng qubit vật lý, chain dài nhất)")
sizes = (32, 64, 128, 256)
print(f"{'':12s}" + "".join(f"n={n:<13d}" for n in sizes))
for name, G in topologies.items():
    cells = []
    for n in sizes:
        H = nx.random_regular_graph(3, n, seed=1)
        r = embed_stats(H.edges, G)
        cells.append("không tìm được" if r is None else f"({r[0]}, {r[1]})")
    print(f"{name:12s}" + "".join(f"{c:<15s}" for c in cells))
"""),
md(r"""
Đồ thị sparse với hàng trăm biến vẫn nhúng được: trên Pegasus và Zephyr chain dài tối đa 5 ở $n = 256$ (Chimera cần chain tới 15), trong khi $K_{32}$ đã cần 339 qubit trên Chimera. Kết luận thực tế: **cấu trúc đồ thị của QUBO quyết định bài toán có vừa với máy hay không**, quan trọng hơn cả số biến.

Lưu ý: `find_embedding` là heuristic ngẫu nhiên, nên số liệu có thể thay đổi chút ít theo hạt giống; đây là các cận trên của một lần thử, không phải nhúng tối ưu (bài toán minor-embedding là NP-hard như bài báo nêu).
"""),
md(r"""
## 3. Đồ thị của bài toán TSP (Ví dụ 8)

Với $n$ thành phố, ta có $n^2$ biến nhị phân $x_{a,j}$ (thành phố $a$ ở vị trí $j$). Hai ràng buộc hoán vị (23), (24) tạo các tương tác bậc hai giữa mọi cặp biến cùng hàng (cùng thành phố) và cùng cột (cùng vị trí). Phần chi phí quãng đường $\sum d_{a,b}\,x_{a,j}\,x_{b,j+1}$ nối thêm mọi cặp ở hai vị trí kề nhau. Kết quả là mỗi biến có bậc khoảng $4(n-1)$.
"""),
code(r"""
def tsp_graph(n):
    G = nx.Graph()
    G.add_nodes_from((a, j) for a in range(n) for j in range(n))
    for j in range(n):
        for a in range(n):
            for b in range(a + 1, n):
                G.add_edge((a, j), (b, j))                  # mỗi vị trí đúng một thành phố
    for a in range(n):
        for j in range(n):
            for k in range(j + 1, n):
                G.add_edge((a, j), (a, k))                  # mỗi thành phố đúng một vị trí
    for j in range(n):
        for a in range(n):
            for b in range(n):
                if a != b:
                    G.add_edge((a, j), (b, (j + 1) % n))    # chi phí quãng đường giữa hai vị trí kề nhau
    return G

print("n   biến logic  bậc tối đa  | " + " | ".join(f"{name:22s}" for name in topologies))
for n_cities in (4, 6, 8, 10, 12):
    H = tsp_graph(n_cities)
    max_deg = max(d for _, d in H.degree())
    cells = []
    for name, G in topologies.items():
        r = embed_stats(H.edges, G, timeout=30)
        cells.append("không tìm được" if r is None else f"{r[0]:5d} qubit, chain<={r[1]:2d}")
    print(f"{n_cities:2d}  {H.number_of_nodes():8d}  {max_deg:9d}   | " + " | ".join(f"{c:22s}" for c in cells))
"""),
md(r"""
Mỗi biến logic của TSP có bậc cỡ $4(n-1)$, vượt xa bậc tối đa của các qubit (6, 15, 20). Vì vậy bài toán đã cần chain dài và tổng số qubit vật lý lớn hơn rất nhiều số biến logic $n^2$, ngay từ các thể hiện rất nhỏ. Ở đây $n = 12$ thành phố (144 biến logic) đã chiếm khoảng 2000 qubit trên Pegasus P16, và heuristic không tìm được nhúng nào cho $n \ge 10$ trên Chimera C16 trong thời hạn đặt ra (kết quả "không tìm được" nghĩa là heuristic thất bại trong thời hạn, chưa phải chứng minh không tồn tại nhúng). Tốc độ tăng này gợi ý rằng TSP cỡ vài chục thành phố sẽ vượt quá khả năng của một chip đơn lẻ nếu mã hóa trực tiếp theo cách này; đó là ngoại suy thô từ các điểm $n \le 12$, không phải measurement.
"""),
]
save(nb4, "04-embedding-scaling.ipynb")

# ------------------------------------------------------------------ B5
nb5 = [
md(r"""
# Notebook B5: So sánh công bằng, và chi phí ẩn của QAOA

Đi kèm [B-07: Benchmark công bằng và tài liệu đọc thêm](../../docs/B-extensions/07-benchmarking.md).

Đây là một **thí nghiệm đồ chơi** để minh họa *cách đếm chi phí*, không phải bằng chứng về lợi thế của bên nào. Ta lấy các thể hiện Ising ngẫu nhiên $n = 10$ spin, và so sánh simulated annealing (SA) với QAOA mô phỏng chính xác về: xác suất tìm được optimal solution của một lần chạy, thời gian-tới-lời-giải TTS, và chi phí vòng tối ưu tham số của QAOA.
"""),
code(r"""
import sys, time
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, "../../code")
from qco_utils import qaoa_state, qaoa_expectation

n = 10
rng = np.random.default_rng(42)

def random_instance():
    J = np.triu(rng.normal(size=(n, n)), 1)
    J = J + J.T                                   # đối xứng, đường chéo 0
    return J

def energies_table(J):
    # E(s) = sum_{i<j} J_ij s_i s_j với s_j = 1 - 2 x_j, bit j của chỉ số (little-endian)
    idx = np.arange(2**n)
    S = 1 - 2 * ((idx[:, None] >> np.arange(n)) & 1)       # (2^n, n)
    return 0.5 * np.einsum("ki,ij,kj->k", S, J, S)

J = random_instance()
E = energies_table(J)
print("thể hiện mẫu: E nhỏ nhất =", round(E.min(), 3), "| số optimal solution (suy biến spin-flip):", int((np.abs(E - E.min()) < 1e-9).sum()))
"""),
md(r"""
## 1. Simulated annealing: xác suất thành công theo số sweep

SA đơn giản (Metropolis, từng spin, lịch beta tuyến tính), chạy song song nhiều lần bằng numpy. Một "lần chạy" gồm `sweeps` lượt quét, mỗi lượt cập nhật $n$ spin.
"""),
code(r"""
def sa_success(J, E_min, sweeps, reads=2000, beta0=0.1, beta1=3.0, seed=0):
    r = np.random.default_rng(seed)
    S = r.choice([-1, 1], size=(reads, n))
    for sw in range(sweeps):
        beta = beta0 + (beta1 - beta0) * sw / max(1, sweeps - 1)
        for i in range(n):
            field = S @ J[:, i]                           # tổng_j J_ij s_j (J_ii = 0)
            dE = -2 * S[:, i] * field
            accept = (dE < 0) | (r.random(reads) < np.exp(-beta * np.clip(dE, 0, None)))
            S[accept, i] *= -1
    En = 0.5 * np.einsum("ki,ij,kj->k", S, J, S)
    return float((En < E_min + 1e-9).mean())

E_min = E.min()
for sweeps in (5, 10, 20, 50, 100):
    print(f"sweeps = {sweeps:3d}: P(một lần chạy ra optimal solution) = {sa_success(J, E_min, sweeps):.3f}")
"""),
md(r"""
## 2. QAOA mô phỏng chính xác: xác suất thành công theo depth $p$

Ta tối ưu $2p$ tham số bằng BFGS từ vài điểm khởi đầu ngẫu nhiên, và đếm **số lần gọi hàm mục tiêu** (`nfev`) mà optimizer cần. Trên phần cứng thật, mỗi lần gọi hàm mục tiêu là một đợt đo nhiều shots.
"""),
code(r"""
def qaoa_best(E, p, starts=6, seed=0):
    r = np.random.default_rng(seed)
    best = (np.inf, None); total_nfev = 0
    scale = np.abs(E).max()
    for _ in range(starts):
        x0 = np.concatenate([r.uniform(0, 1.0 / scale * 3, p), r.uniform(0, np.pi / 2, p)])
        res = minimize(lambda t: qaoa_expectation(E, t[:p], t[p:]), x0, method="BFGS")
        total_nfev += res.nfev
        if res.fun < best[0]:
            best = (res.fun, res.x)
    x = best[1]
    prob = np.abs(qaoa_state(E, x[:p], x[p:])) ** 2
    return float(prob[np.abs(E - E.min()) < 1e-9].sum()), total_nfev

t0 = time.time()
for p in (1, 2, 3):
    ps, nfev = qaoa_best(E, p)
    print(f"p = {p}: P(thành công) = {ps:.3f} | số lần gọi hàm mục tiêu của optimizer (6 điểm khởi đầu) = {nfev}")
print(f"({time.time() - t0:.0f} giây)")
"""),
md(r"""
## 3. Thời gian-tới-lời-giải (TTS) và chi phí ẩn

Nếu một lần chạy thành công với xác suất $p_s$, số shots cần để có xác suất thành công $\ge 99\%$ là
$$R_{99} = \left\lceil \frac{\ln(1 - 0.99)}{\ln(1 - p_s)} \right\rceil .$$

Với SA, chi phí là $R_{99} \times \text{sweeps} \times n$ lần cập nhật spin. Với QAOA, có hai phần: (a) $R_{99}$ shots để sampling với tham số đã tối ưu, và (b) **chi phí tối ưu tham số** = số lần gọi hàm mục tiêu × số shots mỗi lần gọi. Phần (b) thường chiếm đa số nhưng hay bị bỏ qua khi báo cáo.
"""),
code(r"""
import math
def r99(ps):
    return 1 if ps >= 0.99 else math.ceil(math.log(0.01) / math.log(1 - ps))

SHOTS_PER_EVAL = 1000        # giả định số shots mỗi lần đánh giá hàm mục tiêu trên phần cứng

# 12 thể hiện ngẫu nhiên
instances = [random_instance() for _ in range(12)]
Es = [energies_table(Ji) for Ji in instances]

print("SA (sweeps cố định = 50):")
sa_ps = [sa_success(Ji, Ei.min(), 50, reads=1000, seed=k) for k, (Ji, Ei) in enumerate(zip(instances, Es))]
print(f"  P thành công: trung vị {np.median(sa_ps):.3f}, thấp nhất {min(sa_ps):.3f}, cao nhất {max(sa_ps):.3f}")
print(f"  R99 (trung vị) = {r99(np.median(sa_ps))} lần chạy; chi phí = {r99(np.median(sa_ps)) * 50 * n} lần cập nhật spin")

for p in (1, 2, 3):
    res = [qaoa_best(Ei, p, starts=4, seed=k) for k, Ei in enumerate(Es)]
    ps_list = [r[0] for r in res]; nfev_list = [r[1] for r in res]
    ps_med = float(np.median(ps_list)); nfev_med = float(np.median(nfev_list))
    shots_final = r99(ps_med)
    shots_opt = nfev_med * SHOTS_PER_EVAL
    print(f"QAOA p = {p}: P thành công trung vị {ps_med:.3f} (thấp nhất {min(ps_list):.3f}, cao nhất {max(ps_list):.3f})")
    print(f"           shots sampling cuối R99 = {shots_final:6d} | shots cho vòng tối ưu ~ {int(shots_opt):9d} ({nfev_med:.0f} lần gọi x {SHOTS_PER_EVAL})")
"""),
md(r"""
## 4. Đọc kết quả thế nào cho đúng

- Chi phí **vòng tối ưu tham số** của QAOA (hàng trăm nghìn shots ở trên) lớn hơn rất nhiều so với $R_{99}$ shots sampling cuối. Nếu chỉ tính $R_{99}$ thì sẽ đánh giá thấp chi phí thực. Ngược lại, SA không có vòng ngoài này.
- Đơn vị chi phí không so sánh trực tiếp được: "lần cập nhật spin" trên CPU và "shot" trên QPU có thời gian thực khác nhau nhiều bậc. Muốn so sánh nghiêm túc phải dùng **thời gian thực end-to-end** trên phần cứng cụ thể, gồm cả biên dịch, hàng đợi, chuyển dữ liệu.
- Đây là bài $n = 10$ rất nhỏ nên SA chỉ cần vài sweep đã có xác suất thành công đáng kể; không thể suy ra gì về bài lớn. Chỉ có phần *cách đếm* là đáng mang đi.
- Số lần gọi hàm mục tiêu (`nfev`) phụ thuộc optimizer: BFGS ước lượng gradient bằng sai phân hữu hạn nên tốn $2p+1$ lần gọi cho mỗi bước. Optimizer không dùng gradient (như COBYLA) hay kỹ thuật khởi tạo tham số thông minh sẽ cho số khác, nhưng thường vẫn ở cỡ hàng trăm đến hàng nghìn lần gọi. Cả SA lẫn QAOA ở đây đều chưa được tinh chỉnh.
- Các nguyên tắc benchmark đầy đủ nằm ở [B-07](../../docs/B-extensions/07-benchmarking.md).
"""),
]
save(nb5, "05-benchmarking-toy.ipynb")
