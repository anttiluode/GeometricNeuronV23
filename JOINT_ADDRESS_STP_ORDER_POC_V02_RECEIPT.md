# Joint address × STP balanced order POC v0.2 — three-seed receipt

**Date:** 2026-08-15  
**Status:** executed synthetic control. **Not biological evidence and not a novelty claim.**

This receipt closes the passive-tree balanced forward/reverse smoke gate across three independent initializations.

## Run

GitHub Actions:

```text
run 31882943388
workflow .github/workflows/joint-address-stp-order-poc-3seed.yml
3 seeds
60 within-afferent tuple shuffles per seed
balanced forward/reverse temporal-order task
```

The tree arm uses area-normalized source-to-soma passive kernels. The strict shuffle preserves hard addresses, afferent identity, decoder, equal contact weights, and the exact learned `(U,tau_D,tau_F)` multiset; it only reassigns the complete STP tuples among the three contacts belonging to the same afferent.

## Tree result

All four variants reached 1.0 test accuracy. Mean test losses:

```text
fixed                 0.5493544
location only         0.2873722
STP only              0.2771257
joint                 0.1240620
```

The joint model therefore has a much larger margin than either single degree of freedom alone.

But the causal assignment test remains null:

```text
joint baseline loss mean          0.1240620489
shuffled loss mean                0.1240621209
mean loss increase                7.20e-08
mean loss ratio                   1.0000005806
baseline accuracy                 1.000
shuffled accuracy                 1.000
```

Per seed, shuffle-loss ratios were approximately:

```text
seed 0   1.0000008055
seed 1   1.0000005197
seed 2   1.0000004166
```

The learned hard locations were also effectively seed-stable. In the joint tree solution:

```text
afferent 0 -> one repeated site
afferent 1 -> one repeated site
afferent 2 -> three sites
afferent 3 -> three sites
```

Within the afferents that retained multiple sites, the optimized STP tuples were nearly equal. The optimizer specialized temporal dynamics mainly by afferent identity, not by dendritic address.

## Isopotential control

As required, fixed/location-only remained near chance while STP learned the order task:

```text
fixed test accuracy               0.5000
location-only                     0.5031
STP-only                          1.0000
joint                             1.0000
```

The strict shuffle was numerically invariant:

```text
mean loss ratio                   0.9999999606
baseline accuracy                 1.000
shuffled accuracy                 1.000
```

## Verdict

> **A passive dendritic transfer medium and useful temporal synaptic state can both improve a temporal task without becoming mutually bound. Across three independent fits, the exact learned STP tuple multiset can be reassigned among learned addresses with essentially zero cost.**

This is stronger than the earlier imbalanced-task null because the task is balanced, all variants genuinely solve or fail the intended discrimination in interpretable ways, the fixed-STP arm is homogeneous, and the result replicates across seeds.

## Consequence

Do not escalate passive address × STP optimization further by tuning tasks or adding location-diversity rewards. The next gate should add a **local voltage-dependent nonlinearity** while keeping the same strict shuffle intervention. If a specific address × temporal-dynamics binding is real, the next plausible mechanism is threshold/regenerative recruitment at the local site, not merely two linear filters in series.
