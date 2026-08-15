#!/usr/bin/env python3
"""Capacitance-normalized voltage-only geometry x state commutator probe.

This implements the corrected null in GEOMETRY_STATE_COMMUTATOR_V02.md.
It does NOT include dynamic gating-state dimensions.

Physical linearization:
    C dv/dt = -(Gax + Gm(t)) v

Capacitance-normalized coordinates z=C^(1/2)v:
    dz/dt = -(L + D(t)) z
    L    = C^(-1/2) Gax C^(-1/2)
    D(t) = diag(Gm_i(t)/C_i)

For two snapshots a,b:
    [A_a,A_b]_ij = L_ij * (Delta d_j - Delta d_i)

NPZ input
---------
Required:
    Gax : [N,N] physical reciprocal axial/cable conductance matrix
    C   : [N] positive compartment capacitances
    Gm  : [T,N] local *incremental* membrane conductances at snapshots

Optional:
    Cr  : [R,N] receiver projection in normalized z coordinates
    P   : [N,S] source projection in normalized z coordinates

Important:
`Gm` is NOT maximal channel density and NOT a raw gate reserve variable. It is
an instantaneous voltage-only incremental conductance contribution compatible
with the chosen linearization. Full voltage+gating dynamics need NEURON's
extended impedance / the full Jacobian.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import numpy as np
from numpy.linalg import norm


def normalize_operator(Gax: np.ndarray, C: np.ndarray) -> np.ndarray:
    Gax = np.asarray(Gax, dtype=float)
    C = np.asarray(C, dtype=float)
    if Gax.ndim != 2 or Gax.shape[0] != Gax.shape[1]:
        raise ValueError("Gax must be square [N,N]")
    if C.shape != (Gax.shape[0],):
        raise ValueError("C must have shape [N]")
    if np.any(C <= 0):
        raise ValueError("All capacitances must be positive")
    invsqrt = 1.0 / np.sqrt(C)
    return invsqrt[:, None] * Gax * invsqrt[None, :]


def membrane_rates(Gm: np.ndarray, C: np.ndarray) -> np.ndarray:
    Gm = np.asarray(Gm, dtype=float)
    C = np.asarray(C, dtype=float)
    if Gm.ndim != 2 or Gm.shape[1] != C.size:
        raise ValueError("Gm must have shape [T,N] matching C")
    return Gm / C[None, :]


def commutator_from_delta(L: np.ndarray, delta_d: np.ndarray) -> np.ndarray:
    return L * (delta_d[None, :] - delta_d[:, None])


def pair_metrics(
    L: np.ndarray,
    d0: np.ndarray,
    d1: np.ndarray,
    Cr: np.ndarray | None = None,
    P: np.ndarray | None = None,
) -> dict[str, float]:
    delta = d1 - d0
    K = commutator_from_delta(L, delta)
    kfro = float(norm(K, ord="fro"))
    out = {
        "comm_fro": kfro,
        "comm_fro2": kfro * kfro,
        "delta_rate_mean": float(np.mean(delta)),
        "delta_rate_sd": float(np.std(delta)),
        "delta_rate_l2": float(norm(delta)),
    }

    if np.allclose(L, L.T, rtol=1e-10, atol=1e-12):
        iu = np.triu_indices(L.shape[0], k=1)
        dd = delta[iu[1]] - delta[iu[0]]
        edge = float(2.0 * np.sum((L[iu] ** 2) * (dd ** 2)))
        out["edge_energy"] = edge
        out["edge_identity_relerr"] = float(
            abs(edge - kfro * kfro) / (kfro * kfro + 1e-30)
        )

    if Cr is not None or P is not None:
        n = L.shape[0]
        if Cr is None:
            Cr = np.eye(n)
        if P is None:
            P = np.eye(n)
        Cr = np.asarray(Cr, dtype=float)
        P = np.asarray(P, dtype=float)
        if Cr.ndim != 2 or Cr.shape[1] != n:
            raise ValueError(f"Cr must be [R,{n}]")
        if P.ndim != 2 or P.shape[0] != n:
            raise ValueError(f"P must be [{n},S]")
        out["projected_comm_fro"] = float(norm(Cr @ K @ P, ord="fro"))

    return out


def demo(seed: int = 0) -> None:
    rng = np.random.default_rng(seed)
    n = 8

    # Reciprocal physical axial network.
    W = rng.uniform(0.0, 1.0, size=(n, n))
    W = 0.5 * (W + W.T)
    np.fill_diagonal(W, 0.0)
    Gax = np.diag(W.sum(axis=1)) - W

    # Deliberately nonuniform compartment capacitance.
    C = rng.uniform(0.5, 2.0, size=n)
    L = normalize_operator(Gax, C)

    Gm0 = rng.uniform(0.2, 1.0, size=n)
    Gm1 = rng.uniform(0.2, 1.0, size=n)
    d0 = Gm0 / C
    d1 = Gm1 / C

    m = pair_metrics(L, d0, d1)

    A0 = -(L + np.diag(d0))
    A1 = -(L + np.diag(d1))
    explicit = A0 @ A1 - A1 @ A0
    fast = commutator_from_delta(L, d1 - d0)

    print("v0.2 capacitance-normalized sanity demo")
    print("---------------------------------------")
    print(f"explicit identity error : {norm(explicit-fast, ord='fro'):.6g}")
    print(f"edge identity rel error : {m.get('edge_identity_relerr', float('nan')):.6g}")

    # Uniform change in membrane *rate* must commute.  A uniform raw Gm
    # increment would not be uniform in rate when C differs.
    rate_increment = 0.3
    d_uniform = d0 + rate_increment
    mu = pair_metrics(L, d0, d_uniform)
    print(f"uniform-rate commutator : {mu['comm_fro']:.6g}")
    print("Expected: all three values ~ 0 (floating-point error only).")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("npz", nargs="?", type=Path)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    if args.demo or args.npz is None:
        demo()
        if args.npz is None:
            return

    z = np.load(args.npz)
    Gax = np.asarray(z["Gax"], dtype=float)
    C = np.asarray(z["C"], dtype=float)
    Gm = np.asarray(z["Gm"], dtype=float)
    Cr = np.asarray(z["Cr"], dtype=float) if "Cr" in z else None
    P = np.asarray(z["P"], dtype=float) if "P" in z else None

    L = normalize_operator(Gax, C)
    d = membrane_rates(Gm, C)
    if d.shape[0] < 2:
        raise ValueError("Need at least two Gm snapshots")

    rows = []
    for k in range(d.shape[0] - 1):
        rows.append({"k": k, **pair_metrics(L, d[k], d[k + 1], Cr=Cr, P=P)})

    keys = list(rows[0])
    print(",".join(keys))
    for row in rows:
        print(",".join(str(row[k]) for k in keys))

    if args.out is not None:
        with args.out.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
        print(f"saved: {args.out}")


if __name__ == "__main__":
    main()
