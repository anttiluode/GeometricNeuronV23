# Full-state geometry × history decomposition

**Status:** exact algebraic decomposition / falsification tool. **Not a novelty claim.**

This is the full-state extension of the voltage-only edge null in `GEOMETRY_STATE_COMMUTATOR_V02.md`.

The mathematics is standard operator algebra and closely related to reaction–diffusion operator splitting. The possible neuroscience contribution would be using the decomposition to separate **intrinsic local chronology** from **morphology-dependent chronology** in a realistic neuron, then asking which part survives at an actual receiver.

---

## 1. Detailed neuron as fixed spatial coupling + local state dynamics

For a conventional compartmental neuron with local membrane/gating/synaptic mechanisms and no nonlocal mechanism such as a gap junction, arrange the incremental state as blocks by compartment:

```text
x = [x_1, x_2, ..., x_N]
x_i = [voltage_i, local gates_i, local synaptic states_i, ...]
```

Along a nonlinear trajectory,

```text
d(delta x)/dt = A(t) delta x.
```

Split the local Jacobian as

```text
A(t) = S + Q(t).
```

Here:

```text
S       fixed morphology / axial-coupling operator
Q(t)    state-dependent local membrane + gating + synaptic Jacobian
```

For purely local mechanisms, `Q(t)` is block diagonal over compartments:

```text
Q(t) = blockdiag(Q_1(t), ..., Q_N(t)).
```

`S` couples neighboring compartment voltages according to axial geometry. Capacitance/mass normalization should be handled consistently before using Euclidean matrix norms.

This split is an approximation only when supposedly local mechanisms actually couple compartments through concentrations, gap junctions, extracellular mechanisms, or other nonlocal state.

---

## 2. Exact pairwise commutator decomposition

Take two times/states `a,b`:

```text
A_a = S + Q_a
A_b = S + Q_b.
```

Then exactly

```text
[A_a,A_b]
  = [S, Q_b-Q_a] + [Q_a,Q_b].
```

because `[S,S]=0`.

Call the two terms provisionally:

```text
G_ab = [S, Q_b-Q_a]      geometry × history term
L_ab = [Q_a,Q_b]          local intrinsic chronology term
```

so

```text
[A_a,A_b] = G_ab + L_ab.
```

These names are bookkeeping labels, not claims of canonical mathematical objects.

---

## 3. Why this is stronger than “the modes move”

The decomposition asks *why* the instantaneous operators fail to commute.

Two very different possibilities can create chronological sensitivity:

### Local chronology

At one compartment, the local voltage/gating system changes in such a way that

```text
[Q_i(a), Q_i(b)] != 0.
```

This can occur even in an isopotential point neuron. It does not require dendritic morphology.

### Geometry × history chronology

The local dynamical block changes differently across locations, and the fixed axial coupling does not commute with that spatial pattern:

```text
[S, Q_b-Q_a] != 0.
```

This is the piece that specifically requires spatial coupling plus spatial organization of the changing local state.

Therefore a neuron can have large chronology while geometry contributes almost none of it. V23 must separate these cases.

---

## 4. Edge-block form

Let axial coupling between neighboring compartments `i,j` act only through the voltage coordinate. Write schematically

```text
S_ij = ell_ij * E
```

where `E = e_v e_v^T` selects the voltage coordinate inside each local state block.

Let

```text
Delta Q_i = Q_i(b) - Q_i(a).
```

Then for an off-diagonal morphology edge,

```text
G_ab,ij
 = S_ij Delta Q_j - Delta Q_i S_ij
 = ell_ij ( E Delta Q_j - Delta Q_i E ).
```

This is the full-state analogue of

```text
L_ij (Delta d_j - Delta d_i)
```

from the voltage-only model.

It shows that geometry/history coupling can be generated not only by changes in local incremental voltage conductance but also by changes in voltage->gate and gate->voltage couplings at the endpoints of an axial edge.

---

## 5. Voltage-only null is recovered exactly

If every local block contains only voltage,

```text
Q_i(t) = d_i(t)
```

is scalar. Then local blocks always commute:

```text
[Q_i(a),Q_i(b)] = 0
```

and

```text
G_ab,ij = ell_ij (Delta d_j - Delta d_i).
```

So the v0.2 edge-roughness identity is exactly the one-dimensional special case of this full-state split.

That makes it a true null model rather than an unrelated heuristic.

---

## 6. Second Magnus term separates the same way

The chronological variational propagator has Magnus expansion

```text
Phi = exp(Omega_1 + Omega_2 + ...)
```

with

```text
Omega_2
 = 1/2 integral dt1 integral^t1 dt2
     [A(t1), A(t2)].
```

Using the exact decomposition,

```text
Omega_2 = Omega_2^geom + Omega_2^local
```

where

```text
Omega_2^geom
 = 1/2 integral integral
     [S, Q(t2)-Q(t1)]

Omega_2^local
 = 1/2 integral integral
     [Q(t1),Q(t2)].
```

This gives an immediate quantitative question:

> Of the pairwise chronological correction along a real neuronal trajectory, how much comes from local intrinsic dynamics and how much specifically from the interaction of local history with morphology?

Do not infer the same separation for all higher Magnus terms without explicitly deriving them; nested commutators mix these components.

---

## 7. The strongest controls become obvious

### Isopotential / no-geometry control

Set axial morphology coupling to a point-neuron surrogate or remove spatial distinctions while preserving local kinetics.

If chronology survives entirely through `Omega_2^local`, morphology was not required.

### Same local history, shuffled address

Preserve the complete multiset of local blocks

```text
{Q_i(t)}
```

but permute them over the morphology, ideally with branch/path-distance matched variants.

This preserves local kinetics but changes `Omega_2^geom`.

### Freeze history

Freeze the known slow state variable while keeping morphology and instantaneous conductance budget as matched as possible.

Park calibration candidates:

```text
A-type Kv inactivation
slow NaV inactivation
```

### Static heterogeneous field

Keep a spatially heterogeneous `Q_i` fixed in time.

Then it may strongly change the instantaneous spectrum/impedance, but it does **not** generate a pairwise chronology term by itself because `Q(t2)-Q(t1)=0` and `[Q,Q]=0`.

This cleanly distinguishes static spatial heterogeneity from history-dependent operator chronology.

---

## 8. Receiver visibility still decides the biological question

Neither

```text
||Omega_2^geom||
```

nor

```text
||Omega_2^local||
```

is a computational metric by itself.

The meaningful object is physical input/output sensitivity, e.g.

```text
C_R Phi(t,s) B_S
```

or an order-erased comparison at the same source and receiver.

A useful analysis therefore reports both:

```text
internal source of chronology
receiver-visible consequence
```

A huge geometry/history term in distal hidden state that the soma cannot observe is not an explanation of somatic computation.

---

## 9. Coordinate / scaling warning

Gating variables and voltage have different units and arbitrary parameterizations. Raw Frobenius norms of full Jacobian blocks are coordinate dependent.

Therefore:

```text
- use physically motivated state scaling or balancing for diagnostic matrix norms;
- prefer source->receiver transfer effects for final interpretation;
- do not compare raw full-state norm fractions across models with different state parameterizations.
```

The voltage-only capacitance-normalized edge null avoids part of this problem and remains the first baseline.

---

## 10. Relation to established mathematics

For reaction–diffusion systems, splitting diffusion from local reaction and examining commutators is standard mathematics. Descombes et al. (2014), for example, characterize operator-splitting errors in nonlinear reaction–diffusion equations using Lie formalism.

So V23 cannot claim:

```text
spatial coupling + local reaction can fail to commute
```

as new.

The candidate neuroscience question is narrower:

> **Does the morphology-dependent component of chronological operator variation causally predict receiver-visible dendritic computation in a realistic neuron, beyond local channel chronology and ordinary activity/conductance measures?**

---

## 11. Park calibration prediction sharpened

The Park 2025 detailed CA1 model is especially useful because its pure-optogenetic version omits NMDAR and VGCC conductances, while the known bAP-filtering phenotype is produced by spatially distributed NaV/A-type Kv/KDR dynamics and explicit channel history.

This lets us ask, before touching NMDA:

```text
known history-dependent propagation phenotype
        |
        +-- local chronology only?
        |
        +-- geometry × history chronology?
        |
        +-- both?
```

If freezing the history gates kills the phenotype but `Omega_2^geom` contributes almost nothing at the distal receiver, the morphology-chronology hypothesis weakens substantially.

If `Omega_2^geom` rises specifically during the opening/closing window, survives source->receiver projection, changes under address shuffles, and is not explained by total conductance or voltage, then it earns a move to harder dendritic computations.

---

## 12. Current hierarchy of claims

```text
LEVEL 0 — standard math
S and Q(t) can fail to commute.

LEVEL 1 — exact neuron-model decomposition
[A_a,A_b] = [S,Q_b-Q_a] + [Q_a,Q_b].

LEVEL 2 — mechanistic empirical question
Does the first term explain a known history-dependent dendritic phenotype?

LEVEL 3 — computational question
Does its receiver-visible contribution predict sequence/task computation?

LEVEL 4 — discovery question
Does it generalize across mechanisms/morphologies better than established
activity, impedance, conductance, distance, and voltage-rank descriptors?
```

Only Levels 2–4 could become neuroscience results.

---

## References / guardrails

- Magnus W. (1954), *On the exponential solution of differential equations for a linear operator*, Communications on Pure and Applied Mathematics 7:649–673.
- Descombes S, Duarte M, Dumont T, Laurent F, Louvet V, Massot M. (2014), *Analysis of operator splitting in the nonasymptotic regime for nonlinear reaction-diffusion equations*, SIAM Journal on Numerical Analysis 52:1311–1334. DOI: 10.1137/130926006.
- Park P et al. (2025), *Dendritic excitations govern back-propagation via a spike-rate accelerometer*, Nature Communications 16:1333. DOI: 10.1038/s41467-025-55819-9.

## Current one-line result

> **At second Magnus order, a compartmental neuron's chronology separates exactly into an intrinsic local term and a morphology × changing-local-state term. The question worth testing is whether the latter is visible and useful at the biological receiver.**
