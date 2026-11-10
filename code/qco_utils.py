"""Tiện ích dùng chung cho các notebook của tài liệu.

Các hàm bám theo các công thức trong bài báo của Chicano và cộng sự
(arXiv:2412.15778): chuyển QUBO sang Ising (8)-(11), cận dưới/cận trên của
đa thức pseudo-Boolean (34)-(35), hằng số phạt (36), biểu diễn nhị phân của biến
nguyên (18)-(20).

Một đa thức pseudo-Boolean được lưu dưới dạng từ điển {frozenset(S): a_S}, với S là
tập chỉ số biến (đánh số từ 0) và a_S là hệ số; S rỗng ứng với hằng số.
"""
from __future__ import annotations

import itertools
import math

import numpy as np


# --------------------------------------------------------------------------- #
# Đa thức pseudo-Boolean
# --------------------------------------------------------------------------- #
def multilinear(expr, xs):
    """Khai triển biểu thức sympy theo các biến nhị phân `xs` và áp dụng x^k = x.

    Trả về từ điển {frozenset(S): a_S} (chỉ số biến đánh số từ 0).
    """
    import sympy as sp

    poly = sp.Poly(sp.expand(expr), *xs)
    out: dict[frozenset, object] = {}
    for mon, coef in poly.terms():
        S = frozenset(i for i, m in enumerate(mon) if m > 0)
        out[S] = out.get(S, 0) + coef
    return {S: c for S, c in out.items() if c != 0}


def evaluate(poly, x):
    """Giá trị của đa thức pseudo-Boolean tại vector nhị phân x."""
    return sum(c * math.prod(x[i] for i in S) for S, c in poly.items())


def brute_force(poly, n):
    """Duyệt vét cạn {0,1}^n. Trả về (giá trị nhỏ nhất, danh sách các nghiệm tối ưu)."""
    best, arg = None, []
    for x in itertools.product((0, 1), repeat=n):
        v = evaluate(poly, x)
        if best is None or v < best:
            best, arg = v, [x]
        elif v == best:
            arg.append(x)
    return best, arg


def lower_bound(poly):
    """Phương trình (34): lb(f) = a_0 + sum_{S != rỗng} min(0, a_S)."""
    return sum((c if not S else min(0, c)) for S, c in poly.items())


def upper_bound(poly):
    """Phương trình (35): ub(f) = a_0 + sum_{S != rỗng} max(0, a_S)."""
    return sum((c if not S else max(0, c)) for S, c in poly.items())


def penalty_constant(poly):
    """Phương trình (36): P = ub(f) - lb(f) + 1 = 1 + sum_{S != rỗng} |a_S|."""
    return upper_bound(poly) - lower_bound(poly) + 1


# --------------------------------------------------------------------------- #
# Biểu diễn nhị phân của biến nguyên (phương trình (18)-(20))
# --------------------------------------------------------------------------- #
def integer_encoding(a, c):
    """Biểu diễn z trong [a, c] bằng n biến nhị phân.

    Trả về (a, weights) sao cho z = a + sum_j weights[j] * x_{j+1}. Các trọng số là
    1, 2, 4, ..., 2^(n-2) và trọng số cuối 2^(n-1) - b (phương trình (20)).
    """
    n = max(1, math.ceil(math.log2(c - a + 1)))
    b = 2**n - 1 - (c - a)
    weights = [2**j for j in range(n - 1)] + [2 ** (n - 1) - b]
    return a, weights


# --------------------------------------------------------------------------- #
# Mô phỏng chính xác QAOA bằng vector trạng thái (dùng cho Phần B)
# --------------------------------------------------------------------------- #
def cost_vector(poly, n):
    """Mảng giá trị hàm mục tiêu: cost[i] = f(x) với x_{j+1} = bit j của i (little-endian như Qiskit)."""
    out = np.empty(2**n)
    for i in range(2**n):
        x = [(i >> j) & 1 for j in range(n)]
        out[i] = evaluate(poly, x)
    return out


def qaoa_state(cost, gammas, betas):
    """Trạng thái QAOA (41): prod_k exp(-i beta_k sum X) exp(-i gamma_k H_P) |+>^n, với H_P = diag(cost)."""
    cost = np.asarray(cost, dtype=float)
    n = int(round(math.log2(len(cost))))
    psi = np.full(2**n, 2 ** (-n / 2), dtype=complex)
    for g, b in zip(gammas, betas):
        psi = np.exp(-1j * g * cost) * psi
        c, s = math.cos(b), -1j * math.sin(b)  # exp(-i b X) = cos(b) I - i sin(b) X
        for q in range(n):
            v = psi.reshape(2 ** (n - q - 1), 2, 2**q)
            psi = (c * v + s * v[:, ::-1, :]).reshape(-1)
    return psi


def qaoa_expectation(cost, gammas, betas):
    """Phương trình (42): giá trị kỳ vọng của H_P trong trạng thái QAOA."""
    p = np.abs(qaoa_state(cost, gammas, betas)) ** 2
    return float(p @ np.asarray(cost, dtype=float))


# --------------------------------------------------------------------------- #
# QUBO <-> Ising (phương trình (4)-(11))
# --------------------------------------------------------------------------- #
def qubo_value(Q, c, x):
    x = np.asarray(x)
    return float(x @ Q @ x + c)


def qubo_to_ising(Q, c=0.0):
    """Phương trình (8)-(11). Q phải đối xứng. Trả về (J, h) với J[0,0] chứa hằng số."""
    Q = np.asarray(Q, dtype=float)
    assert np.allclose(Q, Q.T), "Q phải đối xứng"
    n = Q.shape[0]
    J = Q / 4.0
    J[np.diag_indices(n)] = 0.0
    J[0, 0] = c + Q.sum() / 4.0 + np.trace(Q) / 4.0  # (9): sum_{j,k} Q/4 + sum_j Q_jj/4
    h = -0.5 * Q.sum(axis=1)  # (11)
    return J, h


def ising_value(J, h, s):
    """Phương trình (7): f(s) = sum_{j,k} J_jk s_j s_k + sum_j h_j s_j."""
    s = np.asarray(s, dtype=float)
    return float(s @ J @ s + h @ s)
