#!/usr/bin/env python3
"""Decompose the second Magnus term into local vs geometry-history pieces.

For a trajectory-local Jacobian

    A[k] = S + Q[k]

with fixed spatial/axial coupling S and state-dependent local dynamics Q[k],

    [A_i, A_j]
      = [S, Q_j - Q_i] + [Q_i, Q_j].

For piecewise-constant samples at equal dt, this script computes

    Omega2_total = 1/2 sum_{i>j} [A_i,A_j] dt^2
    Omega2_geom  = 1/2 sum_{i>j} [S,Q_j-Q_i] dt^2
    Omega2_local = 1/2 sum_{i>j} [Q_i,Q_j] dt^2

and verifies Omega2_total = Omega2_geom + Omega2_local.

This is bookkeeping of established operator algebra, NOT a complexity metric.
Raw full-state norms depend on coordinate scaling. Prefer physical source/receiver
projections and the voltage-only capacitance-normalized null first.

NPZ
---
Required:
    A : [T,N,N] local Jacobians along trajectory
    S : [N,N] fixed morphology/axial part in the SAME coordinates/scaling
    dt: scalar (or pass --dt)

Optional:
    C : [R,N] receiver projection
    P : [N,S] source projection

The script assumes S really is time independent. If synaptic/nonlocal couplings
change with time, they belong in Q and Q may no longer be block diagonal.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
from numpy.linalg import norm


def comm(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    return X @ Y - Y @ X


def decompose_omega2(A: np.ndarray, S: np.ndarray, dt: float):
    A = np.asarray(A)
    S = np.asarray(S)
    if A.ndim != 3 or A.shape[1] != A.shape[2]:
        raise ValueError("A must be [T,N,N]")
    n = A.shape[1]
    if S.shape != (n, n):
        raise ValueError("S must be [N,N] matching A")
    if dt <= 0:
        raise ValueError("dt must be positive")

    Q = A - S[None, :, :]
    dtype = np.result_type(A, S, float)
    total = np.zeros((n, n), dtype=dtype)
    geom = np.zeros((n, n), dtype=dtype)
    local = np.zeros((n, n), dtype=dtype)
    prefix_A = np.zeros((n, n), dtype=dtype)
    prefix_Q = np.zeros((n, n), dtype=dtype)

    # Current i is later than every matrix already in the prefix.
    for i, (Ai, Qi) in enumerate(zip(A, Q)):
        if i:
            total += 0.5 * comm(Ai, prefix_A) * dt**2

            # sum_{j<i} [S, Q_j-Q_i]
            geom += 0.5 * comm(S, prefix_Q - i * Qi) * dt**2

            # sum_{j<i} [Q_i,Q_j]
            local += 0.5 * comm(Qi, prefix_Q) * dt**2

        prefix_A += Ai
        prefix_Q += Qi

    return total, geom, local


def projected_norm(M, C=None, P=None):
    n = M.shape[0]
    if C is None:
        C = np.eye(n)
    if P is None:
        P = np.eye(n)
    C = np.asarray(C)
    P = np.asarray(P)
    if C.ndim != 2 or C.shape[1] != n:
        raise ValueError(f"C must be [R,{n}]")
    if P.ndim != 2 or P.shape[0] != n:
        raise ValueError(f"P must be [{n},S]")
    return float(norm(C @ M @ P, ord="fro"))


def demo(seed: int = 0):
    rng = np.random.default_rng(seed)
    T, n, dt = 11, 7, 1e-3
    S = rng.normal(size=(n, n))
    Q = rng.normal(size=(T, n, n))
    A = Q + S[None]
    total, geom, local = decompose_omega2(A, S, dt)
    err = norm(total - geom - local, ord="fro")
    print("second-Magnus decomposition demo")
    print("--------------------------------")
    print(f"identity error: {err:.6g}")
    print("Expected: ~ floating-point zero.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("npz", nargs="?", type=Path)
    ap.add_argument("--dt", type=float, default=None)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--save", type=Path, default=None)
    args = ap.parse_args()

    if args.demo or args.npz is None:
        demo()
        if args.npz is None:
            return

    z = np.load(args.npz)
    A = np.asarray(z["A"])
    S = np.asarray(z["S"])
    dt = args.dt if args.dt is not None else float(np.asarray(z["dt"]).reshape(()))
    C = np.asarray(z["C"]) if "C" in z else None
    P = np.asarray(z["P"]) if "P" in z else None

    total, geom, local = decompose_omega2(A, S, dt)
    residual = total - geom - local

    print(f"T                         : {A.shape[0]}")
    print(f"N                         : {A.shape[1]}")
    print(f"dt                        : {dt:.9g}")
    print(f"identity residual fro     : {norm(residual, ord='fro'):.9g}")
    print(f"Omega2 total fro          : {norm(total, ord='fro'):.9g}")
    print(f"Omega2 geom fro           : {norm(geom, ord='fro'):.9g}")
    print(f"Omega2 local fro          : {norm(local, ord='fro'):.9g}")
    print(f"projected total           : {projected_norm(total,C,P):.9g}")
    print(f"projected geom            : {projected_norm(geom,C,P):.9g}")
    print(f"projected local           : {projected_norm(local,C,P):.9g}")
    print("NOTE: geom/local projected norms do not add; the matrices can cancel.")

    if args.save is not None:
        np.savez_compressed(
            args.save,
            Omega2_total=total,
            Omega2_geom=geom,
            Omega2_local=local,
            residual=residual,
            dt=dt,
        )
        print(f"saved                     : {args.save}")


if __name__ == "__main__":
    main()
