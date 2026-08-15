# GeometricNeuronV23 — handoff after Dig kill gates

**Date:** 2026-08-15  
**Status:** cross-repo update. The strict address×STP nulls remain unchanged; several broader geometry interpretations have now also been narrowed.

## Read first

In this repo:

- `HANDOFF_CURRENT.md`
- `HANDOFF_RECEIVER_RELATIVE_Q0.md`
- `JOINT_ADDRESS_STP_NONLINEAR_POC_V01_RECEIPT.md`
- `JOINT_ADDRESS_STP_ORDER_POC_V02_RECEIPT.md`

Then in `anttiluode/Dig`:

- `HANDOFF_CURRENT.md`
- `MONOTONE_DISCRIMINATION_RECEIPT.md`
- `RECEIVER_DIMENSION_CONTROL_RECEIPT.md`
- `OPERATING_STATE_Q2_RECEIPT.md`
- `STATE_DEFORMATION_Q1_RECEIPT.md`

---

# What did not change

The exact-address claim is still null in every synthetic regime tested:

```text
passive tree
balanced passive tree
smooth local regenerative nonlinearity
```

Strict post-training STP-tuple/address shuffles did not hurt the task.

Do not reopen this by tuning the toy task.

---

# What Dig killed after that

## 1. Soma as a uniquely collapsing receiver

Initial soma-versus-six-port Q0 looked dramatic:

```text
normalized entropy rank
soma             3.84
six ports        8.52
```

But equal-dimensional controls showed soma is ordinary among one-dimensional readouts:

```text
soma entropy rank                  3.838
random 1-D projection median       4.012
soma percentile in random 1-D      36.9%
```

So do not write:

```text
the soma uniquely destroys dendritic geometry.
```

The surviving result is the ordinary one:

```text
keeping more distributed output dimensions preserves more source information.
```

## 2. Strong small-signal state-dependent geometry deformation

On byte-identical `cell1.asc` with the public Beniaguev/Hay biophysics:

```text
active dendrites vs dendritic-active ablation
six-port pairwise source-distance Pearson = 0.9956
nearest-neighbour changes                 = 0/16

same full-active cell at -85 vs -65 mV
Pearson                                   = 0.99974
nearest-neighbour changes                 = 0/16
```

Thus in these small-signal regimes:

```text
state changes gains / metric details
```

but not:

```text
state dramatically rewires source-neighbour topology.
```

The old sentence `different local states deform those modes` remains broadly biophysically true but was weak as a topology-changing claim under our concrete metric.

---

# The object that survived

Dig replaced normalized shape rank with the monotone finite-horizon pairwise discrimination quantity

```text
D_C,T^2(i,j)
    = integral_0^T || h_i(t) - h_j(t) ||^2 dt
```

where:

```text
i,j   candidate source locations
C     receiver / readout map
T     observation horizon
```

This is standard observability / signal-detection mathematics.

It passed hard monotonicity and orthonormal-readout invariance checks.

The interesting internal result was:

```text
almost all aggregate response energy can already have arrived
while some source pairs remain far from their eventual discrimination energy.
```

At six ports:

```text
10 ms
aggregate response energy arrived      98.23%
median pair discrimination maturity    94.45%
10th-percentile pair maturity          50.43%
pairs >=90% mature                     53.3%
```

Therefore `maturity` should not be one scalar attached to a source/event.

A more faithful object is the whole receiver-relative matrix:

```text
D_C,T[i,j].
```

---

# What this means for the old mode sentence

Old working sentence:

> Different morphologies support different modes. Different local states deform those modes. Different receivers see different subsets of them. Computation may consist partly in controlling that deformation.

After the kill gates:

```text
Different morphologies support different transfer structures.
    established / plausible, not our discovery.

Different local states deform them.
    only modestly in our small-signal source-geometry tests.

Different receivers see different subsets.
    true in the ordinary readout/projection sense;
    soma was not special at equal dimension.

Computation may consist partly in controlling that deformation.
    not earned.
```

The replacement sentence is:

> **A distributed dynamical medium induces receiver- and horizon-dependent distinguishability among possible causes.**

That is enough.

---

# Why this still matters to GeometricNeuron

It changes the coordinate for asking future morphology questions.

Do not assume:

```text
segment identity = computational address.
```

Instead, under a specified receiver/readout and horizon, measure the source dictionary:

```text
h_i(t)
```

and the induced distinguishability:

```text
D_C,T(i,j).
```

Then morphology matters operationally only insofar as it changes those transfer/discrimination relationships for the downstream task.

This is much more conservative than global spectral-statistic stories and much harder to fool with pretty modes.

---

# Future biological address gate, if ever resumed

If the NMDA × active-dendrite × temporal-synapse-state branch is eventually run, preserve these rules:

1. Use a public validated biological model.
2. Freeze the downstream task before measuring address geometry.
3. Define receiver-visible source relationships independently of task success.
4. Keep the strict temporal-tuple/address shuffle.
5. Do not redefine addresses post-hoc to make the shuffle fail.
6. Compare raw anatomical shuffle and any preregistered transfer-class shuffle separately.
7. If both remain null, stop the exact-address specialization branch.

But there is no need to run that next just because it exists.

---

# Current priority

The stronger cross-project question has moved away from dendritic biology:

```text
Given D_C,T and a real decision criterion:

when is WAIT useful?
when has current C saturated?
when must the system ROUTE / PROBE / ACT instead?
```

Prior-art collision says active sequential hypothesis testing / controlled sensing already owns that abstract problem.

So the remaining project-specific test is whether **asynchronous agent temporal provenance** from WidePresent/PivotPoint changes those decisions in cases ordinary agents mishandle.

## One-line handoff

> **Do not rescue the old geometry story. Exact STP↔segment binding is null, strong state deformation was near-null, and soma-special collapse died under equal-dimensional control. The surviving V23 coordinate is the receiver/horizon-specific source discrimination matrix `D_C,T`; use it only where a downstream decision actually needs it.**
