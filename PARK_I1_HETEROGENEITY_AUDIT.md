# Park I1 — heterogeneity audit

**Date:** 2026-08-15  
**Status:** post-hoc audit of the **already frozen I1 artifact**. No model rerun, no receiver reselection. **Not a novelty claim.**

## Why this audit was necessary

I1 showed that the 1-Hz extended normalized success/failure transfer ratio varied strongly across the 13 fixed 490–510 um receivers:

```text
0.868 x ... 6.880 x
```

It was tempting to call that branch-specific history routing.

Before doing so, this audit asked whether the apparent dynamic heterogeneity is already predictable from the simpler/default impedance or ordinary receiver visibility.

Workflow:

```text
.github/workflows/park-i1-heterogeneity-audit.yml
GitHub Actions run 31873287254
artifact analyzed: frozen I1 run 31873026312
n receivers = 13
```

---

# Result: the dramatic receiver spread mostly collapses onto a simpler structure

At 1 Hz, across the fixed receiver set:

```text
corr( log extended state ratio,
      log basic/default state ratio )
    = +0.99495
```

The additional gating-state amplification was defined as

```text
gating excess = extended ratio / basic ratio.
```

Its range was:

```text
minimum     0.8578
median      1.0822
maximum     2.3700
std(log)    0.3821
```

And:

```text
corr( log gating excess,
      log basic/default state ratio )
    = +0.98042
```

So locations that already show a large success/failure contrast in the simpler voltage-slope impedance are almost exactly the locations where the extended gating-state calculation magnifies it further.

That is a strong warning against interpreting the 0.87–6.88x extended range as an independent new branch-history coordinate.

---

# Even stronger: the extra gating effect is almost the inverse of ordinary visibility

Using each receiver's geometric-mean **source-normalized transfer amplitude across all I1 snapshots** as a crude static-position visibility measure:

```text
corr( log gating excess,
      log mean basic receiver visibility )
    = -0.98803

corr( log gating excess,
      log mean extended receiver visibility )
    = -0.98474
```

So the largest apparent history amplification occurs at the receivers that are ordinarily **least visible from the soma**.

The extreme group is obvious in the frozen receiver table:

```text
apical receivers:
    basic normalized mean transfer ~0.11–0.14
    extended success/failure ratios ~0.87–1.28

basal dend[8]/dend[9] receivers near the same 500-um path distance:
    basic normalized mean transfer ~0.0065–0.0094
    extended success/failure ratios ~4.3–6.9
```

Distance itself does not explain the extra gating ratio inside the narrow shell:

```text
corr(log gating excess, path distance)
    = -0.1762
```

But this is only `n=13` and the receivers fall into obvious anatomical groups, so these correlations are descriptive diagnostics, not inferential statistics.

---

# Important correction to the previous I1 interpretation

The previous statement

> extended gating-state effects are highly heterogeneous across branch/site

is descriptively true.

But the stronger interpretation

> therefore detailed morphology is generating a new independent history-routing coordinate

is **not earned**.

The heterogeneity is almost perfectly aligned with the simpler default success/failure contrast and strongly inversely related to ordinary source->receiver visibility.

A plausible mundane explanation is:

```text
weakly coupled / strongly attenuated receivers
    -> small absolute baseline transfer
    -> a state-dependent local change creates a large ratio
```

That is still real state dependence, but a ratio at an ordinarily weak receiver is not automatically computational richness.

This audit therefore kills the most exciting reading of the 6.88x outlier before it can become a story.

---

# What does survive from I1

The **ensemble distal-vs-proximal effect** remains.

At 1 Hz extended impedance:

```text
soma input success/failure       1.135 x
proximal normalized              0.962 x
distal normalized                2.116 x
distal-specific diff-of-diff     2.200 x
```

That cannot be dismissed merely because the receiver-wise heterogeneity has a static-visibility confound.

So the surviving question is now more modest:

> **Why does the distal compartment as an ensemble alternate between high- and low-accessibility states, and does detailed morphology contribute anything beyond the two-compartment history mechanism already supplied by Park?**

---

# Saved-state sanity check

The I1 artifact also contains state summaries exactly 1 ms before the classified somatic spikes.

Success-preceding versus failure-preceding means:

```text
distal voltage
    success -63.123 mV
    failure -57.416 mV
    delta   -5.707 mV

slow NaV gate s_na3
    success 0.90269
    failure 0.85846
    delta  +0.04423

A-type gate l
    success 0.65146
    failure 0.48380
    delta  +0.16766

proximal slow NaV gate s_na3
    success 0.97195
    failure 0.96285
    delta  +0.00910
```

Thus the success/failure states are not merely different in voltage: the **distal history gates differ more strongly than the proximal slow-NaV gate**.

Do not over-interpret the sign of the A-type `l` variable until its exact mechanism semantics are checked against the released `kad/kap` equations.

The slow-NaV interpretation is cleaner: released `na3.mod` explicitly uses dynamic state `s` as a multiplicative Na conductance gate and labels it slow inactivation.

---

# New kill condition produced by this audit

A future detailed-morphology metric must beat both:

```text
1. basic/default state-conditioned transfer ratio
2. ordinary mean source->receiver visibility
```

If a proposed geometry/history score merely rediscovers that low-visibility branches have large relative modulation, it adds no mechanism.

The stronger matched target should use an **absolute or response-normalized change with a floor**, or compare receivers matched on baseline transfer as well as path distance.

---

## One-line result

> **The spectacular 0.87–6.88x receiver spread is almost perfectly predictable from the simpler default state contrast (`r≈.995`) and is largest at the least soma-visible branches (`r≈−.988` with mean visibility), so the branch-heterogeneity excitement is downgraded; only the robust distal-vs-proximal state switch survives this audit.**
