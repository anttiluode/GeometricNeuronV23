#!/usr/bin/env python3
"""Exact cheap probe for the voltage-only geometry x local-state commutator.

Model null
----------
    A(t) = -(L + D(t))

where L is a fixed spatial/cable coupling operator and D(t) is diagonal.
For two states a,b with Delta d = diag(D_b-D_a),

    [A_a,A_b]_{ij} = L_ij * (Delta d_j - Delta d_i).

For a symmetric graph Laplacian L with off-diagonal L_ij=-g_ij,

    ||[A_a,A_b]||_F^2
      = 2 sum_{i<j} g_ij^2 (Delta d_i - Delta d_j)^2.

This is a mechanistic null, not a complexity metric and not a novelty claim.
See GEOMETRY_STATE_COMMUTATOR.md.

NPZ input
---------
Required:
    L : [N,N] fixed coupling/operator matrix
    d : [T,N] diagonal local-state coefficient at each time

Optional:
    C : [R,N] receiver projection
    P : [N,S] source projection

The script reports the exact commutator magnitude between consecutive states
and, if C/P are supplied, its source->receiver projected magnitude.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
from numpy.linalg import norm


def commutator_from_delta(L: np.ndarray, delta_d: np.ndarray) -> np.ndarray:
    """Return [L, diag(delta_d)] without constructing diagonal matrices."""
    L = np.asarray(L)
    delta_d = np.asarray(delta_d)
    if L.ndim != 2 or L.shape[0] != L.shape[1]:
        raise ValueError("L must be square [N,N]")
    if delta_d.shape != (L.shape[0],):
        raise ValueError("delta_d must have shape [N]")
    return L * (delta_d[None, :] - delta_d[:, None])


def symmetric_edge_energy(L: np.ndarray, delta_d: np.ndarray) -> float:
    """2*sum_{i<j} L_ij^2*(delta_j-delta_i)^2.

    For a symmetric graph Laplacian this equals the Frobenius norm squared
    of [L,diag(delta_d)].  Diagonal L entries contribute zero.
    """
    L = np.asarray(L)
    delta_d = np.asarray(delta_d)
    iu = np.triu_indices(L.shape[0], k=1)
    dif = delta_d[iu[1]] - delta_d[iu[0]]
    return float(2.0 * np.sum((L[iu] ** 2) * (dif ** 2)))


def metrics_for_pair(
    L: np.ndarray,
    d_a: np.ndarray,
    d_b: np.ndarray,
    C: np.ndarray | None = None,
    P: np.ndarray | None = None,
) -> dict[str, float]:
    delta = np.asarray(d_b) - np.asarray(d_a)
    K = commutator_from_delta(L, delta)
    kfro = float(norm(K, ord="fro"))

    out: dict[str, float] = {
        "comm_fro": kfro,
        "comm_fro2": kfro * kfro,
        "delta_mean": float(np.mean(delta)),
        "delta_sd": float(np.std(delta)),
        "delta_l2": float(norm(delta)),
    }

    if np.allclose(L, L.T):
        edge = symmetric_edge_energy(L, delta)
        out["edge_energy"] = edge
        out["edge_identity_relerr"] = float(
            abs(edge - kfro * kfro) / (kfro * kfro + 1e-15)
        )

    if C is not None or P is not None:
        n = L.shape[0]
        if C is None:
            C = np.eye(n)
        if P is None:
            P = np.eye(n)
        C = np.asarray(C)
        P = np.asarray(P)
        if C.ndim != 2 or C.shape[1] != n:
            raise ValueError(f"C must have shape [R,{n}]")
        if P.ndim != 2 or P.shape[0] != n:
            raise ValueError(f"P must have shape [{n},S]")
        out["projected_fro"] = float(norm(C @ K @ P, ord="fro"))

    return out


def _demo(seed: int = 0) -> None:
    rng = np.random.default_rng(seed)
    n = 8
    W = rng.uniform(0.0, 1.0, (n, n))
    W = 0.5 * (W + W.T)
    np.fill_diagonal(W, 0.0)
    L = np.diag(W.sum(axis=1)) - W

    d0 = rng.normal(size=n)
    d1 = rng.normal(size=n)
    m = metrics_for_pair(L, d0, d1)

    # Explicit matrix multiplication sanity check.
    A0 = -(L + np.diag(d0))
    A1 = -(L + np.diag(d1))
    K_explicit = A0 @ A1 - A1 @ A0
    K_fast = commutator_from_delta(L, d1 - d0)
    err = norm(K_explicit - K_fast, ord="fro")

    print("Geometry-state commutator sanity demo")
    print("--------------------------------------")
    print(f"explicit identity error   : {err:.6g}")
    print(f"commutator Frobenius      : {m['comm_fro']:.6g}")
    print(f"edge-energy rel. error    : {m.get('edge_identity_relerr', float('nan')):.6g}")

    uniform = d0 + 3.0
    mu = metrics_for_pair(L, d0, uniform)
    print(f"uniform-change commutator : {mu['comm_fro']:.6g}")
    print("Expected: identity errors ~= 0 and uniform-change commutator ~= 0.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("npz", nargs="?", type=Path)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--out", type=Path, default=None, help="Optional CSV output")
    args = ap.parse_args()

    if args.demo or args.npz is None:
        _demo()
        if args.npz is None:
            return

    z = np.load(args.npz)
    L = np.asarray(z["L"])
    d = np.asarray(z["d"])
    C = np.asarray(z["C"]) if "C" in z else None
    P = np.asarray(z["P"]) if "P" in z else None

    if d.ndim != 2 or d.shape[1] != L.shape[0]:
        raise ValueError("d must have shape [T,N] matching L")
    if d.shape[0] < 2:
        raise ValueError("Need at least two state snapshots")

    rows = []
    for k in range(d.shape[0] - 1):
        m = metrics_for_pair(L, d[k], d[k + 1], C=C, P=P)
        m = {"k": k, **m}
        rows.append(m)

    keys = list(rows[0].keys())
    print(",".join(keys))
    for row in rows:
        print(",".join(str(row[k]) for k in keys))

    if args.out is not None:
        import csv
        with args.out.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
        print(f"saved: {args.out}")


if __name__ == "__main__":
    main()
