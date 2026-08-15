# Joint address × STP local-nonlinearity POC — V01 receipt

**Date:** 2026-08-15  
**Workflow:** `Joint address x STP local nonlinear POC`  
**Run:** `31883664252`  
**Commit tested:** `3341fd61dc95fab674ab70308e073c0f84334346`

## Question

After passive address × learned-STP produced a strict shuffle null, test the smallest mechanism that can break passive separability:

```text
STP release
 -> same-site local voltage
 -> smooth regenerative feedback
 -> propagation from that same site to soma
```

The mechanism is intentionally a kill-gate, not a biological NMDA model.

Matched media:

```text
tree_linear             beta = 0
tree_nonlinear          beta = 2
isopotential_nonlinear  beta = 2
```

The decisive test remains the strict within-afferent shuffle of the learned `(U, tau_D, tau_F)` tuples across the post-training addresses.

## Executed result

One seed, 40 strict shuffles.

### Tree linear

```text
joint test loss          0.1181347370
joint test accuracy      1.0
shuffle mean loss        0.1181409799
shuffle loss ratio       1.0000528451
shuffle accuracy         1.0
```

As expected from the previous passive-tree run: null.

### Tree nonlinear

The local regenerative term strongly changed task ease:

```text
fixed test loss          0.4718053341
location-only            0.1648062915
STP-only                 0.0097787641
joint                     0.0008778340
joint test accuracy       1.0
weighted gate occupancy   0.1677593
```

But the address × STP binding test stayed null:

```text
baseline joint loss      0.00087783398
shuffle mean loss        0.00087751875
shuffle min/max loss     0.00087731297 / 0.00087786093
shuffle loss ratio       0.9996408992
baseline/shuffle acc     1.0 / 1.0
baseline gate occupancy  0.1677593
shuffle gate occupancy   0.1678784
```

The shuffled models were, if anything, microscopically better on mean loss. The difference is far too small to interpret and is in the wrong direction for the proposed structured-placement advantage.

### Isopotential nonlinear control

```text
joint test loss          0.0026130856
shuffle mean loss        0.0026130852
shuffle loss ratio       0.9999998597
baseline/shuffle acc     1.0 / 1.0
```

Exactly invariant, as intended.

## Verdict

> **LOCAL-SMOOTH-THRESHOLD NO ADDRESS×STP ADVANTAGE.**

The nonlinear tree is computationally useful in this toy task, but that usefulness does **not** depend on pairing a particular learned STP tuple with its learned dendritic address.

This is an important distinction:

```text
nonlinearity helps                      YES
location optimization helps             YES
STP helps                               YES
joint optimization helps loss           YES
learned STP tuple needs exact address    NO, in this gate
```

Therefore do not tune `beta`, threshold, task difficulty, or location diversity to manufacture a shuffle effect.

## What this closes

The following increasingly expressive synthetic regimes have now failed to produce strong exact-address × temporal-state specialization:

```text
passive transfer
balanced passive transfer
smooth local voltage-dependent feedback
```

The next online-computation test, if pursued, should be biologically grounded and should contain an interaction that the toy gate lacks: **NMDA voltage dependence together with active dendritic conductances / branch events on a real morphology.**

That next test must still keep the same hard control: learn or assign the same temporal-state multiset, then move those temporal states among matched dendritic addresses without changing the rest of the model.

## Stop condition honored

The preregistered handoff said:

```text
nonlinear tree shuffle ~= 1
 -> simple threshold feedback is insufficient
 -> do not tune it to win
 -> next biological gate should use interacting NMDA + active dendritic conductance
```

That is exactly the observed branch.
