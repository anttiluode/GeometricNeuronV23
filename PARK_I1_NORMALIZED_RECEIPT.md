# Park 2025 I1 — source-normalized spatial impedance receipt

**Date:** 2026-08-15  
**Status:** executed known-answer calibration. **Not a novelty claim.**

## Question

I0 found a large state-conditioned soma -> distal transfer difference before widespread distal dSpike success versus failure in the released Park widefield regime.

The simplest confound was global/source excitability:

```text
success-preceding states simply have a larger somatic input impedance
```

which would inflate every downstream transfer without requiring any specifically distal or spatially organized effect.

I1 asks whether the contrast survives normalization by somatic input impedance and whether it is stronger distally than proximally.

---

## Frozen protocol

Exact published Supplementary Software 1, released run 12 — **Optopatch step widefield**.

Environment:

```text
Python 3.10
NEURON 8.2.2
```

Event labels and snapshot timing were inherited unchanged from I0:

```text
success: >=80% of fixed 490–510 um shell receivers cross -40 mV
failure: <=20%
mixed: excluded from success/failure contrast
snapshot: 1.0 ms before each somatic spike peak
```

Groups:

```text
proximal shell   90–110 um,  n = 11
distal shell    490–510 um,  n = 13
```

Source:

```text
soma current perturbation
```

Frequencies:

```text
1, 10, 50, 100 Hz
```

Measurements:

```text
NEURON Impedance.compute(freq,0)
NEURON Impedance.compute(freq,1)
```

For each receiver:

```text
normalized transfer = |Z_soma->receiver| / |Z_in,soma|
```

Workflow:

```text
.github/workflows/park-impedance-i1-normalized.yml
GitHub Actions run 31873026312
job 94984437047
```

---

# Result

## Default / instantaneous `di/dv` impedance

Success-preceding / failure-preceding ratios:

| frequency | soma input | proximal raw | distal raw | proximal normalized | distal normalized | distal-specific difference-of-differences |
|---:|---:|---:|---:|---:|---:|---:|
| 1 Hz | 1.0699 | 1.1713 | 1.6883 | 1.0948 | **1.5780** | **1.4414** |
| 10 Hz | 1.0462 | 1.2033 | 1.6682 | 1.1471 | **1.5902** | **1.3863** |
| 50 Hz | 1.0027 | 1.1740 | 1.4385 | 1.1708 | **1.4347** | **1.2254** |
| 100 Hz | 1.0007 | 1.1442 | 1.2731 | 1.1434 | **1.2722** | **1.1126** |

So even the default voltage-slope linearization retains a distal-specific state contrast after removing somatic input impedance.

---

## Extended impedance including supported differential gating-state dynamics

Success-preceding / failure-preceding ratios:

| frequency | soma input | proximal raw | distal raw | proximal normalized | distal normalized | distal-specific difference-of-differences |
|---:|---:|---:|---:|---:|---:|---:|
| 1 Hz | 1.1353 | 1.0918 | 2.4018 | **0.9617** | **2.1156** | **2.2000** |
| 10 Hz | 1.1012 | 1.0593 | 2.2208 | **0.9619** | **2.0167** | **2.0966** |
| 50 Hz | 1.0371 | 1.0553 | 1.5968 | 1.0175 | **1.5396** | **1.5132** |
| 100 Hz | 1.0162 | 1.0889 | 1.4778 | 1.0716 | **1.4542** | **1.3570** |

The 1-Hz result is especially informative:

```text
soma input changes only          1.135 x
proximal normalized transfer     0.962 x
 distal normalized transfer      2.116 x
 distal-vs-proximal state effect  2.200 x
```

Therefore the ~2.4x I0 distal transfer contrast is **not** primarily explained by a larger somatic input impedance in the success-preceding state.

The extended gating-state calculation makes the state contrast strongly distal: the proximal normalized transfer is essentially unchanged/slightly smaller while distal normalized transfer more than doubles.

---

# Receiver heterogeneity

For the 13 fixed 490–510 um receivers, the 1-Hz normalized success/failure ratio varied as follows.

Default impedance:

```text
minimum     1.4396
median      1.4462
maximum     1.8713
std(log r)  0.0853
```

Extended impedance:

```text
minimum     0.8683
median      1.2744
maximum     6.8814
std(log r)  0.6823
```

So the additional history-dependent gating-state contribution is **strongly heterogeneous across receiver locations even inside a narrow 20-um path-distance shell**.

This is more informative than a proximal/distal gradient alone: all 13 distal receivers have nearly matched soma path distance, yet their extended state-conditioned transfer ratios span roughly eightfold from minimum to maximum.

Do not interpret the maximum receiver post hoc as the canonical computation site. The ensemble and the frozen receiver list remain the primary analysis.

---

# What I1 earns

The strongest simple null from I0 is rejected in this model run:

> **The success/failure transfer contrast does not collapse after normalizing by somatic input impedance.**

Moreover, the state-conditioned effect is much stronger distally than proximally and highly heterogeneous across branches/locations at matched path distance.

Operationally, this means the released Park detailed model contains a real state-conditioned **routing/accessibility** change, not merely a global source-gain change.

That is enough to proceed to a causal history-state control.

---

# What I1 still does not earn

It still does **not** prove that detailed dendritic morphology is necessary.

A two-compartment system with one soma-like and one dendrite-like state can already have:

```text
local history in the dendritic compartment
+ coupling between compartments
-> distal-specific accessibility changes
```

Park et al. explicitly provide a two-compartment Izhikevich model as a coarse qualitative control for the same general phenomenon. Supplementary Software 2 has now been fetched separately for direct execution.

Therefore the next question is no longer merely

```text
does state-dependent routing exist?
```

but

```text
what does the detailed tree add beyond the minimal coupled two-state/compartment mechanism?
```

Also:

- success/failure events alternate along one deterministic trajectory and are not independent samples;
- the extended NEURON impedance calculation is a local small-signal diagnostic, not a full nonlinear causal intervention;
- receiver heterogeneity can arise from branch-specific static channel density or impedance as well as from morphology × history chronology;
- a full geometry/history claim still owes the exact `S + Q(t)` decomposition or an equivalent matched spatial-state shuffle.

---

# Next gates

## I2a — execute the authors' coarse two-compartment control

Run the exact released Supplementary Software 2 code first, without fitting anything.

Ask:

```text
Does a minimal soma+dendrite state system reproduce the qualitative opening / alternation?
```

If yes, detailed morphology is not necessary for the phenotype itself.

Then use that model as a **minimal chronology baseline**, not as a competitor to be beaten cosmetically.

## I2b — causal channel-history control in the detailed model

Inspect the released `na3`, `kad`, and `kap` mechanisms and use an intervention that specifically changes/removes the identified history variable while preserving an interpretable operating regime.

Avoid a dead-arm ablation.

## I3 — only then full chronology decomposition

If the detailed-model history control survives:

```text
A(t) = S + Q(t)
Omega_2 = Omega_2^geom + Omega_2^local
```

with physical source/receiver projections.

Primary falsifier:

```text
state-conditioned routing real
but receiver-visible Omega_2^geom negligible
```

=> local channel chronology is sufficient; the GeometricNeuron morphology × history branch loses.

---

## One-line result

> **After removing somatic source gain, the Park success-preceding state still has ~2.12x larger extended 1-Hz distal transfer and a ~2.20x distal-specific effect relative to the proximal shell; the effect is also strongly branch/site heterogeneous, so state-conditioned routing survives the global-excitability null, but detailed morphology has not yet earned necessity.**
