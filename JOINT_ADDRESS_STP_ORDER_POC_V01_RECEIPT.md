# Joint address × STP balanced-order POC v0.1 — execution receipt

**Date:** 2026-08-15  
**Status:** executed one-seed synthetic mechanism gate. **Not biological evidence and not a novelty claim.**

## Why this run exists

The previous majority-long POC was imbalanced (11/16 positive patterns) and the main baselines sat exactly on the 0.6875 majority-class accuracy. This run replaced that task before changing the desired outcome.

The new task is a balanced four-afferent **forward-vs-reverse burst-order discrimination** problem, in the same broad temporal-discrimination family used as a guardrail by Carvalho & Buonomano (2011).

Frozen design before the result:

```text
passive asymmetric 31-node RC tree
18 candidate synaptic sites
all source->soma kernels area normalized
4 afferents × 3 equal-weight contacts
homogeneous fixed-STP baseline
learned STP = U, tau_D, tau_F
fixed / location-only / STP-only / joint factorial
strict within-afferent complete-STP-tuple shuffle
matched isopotential control
NO location-diversity reward
```

Workflow:

```text
.github/workflows/joint-address-stp-order-poc.yml
GitHub Actions run 31882793653
conclusion: success
```

## One-seed result

### Passive tree

```text
variant       test accuracy     test loss
fixed             1.0000        0.5493544
location-only     1.0000        0.2873722
STP-only          1.0000        0.2775632
joint             1.0000        0.1236391
```

So the balanced task is no longer a majority-baseline failure. The passive tree by itself can encode the forward/reverse pattern through its non-identical normalized temporal kernels, and learned STP can also improve margin/loss.

But the decisive interaction test is again essentially zero:

```text
joint baseline loss              0.1236391440
40 shuffled losses mean          0.1236392455
mean loss increase               0.0000001015
mean loss ratio                  1.0000008211
accuracy baseline / shuffled     1.0000 / 1.0000
```

Therefore the joint model's lower loss is **not** evidence that particular STP tuples became specialized to particular dendritic addresses.

### What the learned solution actually did

Hard learned addresses:

```text
afferent 0: [2,2,2]       one site
afferent 1: [2,2,2]       one site
afferent 2: [9,11,12]     three sites
afferent 3: [14,15,17]    three sites
```

The learned STP values are strongly specialized **between afferents**, but within the afferents that retain several different addresses the tuples are nearly identical. Example:

```text
afferent 2:
U       ~0.9464-0.9468
tau_D   ~5.043-5.046 ms
tau_F   ~496.5 ms

afferent 3:
U       ~0.9423-0.9439
tau_D   ~5.035-5.037 ms
tau_F   ~497.7-498.5 ms
```

This explains the strict shuffle null: the optimizer found **afferent-level temporal specialization**, not within-afferent temporal specialization tied to dendritic address.

### Isopotential control

```text
fixed             test acc 0.5000
location-only     test acc 0.5031
STP-only          test acc 1.0000
joint             test acc 1.0000
```

Thus when space is removed, learned STP alone can solve the temporal-order task, while fixed/homogeneous STP is at chance as expected.

The within-afferent shuffle remains numerically invariant:

```text
joint baseline loss              0.1534538567
shuffled loss mean               0.1534538373
loss ratio                       0.9999998738
accuracy                         1.0000 throughout
```

This is a useful interpretation control: the learned temporal profiles are functionally meaningful at the afferent level, yet their assignment to individual dendritic addresses is not.

## What this one seed earns

It does **not** kill the full biological seam. It does kill a tempting synthetic story:

> A passive area-normalized soma-transfer tree does not automatically cause jointly learned STP profiles to bind to particular dendritic addresses, even on a clean balanced temporal-order task.

The joint model gets a larger margin / lower loss, but the benefit is compatible with two largely separable resources:

```text
spatial temporal filtering by address
+
afferent-specific STP filtering
```

rather than a multiplicative address × STP assignment code.

## Replication already launched

A three-independent-seed replication was launched immediately without changing the model/task:

```text
.github/workflows/joint-address-stp-order-poc-3seed.yml
GitHub Actions run 31882943388
```

Interpret that run before deciding whether the passive synthetic branch deserves any more budget.

## Current provisional decision

If the three-seed run reproduces the near-zero strict shuffle effect, stop tuning the passive soma toy. The next scientifically plausible place for address × temporal-state specialization would have to involve something the passive separable receiver lacks — e.g. location-specific nonlinear recruitment / active dendritic interaction — and should be tested against a strong simpler control rather than built in merely to force a positive result.
