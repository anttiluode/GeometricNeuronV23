# Park 2025 — executed two-compartment minimal control

**Date:** 2026-08-15  
**Status:** executed author-released coarse control + two V23 ablations. **Not a novelty claim.**

## Why this control matters

The detailed Park model now shows a strong distal-specific state-conditioned transfer change after source normalization (`PARK_I1_NORMALIZED_RECEIPT.md`).

Before crediting detailed dendritic morphology, the paper's own coarse model must be confronted. Park et al. state that a two-compartment Izhikevich-type model captures both opening/closing of the dSpike window and period-doubling under simultaneous soma+dendrite drive.

Supplementary Software 2 was therefore fetched and executed directly rather than treated only as a citation.

Workflow:

```text
.github/workflows/park-izhikevich-control.yml
GitHub Actions run 31873174996
job 94984791773
```

The exact released ZIP contained:

```text
Readme_Izhikevich.pdf
Readme_Izhikevich.docx
Two_compartment_Izhikevich.m
```

The MATLAB update equations were translated literally to Python at the released timestep (`dt=0.001`) for an auditable headless run.

---

## What the authors say the model is

The released README describes:

```text
soma compartment
+ dendrite compartment
+ independent optogenetic conductances
+ coupling between compartments
```

and explicitly states that adaptation/recovery parameters `a`, `b`, and `d` apply to the **dendrite only; soma has no adaptation**.

Released defaults:

```text
a = 0.0025
b = 0.01
c = -55      dendrite reset
cSoma = -65  soma reset
d = 1        dendrite only
vmax = 0     dendrite spike threshold
rho = 1
Coupling = 0.325
```

The README gives two named conductance examples:

```text
Conductance = 0.16, ConductanceDendrites = 0.0
    -> F S S S S F F F

Conductance = 0.3, ConductanceDendrites = 0.05
    -> alternating success-failure motif
```

The paper makes the same qualitative claim: this coarse two-compartment model captures the spike-rate-accelerometer window and period-doubling.

---

# Exact released default execution

Released default drive:

```text
soma conductance      0.16
dendrite conductance  0.0
coupling               0.325
```

During the driven interval, the literal translation produced:

```text
46 somatic spikes
4 dendritic spikes
```

Dendritic spike times (native model time units):

```text
108.740
113.266
116.406
120.030
```

while somatic spiking continued until approximately:

```text
395.892
```

Thus the executed model shows the essential coarse phenomenon without any tree:

> **dendritic events occur only in an early transient window and then disappear despite continued somatic spiking.**

Our automated one-to-one event-pairing heuristic does not reproduce the README's exact printed `FSSSSFFF` label because soma and dendrite threshold crossings can occur with small relative lead/lag and the released MATLAB file does not include a discrete pairing/classification routine. Raw event times are therefore the primary receipt; we do not retune the pairing rule to force the README label.

---

# Other conductance pairs explicitly suggested by the authors

These were exhausted because they are listed in the released code/README, not selected adaptively.

```text
g_soma 0.16, g_dend 0.05 -> 54 soma spikes, 7 dendrite spikes
g_soma 0.30, g_dend 0.00 -> 109 soma spikes, 4 dendrite spikes
g_soma 0.30, g_dend 0.05 -> 112 soma spikes, 8 dendrite spikes
```

For the authors' named `0.30 / 0.05` alternating condition, the dendritic events again occupy the early stimulated interval while soma spiking is much more sustained. The paper/README's qualitative period-doubling interpretation is therefore the appropriate author-level label; V23 does not invent a different event-matching rule after seeing the traces.

---

# V23 ablation 1 — remove dynamic dendritic recovery

This is **not** an authors' condition.

For the released default, V23 froze the dendritic recovery variable `u2` and also suppressed its post-dendritic-spike increment, leaving the rest of the simple model unchanged.

Result:

```text
125 soma spikes
180 dendritic spikes
```

Dendritic spiking no longer closes after a short transient; it persists densely through the run.

Interpretation:

> The minimal model's history window depends critically on its **local dendritic recovery/adaptation state**.

This is a deliberately strong ablation, not a subtle parameter perturbation. It establishes sufficiency/necessity only inside this toy model, not in CA1 biology.

---

# V23 ablation 2 — remove soma-dendrite coupling

Again, not an authors' condition.

Set:

```text
Coupling = 0
```

with released default soma drive.

Result:

```text
87 soma spikes during drive
no stimulus-related dendritic spikes
```

The only dendritic threshold events occurred during the model's initial autonomous transient before the optogenetic step.

So in the minimal model:

```text
local dendritic history alone is not enough to transmit the somatic event;
spatial coupling is required.
```

---

# What this does to the GeometricNeuron hypothesis

This is an important narrowing.

The qualitative Park phenotype requires **neither a detailed dendritic tree nor many branch-specific modes**. The author-released coarse system already implements the essential logic with:

```text
one soma state
one dendrite state
one coupling edge
one local dendritic recovery variable
```

The two V23 controls sharpen it further:

```text
remove local history  -> transient closing disappears
remove spatial coupling -> soma-driven dendritic events disappear
```

That is almost the smallest possible realization of:

```text
local history
+ spatial coupling
-> history-conditioned accessibility
```

Therefore a detailed-morphology claim cannot be based on the existence of the accelerometer or period-doubling phenotype.

The detailed tree now has to earn something **above this minimal two-compartment mechanism**.

---

# What the detailed model may still add

I1 gives one concrete candidate:

```text
inside a fixed 490–510 um path-distance shell,
extended state-conditioned normalized transfer ratios span
approximately 0.87x to 6.88x across 13 receivers.
```

A two-compartment model has no branch-address dimension capable of expressing that spatial heterogeneity.

So the surviving question is no longer:

> Does morphology make history-dependent propagation possible?

The coarse control says **not in that broad sense**.

It is:

> **Does detailed morphology organize a local-history mechanism into receiver-specific routing/accessibility that cannot be reduced to a single dendritic compartment or ordinary static impedance?**

That is a substantially narrower target.

---

# Mathematical caution: the coarse model is hybrid

The Izhikevich model contains threshold/reset events. Its continuous-time Jacobian between resets can be analyzed, but a full variational propagator across spikes requires hybrid-system reset/saltation terms.

Therefore do not take the smooth-flow Jacobian alone, compute a Magnus commutator across reset events, and call it the whole mechanism.

For the detailed NEURON model, the next clean test remains the state-conditioned transfer / gate-state route already underway.

---

## One-line result

> **Park's qualitative history window is already realizable by one dendritic recovery state plus one soma-dendrite coupling edge; detailed morphology is therefore not necessary for the phenomenon itself, and V23 must now explain the branch/site-specific routing heterogeneity seen in the detailed model rather than the accelerometer motif.**
