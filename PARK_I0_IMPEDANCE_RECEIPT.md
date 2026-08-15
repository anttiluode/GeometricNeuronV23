# Park 2025 I0 — state-conditioned impedance receipt

**Date:** 2026-08-15  
**Status:** executed known-answer calibration. **Not a novelty claim.**

## Question

Before paying for a full time-dependent Jacobian / Magnus decomposition, does the actually reproduced Park widefield phenotype leave a measurable state-conditioned change in the small-signal source-to-receiver operator?

If not, stop the chronology branch.

## Protocol frozen before looking at impedance

Model/protocol:

```text
exact Park et al. Supplementary Software 1
released run 12 — Optopatch step widefield
Python 3.10 / NEURON 8.2.2
```

Receiver policy inherited from P0:

```text
all non-axonal receivers at path distance 490–510 um
n = 13
```

Event classification used the same finite-amplitude receiver shell:

```text
success event: >= 80% of shell receivers cross -40 mV
failure event: <= 20%
mixed: otherwise
```

Snapshot time was fixed at:

```text
1.0 ms before each somatic spike peak
```

Frequencies:

```text
1, 10, 50, 100 Hz
```

Source:

```text
soma current perturbation
```

Measurements:

```text
NEURON Impedance.compute(freq,0)  — default di/dv linearization
NEURON Impedance.compute(freq,1)  — extended voltage + supported gating-state linearization
```

No zero-amplitude `gclamp` point process was instantiated in the I0 replay so that the extended impedance calculation remained compatible with the model's differential system.

Workflow:

```text
.github/workflows/park-impedance-i0.yml
GitHub Actions run 31872873718
artifact: park-impedance-i0
```

---

## Finite-amplitude event labels

The fixed 490–510 um shell gave:

```text
event   shell success fraction   label
1       1.0000                   success
2       0.6154                   mixed
3       1.0000                   success
4       0.0769                   failure
5       0.9231                   success
6       0.0000                   failure
7       1.0000                   success
8       0.0000                   failure
9       1.0000                   success
10      0.0000                   failure
11      1.0000                   success
12      0.0000                   failure
13      0.7692                   mixed
```

Primary comparison therefore used:

```text
6 success-preceding states
5 failure-preceding states
2 mixed states excluded from the contrast
```

---

## Result

For each event and frequency, soma -> shell transfer amplitudes were summarized in log space over the fixed receiver ensemble.

### Default / instantaneous-conductance impedance

Geometric-mean transfer amplitude ratio:

```text
success-preceding / failure-preceding

1 Hz      1.6883 x
10 Hz     1.6682 x
50 Hz     1.4385 x
100 Hz    1.2731 x
```

Corresponding shell circular phase contrasts (success minus failure):

```text
1 Hz     -0.00695 rad
10 Hz    -0.06683 rad
50 Hz    -0.18787 rad
100 Hz   -0.17042 rad
```

### Extended impedance including differential gating-state dynamics

Geometric-mean transfer amplitude ratio:

```text
success-preceding / failure-preceding

1 Hz      2.4018 x
10 Hz     2.2208 x
50 Hz     1.5968 x
100 Hz    1.4778 x
```

Corresponding shell circular phase contrasts:

```text
1 Hz     -0.18820 rad
10 Hz    -0.44036 rad
50 Hz    +0.19492 rad
100 Hz   +0.22282 rad
```

No extended-impedance exception occurred in this run.

---

## What I0 earns

The cheap gate **survives strongly**:

> The small-signal soma -> distal transfer operator is measurably different in states that precede widespread distal dSpike success versus widespread failure.

The effect is not only a high-frequency spike singularity: it is already large at 1–10 Hz in a snapshot taken 1 ms before the somatic spike.

The extended gating-state calculation increases the success/failure transfer contrast substantially relative to the default `di/dv` calculation, especially at low frequency.

This is consistent with the known Park mechanism being history-bearing channel state rather than a purely instantaneous voltage effect.

It is enough to justify one more mechanistic gate.

---

## What I0 absolutely does **not** earn

I0 does **not** establish the GeometricNeuron morphology × history hypothesis.

A simpler explanation remains fully viable:

```text
success-preceding states simply have globally / locally greater excitability
or a more favorable dendritic refractory state,
without any special contribution from detailed morphology.
```

This warning is especially strong because Park et al. explicitly report that the widefield period-doubling arises when distal dendritic refractoriness slightly exceeds somatic refractoriness, and they also show that a coarse two-compartment Izhikevich-type model captures both the opening/closing window and the period-doubling phenotype.

Therefore the **phenotype itself is not evidence that detailed dendritic geometry is necessary**.

Also:

- `Impedance.compute(freq,1)` is an established NEURON local linearization with documented limitations; it is not a full arbitrary `df/dy` oracle.
- this is a small-signal diagnostic around an already-generated nonlinear trajectory;
- success/failure states alternate along one deterministic trajectory and are not independent samples;
- raw soma -> distal transfer can change because the source/somatic input impedance changes, even if distal routing itself does not.

---

## Next gate — source-normalized and spatially comparative I1

Before full Jacobians, separate a global/source-state explanation from distal routing.

For the **same fixed event labels and snapshot policy**, measure:

```text
1. somatic input impedance Z_in,soma(state)
2. soma -> proximal transfer
3. soma -> distal 490–510 um transfer
4. distal transfer normalized by soma input impedance
      |Z_soma->distal| / |Z_in,soma|
5. receiver-by-receiver success/failure ratio across the distal shell
```

Primary question:

> Does the ~2.4x extended low-frequency distal contrast survive after normalization by the state-dependent somatic input impedance, and is it stronger / spatially structured distally than proximally?

Interpretation:

```text
contrast collapses after soma normalization
    -> mostly source/global excitability; geometry-history story weakens

normalized contrast persists but is spatially uniform
    -> history-dependent dendritic accessibility, still not detailed geometry

normalized contrast is strongly location/branch dependent
    -> proceed to causal gate-state controls and morphology/history decomposition
```

Only after I1 should we attempt `Omega_2^geom` vs `Omega_2^local`.

---

## References / guardrails

- Park P et al. (2025), *Dendritic excitations govern back-propagation via a spike-rate accelerometer*, Nature Communications 16:1333. DOI: 10.1038/s41467-025-55819-9.
- NEURON 8.2 Impedance documentation: default impedance uses `di/dv`; `compute(freq,1)` extends the linearization to supported differential gating states and has explicit limitations.

## One-line result

> **Known success/failure states in the released Park model differ by ~2.4x in extended 1-Hz soma-to-distal transfer, so state-conditioned operator change is real enough to continue; detailed morphology has not yet earned credit.**
