# GeometricNeuronV23 — CURRENT HANDOFF

**Updated:** 2026-08-15, third pass

**Status:** active falsification program. Nothing here is a novelty claim.

## Read in this order

1. `HANDOFF_NONCOMMUTING_DENDRITES.md` — literature collision and Park calibration ladder.
2. `GEOMETRY_STATE_COMMUTATOR_V02.md` — corrected capacitance-normalized voltage-only null.
3. `FULL_STATE_GEOMETRY_HISTORY_DECOMPOSITION.md` — exact full-state local-vs-morphology chronology split.
4. `CHRONOLOGY_LOCALITY.md` — graph-distance / short-time support guardrail.
5. `chronology_probe.py` — time-ordered propagator vs first/second Magnus diagnostic.
6. `chronology_decompose.py` — second-Magnus geometry-history vs local decomposition.
7. `geometry_state_commutator_v02.py` — capacitance-normalized voltage-only edge probe.
8. `OPERATOR_ATLAS_HYPOTHESIS.md`, `SPACETIME_SEPARABILITY_GATE.md` — upstream lineage.

The original `GEOMETRY_STATE_COMMUTATOR.md` / `geometry_state_commutator.py` are v0.1 shorthand. Prefer v0.2.

---

## Current hypothesis

The vague statement

> state changes the neuron's modes

is established territory and is not the target.

Current candidate:

> **Local history makes the neuron's incremental operator vary in time, and morphology determines whether the resulting chronological transformations remain distinguishable at a chosen receiver.**

For a nonlinear trajectory,

```text
d(delta x)/dt = A(t) delta x + B(t) delta u
delta y        = C_R(t) delta x
```

with

```text
H_R(t,s) = C_R(t) Phi(t,s) B(s)
Phi      = Texp integral A(t) dt.
```

First chronology-erased Magnus surrogate:

```text
Phi_1 = exp(integral A(t) dt).
```

Second Magnus term:

```text
Omega_2 = 1/2 integral dt1 integral^t1 dt2 [A(t1),A(t2)].
```

This is standard mathematics. Comparing `Phi` and `Phi_1` on a fixed baseline trajectory measures **incremental chronological sensitivity**, not yet causal task computation.

---

## First exact null: voltage-only morphology × changing local state

Begin with

```text
C dv/dt = -(G_ax + G_m(t)) v.
```

After capacitance normalization `z=C^(1/2)v`:

```text
dz/dt = -(L + D(t)) z
L      = C^(-1/2) G_ax C^(-1/2)
D(t)   = diag(G_m,i(t)/C_i).
```

For two states:

```text
[A_a,A_b] = [L,D_b-D_a]
[A_a,A_b]_ij = L_ij (Delta d_j - Delta d_i).
```

For reciprocal axial coupling:

```text
||[A_a,A_b]||_F^2
 = 2 sum_edges [g_ij^2/(C_i C_j)]
   [Delta(G_m,j/C_j)-Delta(G_m,i/C_i)]^2.
```

So the lowest-order voltage-only chronology source is exactly an **edge-weighted spatial roughness of change in incremental membrane rate**.

It is not raw channel amount and not a raw gating variable.

Harsh controls:

```text
real state field
random site shuffle
branch-preserving shuffle
path-distance-bin shuffle
smoothed same mean/variance field
uniform same mean field
```

The path-bin control is mandatory where known proximal-distal channel gradients exist.

---

## New exact full-state decomposition

For a conventional compartmental model with fixed axial coupling and local membrane/gating/synaptic mechanisms, split the trajectory Jacobian as

```text
A(t) = S + Q(t)
```

where

```text
S       fixed spatial / axial morphology operator
Q(t)    local state-dependent dynamics
```

and, when mechanisms are local,

```text
Q(t) = blockdiag(Q_1(t),...,Q_N(t)).
```

Then for two times `a,b`:

```text
[A_a,A_b]
 = [S,Q_b-Q_a] + [Q_a,Q_b].
```

This is exact algebra.

Interpretation:

```text
[S,Q_b-Q_a]     morphology × changing-local-state chronology
[Q_a,Q_b]       intrinsic local chronology that could exist in a point neuron
```

This matters enormously for the V23 claim. A neuron can have strong chronological/noncommuting dynamics entirely because its local channel system is stateful; morphology may contribute nothing special. We must separate the two.

At second Magnus order the split remains exact:

```text
Omega_2 = Omega_2^geom + Omega_2^local.
```

`chronology_decompose.py` implements the pairwise decomposition and identity check. Raw matrix norms remain coordinate dependent; final interpretation must use physical source/receiver projections.

This decomposition is standard operator algebra / reaction-diffusion territory, not a novelty claim. Descombes et al. (SIAM J. Numer. Anal. 2014) is one guardrail showing Lie/commutator analysis of reaction–diffusion operator splitting is established mathematics.

---

## Locality guardrail

The voltage-only first commutator is edge-local. Additional nested commutators/products can extend support only through additional cable factors.

Established graph heat-kernel theory (Keller et al. 2016) shows that short-time transfer between graph vertices at combinatorial distance `r` begins at order roughly `t^r`.

For the stripped two-state order contrast, an order-sensitive source-to-receiver term at graph distance `r` heuristically needs

```text
r cable moves + one state-difference insertion
```

and therefore first appears around `t^(r+1)`.

**Do not call this a light cone.** Compartment graph distance is discretization dependent and the continuum passive cable remains diffusive. The useful statement is only that sparse morphology imposes an algebraic hierarchy on short-time compositions.

---

## Park 2025 = known-answer calibration organism

Park et al. (Nature Communications 2025) provide a particularly clean history-dependent CA1 phenomenon:

```text
A-type Kv inactivation opens distal dSpike propagation
slow NaV inactivation closes it
```

Their detailed NEURON model reproduces failure -> dSpike -> dSpike -> failure and period-doubling. In the pure-optogenetic model, VGCC and NMDAR conductances are intentionally omitted, making this a clean active-channel history calibration before NMDA.

The Methods say the detailed model adapts ModelDB 116084 (Jarsky et al. 2005) and adds slow NaV inactivation plus changed spatial NaV/A-type Kv distributions. The Fig. 4 caption instead labels the morphology ModelDB 64167. These are related CA1 model lineages, but the article is internally inconsistent on the accession label. Do not guess; inspect Supplementary Software 1.

Supplementary Software 1 is publicly listed by the paper. Binary retrieval from the current tool session has failed, and the GitHub mirror of ModelDB 116084 stores its baseline as a binary legacy ZIP. **Park has not yet been run here.**

---

## Cheap gate before a full Jacobian

Official NEURON `Impedance.compute(freq,1)` performs an extended linearization at the current model state, including supported differential gating-state contributions.

Once the Park code is runnable:

```text
P0 reproduce the published phenotype exactly

I0 save snapshots:
   first bAP failure
   opening of dSpike window
   successful dSpike regime
   closing of window
   late failure

I1 extended transfer impedance vs frequency:
   soma -> distal
   soma -> soma
   selected dendrite -> soma
   selected dendrite -> distal

I2 freeze A-type Kv history; repeat
I3 freeze slow NaV history; repeat

I4 compare:
   voltage-only edge null
   full extended gating-state impedance
```

If known history dependence creates no meaningful source->receiver operator change, stop before giant Jacobians.

If it survives, then obtain short-window `A(t)`, direct `Phi`, `Omega_1`, `Omega_2`, and split `Omega_2^geom` from `Omega_2^local`.

---

## Stronger falsifier introduced by the full-state split

The central question is no longer merely

```text
is chronology present?
```

but

```text
is the chronology morphology-dependent?
```

A clean failure would be:

```text
Park phenotype present
chronological sensitivity present
Omega_2^local large
Omega_2^geom negligible at the distal receiver
```

Then the neuron is stateful, but V23 has not earned a geometry × history mechanism.

A more interesting result would require all of:

```text
known history gates -> geometry/history term changes
geometry/history term -> receiver-visible transfer changes
address/path-matched shuffles -> destroy or alter the term
same total conductance/activity -> cannot explain result
finite-amplitude phenotype -> covaries causally
```

---

## 2026 experimental constraints / motivation

Wong-Campos, Park et al. (Nature Neuroscience 2026) report broadly correlated membrane voltage across L2/3 cortical dendritic arbors, with only weak branch-level electrical compartmentalization, while distal bAP propagation remains strongly history-dependent.

So avoid a story requiring thousands of electrically independent mini-computers. A more defensible target is **history-conditioned accessibility/routing of relatively shared electrical events**.

Maristany de Las Casas et al. (Science 2026) provide a separate behavioral anchor: suppressing apical tuft dendritic calcium signaling in ALM impaired relearning in a rule-switching task without abolishing already learned behavior, and excitatory tuft inputs showed rule-dependent clustering. This does not support the commutator metric specifically, but it strengthens the reason to ask how spatially organized dendritic state participates in flexible computation.

---

## Modes are now explanatory, not primitive

If the mechanism survives, selected states can still be described by

```text
lambda_n(t)  pole drift
v_n(t)       mode rotation
R_n(t)       source/receiver residue or accessibility
```

but do not begin by clustering modes.

Current primitive chain:

```text
local history
 -> changing local dynamical blocks Q_i(t)
 -> local chronology + morphology/history chronology
 -> propagation through sparse morphology
 -> receiver-visible consequence
 -> finite-amplitude behavior/task consequence
```

The strongest effect may be changing accessibility/residue with modest eigenvalue movement.

---

## Only after Park: TwinProp / Aizenbud

TwinProp already reports harder tasks with richer dendritic voltage activity and stronger NMDA recruitment. V23 must not rename their voltage-PCA observation.

Later question:

> **Does receiver-visible morphology × history chronology add predictive information beyond NMDA current, voltage PCA rank, voltage variance, recruited-compartment count, synapse count and firing rate?**

If no, kill the computational bridge.

---

## Current kill question

> **In a known history-dependent dendritic computation, does the receiver-visible chronology contain a specifically morphology × changing-local-state component, rather than merely local channel-state chronology, and does that component survive controls for total activity, ordinary channel gradients, and static impedance?**

If Park says no, stop this branch before TwinProp.
