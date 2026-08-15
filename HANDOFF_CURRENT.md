# GeometricNeuronV23 — CURRENT HANDOFF

**Updated:** 2026-08-15

**Status:** active falsification program. Nothing below is a novelty claim.

Read first:

- `HANDOFF_NONCOMMUTING_DENDRITES.md` — full derivation / literature guardrails / Park calibration ladder.
- `chronology_probe.py` — generic synthetic/test implementation of chronological propagator vs order-erased first Magnus term.
- `OPERATOR_ATLAS_HYPOTHESIS.md` — upstream state-conditioned operator idea.
- `SPACETIME_SEPARABILITY_GATE.md` — passive gain+delay / receiver-separability null.

## Current hypothesis

The vague statement

> state changes the neuron's modes

is already established territory and is **not** the target.

The current sharper candidate is:

> **Local history makes the neuron's incremental operator vary in time, and morphology determines whether the resulting chronological transformations remain distinguishable at a chosen receiver.**

The first mathematical diagnostic is the variational system along an **actual nonlinear trajectory**:

```text
d(delta x)/dt = A(t) delta x
A(t) = dF/dx | x(t),u(t)
```

and its time-ordered propagator

```text
Phi = Texp integral A(t) dt.
```

Compare it with the chronology-erased first-Magnus object

```text
Phi_1 = exp(integral A(t) dt).
```

The first missing term is built from pairwise commutators:

```text
Omega_2 = 1/2 integral dt1 integral^{t1} dt2 [A(t1), A(t2)].
```

This is established mathematics (Magnus 1954), not V23 novelty.

## Correction after the first code pass

`chronology_probe.py` currently reports

```text
eta_R = || C (Phi - Phi_1) P || / || C Phi P ||
```

for source directions `P` applied at the start of a window and receiver projection `C` at the end.

That is a useful **incremental chronology diagnostic**, but two cautions are now mandatory:

### 1. It is not yet “computation disappears”

`Phi` and `Phi_1` are compared along the same already-generated nonlinear baseline trajectory. This tells us how chronology changes **small perturbation propagation around that trajectory**.

It does **not** constitute a causal replacement of the nonlinear neuron by an order-erased neuron.

A computational claim therefore still needs either:

```text
finite-amplitude biological ablations / matched surrogates
```

or an independent input-output nonlinear identification test.

### 2. Use physical source -> receiver quantities

Do not interpret an unprojected norm over all hidden state coordinates as biology. State variables have arbitrary units/scales.

Preferred object:

```text
source perturbation / current at real location(s)
    -> variational propagation
    -> voltage/current at real receiver(s)
```

In general, for

```text
d(delta x)/dt = A(t) delta x + B(t) delta u
 delta y       = C_R(t) delta x
```

the physical time-varying kernel is

```text
H_R(t,s) = C_R(t) Phi(t,s) B(s).
```

Ultimately compare the full chronological kernel with an order-erased surrogate kernel, not arbitrary state-space matrices.

## Very useful practical shortcut: NEURON already supplies the snapshot operator

Before attempting a giant full Jacobian, use NEURON's established extended impedance calculation.

At an instant of a detailed simulation:

```text
imp.compute(freq, 1)
```

linearizes the system including membrane potentials and differential gating states and returns source-to-receiver transfer impedance at the **current neuron state** (subject to documented mechanism limitations).

This gives a cheap first atlas:

```text
history / state snapshot
        -> H_R<-S(omega | state)
```

Reference: official NEURON `Impedance` documentation.

### Fast kill gate I0

On the Park detailed CA1 model, save snapshots during:

```text
first bAP failure
opening of distal dSpike window
successful dSpike regime
closing of window
later failure
```

At each snapshot use extended impedance at a modest frequency grid and compare:

```text
soma -> distal transfer
soma -> soma transfer
selected dendrite -> soma transfer
selected dendrite -> distal transfer
```

Remove / report trivial gain separately from phase and shape.

If the known history-dependent propagation window produces essentially no detectable change in the appropriate incremental transfer atlas away from the spike singularity, stop and rethink before doing full Jacobians.

If it does change strongly, then proceed to chronology.

## Why Park 2025 remains the calibration target

Park et al. (Nature Communications 2025) experimentally and computationally identify a known-answer history mechanism:

```text
A-type Kv inactivation opens distal propagation
slow NaV inactivation closes it
```

and their detailed model reproduces the failure -> dSpike -> dSpike -> failure motif and period-doubling. Their detailed simulation code is supplied as `Supplementary Software 1`.

This phenotype itself is not new. Older CA1 work already establishes activity/history-dependent bAP invasion and conditional dendritic spike propagation. The Park model is valuable because the causal gates are unusually explicit.

The Park paper adapts the Jarsky et al. CA1 model lineage (ModelDB 116084); the public ModelDB GitHub mirror is `ModelDBRepository/116084` and contains the original `Gating.zip` baseline.

## 2026 in-vivo constraint

Wong-Campos, Park et al. (Nature Neuroscience 2026) report that cortical L2/3 dendritic membrane voltage is broadly correlated across the arbor with only weak branch-level compartmentalization, while distal bAP propagation is nevertheless strongly modulated by recent spiking history.

So any V23 story requiring thousands of electrically independent branch states is suspect.

The more defensible target is **history-conditioned accessibility/routing of a relatively shared electrical event**, not arbitrary branch independence.

## Modal question, demoted but retained

At selected snapshots we may still track:

```text
lambda_n(t)       pole/eigenvalue drift
v_n(t)            mode rotation
R_n(t)            source/receiver residue/accessibility
```

The strongest biological effect may be in `R_n(t)` with modest pole motion:

> a mode/pathway need not be created; history may make it reachable or visible.

This is why transfer impedance / source-receiver kernels come before a global spectrum.

## Magnus numerical guardrail

Do not use a low-order Magnus series over arbitrarily long/stiff neuronal windows. Magnus convergence has nontrivial bounds; a standard sufficient condition involves the integrated operator norm. In practice:

```text
use short windows
check convergence by subdivision
compare Omega1 vs Omega1+Omega2 against directly integrated Phi
never infer biology from Omega2 when the approximation itself is poor
```

Reference: Blanes, Casas, Oteo & Ros (2009), *The Magnus expansion and some of its applications*, Physics Reports 470:151–238, DOI 10.1016/j.physrep.2008.11.001.

## Finite-amplitude bridge

The variational metric is local. Pair it with an actual sequence test:

```text
A then B
B then A
```

at the full nonlinear amplitude, after subtracting the fixed linear source/location kernel prediction.

Independent input-output route:

```text
MIMO Volterra first-order kernels
MIMO second-order cross-kernels
```

Ask whether the order-specific nonlinear interaction measured at the receiver covaries with the state-space chronology diagnostic.

Do **not** call a generic second-order Volterra term a commutator.

## Immediate execution order

```text
0. Get/reproduce Park Supplementary Software 1 detailed model.
   Publisher and PMC both expose the ZIP; direct binary fetch from this session
   is currently blocked, so use the published supplement or reconstruct only if
   necessary from the public ModelDB 116084 baseline + Park modifications.

1. Reproduce Park failure -> dSpike -> dSpike -> failure exactly.

2. Snapshot extended NEURON impedance with compute(freq, 1).
   This is the cheap I0 gate.

3. Freeze A-type Kv inactivation; repeat phenotype + impedance atlas.

4. Freeze slow NaV inactivation; repeat.

5. Only if I0 survives, obtain/reconstruct A(t) on short windows and run
   `chronology_probe.py` with physical source/receiver projections.

6. Validate Magnus-2 by direct Phi and window subdivision.

7. Run finite-amplitude AB/BA and Volterra bridge.

8. Only then move the same measurement into TwinProp and ask whether it adds
   predictive information beyond NMDA current, voltage PCA rank, voltage
   variance, recruited-compartment count, and firing rate.
```

## Current kill question

> **Does known dendritic history dependence produce a receiver-visible chronological contribution that disappears when the known history-bearing gates are frozen?**

If Park says **no**, this V23 branch dies before TwinProp.

If Park says **yes**, the harder discovery question becomes whether the same object scales with learned single-neuron computation rather than merely with excitability.
