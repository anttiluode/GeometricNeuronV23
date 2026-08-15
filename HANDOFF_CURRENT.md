# GeometricNeuronV23 — CURRENT HANDOFF

**Updated:** 2026-08-15, fourth pass — **Park code now executed**

**Status:** active falsification program. Nothing here is a novelty claim.

## Read in this order

1. `PARK_P0_EXECUTION_RECEIPT.md` — **actual published supplement execution and receiver census. Start here.**
2. `HANDOFF_NONCOMMUTING_DENDRITES.md` — literature collision and original Park calibration ladder.
3. `GEOMETRY_STATE_COMMUTATOR_V02.md` — capacitance-normalized voltage-only null.
4. `FULL_STATE_GEOMETRY_HISTORY_DECOMPOSITION.md` — local-vs-morphology chronology split.
5. `CHRONOLOGY_LOCALITY.md` — graph-distance / short-time support guardrail.
6. `chronology_probe.py`, `chronology_decompose.py`, `geometry_state_commutator_v02.py` — analysis utilities.
7. `OPERATOR_ATLAS_HYPOTHESIS.md`, `SPACETIME_SEPARABILITY_GATE.md` — upstream lineage.

The original `GEOMETRY_STATE_COMMUTATOR.md` / `geometry_state_commutator.py` are v0.1 shorthand. Prefer v0.2.

---

## Current hypothesis

The vague statement

> state changes the neuron's modes

is established territory and is not the target.

Current candidate:

> **Local history makes the neuron's incremental operator vary in time, and morphology determines whether the resulting chronological transformations remain distinguishable at a chosen receiver.**

For a detailed trajectory:

```text
d(delta x)/dt = A(t) delta x + B(t) delta u
delta y        = C_R(t) delta x
H_R(t,s)       = C_R(t) Phi(t,s) B(s)
```

with

```text
Phi = Texp integral A(t) dt.
```

Compare against the chronology-erased first-Magnus surrogate

```text
Phi_1 = exp(integral A(t) dt).
```

This diagnoses incremental chronological sensitivity around the same nonlinear trajectory. It is not by itself a causal removal of computation.

---

## Exact decomposition that the hypothesis must survive

For a conventional compartmental model with fixed axial coupling and local channel/synaptic dynamics,

```text
A(t) = S + Q(t)
```

and exactly

```text
[A_a,A_b]
 = [S,Q_b-Q_a] + [Q_a,Q_b].
```

Bookkeeping interpretation:

```text
[S,Q_b-Q_a]     morphology × changing-local-state chronology
[Q_a,Q_b]       intrinsic local chronology possible in a point neuron
```

At second Magnus order the pairwise chronological term separates correspondingly into

```text
Omega_2^geom + Omega_2^local.
```

A neuron can therefore be strongly history dependent while geometry contributes little. That is the principal falsifier.

The simplest capacitance-normalized voltage-only case reduces to

```text
[A_a,A_b]_ij = L_ij (Delta d_j - Delta d_i)
```

so the first morphology/history source is an edge-weighted roughness of the **change in local incremental membrane rate**, not raw channel amount.

---

# PARK 2025 EXECUTION STATUS

## The previous blocker is gone

The exact public **Supplementary Software 1** from Park et al. (Nature Communications 2025) has now been fetched, compiled, and run in GitHub Actions under Python 3.10 + NEURON 8.2.2.

Execution/provenance is frozen in:

```text
PARK_P0_EXECUTION_RECEIPT.md
```

Main successful runs:

```text
supplement fetch/inspect   31872229100
phenotype reproduction    31872543670
500-um receiver census    31872658435
```

The exact package had minor reproducibility rough edges (unused non-ASCII `cheriff.mod`, constructor/helper drift, duplicate auto-loading trap). They were handled without editing active channel equations; details are in the receipt.

---

## Important P0 result: receiver choice matters substantially

The paper describes distal spike classification at a compartment around 500 um from the soma. In this branched morphology that does not identify a unique receiver.

A post-hoc chosen receiver is unacceptable, so the audit recorded **every non-axonal segment from 450–550 um**.

### Released run 3 — soma step

Five somatic spikes.

At 490–510 um (`n=13`):

```text
FFFFF   5
SSSSS   7
SSSSF   1
```

At 450–550 um (`n=62`):

```text
FFFFF   22
SSSSS   33
FSSFF    4
SSSSF    3
```

So the exact released model **does contain the qualitative failure -> success -> success -> failure motif**, but only on a subset of branches in the broad ~500-um shell under this released run.

Do **not** select one of those FSSFF branches after seeing the outcome and call it the canonical paper receiver.

### Released run 12 — widefield step

Thirteen somatic spikes.

At 490–510 um the exact initial prefix varies, but every recorded branch enters a strong alternating success/failure regime. Across 450–550 um, the two largest classes were:

```text
SSSFSFSFSFSFS   31 / 62
SFSFSFSFSFSFS   13 / 62
```

The **period-doubled / alternating propagation regime is therefore a cleaner receiver-robust known-answer calibration** than the exact initial FSS prefix.

This is a methodological result about how to run the next gate, not a discovery claim.

---

## Predeclared follow-up found in the authors' own stored scan

The released file

```text
Model Robustness/Figures/Figure_S19c-e/Plot_Phase_Diagrams.m
```

contains the authors' stored parameter-scan outcomes.

Before running any V23 follow-up, one table point was predeclared because the authors already label it `FSSFFF`:

```text
NaV soma        0.05 S/cm2
NaV dendrite    0.048 S/cm2
stimmax         7e-4
Nav_inactivation [1, 0.5, 300, 100]
Kad             [-0.2, 0.3, 0, 150]
expected stored table code 011000 = FSSFFF
```

This is not parameter tuning by V23; it is a reproduction of a pre-existing published-supplement table coordinate.

That run is next.

---

# NEXT EXECUTION — NO NEW THEORY FIRST

## P0b — reproduce the predeclared stored FSSFFF parameter point

Run the authors' stored scan coordinate above and again census a fixed receiver shell rather than selecting a favorable branch.

Purpose:

```text
- verify the stored phase-diagram receipt against the released executable model
- obtain a cleaner opening/closing trajectory if possible
- determine how much of FSSFFF is branch-specific
```

## I0 — state-conditioned transfer gate

The first chronology instrument is **not** the giant Jacobian.

Use NEURON's extended state-dependent impedance calculation on the already running detailed model.

Freeze receiver policy before seeing impedance:

```text
A. soma
B. authors-helper longest-path receiver near 500 um
C. fixed 490–510 um receiver ensemble
```

Use matched inter-spike states away from the spike singularity, comparing states preceding distal success versus failure.

Measure source->receiver transfer over a modest frequency grid, separating gain, phase/delay, and normalized shape.

If the known history-dependent phenotype produces essentially no meaningful state-conditioned transfer change, stop before building a giant `A(t)`.

## I1 — causal channel-history controls

Only if I0 survives:

```text
slow NaV history control
A-type Kv control
```

Use interventions grounded in the released mechanisms / Park experiments and verify that the operating regime remains interpretable. Do not repeat the older mistake of calling a dead intervention a mechanism test.

## I2 — chronology decomposition

Only after P0/I0/I1:

```text
short-window A(t)
direct Phi
Omega_1
Omega_2
Omega_2^geom vs Omega_2^local
physical B/C source-receiver projections
```

Primary kill condition:

```text
known history phenotype present
chronological sensitivity present
Omega_2^local large
receiver-visible Omega_2^geom negligible
```

=> neuron is stateful, but the GeometricNeuron morphology × history mechanism loses here.

---

# JOINT OPTIMIZATION BRANCH — DEFERRED AND NARROWED

Gemini's suggested later discovery harness is directionally sensible, but a new prior-art collision narrows it.

Torben-Nielsen & Stiefel (2009), *Systematic mapping between dendritic function and structure*, already used a genetic algorithm to optimize realistic dendritic morphology / channel distributions for temporal input-order detection.

Therefore V23 cannot claim as new:

```text
optimize morphology or spatial ion-channel allocation for a sequence task
```

The still-unclosed candidate seam is narrower:

```text
fixed realistic morphology
    x trainable synaptic address
    x trainable full presynaptic STP dynamics (U, tau_D, tau_F)
```

with strict learned-parameter-multiset shuffles and transfer-kernel analysis.

Before building that harness, collide this exact seam harder with literature. Do not spend 500 optimizer restarts on a novelty premise that has not survived search.

The earlier passive rearrangement lemma remains a **linear null**, not a lead: morphology-induced passive delays are small relative to ordinary STP time constants, so a large learned address effect would need to beat that trivial explanation.

---

## Current reality constraints

- Park 2025 gives a known active-channel history mechanism suitable for calibration.
- Wong-Campos/Park et al. 2026 argue against a story requiring thousands of electrically independent branch mini-computers; dendritic voltage is broadly correlated while propagation remains history dependent.
- TwinProp already reports richer dendritic voltage activity / NMDA recruitment with harder optimized tasks; V23 must add mechanism, not rename PCA rank.
- Poleg-Polsky 2026 remains the methodological model if/when we reach discovery search: constrained biology, many solutions, clustering, literature collision, then ablation.

---

## Current kill question

> **In an actually reproduced history-dependent dendritic phenomenon, does the receiver-visible chronology contain a specifically morphology × changing-local-state component, rather than merely local channel-state chronology, and does that component survive predeclared receiver controls?**

The next commit should answer with data, not another derivation.
