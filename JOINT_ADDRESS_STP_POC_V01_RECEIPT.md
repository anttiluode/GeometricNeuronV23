# Joint synaptic address × STP POC v0.1 — execution receipt

**Date:** 2026-08-15  
**Status:** executed synthetic mechanism smoke test. **Not biological evidence and not a novelty claim.**

## Purpose

After the literature collision in `JOINT_ADDRESS_STP_COLLISION.md`, V23 built the smallest runnable test of the remaining seam:

```text
spatial address
×
learned presynaptic temporal dynamics (U, tau_D, tau_F)
```

The question was deliberately narrow:

> If location and STP are optimized together, does a strict post-training shuffle of complete learned STP tuples over the learned addresses hurt performance while an isopotential control remains shuffle-invariant?

Implementation:

```text
joint_address_stp_poc.py
.github/workflows/joint-address-stp-poc.yml
GitHub Actions run 31873947124
artifact joint-address-stp-poc
```

---

## Synthetic medium and controls

The POC used a deterministic asymmetric 31-node passive RC tree with 18 candidate synaptic sites.

Every source-to-soma temporal kernel was **area normalized**, removing the trivial DC-gain benefit of choosing a proximal/high-transfer site. Thus location could matter only through passive temporal kernel shape/delay in this toy.

Task:

```text
4 presynaptic afferents
3 equal-weight contacts per afferent
short/long interval triplets
classify whether >=2 of 4 afferents carry the long interval
```

Learnable per-contact STP:

```text
U
tau_D
tau_F
```

Variants:

```text
fixed address + fixed STP
learned address + fixed STP
fixed address + learned STP
joint learned address + learned STP
```

Strict shuffle:

```text
within each afferent only,
permute complete (U,tau_D,tau_F) tuples
across the three already-frozen learned addresses
```

This preserves afferent identity, hard addresses, decoder, contact weights, and the exact temporal-parameter multiset.

Isopotential control:

```text
replace every spatial kernel by the same mean kernel
```

where the within-afferent shuffle should be exactly irrelevant.

---

# v0.1 result

## Passive tree

Reported means in the run:

```text
fixed        test acc 0.6875   loss 0.63185
location     test acc 0.6875   loss 0.57492
STP          test acc 0.6875   loss 0.58688
joint        test acc 0.7125   loss 0.48534
```

At first sight the joint model looks somewhat better in loss and slightly better in accuracy.

But the decisive shuffle is essentially null:

```text
joint baseline test loss        0.4853353
mean shuffled test loss         0.4854112
mean loss increase              0.0000759
mean loss ratio                 1.0001565
baseline accuracy               0.7125
shuffled accuracy               0.7125
```

So **the joint model's improvement is not evidence for address × STP specialization**. Reassigning the learned STP tuples over the learned addresses changes essentially nothing.

The hard-location solution also collapses almost every contact onto the same candidate site:

```text
[0,2,2,2,2,2,2,2,2,2,2,2]
```

which is another reason the address-shuffle effect is expected to be tiny.

## Isopotential control

As required, the shuffle is numerically irrelevant:

```text
baseline loss                  0.6038066
mean shuffled loss             0.6038066
mean loss ratio                ~1.0000000
accuracy before/after          0.6875
```

So the strict shuffle implementation passes its exchangeability control.

---

# Important audit caught immediately afterward

The nominal three optimization seeds were **not independent** in v0.1.

Inside `AddressSTP.__init__`, the STP initialization used its own hard-coded

```text
torch.Generator().manual_seed(12345)
```

which overrode the outer `fit_variant(seed)` initialization for the STP parameters. Because the rest of the optimizer and data were deterministic, seeds 0/1/2 produced identical fitted solutions.

Therefore:

```text
DO NOT report n=3 independent fits.
```

The correct interpretation is:

```text
one deterministic fitted solution, accidentally repeated three times.
```

The isopotential shuffle-null remains a valid software-control observation, and the within-solution tree shuffle-null remains valid for that fitted solution, but multi-seed robustness is **not earned** by v0.1.

A separate v0.2 workflow fixes this before rerunning:

```text
.github/workflows/joint-address-stp-poc-v02.yml
```

---

# Second limitation discovered from the result

The task target is imbalanced:

```text
label 1 when >=2 of four bits are long
=> 11 / 16 bit patterns are positive
=> majority-class accuracy = 0.6875
```

Thus fixed/location/STP-only accuracy sitting at `0.6875` is literally the majority baseline. Even the joint accuracy `0.7125` is only a small escape from that baseline.

This POC is therefore a useful software/mechanism check but a weak scientific task.

Do **not** tune this exact task until it produces a positive address effect.

If v0.2 confirms the shuffle null, the next POC should replace the target with a **balanced task whose solution actually requires temporal discrimination** before any realistic-neuron port.

---

## v0.1 verdict

> **The first runnable synthetic test did not show mutual address × STP specialization: the strict temporal-parameter shuffle was essentially invisible. The control behaved correctly, but the run also exposed a seed bug and a majority-baseline task flaw, so this is a useful negative engineering gate rather than a scientific result.**
