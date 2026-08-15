# Park 2025 P0 execution receipt

**Date:** 2026-08-15  
**Status:** executed reproduction / receiver audit. **This is a data/provenance receipt, not a theory note and not a novelty claim.**

## 1. What was actually run

The exact public **Supplementary Software 1** ZIP for Park et al. (2025), *Dendritic excitations govern back-propagation via a spike-rate accelerometer*, was fetched directly from the Springer Nature supplementary-media host in GitHub Actions.

Published supplement URL used by the workflow:

```text
https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-025-55819-9/MediaObjects/41467_2025_55819_MOESM7_ESM.zip
```

The untouched ZIP was archived as a temporary workflow artifact by `.github/workflows/park-fetch-inspect.yml`.

The conductance-based CA1 model was then compiled and run under:

```text
Python 3.10
NEURON 8.2.2
Ubuntu GitHub Actions runner
```

The main execution workflows are:

```text
.github/workflows/park-reproduce-gate.yml
.github/workflows/park-readout-census.yml
```

Successful runs at the time of this receipt:

```text
supplement fetch/inspect   GitHub Actions run 31872229100
phenotype reproduction    GitHub Actions run 31872543670
500 um receiver census    GitHub Actions run 31872658435
```

## 2. Released-package rough edges encountered

These were handled minimally and are recorded because they matter for reproducibility.

### Unused `cheriff.mod`

The released `cheriff.mod` contains a non-ASCII bibliography character that NEURON 8.2's legacy NMODL translator rejects.

`FullCA1Model` hard-codes `CheRiff=False` and the relevant released simulations use `chr.mod`, so the workflow excludes the **unused** `cheriff.mod` rather than altering any active channel kinetics.

### Duplicate mechanism loading

When the compiled `x86_64/libnrnmech.so` is present in the working directory, NEURON loads it automatically. An explicit second `load_mechanisms('.')` call duplicated point-process names and was removed.

### Helper/API drift

The released `run_morphology.py` calls the current `FullCA1Model` constructor with an older argument signature. For the audit we instantiate the released `FullCA1Model` directly and reuse only the helper's `longest_path_from_soma_sections` function where needed.

No channel equation was edited for these fixes.

---

## 3. First receiver choice: arbitrary nearest segment to 500 um

The first custom reproduction selected the non-axonal segment with path distance nearest 500 um from the soma.

This was:

```text
apic[53](0.9)
path distance = 499.724 um
```

For released **run 3 — Optopatch step soma**:

```text
5 somatic spikes
500-um receiver pattern: SSSSS
```

For released **run 12 — Optopatch step widefield**:

```text
13 somatic spikes
receiver pattern: SSSSFFSFSFSFS
```

This did **not** reproduce the paper's qualitative failure-success-success-failure step pattern at the chosen branch.

That was treated as a failed readout choice, not as evidence against the published model.

---

## 4. Second receiver choice: authors' helper-defined longest dendritic path

The next run reused the released helper `longest_path_from_soma_sections` and chose the segment on that path nearest 500 um.

The path included:

```text
soma -> apic[0] -> apic[2] -> apic[6] -> ... -> apic[59] -> apic[61] -> apic[63] -> apic[65]
```

The selected receiver was:

```text
apic[59](0.642857...)
path distance = 506.989 um
```

Released run 3:

```text
5 somatic spikes
receiver peaks (mV):
-22.496, -22.190, -24.820, -27.280, -43.098

threshold -40 mV -> SSSSF
```

Released run 12:

```text
13 somatic spikes
threshold pattern -> SSSFSFSFSFSFS
```

Again, the exact initial step sequence was receiver dependent.

---

## 5. Predeclared receiver census instead of cherry-picking

Because the paper describes classification at a compartment around **500 um from the soma** but the morphology is branched, the next run recorded **every non-axonal segment from 450 to 550 um** and reported all patterns rather than choosing the branch that best matched the paper.

There were 62 candidate segments.

Classification used the paper's stated distal-spike threshold convention:

```text
success = receiver peak > -40 mV
```

### Released run 3 — soma step

Five somatic spikes.

#### 490–510 um, n=13

```text
FFFFF   5
SSSSS   7
SSSSF   1
```

Among the helper-defined longest-path receivers in this distance window:

```text
SSSSS   1
SSSSF   1
```

#### 480–520 um, n=24

```text
FFFFF   10
SSSSS   13
SSSSF    1
```

#### 450–550 um, n=62

```text
FFFFF   22
SSSSS   33
FSSFF    4
SSSSF    3
```

Thus the qualitative **FSSFF** opening/closing motif is present in the exact released model, but only on a subset of branches in the broad ~500-um shell under this released run.

Example (reported only as an existence example, **not selected as the canonical receiver**):

```text
apic[50](0.954545...)
path distance = 476.331 um
pattern = FSSFF
receiver peaks (mV) approximately:
-59.69, +1.67, +0.33, -62.92, -63.19
```

This means we must not choose one FSSFF branch post hoc and call it the paper's receiver.

### Released run 12 — widefield step

Thirteen somatic spikes.

#### 490–510 um, n=13

```text
SFSFSFSFSFSFF    3
SFSFSFSFSFSFS    2
SSSSFFSFSFSFS    1
SSSFSFSFSFSFS    7
```

#### 480–520 um, n=24

```text
SFSFSFSFSFSFS     5
SFSFSFSFSFSFF     5
SSSSFFSFSFSFS     3
SSSFSFSFSFSFS    11
```

#### 450–550 um, n=62

The exact initial prefix varies across branches, but strong alternating success/failure behavior is widespread after the early events. The two largest pattern classes were:

```text
SSSFSFSFSFSFS    31
SFSFSFSFSFSFS    13
```

with the remaining receivers mostly variants of the same alternating regime.

---

## 6. What P0 earned and did not earn

### Earned

1. The exact published supplement can be fetched, compiled and executed automatically.
2. The released conductance-based model contains the reported qualitative **transient distal dSpike window** on a subset of ~500-um branches.
3. The released model robustly enters the reported **alternating / period-doubled distal propagation regime** under the widefield protocol across many receiver branches.
4. Distal outcome is strongly receiver dependent in the branched morphology.

### Not earned

1. We have **not** uniquely reproduced the exact Figure-4 receiver because the released/paper description does not yet identify a unique ~500-um branch in this audit.
2. We have **not** measured any Magnus term, commutator, operator-atlas dimension, or geometry-history decomposition yet.
3. We have **not** shown that receiver dependence is a new phenomenon. It is expected that active dendritic propagation depends on branch and local channel state.
4. We have **not** selected the branch that happens to give FSSFF as the next analysis receiver.

---

## 7. Consequence for the kill gate

The cleanest next known-answer calibration is now the **widefield alternating regime**, because it is much less sensitive to which ~500-um branch is chosen than the exact initial FSSFF prefix.

Receiver policy for the next state-conditioned impedance gate should be fixed before looking at impedance results:

```text
A. soma
B. helper-defined longest-path receiver near 500 um
C. all receivers in a fixed 490–510 um shell, summarized as an ensemble
```

This prevents post-hoc receiver selection while preserving the scientific fact that the neuron is a multi-receiver object internally.

The next experiment is not yet the full Magnus decomposition. It is the cheaper state-conditioned transfer gate:

```text
known success-preceding state
vs
known failure-preceding state

NEURON extended impedance / source->receiver transfer
at matched inter-spike phases away from spike singularities
```

If the known history-dependent phenotype leaves almost no detectable change in the relevant incremental transfer objects, stop before investing in giant full-state Jacobians.

---

## 8. Additional predeclared published parameter point found in the supplement

The released MATLAB file

```text
Model Robustness/Figures/Figure_S19c-e/Plot_Phase_Diagrams.m
```

contains the authors' stored parameter-scan outcomes and the simulation settings used for that scan.

For the NaV-soma × NaV-dendrite scan it states:

```text
stimmax          = 7e-4
Nav_inactivation = [1, 0.5, 300, 100]
Kad_params       = [-0.2, 0.3, 0, 150]
```

and at the pre-existing table coordinate

```text
NaV soma      = 0.05 S/cm2
NaV dendrite  = 0.048 S/cm2
```

the stored code is

```text
011000 = FSSFFF
```

according to the legend in the same released file.

This point was selected from the **authors' stored table before running it in V23**, so it is a legitimate predeclared follow-up rather than outcome tuning.

That follow-up is the next execution receipt.

---

## References

- Park P et al. (2025), *Dendritic excitations govern back-propagation via a spike-rate accelerometer*, Nature Communications 16:1333. DOI: 10.1038/s41467-025-55819-9.

## One-line status

> **P0 is qualitatively alive, but the exact 500-um monitor is receiver-ambiguous; use the robust widefield alternation and a predeclared receiver ensemble for the chronology kill gate rather than cherry-picking an FSS branch.**
