# GeometricNeuronV23 — CURRENT HANDOFF

**Updated:** 2026-08-15, second pass

**Status:** active falsification program. Nothing here is a novelty claim.

## Read in this order

1. `HANDOFF_NONCOMMUTING_DENDRITES.md` — full literature collision and Park calibration ladder.
2. `GEOMETRY_STATE_COMMUTATOR_V02.md` — corrected capacitance-normalized cheap null.
3. `CHRONOLOGY_LOCALITY.md` — graph-distance / short-time support guardrail.
4. `chronology_probe.py` — generic time-ordered Jacobian vs first/second Magnus diagnostic.
5. `geometry_state_commutator.py` — exact toy voltage-only edge commutator probe; its input `L,d` must be interpreted as **rate-normalized** quantities per v0.2.
6. `OPERATOR_ATLAS_HYPOTHESIS.md` and `SPACETIME_SEPARABILITY_GATE.md` — upstream lineage.

The original `GEOMETRY_STATE_COMMUTATOR.md` used shorthand that could be read as raw physical conductance. **Use v0.2 instead.**

---

## Current hypothesis

The vague idea

> state changes the neuron's modes

is established territory and is not the target.

Current candidate:

> **Local history makes the neuron's incremental operator vary in time, and morphology determines whether the resulting chronological transformations remain distinguishable at a chosen receiver.**

Use the local variational system along an **actual nonlinear trajectory**:

```text
d(delta x)/dt = A(t) delta x + B(t) delta u
A(t) = dF/dx | x(t),u(t)
delta y = C_R(t) delta x
```

with physical source-to-receiver kernel

```text
H_R(t,s) = C_R(t) Phi(t,s) B(s).
```

Chronological propagator:

```text
Phi = Texp integral A(t) dt.
```

Order-erased first-Magnus surrogate:

```text
Phi_1 = exp(integral A(t) dt).
```

The first missing term is

```text
Omega_2 = 1/2 integral dt1 integral^t1 dt2 [A(t1),A(t2)].
```

This is standard Magnus mathematics.

Important: comparing `Phi` with `Phi_1` along a fixed nonlinear trajectory diagnoses **incremental chronological sensitivity**. It is not yet a causal statement that nonlinear computation has been removed.

---

## New exact cheap null

Start from a voltage-only compartmental linearization

```text
C dv/dt = -(G_ax + G_m(t)) v.
```

In capacitance-normalized coordinates `z=C^(1/2)v`,

```text
dz/dt = -(L + D(t)) z
L    = C^(-1/2) G_ax C^(-1/2)
D(t) = diag(G_m,i(t)/C_i).
```

For two states:

```text
[A_a,A_b] = [L, D_b-D_a]
```

and exactly

```text
[A_a,A_b]_ij
 = L_ij (Delta d_j - Delta d_i).
```

For reciprocal axial coupling,

```text
||[A_a,A_b]||_F^2
 = 2 sum_edges
   [g_ij^2/(C_i C_j)]
   [Delta(G_m,j/C_j)-Delta(G_m,i/C_i)]^2.
```

So the lowest-order voltage-only chronology source is an edge-weighted spatial roughness of **change in incremental membrane rate**, not raw channel amount and not a raw gate variable.

This creates very strong matched controls:

```text
real state field
random site shuffle
branch-preserving shuffle
path-distance-bin shuffle
smoothed same mean/variance field
uniform same mean field
```

The path-bin control is mandatory because Park deliberately has proximal-distal channel gradients.

---

## New locality guardrail

The first commutator above is edge-local. Higher nested commutators/products can spread support only through additional cable factors.

Established graph heat-kernel theory already shows that short-time propagation between graph vertices at combinatorial distance `r` begins at order roughly `t^r`.

For the stripped two-state order contrast, a source-receiver effect at distance `r` needs roughly

```text
r cable moves + one state-difference insertion,
```

so the earliest possible short-time order is heuristically `t^(r+1)`.

Do **not** turn this into a physical light cone. Compartment graph distance depends on discretization; the continuum passive cable remains diffusive with immediate tails. The useful message is only that sparse morphology imposes an algebraic hierarchy on short-time compositions.

---

## Park 2025 = known-answer calibration organism

Park et al., Nature Communications 2025, give an experimentally constrained CA1 phenomenon:

```text
A-type Kv inactivation opens distal dSpike propagation
slow NaV inactivation closes it
```

with a detailed NEURON model that reproduces the failure -> dSpike -> dSpike -> failure motif and period doubling.

The Methods explicitly say the model adapts **ModelDB 116084** (Jarsky et al. 2005) and adds slow NaV inactivation plus new spatial channel distributions. The Fig. 4 caption, however, says the morphology is from **ModelDB 64167**. These are related CA1 model lineages, but the paper is internally inconsistent on the accession label. Do not resolve this by guessing; inspect Supplementary Software 1 when available.

The published Supplementary Software 1 ZIP exists both at Nature and PMC, but binary retrieval from the present tool session has failed. The public GitHub mirror of ModelDB 116084 was located, but its legacy model is packaged as a binary `Gating.zip`, which the connector cannot decode. **We have not run Park yet.**

---

## Fast gate before a full Jacobian

Official NEURON `Impedance.compute(freq, 1)` performs an extended linearization at the **current neuron state**, including membrane voltage and supported differential gating-state contributions (`di/dv`, `di/ds`, `ds'/dv`, `ds'/ds`). It has documented limitations, so it is a diagnostic, not oracle.

Once Park code is runnable:

```text
P0 reproduce published phenotype exactly

I0 save states at:
   first bAP failure
   opening of dSpike window
   successful dSpike regime
   closing of window
   late failure

I1 at each snapshot compute extended transfer impedance over frequencies:
   soma -> distal dendrite
   soma -> soma
   selected dendrite -> soma
   selected dendrite -> distal dendrite

I2 freeze A-type Kv history; repeat
I3 freeze slow NaV history; repeat
```

If the known history window produces no meaningful state-conditioned source->receiver transfer change away from singular spike moments, stop before building giant Jacobians.

If it does, continue with short-window `A(t)`, direct `Phi`, `Omega_1`, `Omega_2`, physical B/C projections, and finite-amplitude AB/BA tests.

---

## Reality constraint from 2026 in vivo work

Wong-Campos, Park et al. (Nature Neuroscience 2026) report broadly correlated L2/3 dendritic membrane voltage across the arbor with only weak branch-level compartmentalization, while distal bAP propagation remains strongly history-dependent.

Therefore avoid a story requiring thousands of independent branch computers. A more plausible target is **history-conditioned accessibility/routing of relatively shared electrical events**.

---

## Modal analysis is secondary

If the mechanism survives, selected snapshots can still be described by

```text
lambda_n(t)  pole drift
v_n(t)       mode rotation
R_n(t)       source/receiver residue or accessibility
```

but do not begin by clustering modes. The current primitive chain is

```text
local history
 -> spatially nonuniform incremental state field
 -> local edge noncommutation sources
 -> propagation through morphology
 -> receiver-visible chronological effect
 -> finite-amplitude behavior / task consequence
```

A mode may hardly move in eigenvalue yet become much more or less reachable/observable.

---

## Independent input/output bridge

Pair state-space analysis with a finite-amplitude sequence test and, if useful, MIMO Volterra identification:

```text
A then B
B then A
```

after subtracting the fixed linear source/location kernel prediction.

Volterra first/second-order kernels are established neuroscience tools. A second-order term is not automatically a commutator. The useful question is whether measured order-specific nonlinear interaction covaries with the mechanistic chronology diagnostic.

---

## Only after Park: TwinProp

TwinProp already reports harder tasks with richer dendritic voltage activity and stronger NMDA recruitment. V23 must not rename that result.

Later test:

> Does receiver-visible chronological sensitivity add predictive information beyond mean NMDA current, voltage PCA rank, voltage variance, recruited compartment count, synapse count and firing rate?

If no, kill the bridge.

---

## Current kill question

> **Does a known dendritic history mechanism create receiver-visible chronological sensitivity that disappears when the known history-bearing gates are frozen, and is that sensitivity better predicted by morphology × state-field alignment than by total conductance or activity alone?**

If Park says no, stop this branch before TwinProp.
