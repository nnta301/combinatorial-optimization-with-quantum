import nbformat as nbf

def md(s): return nbf.v4.new_markdown_cell(s.strip("\n"))
def code(s): return nbf.v4.new_code_cell(s.strip("\n"))

def save(cells, path):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nbf.write(nb, path)

# ------------------------------------------------------------------ NB1
nb1 = [
md(r"""
# Notebook 1: QUBO và mô hình Ising

Đi kèm [Phần A, Mục 2.1](../../docs/A-translation/02-background.md). Notebook kiểm tra bằng số các công thức chuyển QUBO sang mô hình Ising, phương trình (8)–(11), trên mọi tổ hợp nhị phân.

Ý tưởng: với phép thế $x_j = (1 - s_j)/2$, hàm QUBO $f(x) = \sum_{j,k} Q_{j,k} x_j x_k + c$ trở thành hàm Ising $f(s) = \sum_{j,k} J_{j,k} s_j s_k + \sum_j h_j s_j$ có cùng giá trị tại các điểm tương ứng.
"""),
code(r"""
import itertools, sys
import numpy as np
sys.path.insert(0, "../../code")
from qco_utils import qubo_value, qubo_to_ising, ising_value
"""),
md("## 1. Kiểm tra trên một QUBO ngẫu nhiên"),
code(r"""
rng = np.random.default_rng(0)
n = 5
A = rng.integers(-5, 6, size=(n, n)).astype(float)
Q = (A + A.T) / 2          # QUBO đối xứng, như giả thiết của bài báo
c = 3.0
J, h = qubo_to_ising(Q, c)

max_err = 0.0
for x in itertools.product((0, 1), repeat=n):
    s = [1 - 2 * xi for xi in x]                  # x = (1 - s)/2  <=>  s = 1 - 2x
    max_err = max(max_err, abs(qubo_value(Q, c, x) - ising_value(J, h, s)))
print("sai số lớn nhất trên 2^5 tổ hợp:", max_err)
"""),
md(r"""
## 2. Kiểm tra trên QUBO của Ví dụ 15 (phương trình (39))

Với $P = 7$ và các biến theo thứ tự $(x_1, x_2, x_3, z)$:

$$f(x, z) = x_1 z - 2z - x_1 x_3 + x_2 + x_3 + P\,(x_2 x_3 - 2x_2 z - 2x_3 z + 3z).$$

Ma trận $Q$ đối xứng nhận được bằng cách chia đôi coefficient của mỗi tích hai biến khác nhau vào hai vị trí $(j,k)$ và $(k,j)$.
"""),
code(r"""
P = 7
def f39(x1, x2, x3, z):
    return x1*z - 2*z - x1*x3 + x2 + x3 + P*(x2*x3 - 2*x2*z - 2*x3*z + 3*z)

Q = np.zeros((4, 4))
def add_pair(j, k, coef):            # coefficient của x_j x_k (j != k), chia đều cho (j,k) và (k,j)
    Q[j, k] += coef / 2; Q[k, j] += coef / 2
# thứ tự biến: 0:x1, 1:x2, 2:x3, 3:z
add_pair(0, 3, 1)                    # x1 z
Q[3, 3] += -2 + 3 * P                # -2z + 3P z
add_pair(0, 2, -1)                   # -x1 x3
Q[1, 1] += 1                         # x2
Q[2, 2] += 1                         # x3
add_pair(1, 2, P)                    # P x2 x3
add_pair(1, 3, -2 * P)               # -2P x2 z
add_pair(2, 3, -2 * P)               # -2P x3 z

J, h = qubo_to_ising(Q, 0.0)
err_q = max(abs(qubo_value(Q, 0, x) - f39(*x)) for x in itertools.product((0, 1), repeat=4))
err_i = max(abs(ising_value(J, h, [1 - 2 * xi for xi in x]) - f39(*x)) for x in itertools.product((0, 1), repeat=4))
print("Q khớp (39):", err_q, "| Ising khớp (39):", err_i)
print("J =\n", J)
print("h =", h)
"""),
md(r"""
Cả hai sai số bằng 0: ma trận $Q$ và mô hình Ising thu được từ (8)–(11) cho đúng giá trị của hàm trong phương trình (39) ở cả 16 tổ hợp. Ghi chú: $J_{1,1}$ chứa toàn bộ hằng số của mô hình (nó chỉ dịch hàm mục tiêu, không đổi optimal solution).
"""),
]
save(nb1, "01-qubo-and-ising.ipynb")

# ------------------------------------------------------------------ NB2
nb2 = [
md(r"""
# Notebook 2: Biểu diễn solution và hàm mục tiêu

Đi kèm [Phần A, Mục 4.1–4.2](../../docs/A-translation/04-problem-transformation.md): Ví dụ 4, 5, 6 (biến nguyên), Ví dụ 9 (MAX-SAT), Ví dụ 10 (hàm số nguyên), Ví dụ 11 (tô màu đồ thị). Mọi kết quả đều được đối chiếu bằng duyệt vét cạn.
"""),
code(r"""
import itertools, sys
from collections import defaultdict
import sympy as sp
sys.path.insert(0, "../../code")
from qco_utils import integer_encoding, multilinear, evaluate, brute_force, penalty_constant
"""),
md(r"""
## 1. Biến nguyên → biến nhị phân (Ví dụ 4, 5, 6)

Hàm `integer_encoding(a, c)` trả về $a$ và các trọng số của $z = a + \sum_j w_j x_j$ theo phương trình (20). Với mỗi ví dụ ta kiểm tra rằng tập giá trị $z$ có thể biểu diễn đúng bằng $[a, c]$.
"""),
code(r"""
def reachable(a, ws):
    return sorted({a + sum(w * xi for w, xi in zip(ws, x)) for x in itertools.product((0, 1), repeat=len(ws))})

for name, (lo, hi), expected in [
    ("Ví dụ 4: z in [0, 7]",  (0, 7),  [1, 2, 4]),
    ("Ví dụ 5: z in [0, 5]",  (0, 5),  [1, 2, 2]),
    ("Ví dụ 6: z in [-3, 3]", (-3, 3), [1, 2, 3]),
]:
    a, ws = integer_encoding(lo, hi)
    vals = reachable(a, ws)
    print(f"{name:24s} a={a:3d} trọng số={ws}  (bài báo: {expected})  giá trị biểu diễn được: {vals[0]}..{vals[-1]}")
    assert ws == expected and vals == list(range(lo, hi + 1))
"""),
md(r"""
Mỗi giá trị của $z$ có thể có nhiều biểu diễn (ví dụ $z = 3$ trong Ví dụ 5). Điều này đúng như bài báo nêu, và không gây hại vì các biểu diễn khác nhau cho cùng một giá trị mục tiêu.
"""),
code(r"""
a, ws = integer_encoding(0, 5)
reps = defaultdict(list)
for x in itertools.product((0, 1), repeat=3):
    reps[a + sum(w * xi for w, xi in zip(ws, x))].append(x)
print(dict(reps))
"""),
md(r"""
## 2. MAX-SAT: Ví dụ 9, phương trình (25)

Clause $c$ không được thỏa chỉ khi mọi literal sai. Với literal dương $x_j$ ta dùng $(1 - x_j)$, với literal âm $\neg x_j$ ta dùng $x_j$.
"""),
code(r"""
x1, x2, x3 = sp.symbols("x1 x2 x3")
clauses = [
    ((x1, True), (x2, False), (x3, True)),    # x1 or not x2 or x3
    ((x1, True), (x2, True),  (x3, False)),   # x1 or x2 or not x3
    ((x1, False), (x2, False), (x3, True)),   # not x1 or not x2 or x3
]
def unsat_poly(clause):
    expr = 1
    for var, positive in clause:
        expr *= (1 - var) if positive else var
    return expr

f_expr = sum(unsat_poly(c) for c in clauses)
f_poly = multilinear(f_expr, [x1, x2, x3])
print("f(x) =", sp.expand(f_expr))
print("khớp phương trình (25):", sp.expand(f_expr - (x1*x2*x3 - 2*x2*x3 - x1*x3 + x2 + x3)) == 0)

# đối chiếu với việc đếm trực tiếp số clause không được thỏa
def count_unsat(x):
    xs = dict(zip((x1, x2, x3), x))
    return sum(0 if any((xs[v] == 1) == pos for v, pos in c) else 1 for c in clauses)
assert all(evaluate(f_poly, x) == count_unsat(x) for x in itertools.product((0, 1), repeat=3))
best, arg = brute_force(f_poly, 3)
print("giá trị nhỏ nhất:", best, "| các phép gán thỏa mọi clause:", arg)
"""),
md(r"""
Có **5** phép gán thỏa mọi clause: `000`, `011`, `100`, `101`, `111`. Con số này quan trọng khi đọc kết quả của Hình 4 và Bảng 2 ở [Notebook 4](04-quantum-annealer-maxsat.ipynb).
"""),
md(r"""
## 3. Hàm số nguyên: Ví dụ 10

$f(z) = z^3 - 6z$ với $z \in [-3, 3]$ và $z = -3 + x_1 + 2x_2 + 3x_3$. Ta khai triển và áp dụng $x^k = x$.
"""),
code(r"""
x1, x2, x3 = sp.symbols("x1 x2 x3")
z = -3 + x1 + 2*x2 + 3*x3
f_expr = z**3 - 6*z
f_poly = multilinear(f_expr, [x1, x2, x3])
names = {0: "x1", 1: "x2", 2: "x3"}
for S, c in sorted(f_poly.items(), key=lambda kv: (len(kv[0]), sorted(kv[0]))):
    print(f"{str(c):>5}  *","*".join(names[i] for i in sorted(S)) or "1")

# so với đáp án trong bài báo: -9 + 13x1 + 14x2 + 9x3 - 18x1x2 - 18x1x3 - 18x2x3 + 36x1x2x3
paper = {frozenset(): -9, frozenset({0}): 13, frozenset({1}): 14, frozenset({2}): 9,
         frozenset({0, 1}): -18, frozenset({0, 2}): -18, frozenset({1, 2}): -18, frozenset({0, 1, 2}): 36}
print("khớp bài báo:", f_poly == paper)
# và khớp với hàm gốc z^3 - 6z trên mọi tổ hợp
fz = lambda t: t**3 - 6*t
assert all(evaluate(f_poly, x) == fz(-3 + x[0] + 2*x[1] + 3*x[2]) for x in itertools.product((0, 1), repeat=3))
print("giá trị nhỏ nhất:", brute_force(f_poly, 3))
"""),
md(r"""
## 4. Tô màu đồ thị: Ví dụ 7 và 11

Đồ thị đường đi gồm 3 nút, các cạnh $(0,1)$ và $(1,2)$, với 3 màu. Hàm mục tiêu (28) là $\sum_{(j,k)\in E}\sum_{\ell} x_{j,\ell} x_{k,\ell}$, cộng penalty function one-hot $P\sum_j (\sum_\ell x_{j,\ell} - 1)^2$ cho ràng buộc (22).
"""),
code(r"""
nodes, edges, colors = 3, [(0, 1), (1, 2)], 3
xs = sp.symbols(f"y0:{nodes*colors}")
X = lambda j, l: xs[j*colors + l]

objective = sum(X(j, l) * X(k, l) for (j, k) in edges for l in range(colors))
onehot = sum((sum(X(j, l) for l in range(colors)) - 1)**2 for j in range(nodes))
obj_poly = multilinear(objective, xs)
P = penalty_constant(obj_poly)                     # theo (36), áp dụng cho phần mục tiêu
total = multilinear(objective + P * onehot, xs)
print("P =", P)

best, arg = brute_force(total, nodes*colors)
def decode(x):
    return [x[j*colors:(j+1)*colors].index(1) for j in range(nodes)]
print("giá trị nhỏ nhất:", best, "| số optimal solution:", len(arg))
assert all(sum(x[j*colors:(j+1)*colors]) == 1 for x in arg for j in range(nodes))        # mọi optimal solution đều feasible
assert all(decode(x)[0] != decode(x)[1] and decode(x)[1] != decode(x)[2] for x in arg)
print("ví dụ vài cách tô:", [decode(x) for x in arg[:4]])
"""),
md(r"""
Có $3 \cdot 2 \cdot 2 = 12$ cách tô hợp lệ cho đường đi 3 nút với 3 màu, và duyệt vét cạn trên 9 biến nhị phân cho đúng 12 optimal solution, tất cả đều thỏa ràng buộc one-hot và không có hai nút kề nhau cùng màu.
"""),
]
save(nb2, "02-binary-encoding-and-objective.ipynb")
