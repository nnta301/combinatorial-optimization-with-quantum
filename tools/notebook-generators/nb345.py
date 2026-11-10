import nbformat as nbf

def md(s): return nbf.v4.new_markdown_cell(s.strip("\n"))
def code(s): return nbf.v4.new_code_cell(s.strip("\n"))

def save(cells, path):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nbf.write(nb, path)

# ------------------------------------------------------------------ NB3
nb3 = [
md(r"""
# Notebook 3: Ràng buộc, biến slack và hằng số phạt

Đi kèm [Phần A, Mục 4.3](../../docs/A-translation/04-problem-transformation.md): Ví dụ 13 và 14, các phương trình (32)–(38). Notebook kiểm tra bằng duyệt vét cạn rằng hàm đã phạt có cùng nghiệm tối ưu với bài toán có ràng buộc, đồng thời khảo sát hai nhận xét của người dịch: cận dưới của $h$ khá lỏng, và $P = 127$ lớn hơn mức cần thiết.
"""),
code(r"""
import itertools, sys
import sympy as sp
sys.path.insert(0, "../../code")
from qco_utils import (multilinear, evaluate, brute_force, lower_bound, upper_bound,
                       penalty_constant, integer_encoding)
"""),
md(r"""
## 1. Ví dụ 13: biến slack cho ràng buộc $3x_1x_4x_6 - 4x_3x_5 \le 0$
"""),
code(r"""
x1, x3, x4, x5, x6 = xs = sp.symbols("x1 x3 x4 x5 x6")
g = multilinear(3*x1*x4*x6 - 4*x3*x5, xs)
gmin, _ = brute_force(g, 5)
print("min g =", gmin, "=> s thuộc [0, %d]" % (-gmin))
a, w = integer_encoding(0, -gmin)
print("trọng số của slack:", w, "(bài báo: s = t1 + 2 t2 + t3)")
"""),
md(r"""
## 2. Ví dụ 14: ràng buộc $(z-1)^2 \le 6$ cho hàm của Ví dụ 10

Các biến: $z = -3 + x_1 + 2x_2 + 3x_3$, $f(z) = z^3 - 6z$, $h(z) = (z-1)^2 - 6$.
"""),
code(r"""
x1, x2, x3 = X = sp.symbols("x1 x2 x3")
z = -3 + x1 + 2*x2 + 3*x3
f_poly = multilinear(z**3 - 6*z, X)
h_poly = multilinear((z - 1)**2 - 6, X)

paper37 = {frozenset(): 10, frozenset({0}): -7, frozenset({1}): -12, frozenset({2}): -15,
           frozenset({0, 1}): 4, frozenset({0, 2}): 6, frozenset({1, 2}): 12}
print("h khớp phương trình (37):", h_poly == paper37)

print("lb(h) theo (34) =", lower_bound(h_poly), "| min h thực (vét cạn) =", brute_force(h_poly, 3)[0])
print("P theo (36) =", penalty_constant(f_poly), "(bài báo: 127)")
print("ub(f) =", upper_bound(f_poly), " lb(f) =", lower_bound(f_poly),
      "| khoảng dao động thực của f:", (brute_force(f_poly, 3)[0], max(evaluate(f_poly, x) for x in itertools.product((0, 1), repeat=3))))
"""),
md(r"""
Cận dưới của $h$ là $-24$ nhưng giá trị nhỏ nhất thực là $-6$. Cận này an toàn nhưng lỏng: nó cần slack trong $[0, 24]$, tức 5 biến phụ, trong khi $[0, 6]$ chỉ cần 3.
"""),
code(r"""
for hi in (24, 6):
    a, w = integer_encoding(0, hi)
    print(f"slack trong [0, {hi:2d}]: {len(w)} biến phụ, trọng số {w}")
"""),
md(r"""
## 3. Hàm đã phạt $f'(x, t) = f(x) + P\,(h(x) + s)^2$

Ta dựng $f'$ với slack 5 biến (như bài báo) và kiểm tra: cực tiểu của $f'$ trên cả 8 biến nhị phân phải bằng cực tiểu của $f$ trên các $z$ thỏa $(z-1)^2 \le 6$.
"""),
code(r"""
def build(slack_hi, P):
    a, w = integer_encoding(0, slack_hi)
    ts = sp.symbols(f"t1:{len(w)+1}")
    s = sum(wi * ti for wi, ti in zip(w, ts))
    allvars = list(X) + list(ts)
    F = multilinear(z**3 - 6*z + P*((z - 1)**2 - 6 + s)**2, allvars)
    return F, len(allvars), w

# đáp án đúng: duyệt các z thỏa ràng buộc
feasible = {zz: zz**3 - 6*zz for zz in range(-3, 4) if (zz - 1)**2 <= 6}
print("z khả thi:", feasible)
fstar = min(feasible.values())
print("giá trị tối ưu mong đợi:", fstar)

F, n, w = build(24, 127)
best, arg = brute_force(F, n)
print("min f' =", best, "| nghiệm tối ưu (x1,x2,x3,t...):", arg)
zs = {-3 + x[0] + 2*x[1] + 3*x[2] for x in arg}
print("các z tương ứng:", zs)
assert best == fstar and all((zz - 1)**2 <= 6 for zz in zs)
"""),
md(r"""
## 4. $P = 127$ có cần thiết không?

Với $f$ và $h$ trên, ta tìm $P$ nhỏ nhất sao cho mọi nghiệm tối ưu của $f'$ đều khả thi và đạt giá trị tối ưu của bài toán gốc. Phép thử được thực hiện cho slack 5 biến (cận lỏng) và slack 3 biến (cận chặt).
"""),
code(r"""
def smallest_working_P(slack_hi):
    a, w = integer_encoding(0, slack_hi)
    ts = sp.symbols(f"t1:{len(w)+1}")
    s = sum(wi * ti for wi, ti in zip(w, ts))
    allvars = list(X) + list(ts)
    fpoly = multilinear(z**3 - 6*z, allvars)
    gpoly = multilinear(((z - 1)**2 - 6 + s)**2, allvars)
    combos = list(itertools.product((0, 1), repeat=len(allvars)))
    fv = [evaluate(fpoly, c) for c in combos]
    gv = [evaluate(gpoly, c) for c in combos]
    fstar = min(f for f, g in zip(fv, gv) if g == 0)
    for P in range(1, 200):
        vals = [f + P * g for f, g in zip(fv, gv)]
        m = min(vals)
        if all(g == 0 and f == fstar for f, g, v in zip(fv, gv, vals) if v == m):
            return P, len(w)

for hi in (24, 6):
    P, nb_ = smallest_working_P(hi)
    print(f"slack trong [0, {hi:2d}] ({nb_} biến phụ): P nhỏ nhất dùng được = {P}")
"""),
md(r"""
Công thức (36) cho $P = 127$ vì nó chỉ dựa vào tổng các hệ số tuyệt đối, không dùng thông tin gì khác về bài toán. Giá trị này an toàn nhưng lớn hơn rất nhiều so với mức tối thiểu của thể hiện cụ thể này.

Cần lưu ý đừng suy ra rằng $P = 1$ luôn đủ. Ở thể hiện này mọi lời giải vi phạm ràng buộc đều vi phạm khá nhiều (với $z = -3$ thì $h = 10$, với $z = -2$ thì $h = 3$), và vì phạt dùng bình phương nên $(h+s)^2 \ge 9$ đã vượt xa khoảng dao động của $f$. Với một ràng buộc mà mức vi phạm nhỏ nhất chỉ là 1, ta sẽ cần $P$ lớn hơn. Công thức (36) là cận an toàn cho mọi trường hợp, còn một cận chặt hơn thì phải khai thác cấu trúc của bài toán.

Điều này quan trọng trong thực tế: hằng số phạt lớn làm hàm mục tiêu có dải giá trị rộng, và trên phần cứng lượng tử (độ phân giải hữu hạn của các hệ số) có thể làm "chìm" phần mục tiêu thật. Đây là một lý do để chọn $P$ cẩn thận, và là chủ đề của Phần B.
"""),
]
save(nb3, "03-constraints-and-penalty.ipynb")

# ------------------------------------------------------------------ NB4
nb4 = [
md(r"""
# Notebook 4: Quantum annealer với MAX-SAT (Hình 4, Bảng 2, Ví dụ 15–16)

Đi kèm [Phần A, Mục 5](../../docs/A-translation/05-quantum-annealer.md). Notebook này **không cần tài khoản D-Wave**: ta dùng `ExactSolver` (liệt kê mọi trạng thái) và `SimulatedAnnealingSampler` của `dimod` thay cho máy thật.

Mục tiêu chính là làm rõ lỗi trong Hình 4 của bài gốc: hàm phạt trong code thiếu số hạng $-2x_3 z$ so với phương trình (39).
"""),
code(r"""
import itertools, sys
from collections import Counter
from dimod import Binary, ExactSolver, SimulatedAnnealingSampler
sys.path.insert(0, "../../code")
from qco_utils import penalty_constant

x1, x2, x3, z = (Binary(v) for v in ("x1", "x2", "x3", "z"))
P = 7
# Phần mục tiêu sau khi giảm bậc bằng z = x2*x3 (Ví dụ 15)
base = x1*z - 2*z - x1*x3 + x2 + x3
penalty_paper = x2*x3 - 2*x2*z + 3*z                 # Hình 4 trong bài gốc (thiếu -2*x3*z)
penalty_fixed = x2*x3 - 2*x2*z - 2*x3*z + 3*z        # phương trình (39)
model_paper = base + P * penalty_paper
model_fixed = base + P * penalty_fixed
"""),
md(r"""
## 1. Hằng số phạt

Phần mục tiêu sau khi giảm bậc có các hệ số $1, -2, -1, 1, 1$ (cho $x_1 z$, $z$, $x_1 x_3$, $x_2$, $x_3$), nên theo (36) $P = 1 + 6 = 7$, đúng với giá trị bài báo dùng.
"""),
code(r"""
reduced = {frozenset({0, 3}): 1, frozenset({3}): -2, frozenset({0, 2}): -1, frozenset({1}): 1, frozenset({2}): 1}
print("P theo (36) =", penalty_constant(reduced))
"""),
md(r"""
## 2. Các trạng thái năng lượng thấp nhất (ExactSolver)

`ExactSolver` liệt kê cả 16 tổ hợp của $(x_1, x_2, x_3, z)$.
"""),
code(r"""
def ground_states(model):
    res = ExactSolver().sample(model)
    lowest = res.lowest()
    out = sorted(tuple(int(s[v]) for v in ("x1", "x2", "x3", "z")) for s in lowest.samples())
    return float(lowest.first.energy), out

# Các phép gán thỏa mọi clause của MAX-SAT (Ví dụ 2), tính trực tiếp từ các clause
def count_unsat(a, b, c):
    clauses = [(a or (not b) or c), (a or b or (not c)), ((not a) or (not b) or c)]
    return sum(1 for cl in clauses if not cl)
sat = [t for t in itertools.product((0, 1), repeat=3) if count_unsat(*t) == 0]
print("Phép gán thỏa mọi clause (3 biến):", sat, f"-> {len(sat)} phép gán")

for name, model in (("Phương trình (39), đã sửa", model_fixed), ("Hình 4 gốc, thiếu -2*x3*z", model_paper)):
    e, gs = ground_states(model)
    print(f"\n{name}: năng lượng cực tiểu = {e}, số trạng thái cực tiểu = {len(gs)}")
    for g in gs:
        print("   (x1,x2,x3,z) =", g, "| (x1,x2,x3) =", g[:3], "| z == x2*x3 ?", g[3] == g[1]*g[2])
"""),
md(r"""
- **Phương trình (39) / mã đã sửa:** đúng 5 trạng thái cực tiểu, ứng với đúng 5 phép gán thỏa mọi clause; hai trong số đó (`011` và `111`) có $z = 1$.
- **Mã trong Hình 4 gốc:** chỉ còn 3 trạng thái cực tiểu (`000`, `100`, `101`). Phép gán `011` và `111` bị loại vì với $x_2 = x_3 = z = 1$ hàm phạt bị tính sai thành $2P$ thay vì 0.

Vì vậy Bảng 2 của bài báo (chỉ có ba phép gán Energy 0) phản ánh QUBO bị thiếu số hạng, không phải toàn bộ lời giải của MAX-SAT.
"""),
md(r"""
## 3. Lấy mẫu bằng simulated annealing (thay cho máy thật)

Đây là tương tự Bảng 2: mỗi hàng là một tổ hợp quan sát được qua 1000 lần chạy. Cột `unsat` là số clause không được thỏa tại $(x_1, x_2, x_3)$.
"""),
code(r"""
def sample_table(model, reads=1000):
    res = SimulatedAnnealingSampler().sample(model, num_reads=reads).aggregate()
    rows = []
    for rec in res.data(["sample", "energy", "num_occurrences"]):
        s = rec.sample
        rows.append((int(s["x1"]), int(s["x2"]), int(s["x3"]), int(s["z"]), float(rec.energy),
                     count_unsat(int(s["x1"]), int(s["x2"]), int(s["x3"])), int(rec.num_occurrences)))
    return sorted(rows, key=lambda r: (r[4], -r[6]))

for name, model in (("Mã đã sửa (39)", model_fixed), ("Hình 4 gốc", model_paper)):
    print(name)
    print("  x1 x2 x3 z  energy  unsat  occurrences")
    for r in sample_table(model)[:8]:
        print(f"   {r[0]}  {r[1]}  {r[2]}  {r[3]}  {r[4]:6.1f}  {r[5]:5d}  {r[6]:11d}")
    print()
"""),
md(r"""
Với mã đã sửa, các trạng thái Energy $= 0$ gồm cả `011` và `111` (với $z = 1$). Với mã gốc chúng không bao giờ xuất hiện ở mức năng lượng thấp nhất, khớp với Bảng 2 của bài báo. (Số lần xuất hiện cụ thể phụ thuộc vào sampler và hạt giống ngẫu nhiên, nên không trùng với số liệu trên phần cứng D-Wave.)
"""),
md(r"""
## 4. Biến đổi cục bộ (Ví dụ 16)

Ta cực tiểu hóa $-f(x)$ với $f$ ở Ví dụ 10. Số hạng bậc ba $-36x_1x_2x_3$ được thay bằng $-36(x_1 + x_2 + x_3 - 2)t$. Kiểm tra: lấy cực tiểu theo $t$ phải cho lại đúng $-f(x)$ tại mọi $x$.
"""),
code(r"""
def f(x1, x2, x3):
    zz = -3 + x1 + 2*x2 + 3*x3
    return zz**3 - 6*zz

def f_local(x1, x2, x3, t):                   # phương trình (40), đã sửa x2 + x2 -> x1 + x2
    return 9 - 13*x1 - 14*x2 - 9*x3 + 18*x1*x2 + 18*x1*x3 + 18*x2*x3 - 36*(x1 + x2 + x3 - 2)*t

ok = all(min(f_local(*x, t) for t in (0, 1)) == -f(*x) for x in itertools.product((0, 1), repeat=3))
print("min_t f'(x,t) == -f(x) với mọi x:", ok)

# và nếu dùng nhầm bản in sai (x2 + x2 + x3 - 2) thì không còn đúng:
def f_typo(x1, x2, x3, t):
    return 9 - 13*x1 - 14*x2 - 9*x3 + 18*x1*x2 + 18*x1*x3 + 18*x2*x3 - 36*(x2 + x2 + x3 - 2)*t
print("với bản in sai của bài gốc:", all(min(f_typo(*x, t) for t in (0, 1)) == -f(*x) for x in itertools.product((0, 1), repeat=3)))
"""),
md(r"""
## 5. Chạy trên máy D-Wave thật (tùy chọn)

Hướng dẫn tạo tài khoản D-Wave Leap, lấy API token và chạy `EmbeddingComposite(DWaveSampler())` trên phần cứng thật sẽ có ở Phần C (`docs/C-hardware/dwave-leap.md`, đang soạn). Khi chạy bằng mã đã sửa, ta kỳ vọng thấy cả 5 phép gán thỏa mọi clause trong kết quả.
"""),
]
save(nb4, "04-quantum-annealer-maxsat.ipynb")

# ------------------------------------------------------------------ NB5
nb5 = [
md(r"""
# Notebook 5: QAOA cho hàm số nguyên (Ví dụ 17–19, Hình 8–10, Bảng 3)

Đi kèm [Phần A, Mục 6](../../docs/A-translation/06-gate-based.md). Notebook chạy hoàn toàn trên trình mô phỏng `AerSimulator`, không cần tài khoản. Ta (1) kiểm tra Hamiltonian ở phương trình (43), (2) dựng mạch của Hình 9, (3) so sánh code **gốc** của Hình 8 và 10 với code **đã sửa**.
"""),
code(r"""
import itertools
import numpy as np
from scipy.optimize import minimize
from qiskit.circuit import QuantumCircuit
from qiskit_aer import AerSimulator

def f(x):                                      # hàm mục tiêu của Ví dụ 10 dạng pseudo-Boolean
    return (-9 + 13*x[0] + 14*x[1] + 9*x[2]
            - 18*x[0]*x[1] - 18*x[0]*x[2] - 18*x[1]*x[2] + 36*x[0]*x[1]*x[2])
"""),
md(r"""
## 1. Hamiltonian của bài toán (Ví dụ 17, phương trình (43))

$$H_P = -2Z_1 - \tfrac{5}{2}Z_2 - \tfrac{9}{2}Z_1 \otimes Z_2 \otimes Z_3.$$

$H_P$ là ma trận đường chéo, nên phần tử đường chéo ứng với trạng thái $|x\rangle$ phải bằng $f(x)$. Ta dùng quy ước của Qiskit: qubit 0 là bit ít quan trọng nhất, và $x_1$ ứng với qubit 0.
"""),
code(r"""
I2, Z = np.eye(2), np.diag([1.0, -1.0])
def op(*ops_by_qubit):                         # ops_by_qubit = [op_q0, op_q1, op_q2]; kron theo thứ tự little-endian
    out = np.array([[1.0]])
    for m in reversed(ops_by_qubit):
        out = np.kron(out, m)
    return out

HP = -2*op(Z, I2, I2) - 2.5*op(I2, Z, I2) - 4.5*op(Z, Z, Z)
diag = np.diag(HP)
ok = True
for idx in range(8):
    x = [(idx >> q) & 1 for q in range(3)]      # x1 = qubit 0, x2 = qubit 1, x3 = qubit 2
    ok &= abs(diag[idx] - f(x)) < 1e-12
print("đường chéo của H_P khớp f(x) trên mọi tổ hợp:", ok)
"""),
md(r"""
## 2. Mạch QAOA (Hình 9)

Mỗi lớp gồm $U(H_P, \gamma)$ (hai cổng RZ và chuỗi CNOT quanh cổng RZ cho số hạng $Z_1 Z_2 Z_3$) rồi mixer $U(H_M, \beta)$ (các cổng RX). Mã giống Hình 9 của bài báo.
"""),
code(r"""
def build_ansatz(theta):
    num_qubits = 3
    qaoa_depth = len(theta) // 2
    circuit = QuantumCircuit(num_qubits)
    gamma = theta[:qaoa_depth]
    beta = theta[qaoa_depth:]
    for i in range(num_qubits):
        circuit.h(i)
    for i in range(qaoa_depth):
        circuit.rz(-4 * gamma[i], 0)
        circuit.rz(-5 * gamma[i], 1)
        circuit.cx(0, 1)
        circuit.cx(1, 2)
        circuit.rz(-9 * gamma[i], 2)
        circuit.cx(1, 2)
        circuit.cx(0, 1)
        for qbit in range(num_qubits):
            circuit.rx(2 * beta[i], qbit)
    circuit.measure_all()
    return circuit

print(build_ansatz([0.1, 0.1, 0.1, 0.1]).draw(fold=-1))
"""),
md(r"""
## 3. Lỗi trong code gốc (Hình 8 và 10)

**(a) `nshots` bị bỏ qua.** Tên tham số đúng của Aer là `shots`.
"""),
code(r"""
sim = AerSimulator()
c = build_ansatz([0.1, 0.1, 0.1, 0.1])
print("run(..., nshots=1000) -> tổng số mẫu:", sum(sim.run(c, nshots=1000).result().get_counts().values()))
print("run(..., shots=1000)  -> tổng số mẫu:", sum(sim.run(c, shots=1000).result().get_counts().values()))
"""),
md(r"""
**(b) `value = ...` thay vì `value += ...`.** Dưới đây là hai hàm mục tiêu cổ điển: bản gốc (giữ nguyên lỗi) và bản đã sửa. Ta dùng cùng `seed_simulator` cho cả hai để kết quả lặp lại được.
"""),
code(r"""
SEED = 7

def classical_obj_fn_original(theta, num_executions=1000):      # Hình 10 gốc: value = ... (ghi đè)
    counts = sim.run(build_ansatz(theta), shots=num_executions, seed_simulator=SEED).result().get_counts()
    value = 0
    sampled = 0
    for solution, occurrences in counts.items():
        x = [int(v) for v in solution[::-1]]
        value = f(x) * occurrences                               # BUG: không cộng dồn
        sampled += occurrences
    return value / sampled

def classical_obj_fn_fixed(theta, num_executions=1000):         # đã sửa: value += ...
    counts = sim.run(build_ansatz(theta), shots=num_executions, seed_simulator=SEED).result().get_counts()
    value = 0
    sampled = 0
    for solution, occurrences in counts.items():
        x = [int(v) for v in solution[::-1]]
        value += f(x) * occurrences
        sampled += occurrences
    return value / sampled
"""),
md(r"""
## 4. Chạy COBYLA với từng hàm mục tiêu và so sánh

Sau mỗi lần tối ưu, ta đánh giá lại tham số tìm được bằng 20000 shots để ước lượng giá trị trung bình thật của $f$ và xác suất đo được lời giải tối ưu $(0,0,0)$.
"""),
code(r"""
def assess(theta, shots=20000, seed=5):
    counts = sim.run(build_ansatz(theta), shots=shots, seed_simulator=seed).result().get_counts()
    mean = sum(f([int(v) for v in k[::-1]]) * n for k, n in counts.items()) / shots
    return mean, counts.get("000", 0) / shots

results = {}
for name, fn in (("gốc (value = ...)", classical_obj_fn_original), ("đã sửa (value += ...)", classical_obj_fn_fixed)):
    res = minimize(fn, [0.1, 0.1, 0.1, 0.1], method="COBYLA")
    mean, p000 = assess(res.x)
    results[name] = res.x
    print(f"{name:24s} tham số={np.round(res.x, 3)}  giá trị trung bình thật của f = {mean:6.2f}   P(000) = {p000:.3f}")
print("tham chiếu: phân phối đều cho trung bình 0.00 và P(000) = 0.125; giá trị nhỏ nhất của f là -9")
"""),
md(r"""
Hàm mục tiêu **đã sửa** cho giá trị trung bình thấp hơn rõ rệt và xác suất đo được lời giải tối ưu cao hơn. Lưu ý: bản gốc trả về giá trị phụ thuộc vào thứ tự khóa trong từ điển kết quả, nên nó không phải là hàm tốt cho COBYLA. Kết quả chính xác thay đổi theo hạt giống và điểm khởi đầu, nên hãy xem đây là minh họa, không phải phép đo chặt chẽ.
"""),
md(r"""
## 5. Kết quả lấy mẫu với tham số đã tối ưu (so với Bảng 3)

Khóa của Qiskit có dạng `q2 q1 q0`, nên khi đọc $(x_1, x_2, x_3)$ ta đảo chuỗi.
"""),
code(r"""
theta = results["đã sửa (value += ...)"]
counts = sim.run(build_ansatz(theta), shots=1000, seed_simulator=11).result().get_counts()
print("Khóa Qiskit | (x1,x2,x3) |  f(x) | Occurrences")
for key, n in sorted(counts.items(), key=lambda kv: -kv[1]):
    x = tuple(int(v) for v in key[::-1])
    print(f"    {key}     |  {x}  | {f(x):5d} | {n:5d}")
print("tổng:", sum(counts.values()))
"""),
]
save(nb5, "05-qaoa-integer-function.ipynb")
