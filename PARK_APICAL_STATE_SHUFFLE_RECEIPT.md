# Park 2025 — apical history-state address-shuffle receipt

**Date:** 2026-08-15  
**Status:** executed cheap geometry × history kill gate on the corrected distal-apical receiver set. **Not a novelty claim.**

## Question

After the literature-correct apical-only I1 result reduced the state-conditioned transfer effect to ~10–12%, does the **spatial address** of the known history-bearing channel states inside the detailed apical tree materially create that contrast?

This is the cheap direct test before any full trajectory Jacobian / Magnus decomposition.

---

## Frozen design

Model/protocol:

```text
exact Park et al. Supplementary Software 1
released run 12 — Optopatch step widefield
Python 3.10 / NEURON 8.2.2
```

Receiver and classifier:

```text
distal APICAL receivers only
490–510 um path distance
n = 8
same finite-amplitude event labels as the apical correction
```

Small-signal diagnostic:

```text
1 Hz
NEURON extended impedance compute(freq,1)
soma source
soma-input-normalized distal-apical transfer
snapshot = 1 ms before each somatic spike peak
```

State fields:

```text
slow NaV inactivation state  s_na3
A-type Kv inactivation state l_kad / l_kap
```

Address control:

```text
all 537 apical segments
preserve exact gate-state multiset
shuffle only within 50-um path-distance bins
A-type shuffles also preserve mechanism kind (kad vs kap)
10 fixed random seeds
```

Three predeclared shuffles:

```text
slowNa   shuffle s_na3 only
Atype    shuffle A-type l only
joint    shuffle both
```

The nonlinear baseline trajectory is not rerun under the shuffled states. At each frozen snapshot the gate values are permuted, extended impedance is calculated without advancing time, and the original state is restored.

Workflow:

```text
.github/workflows/park-apical-state-shuffle.yml
GitHub Actions run 31873551235
job 94985688491
artifact park-apical-state-shuffle
```

---

# Baseline

The real spatial assignment gives an extended 1-Hz success/failure ratio in soma-normalized distal-apical transfer of:

```text
1.1443439 x
```

This agrees with `PARK_APICAL_I1_CORRECTION.md`.

---

# Slow-NaV address shuffle

Ten path-bin-preserving shuffled ratios:

```text
1.1402564
1.1395545
1.1397671
1.1403098
1.1394712
1.1399320
1.1400422
1.1396592
1.1393221
1.1395510
```

Summary:

```text
mean      1.1397866
median    1.1397132
min       1.1393221
max       1.1403098
std       0.0003197
baseline  1.1443439
```

The real address is above all ten shuffled values, but the effect size is tiny:

```text
baseline - shuffle mean ≈ 0.00456 in the ratio
```

or well under one percentage point of transfer ratio.

The ten seeds are not ten independent neurons and must not be converted into a biological significance claim.

### Interpretation

> Within coarse path-distance bins, the detailed spatial assignment of slow-NaV history contributes **very little** to the measured distal-apical state contrast.

This is not evidence for a strong geometry × slow-history organization effect.

---

# A-type address shuffle

Ten shuffled ratios:

```text
1.1778896
1.1714112
1.1714416
1.1552676
1.1488663
1.1589925
1.1652785
1.1599484
1.1599931
1.1703800
```

Summary:

```text
mean      1.1639469
median    1.1626358
min       1.1488663
max       1.1778896
std       0.0084164
baseline  1.1443439
```

**Every shuffled A-type assignment produced a larger success/failure contrast than the real assignment.**

### Interpretation

The real A-type history-state arrangement is not maximizing or enhancing this operator contrast. Under this metric, random path-matched reassignment tends to make the contrast modestly larger.

That is evidence **against** the simple story that the biological/detailed spatial arrangement is specially organized to amplify the measured history-dependent transfer distinction.

Do not reverse this into a claim that the real morphology deliberately suppresses the contrast; no objective of that kind has been established.

---

# Joint slow-NaV + A-type shuffle

Summary over ten seeds:

```text
mean      1.1606086
median    1.1592507
min       1.1452640
max       1.1748900
std       0.0084759
baseline  1.1443439
```

Again, all ten shuffled assignments were at or above the real-assignment contrast.

The A-type effect dominates the direction of the joint shuffle.

---

# Verdict on the Park geometry × history branch

This is the most direct cheap test so far of the V23 address hypothesis inside the biologically correct distal-apical compartment.

The result is mostly negative:

```text
slow-NaV address:
    real vs path-bin shuffle difference is tiny

A-type address:
    shuffling increases, rather than destroys, the measured contrast

joint address:
    shuffling likewise increases the contrast
```

Combined with the other Park controls:

```text
1. the author-released two-compartment model already reproduces the broad
   transient-history mechanism without a detailed tree;

2. slow NaV inactivation and A-type Kv causally control the detailed-model
   distal-apical phenotype;

3. the literature-correct apical-only state-conditioned transfer difference
   is modest (~10–12%), not the earlier mixed-shell ~2x effect;

4. path-matched history-state address shuffling does not reveal a large
   special contribution from the real detailed apical arrangement.
```

Therefore:

> **Park 2025 does not currently earn escalation to a large full-Jacobian/Magnus calculation as a discovery bet.**

A full `Omega_2^geom` / `Omega_2^local` decomposition could still be done for mechanistic closure, but the cheaper controls already say that the broad phenomenon is principally **local history + coupling**, with little evidence that the detailed spatial address of the tested history gates is the special ingredient.

---

# Caveats

This gate is deliberately narrow.

It does **not** prove that detailed morphology is irrelevant in Park or in dendritic computation generally.

Limitations:

```text
- snapshot small-signal test, not finite-amplitude shuffled trajectories
- shuffled gate states are not dynamically co-evolved with local voltage
- 50-um path bins preserve only a coarse anatomical coordinate
- only two identified history fields were permuted
- only 1-Hz extended transfer was used as the primary address metric
- full local Jacobian blocks Q_i(t) contain more than s_na3 and A-type l
- chronology across time was not directly decomposed
```

But these caveats do not rescue a positive claim. They merely bound the negative result.

A stronger geometry-history hypothesis now needs a **new reason** to spend the computation, not merely a more elaborate analysis of the same Park effect.

---

## One-line result

> **On the correct distal-apical receiver set, path-matched shuffling of slow-NaV history barely changes the 1-Hz state contrast (1.144 real vs ~1.140 shuffled), while A-type and joint shuffles make the contrast larger; the real detailed history-state address is therefore not earning a strong geometry-specific role in the Park calibration.**
