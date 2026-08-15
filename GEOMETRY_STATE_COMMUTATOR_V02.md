# Geometry × local state commutator v0.2 — capacitance-normalized null

**Status:** corrected mechanistic null / derivation. **Not a novelty claim.**

This supersedes the notation in `GEOMETRY_STATE_COMMUTATOR.md` wherever `L` was read as a raw physical-conductance matrix. The edge identity is exact only after the membrane-capacitance / mass matrix has been normalized away, or when `L` and `D` were already defined as rate operators.

---

## 1. Start from the compartmental equation with capacitance

For the voltage-only local linearization, write

```text
C dv/dt = -(G_ax + G_m(t)) v
```

where

```text
C       diagonal compartment capacitance matrix
G_ax    fixed symmetric axial/cable conductance matrix
G_m(t)  diagonal local incremental membrane conductance matrix
```

The physical state matrix in voltage coordinates is

```text
A_v(t) = -C^-1 (G_ax + G_m(t)).
```

If compartment capacitances differ, `C^-1 G_ax` is generally not symmetric even when the physical axial conductances are reciprocal.

---

## 2. Energy/capacitance-normalized coordinates

Use

```text
z = C^(1/2) v.
```

Then

```text
dz/dt = -(L + D(t)) z
```

with

```text
L    = C^(-1/2) G_ax C^(-1/2)
D(t) = C^(-1/2) G_m(t) C^(-1/2)
     = diag( G_m,i(t) / C_i ).
```

Now `L` is symmetric when the axial conductance matrix is symmetric, and `D(t)` is diagonal with units of inverse time.

This is the clean coordinate system for the cheap commutator null.

---

## 3. Exact identity

For two operating states `a,b`,

```text
A_a = -(L + D_a)
A_b = -(L + D_b)
Delta D = D_b - D_a = diag(Delta d_i).
```

Because the two diagonal matrices commute,

```text
[A_a,A_b] = [L, Delta D].
```

Elementwise,

```text
[A_a,A_b]_ij
    = L_ij (Delta d_j - Delta d_i).
```

For reciprocal axial coupling,

```text
L_ij = -g_ij / sqrt(C_i C_j)
```

on an edge `(i,j)`, where `g_ij` is the physical axial conductance.

Therefore

```text
||[A_a,A_b]||_F^2
 = 2 sum_edges
     [ g_ij^2 / (C_i C_j) ]
     [ Delta(G_m,j/C_j) - Delta(G_m,i/C_i) ]^2.
```

The relevant local field is therefore **incremental membrane rate** `G_m/C`, not raw conductance and certainly not a raw gating variable.

---

## 4. Why this correction matters biologically

NEURON compartments can have different membrane areas and the Park model also treats axonal membrane capacitance specially. Raw `g` or raw gate reserve cannot simply be dropped into the edge formula.

For a channel current such as

```text
I = gbar * gates * (V - Erev),
```

the instantaneous `gbar*gates` is only part of the local linearized dynamics.

The full extended linearization can also contain

```text
di/dgate
dgate'/dV
dgate'/dgate
```

terms. NEURON's documented extended impedance calculation `Impedance.compute(freq, 1)` includes those differential gating-state contributions for supported mechanisms.

Thus the v0.2 edge formula is deliberately a **voltage-only null**. It asks:

> how much chronology would already be expected from fixed axial coupling interacting with a changing diagonal incremental membrane-rate field?

The full Park model must beat this null before gating-state block structure gets an explanatory role.

---

## 5. Biological state variables are not `d_i`

In Park et al. 2025, the A-type potassium inactivation variable and the slow sodium inactivation variable are biologically attractive history coordinates.

But do not substitute either variable directly for `d_i`.

Correct sequence:

```text
saved biological state
       -> linearize ionic current / gating dynamics at that state
       -> obtain local incremental voltage-rate coefficient d_i
       -> compute the voltage-only edge null
```

Then compare with the full voltage+gating extended impedance/Jacobian.

That comparison tells us what the explicit gating-state dimensions add beyond an instantaneous conductance field.

---

## 6. Controls become cleaner

At two times preserve the multiset

```text
{Delta d_i = Delta(G_m,i/C_i)}
```

while changing its assignment to morphology.

Useful controls:

```text
real field
random site shuffle
branch-preserving shuffle
path-distance-bin shuffle
spatially smoothed same mean/variance field
uniform field with same mean
```

The path-distance-bin control is especially important because Park deliberately uses distance-dependent NaV and A-type Kv distributions. A result that is only a restatement of the proximal-distal gradient is not enough.

---

## 7. Receiver gate still dominates interpretation

The full-state Frobenius commutator is not the biological endpoint.

Use actual source and receiver maps:

```text
source current at S
    -> chronological variational propagation
    -> voltage at receiver R.
```

The local pairwise diagnostic is schematically

```text
C_R [A_a,A_b] P_S,
```

while the finite-window target is

```text
C_R (Phi - Phi_order-erased) P_S.
```

A large internal edge roughness that is invisible at the distal dendrite / soma is not a computation at that receiver.

---

## 8. Current one-line null

> **After capacitance normalization, the lowest-order voltage-only noncommutation is exactly an edge-weighted spatial roughness of the change in local incremental membrane rate.**

The possible neuroscience is not this algebra. It is whether that morphology × history alignment predicts receiver-visible behavior beyond total conductance, voltage, distance, and known channel gradients.

---

## References / guardrails

- NEURON `Impedance` documentation: extended `compute(freq, 1)` linearizes the voltage + differential gating-state system and includes `di/dv`, `di/ds`, `ds'/dv`, and `ds'/ds` terms for supported mechanisms.
- Park P et al. (2025), *Dendritic excitations govern back-propagation via a spike-rate accelerometer*, Nature Communications 16:1333. DOI: 10.1038/s41467-025-55819-9.
- Magnus W. (1954), *On the exponential solution of differential equations for a linear operator*, Communications on Pure and Applied Mathematics 7:649–673.
