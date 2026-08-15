# Park 2025 — causal history controls in the detailed model

**Date:** 2026-08-15  
**Status:** executed causal phenotype controls in the released detailed CA1 model. **Not a novelty claim.**

## Purpose

The detailed-model I0/I1 analyses showed that states preceding distal dSpike success and failure have different small-signal transfer properties. This still did not establish that the identified history-bearing ion-channel mechanisms caused the finite-amplitude success/failure pattern.

This run therefore intervened on the two Park mechanisms directly, before any full Jacobian/Magnus analysis.

Workflow:

```text
.github/workflows/park-history-causal-controls.yml
GitHub Actions run 31873317216
job 94985130689
```

Model/protocol:

```text
exact Supplementary Software 1
released run 12 — Optopatch step widefield
fixed 490–510 um receiver shell, n=13
same >=80% success / <=20% failure consensus rule as I0/I1
```

---

# Baseline

Released parameters:

```text
Nav slow-inactivation parameter bundle [1, 0.6, 300, 100]
A-type Kv unchanged
```

13 somatic spikes.

Shell consensus:

```text
S M S F S F S F S F S F M
```

or compactly:

```text
SMSFSFSFSFSFM
```

This reproduces the receiver-ensemble alternation used for I0/I1.

At 1 ms before the classified events, baseline distal slow-NaV state `s_na3` progressively declined, and the baseline A-type gate oscillated with the success/failure phase.

---

# Control 1 — remove slow NaV inactivation drive while retaining Na current

The released `na3.mod` uses dynamic state

```text
s' = (sinf - s) / taus
```

with

```text
sinf = c + ar2 * (1-c).
```

Thus setting

```text
ar2 = 1
```

makes `sinf = 1` exactly: the slow-inactivation drive is disabled without deleting the NaV current or its fast `m/h` gates.

V23 therefore changed only the released slow-inactivation bundle from

```text
[1, 0.6, 300, 100]
```

to

```text
[1, 1, 300, 100].
```

Result:

```text
13 somatic spikes
s_na3 = 1.0 throughout the recorded shell snapshots
```

Consensus sequence:

```text
S M S M S M S M S M S M S
```

There were **no consensus failure events** under the frozen >=80% / <=20% rule.

Receiver-level patterns separated into two groups:

```text
SSSSSSSSSSSSS    8 / 13 receivers
SFSFSFSFSFSFS    5 / 13 receivers
```

Interpretation:

> Removing slow NaV inactivation abolishes the baseline progression into shell-wide failure states, while leaving somatic spiking and an alternating subset of distal receiver behavior alive.

This is a live causal intervention, not a dead arm.

It supports Park's identified role for slow NaV inactivation in closing / restricting the distal propagation regime.

It also exposes an important spatial fact: even with the common slow-NaV closing mechanism removed, five of thirteen receivers still alternate while eight transmit every event. That residual receiver split cannot be attributed to slow NaV inactivation alone.

Do not yet interpret that split as detailed-morphology computation; static channel distribution and ordinary transfer differences remain controls.

---

# Control 2 — remove A-type Kv conductance

This is a strong blocker-like intervention, not a subtle freeze of one gate.

Both released proximal/distal A-type conductance densities were set to zero while preserving the rest of the model.

Result:

```text
9 somatic spikes
all 13 receivers succeed on all 9 events
consensus = SSSSSSSSS
receiver patterns: 13 / 13 identical SSSSSSSSS
```

The operating regime remained excitable and produced repeated somatic spikes, although the somatic firing pattern changed substantially (13 -> 9 spikes).

Interpretation:

> Removing A-type Kv removes the failure/alternation phenotype entirely in this detailed-model protocol.

This is directionally consistent with Park's mechanism that A-type Kv limits initial/distal propagation and its inactivation opens the dSpike window.

Because firing rate and trajectory also change, this arm should not be used quantitatively as a matched `Omega_geom` intervention without a rate/trajectory control. It is a finite-amplitude causal sanity check.

---

# What these controls earn

The baseline success/failure alternation is causally sensitive to the identified history-bearing channel mechanisms:

```text
slow NaV inactivation removed
    -> shell-wide failures disappear

A-type Kv removed
    -> all shell receivers propagate every surviving somatic event
```

So the state-conditioned transfer difference measured in I0/I1 is not an arbitrary impedance fluctuation unrelated to the known biology.

---

# What they do not earn

They do **not** establish a detailed-morphology contribution.

The author-released two-compartment model already demonstrated that:

```text
one dendritic recovery state + one soma-dendrite coupling edge
```

is sufficient for a transient propagation window.

The detailed model must therefore earn something beyond that minimal mechanism.

The no-slow-NaV arm is particularly informative here: it leaves a stable split of

```text
8 receivers: always success
5 receivers: alternating success/failure
```

under a common soma drive and with `s_na3=1` throughout.

That residual split is now a candidate **spatial-organization** target, but it still owes strong static controls before any chronology claim.

---

# Immediate next correction / control

The Park paper describes the relevant dSpikes specifically in **distal apical dendrites** and the widefield experiment illuminates the soma + apical trunk.

The earlier fixed 490–510 um shell was selected by path distance alone and unintentionally included both `apic[]` and basal `dend[]` sections.

This became important because the largest I1 state-ratio outliers were precisely the weakly soma-visible basal receivers.

Therefore the next run is a literature-grounded correction, frozen before seeing its result:

```text
repeat I1 using only apic[] receivers
for both finite-amplitude classification and proximal/distal impedance summaries
```

This is **not** outcome tuning. It corrects the anatomical receiver definition to match the primary paper.

If the impressive distal-specific I1 effect collapses under the apical-only analysis, that positive must be withdrawn.

---

## One-line result

> **The Park detailed-model alternation is causally controlled by slow NaV inactivation and A-type Kv, but this still does not credit detailed morphology; the next gate corrects the receiver set to the paper's distal apical dendrites before any full chronology analysis.**
