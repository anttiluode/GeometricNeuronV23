# Geometry × local state commutator — an exact cheap null

**Status:** derivation / mechanistic null. **Not a novelty claim.**

This is the cleanest mathematical residue of the current noncommuting-dendrite dig.

The point is not that commutators are new. They are standard in time-dependent linear systems, Magnus expansions, Lie/Strang splitting, and reaction–diffusion analysis. The useful part here is that the simplest dendritic linearization gives an **exact edge-local expression** for when morphology and a changing local conductance field can fail to commute.

---

## 1. Simplest voltage-only local linearization

Ignore gating-state dynamics for one moment and approximate the incremental voltage dynamics by

```text
dv/dt = A(t) v
```

with

```text
A(t) = -( L + D(t) ).
```

Here:

```text
L       fixed cable / axial-coupling / morphology operator
D(t)    diagonal field of local incremental membrane conductances
```

`L` may include the fixed leak if desired; any component proportional to identity is irrelevant to the commutator.

Take two operating states `a,b`:

```text
A_a = -(L + D_a)
A_b = -(L + D_b).
```

Since diagonal matrices commute with one another,

```text
[A_a, A_b]
    = [L, D_b - D_a].
```

Let

```text
Delta D = D_b - D_a = diag(Delta d_1, ..., Delta d_N).
```

Then exactly

```text
[A_a,A_b]_{ij}
    = L_{ij} (Delta d_j - Delta d_i).
```

This identity needs no neuroscience assumptions beyond the stated linearization.

---

## 2. Interpretation

The lowest-order chronology term needs **both**:

```text
spatial coupling
AND
spatially nonuniform state change.
```

If the membrane state changes everywhere by the same scalar amount,

```text
Delta D = alpha I,
```

then

```text
[A_a,A_b] = 0.
```

If sites do not couple, the commutator also vanishes.

Therefore, in this stripped-down model:

> **Chronological noncommutation is created where a changing local conductance field has a spatial gradient across the morphology's coupling edges.**

This is much more precise than “state deforms modes.”

---

## 3. Exact graph-edge formula

For an undirected graph Laplacian with off-diagonal entries

```text
L_ij = -g_ij
```

on coupled edges, the Frobenius norm is

```text
|| [A_a,A_b] ||_F^2
    = 2 sum_{(i,j) in undirected edges}
        g_ij^2 (Delta d_i - Delta d_j)^2.
```

So the raw commutator magnitude is an edge-weighted spatial roughness / Dirichlet-like energy of the **change** in local membrane state.

Important distinction:

```text
large state value
    !=
large chronology term
```

A huge but spatially uniform conductance change can commute with the fixed cable operator.

Conversely, a smaller but sharply localized state change at a strongly coupled edge can contribute strongly.

This immediately supplies controls against the trivial explanation “more NMDA / more channel current = larger metric.”

---

## 4. Continuous-cable analogue

For the schematic one-dimensional operator

```text
A(t) = D_cable * d2/dx2 - q(x,t),
```

where `q` acts by multiplication, the relevant commutator contains

```text
[d2/dx2, q] f
    = q'' f + 2 q' f'.
```

Thus the same message survives continuously: diffusion/cable propagation commutes with a spatially uniform local reaction/conductance field, but not generally with a spatially varying one.

This is standard reaction–diffusion / operator-splitting mathematics. V23 must not claim it as new.

Relevant mathematical guardrails include the broad Magnus literature and operator-splitting analyses of reaction–diffusion systems, where commutators control chronological/splitting corrections.

---

## 5. Biological translation

For Park et al. 2025, two explicitly history-bearing local fields are attractive first candidates:

```text
A-type Kv availability / inactivation
slow NaV availability / inactivation
```

Their model gives both spatial gradients in channel properties and time-varying channel reserve during the bAP-filtering sequence.

The simple null predicts that the raw chronology source should not merely track

```text
mean Kv reserve
mean NaV reserve
```

but should track **where those reserves change relative to axial coupling**.

A first cheap summary is therefore:

```text
G_state(t_a,t_b)
    = 2 sum_edges g_ij^2
        (Delta d_i - Delta d_j)^2.
```

This is only an internal source term. It still owes the receiver gate.

---

## 6. Receiver gate

A large full-state commutator is not enough.

For source directions `P` and receiver `C_R`, the actual object remains something like

```text
C_R [A_a,A_b] P
```

for the local pairwise approximation, or the full chronological propagator difference

```text
C_R (Phi - Phi_order_erased) P
```

for a finite window.

Thus there are two separable questions:

```text
1. Does geometry × state heterogeneity generate noncommutation internally?
2. Can the chosen biological source and receiver see it?
```

That second question is where morphology can make the same local-state multiset computationally different.

---

## 7. Strong shuffle control falls out automatically

At a fixed pair of times, preserve exactly the multiset

```text
{Delta d_i}
```

but permute it over dendritic sites.

The mean, variance and histogram of state change are unchanged.

What changes is

```text
sum_edges g_ij^2 (Delta d_i - Delta d_j)^2.
```

Therefore a **state-field shuffle over fixed morphology** is an exact matched control for the geometry–state coupling term in this simplified model.

This is stronger than comparing “more vs less active channels.”

Candidate controls:

```text
real state field
random site shuffle
branch-preserving shuffle
path-distance-bin shuffle
spatially smoothed field with same mean/variance
spatially uniform field with same mean
```

The branch/path-bin shuffles are essential if ordinary proximal-distal channel gradients explain everything.

---

## 8. A very sharp prediction

Suppose two neurons have similar total channel-state variance but different morphology, or the same morphology receives two state fields with identical histograms.

Then the simple model predicts that chronological sensitivity should be ordered by the **edge alignment** between morphology and the state-change field, not by state variance alone.

If receiver-visible chronology is entirely predicted by:

```text
mean conductance
state variance
raw distance from soma
```

with no added value from the edge-weighted state gradient, this geometry-state version has contributed little.

---

## 9. What breaks the simple formula

Real detailed neurons add:

```text
gating-state dimensions
voltage <-> gating cross-derivatives
multiple channel species
capacitance / generalized mass matrix
nonuniform compartment areas
synaptic states
NMDA voltage dependence
ion concentrations
spikes / strongly nonlinear excursions
```

Then `D(t)` is no longer the whole story and the Jacobian is block structured.

That is fine. The formula is valuable precisely as the **lowest-order null**:

> How much of the measured chronology is already explained by fixed cable coupling interacting with a changing diagonal local conductance field?

Anything more elaborate has to beat that baseline.

---

## 10. Relation to the old “modes” thought

Because the instantaneous operator is

```text
A(t) = -(L + D(t)),
```

the modes of `A(t)` can rotate as `D(t)` changes.

But the commutator identity says something more primitive than following eigenvectors:

```text
mode deformation is expected wherever
fixed spatial coupling and local state field do not commute.
```

So do not begin by clustering eigenmodes.

Begin with the edge-local source of noncommutation, then ask what survives at the receiver. Modal analysis is explanatory afterward.

---

## 11. Current falsifiable chain

```text
local history
    -> spatially nonuniform conductance-state change
    -> [L, Delta D] != 0
    -> chronological perturbation transfer differs from order-erased transfer
    -> receiver can distinguish the difference
    -> finite-amplitude output / task performance depends on it
```

Every arrow can fail.

That is good.

---

## References / guardrails

- Magnus W. (1954), *On the exponential solution of differential equations for a linear operator*, Communications on Pure and Applied Mathematics 7:649–673. DOI: https://doi.org/10.1002/cpa.3160070404
- Blanes S, Casas F, Oteo JA, Ros J. (2009), *The Magnus expansion and some of its applications*, Physics Reports 470:151–238. DOI: https://doi.org/10.1016/j.physrep.2008.11.001
- Descombes S et al. (2014), *Analysis of operator splitting in the nonasymptotic regime for nonlinear reaction-diffusion equations*, SIAM Journal on Numerical Analysis 52. DOI: https://doi.org/10.1137/130926006
- Park P et al. (2025), *Dendritic excitations govern back-propagation via a spike-rate accelerometer*, Nature Communications 16:1333. DOI: https://doi.org/10.1038/s41467-025-55819-9

## Current one-line residue

> **In the simplest cable-plus-local-state model, morphology and history fail to commute exactly where history changes differently across coupled locations.**

The discovery question is not this identity; it is whether that edge-local quantity predicts receiver-visible dendritic computation in realistic neurons better than ordinary conductance load, distance, or activity measures.
