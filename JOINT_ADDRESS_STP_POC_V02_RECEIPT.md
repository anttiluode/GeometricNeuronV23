# Joint synaptic address × STP POC v0.2 — audited seed rerun

**Date:** 2026-08-15  
**Status:** executed synthetic software/mechanism gate. **Not biological evidence and not a novelty claim.**

## Why v0.2 existed

The v0.1 run accidentally initialized every nominal optimization seed from the same hard-coded PyTorch generator. v0.2 removed that internal seed and reran three genuinely distinct initializations without changing the task or model otherwise.

Workflow:

```text
.github/workflows/joint-address-stp-poc-v02.yml
GitHub Actions run 31874235661
conclusion: success
```

## Result: the shuffle null survives the seed repair

Passive tree, three independent initializations:

```text
fixed      test acc mean 0.6875   loss 0.6311414
location   test acc mean 0.6875   loss 0.5744376
STP        test acc mean 0.6875   loss 0.5867305
joint      test acc mean 0.7125   loss 0.4852212
```

Joint learned model, strict within-afferent shuffle of complete learned `(U,tau_D,tau_F)` tuples over the frozen learned addresses:

```text
baseline loss mean                   0.4852212
shuffled loss mean                   0.4852972
mean loss increase                   0.00007594
mean loss ratio                      1.0001565
baseline accuracy mean               0.7125000
shuffled accuracy mean               0.7113194
```

The three hard-address solutions again collapse nearly all trainable contacts onto the same candidate location:

```text
[0,2,2,2,2,2,2,2,2,2,2,2]
```

for every audited seed.

So the original conclusion is strengthened:

> **This task does not produce meaningful mutual specialization between dendritic address and learned STP tuple.**

The joint model has lower loss than the separate variants, but the gain does not depend on the learned STP-to-address assignment, which is the actual interaction under test.

## Isopotential exchangeability control

The matched isopotential medium again behaves as required:

```text
joint baseline loss mean             0.6037688
shuffled loss mean                   0.6037688
mean loss ratio                      1.000000009
accuracy before / after              0.6875 / 0.6875
```

Thus the shuffle implementation itself is behaving correctly.

## Why this is still only an engineering null

The task remains badly imbalanced:

```text
label 1 when >=2 of four bits are long
11/16 patterns are positive
majority-class accuracy = 0.6875
```

The fixed/location/STP-only variants sit exactly on that majority baseline; the joint model only reaches 0.7125.

Therefore do not infer from this run that the scientific joint-address × STP seam is dead. The task is a weak test of it.

## Next gate frozen before seeing its result

Replace the majority task with a **balanced forward-vs-reverse spatiotemporal sequence discrimination** task, following the general FWD/REV temporal-discrimination lineage used by Carvalho & Buonomano (2011), while preserving:

```text
area-normalized passive spatial kernels
fixed / location-only / STP-only / joint factorial
strict within-afferent complete-tuple shuffle
isopotential exchangeability control
independent optimization seeds
```

Do not add a diversity reward that forces contacts onto different dendritic sites. If learned locations still collapse and the shuffle remains null, record the null rather than tuning the optimizer to manufacture an address effect.

Reference guardrail:
- Carvalho TP, Buonomano DV. 2011. *A novel learning rule for long-term plasticity of short-term synaptic plasticity enhances temporal processing*. Frontiers in Integrative Neuroscience 5:20. DOI 10.3389/fnint.2011.00020.

## v0.2 verdict

> **After repairing the seed bug, the strict address × STP assignment effect remains essentially zero. The next experiment changes the flawed task, not the desired outcome.**
