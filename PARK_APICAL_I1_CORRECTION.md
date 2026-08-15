# Park 2025 — apical-only correction to I1

**Date:** 2026-08-15  
**Status:** executed correction of the biological receiver definition. **This supersedes the mixed-apical/basal interpretation of `PARK_I1_NORMALIZED_RECEIPT.md`. Not a novelty claim.**

## Why this correction was mandatory

The Park et al. primary paper repeatedly defines the relevant history-dependent dSpikes as events in the **distal apical dendrites**. In the wide-field Fig. 4 condition, illumination covers the soma and apical trunk.

The earlier V23 I1 receiver shell was chosen only by path distance (`490–510 um`) and therefore accidentally pooled:

```text
apic[]   apical dendrites
and
dend[]   basal dendrites
```

The largest state-conditioned transfer ratios in that mixed shell came from weakly soma-visible basal `dend[]` receivers. The primary paper therefore supplied an anatomical correction independent of the observed outcome.

Before seeing this rerun, V23 froze:

```text
finite-amplitude classifier: apic[] only, 490–510 um
proximal comparison:          apic[] only, 90–110 um
source:                       soma
snapshot:                     1 ms before somatic spike peak
frequencies:                  1, 10, 50, 100 Hz
success/failure rule:         same >=80% / <=20% receiver consensus
```

Workflow:

```text
.github/workflows/park-apical-i1-correction.yml
GitHub Actions run 31873436618
job 94985403420
```

---

# Correct finite-amplitude receiver set

```text
proximal apical receivers   n = 5
distal apical receivers     n = 8
```

Distal-apical receiver patterns in released run 12:

```text
SSSSFFSFSFSFS    1 / 8
SSSFSFSFSFSFS    7 / 8
```

Apical-ensemble event classification:

```text
event 1   success  8/8
event 2   success  8/8
event 3   success  8/8
event 4   failure  1/8
event 5   success  7/8
event 6   failure  0/8
event 7   success  8/8
event 8   failure  0/8
event 9   success  8/8
event 10  failure  0/8
event 11  success  8/8
event 12  failure  0/8
event 13  success  8/8
```

So the biologically relevant distal apical ensemble still shows the robust period-doubled success/failure phenotype.

There are now:

```text
8 success-preceding states
5 failure-preceding states
0 mixed states
```

---

# Corrected source-normalized transfer result

## Default `di/dv` impedance

Success/failure ratios after normalization by somatic input impedance:

| frequency | soma input | proximal apical | distal apical | distal-specific difference-of-differences |
|---:|---:|---:|---:|---:|
| 1 Hz | 1.0915 | 1.0203 | **1.1174** | **1.0951** |
| 10 Hz | 1.0879 | 1.0200 | **1.1135** | **1.0917** |
| 50 Hz | 1.0525 | 1.0160 | **1.0718** | **1.0549** |
| 100 Hz | 1.0304 | 1.0124 | **1.0463** | **1.0335** |

## Extended impedance including differential gating-state dynamics

| frequency | soma input | proximal apical | distal apical | distal-specific difference-of-differences |
|---:|---:|---:|---:|---:|
| 1 Hz | 1.1235 | 1.0329 | **1.1443** | **1.1079** |
| 10 Hz | 1.0751 | 1.0189 | **1.1393** | **1.1182** |
| 50 Hz | 1.5694 | 0.8553 | **1.0306** | **1.2050** |
| 100 Hz | 1.1864 | 0.9507 | **1.0868** | **1.1432** |

At the primary low-frequency end, the previous dramatic mixed-shell result is gone.

The earlier mixed-shell I1 had suggested:

```text
1-Hz extended distal normalized success/failure     ~2.116 x
1-Hz distal-specific difference-of-differences      ~2.200 x
```

The literature-correct apical-only result is instead:

```text
1-Hz extended distal normalized success/failure      1.144 x
1-Hz distal-specific difference-of-differences       1.108 x
```

That is a major downgrade.

---

# Receiver-wise apical result

At 1 Hz, the eight distal apical receivers have tightly grouped default ratios:

```text
1.014 ... 1.150
```

and extended ratios:

```text
0.908 ... 1.220
```

There is no apical analogue of the 4–7x basal outliers that drove the mixed-shell excitement.

So the earlier apparent huge branch/site heterogeneity was largely an anatomical pooling error plus weak-baseline ratio effect.

---

# Scientific interpretation

## What survives

The finite-amplitude distal-apical success/failure alternation is robust and causally depends on the known Park channel-history mechanisms (`PARK_HISTORY_CAUSAL_RECEIPT.md`).

There is also a **modest** state-conditioned small-signal apical transfer change:

```text
~11% distal-specific at 1 Hz extended
~12% at 10 Hz
```

This is real enough to report, but not remotely the dramatic ~2.2x geometry-looking signal inferred from the mixed shell.

## What is killed / downgraded

The following interpretation is withdrawn:

> Park gives a large branch-specific detailed-morphology routing effect in the biologically relevant distal receiver set.

It does not, under this measurement.

The correct apical data are much more compatible with the paper's own coarse story:

```text
shared somatic event
+ distal dendritic state/refractoriness
-> alternating distal accessibility
```

with only a modest incremental transfer difference between proximal and distal apical compartments.

The author-released two-compartment model already shows that a detailed tree is unnecessary for the qualitative accelerometer/window phenomenon.

---

# Consequence for the Magnus / commutator branch

**Do not escalate directly to a giant full-state Magnus decomposition merely because the old mixed-shell I1 looked large.**

The actual GeometricNeuron question has become narrower:

> Does the *spatial arrangement* of the known history state within the apical tree contribute measurably beyond its mean/distal compartment state?

A cheaper and more direct next gate is therefore a **snapshot state-address shuffle**:

```text
same detailed morphology
same apical slow-NaV state multiset
same event snapshot
same soma source
same distal-apical receivers

real spatial assignment of s_na3
vs
path-distance-bin shuffles of s_na3 over apical segments
```

using state-conditioned impedance before attempting full `Omega_2`.

If path-matched shuffling of the history-state field barely changes the receiver transfer, detailed geometry/history alignment has failed its simplest direct test.

If it changes transfer substantially, then a full trajectory-level `S + Q(t)` chronology decomposition becomes worth paying for.

---

## One-line corrected result

> **After restricting the analysis to the distal apical dendrites actually studied by Park et al., the spectacular ~2.2x distal-specific I1 effect collapses to ~1.11x at 1 Hz; the finite-amplitude history phenotype survives, but the evidence for a large detailed-morphology routing effect does not.**
