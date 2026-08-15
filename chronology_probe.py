#!/usr/bin/env python3
"""Receiver-visible chronology / noncommutation probe.

This is a generic analysis utility for GeometricNeuronV23.

Input is a time series of local Jacobians A[k] along an already-generated
nonlinear trajectory.  The script compares the true piecewise-constant
chronological variational propagator

    Phi = exp(A[T-1] dt) ... exp(A[1] dt) exp(A[0] dt)

with an order-erased first-Magnus surrogate

    Phi_avg = exp(sum_k A[k] dt)

and with a second-Magnus approximation that includes pairwise commutators.

This does NOT establish that a biological computation is caused by
noncommutativity.  It is only a diagnostic.  Biological ablations and
input/output controls are still required; see HANDOFF_NONCOMMUTING_DENDRITES.md.

NPZ format
----------
Required:
    A   : float array [T, N, N]

Optional:
    dt  : scalar timestep.  Can instead be supplied by --dt.
    C   : float array [R, N], receiver/readout projection.
    P   : float array [N, S], physically reachable/source perturbation map.

If C/P are absent, identity matrices are used.  For biological use, prefer
physical source and receiver maps rather than the identity so the result is
receiver-relative and insensitive to arbitrary inaccessible state directions.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
from scipy.linalg import expm, norm


def ordered_propagator(A: np.ndarray, dt: float) -> np.ndarray:
    """Piecewise-constant time-ordered propagator."""
    n = A.shape[1]
    phi = np.eye(n, dtype=np.result_type(A, float))
    for ak in A:
        # Later evolution multiplies on the left.
        phi = expm(ak * dt) @ phi
    return phi


def magnus_12(A: np.ndarray, dt: float) -> tuple[np.ndarray, np.ndarray]:
    """Discrete first and second Magnus terms.

    Omega_1 = sum_i A_i dt

    Omega_2 ~= 1/2 sum_{i>j} [A_i, A_j] dt^2

    The second term is accumulated in O(T) matrix multiplications by keeping
    the prefix sum S = sum_{j<i} A_j.
    """
    n = A.shape[1]
    dtype = np.result_type(A, float)
    omega1 = np.zeros((n, n), dtype=dtype)
    omega2 = np.zeros((n, n), dtype=dtype)
    prefix = np.zeros((n, n), dtype=dtype)

    for ak in A:
        omega1 += ak * dt
        omega2 += 0.5 * (ak @ prefix - prefix @ ak) * (dt * dt)
        prefix += ak

    return omega1, omega2


def projected_relative_error(
    reference: np.ndarray,
    candidate: np.ndarray,
    C: np.ndarray,
    P: np.ndarray,
    eps: float = 1e-15,
) -> float:
    """Receiver/source projected Frobenius relative error."""
    ref = C @ reference @ P
    err = C @ (reference - candidate) @ P
    return float(norm(err, ord="fro") / (norm(ref, ord="fro") + eps))


def chronology_metrics(
    A: np.ndarray,
    dt: float,
    C: np.ndarray | None = None,
    P: np.ndarray | None = None,
) -> dict[str, object]:
    if A.ndim != 3 or A.shape[1] != A.shape[2]:
        raise ValueError("A must have shape [T, N, N]")
    if dt <= 0:
        raise ValueError("dt must be positive")

    n = A.shape[1]
    if C is None:
        C = np.eye(n)
    if P is None:
        P = np.eye(n)

    C = np.asarray(C)
    P = np.asarray(P)
    if C.ndim != 2 or C.shape[1] != n:
        raise ValueError(f"C must have shape [R, {n}]")
    if P.ndim != 2 or P.shape[0] != n:
        raise ValueError(f"P must have shape [{n}, S]")

    phi = ordered_propagator(A, dt)
    omega1, omega2 = magnus_12(A, dt)
    phi_avg = expm(omega1)
    phi_m2 = expm(omega1 + omega2)

    eta_order_erased = projected_relative_error(phi, phi_avg, C, P)
    eta_after_magnus2 = projected_relative_error(phi, phi_m2, C, P)

    # A dimensionless descriptive size for the pairwise chronological term.
    # This is NOT itself a receiver-visible output metric.
    omega2_ratio = float(norm(omega2, ord="fro") / (norm(omega1, ord="fro") + 1e-15))

    return {
        "T": int(A.shape[0]),
        "N": int(n),
        "dt": float(dt),
        "window": float(A.shape[0] * dt),
        "eta_order_erased": eta_order_erased,
        "eta_after_magnus2": eta_after_magnus2,
        "omega2_over_omega1": omega2_ratio,
        "Phi": phi,
        "Phi_avg": phi_avg,
        "Phi_magnus2": phi_m2,
        "Omega1": omega1,
        "Omega2": omega2,
    }


def _demo() -> None:
    """Two sanity checks: commuting matrices and a noncommuting pair."""
    T = 100
    dt = 1e-3

    commuting = np.array(
        [
            np.diag(
                [
                    -1.0 - 0.2 * np.sin(k / 10.0),
                    -2.0 + 0.1 * np.cos(k / 10.0),
                ]
            )
            for k in range(T)
        ]
    )
    mc = chronology_metrics(commuting, dt)

    a = np.array([[-1.0, 3.0], [0.0, -2.0]])
    b = np.array([[-1.0, 0.0], [2.0, -2.0]])
    noncommuting = np.array([a if k < T // 2 else b for k in range(T)])
    mn = chronology_metrics(noncommuting, dt)

    print("Sanity demo")
    print("-----------")
    print(f"commuting eta_order_erased : {mc['eta_order_erased']:.6g}")
    print(f"noncommuting eta_order_erased: {mn['eta_order_erased']:.6g}")
    print(f"noncommuting eta_after_M2   : {mn['eta_after_magnus2']:.6g}")
    print()
    print("Expected: commuting ~= 0; noncommuting > 0; Magnus-2 should reduce")
    print("the error for this short-window example.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("npz", nargs="?", type=Path, help="NPZ containing A and optional dt/C/P")
    ap.add_argument("--dt", type=float, default=None, help="Override timestep")
    ap.add_argument("--save", type=Path, default=None, help="Optional NPZ for matrices/results")
    ap.add_argument("--demo", action="store_true", help="Run synthetic sanity checks")
    args = ap.parse_args()

    if args.demo or args.npz is None:
        _demo()
        if args.npz is None:
            return

    data = np.load(args.npz)
    A = np.asarray(data["A"])
    dt = args.dt
    if dt is None:
        if "dt" not in data:
            raise ValueError("dt missing: put scalar dt in NPZ or pass --dt")
        dt = float(np.asarray(data["dt"]).reshape(()))

    C = np.asarray(data["C"]) if "C" in data else None
    P = np.asarray(data["P"]) if "P" in data else None
    m = chronology_metrics(A, dt, C=C, P=P)

    print(f"T samples             : {m['T']}")
    print(f"state dimension N     : {m['N']}")
    print(f"dt                    : {m['dt']:.9g}")
    print(f"window                : {m['window']:.9g}")
    print(f"eta order-erased      : {m['eta_order_erased']:.9g}")
    print(f"eta after Magnus-2    : {m['eta_after_magnus2']:.9g}")
    print(f"||Omega2||/||Omega1|| : {m['omega2_over_omega1']:.9g}")

    if args.save is not None:
        np.savez_compressed(
            args.save,
            eta_order_erased=m["eta_order_erased"],
            eta_after_magnus2=m["eta_after_magnus2"],
            omega2_over_omega1=m["omega2_over_omega1"],
            Phi=m["Phi"],
            Phi_avg=m["Phi_avg"],
            Phi_magnus2=m["Phi_magnus2"],
            Omega1=m["Omega1"],
            Omega2=m["Omega2"],
            dt=m["dt"],
        )
        print(f"saved                 : {args.save}")


if __name__ == "__main__":
    main()
