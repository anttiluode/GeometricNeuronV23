# Chronology locality — what graph distance buys, and what it does not

**Status:** mathematical guardrail / intuition aid. **Not a novelty claim.**

A useful consequence of the sparse cable operator fell out of the commutator calculation. It resembles the old “space becomes time” intuition, but the correct statement is about **short-time expansion order**, not a finite-speed causal cone.

---

## 1. Classical graph heat-kernel fact

For a sparse graph generator `L`,

```text
exp(-t L) = I - tL + t^2 L^2/2! - ...
```

and `(L^k)_ij` can only be nonzero when a walk of length at most `k` connects `j` to `i` (modulo diagonal factors).

Therefore, if the combinatorial distance between vertices `i,j` is `r`, the short-time off-diagonal heat kernel begins at order roughly

```text
t^r.
```

This is established graph heat-kernel mathematics. Keller, Lenz, Münch, Schmidt & Telcs (2016) show that short-time graph heat kernels behave like `t^d`, where `d` is combinatorial distance; Steinerberger (2018) gives the corresponding leading shortest-path coefficient for finite graphs.

References:
- Keller M, Lenz D, Münch F, Schmidt M, Telcs A. (2016), *Note on short-time behavior of semigroups associated to self-adjoint operators*, Bull. London Math. Soc. 48:935–944. DOI: 10.1112/blms/bdw054.
- Steinerberger S. (2018), *Varadhan Asymptotics for the Heat Kernel on Finite Graphs*, arXiv:1801.02183.

---

## 2. Chronology adds one extra ingredient: state difference

For the corrected voltage-only null,

```text
A_a = -(L + D_a)
A_b = -(L + D_b)
```

with diagonal `D_a,D_b`, the two-state order contrast is

```text
U_BA(t) - U_AB(t)
 = exp(A_b t) exp(A_a t)
   - exp(A_a t) exp(A_b t).
```

Its first term is

```text
 t^2 [A_b,A_a] + O(t^3)
```

and

```text
[A_b,A_a] = [L, D_a-D_b].
```

That first commutator is supported only on cable edges.

So for a source and receiver separated by more than one graph edge, pairwise noncommutation cannot reach the receiver at order `t^2`.

Higher nested commutators/products add further factors of the sparse cable operator. Each additional cable factor can extend support by at most one graph hop.

Heuristically, for source–receiver graph distance `r > 0`, an order-sensitive term in this stripped model needs at least

```text
r cable moves + one state-difference insertion,
```

so its earliest possible Taylor order is approximately

```text
t^(r+1).
```

This is a support/order statement, not a claim about amplitude or a biological law.

---

## 3. Why this is not a light cone

A passive cable is diffusive. Its continuum Green function has nonzero tails at every positive time; there is no sharp propagation front.

As a compartmental discretization is refined, the combinatorial distance between two fixed physical points increases while axial rates also change. The `t^r` graph-series picture converges toward the continuum heat-kernel short-time behavior rather than giving a discretization-independent signal speed.

Therefore do **not** report:

```text
bracket depth = physical distance
or
finite commutator cone
or
chronological light cone.
```

The useful statement is only:

> **Sparse morphology imposes a hierarchy on how many local operator compositions are required before a distant source can influence a distant receiver in a short-time expansion.**

---

## 4. Why this helps the experiment

It tells us not to expect a raw one-step commutator norm to explain a soma hundreds of compartments away.

There are now three levels:

```text
edge source:
    [L, Delta D]

finite local chronology:
    nested commutators / Magnus terms

biological receiver:
    C_R Phi(t,s) B_S
```

So the cheap edge metric is a **source map** for chronology, not the endpoint.

A state gradient can be large on a distal branch yet fail to matter to the soma because the subsequent propagation/observation factors erase it.

---

## 5. A potentially useful spatial diagnostic

For every edge compute

```text
q_ij(t_a,t_b)
  = |L_ij|^2 * |Delta d_i - Delta d_j|^2.
```

This gives a map of where the first chronology-generating term is being produced.

Then compare that map with receiver sensitivity / adjoint influence from the chosen receiver.

A natural next object is therefore not merely total edge roughness but a receiver-weighted version:

```text
chronology source q_ij
    ×
receiver visibility of edge (i,j)
```

The exact weighting should come from the variational propagator or an adjoint, not from an invented Euclidean-distance weight.

---

## 6. Relation to older “modes” language

This provides a reason to demote eigenmodes still further.

The primitive sequence is

```text
fixed sparse coupling
 + spatially varying history field
 -> local noncommutation sources on edges
 -> propagation through the tree
 -> receiver-visible consequence
```

Eigenvalue/eigenvector motion is one coordinate system for describing the resulting operator, but it is not the mechanism itself.

---

## Current sentence

> **Space does not become time; sparse spatial coupling constrains the algebraic order at which temporal state changes can become visible across distance.**

That sentence is classical-math-compatible and does not turn a diffusive dendrite into a wave equation.
