# GeometricNeuronV23 — receiver-relative geometry bridge

**Date:** 2026-08-15  
**Status:** new measurement result from `anttiluode/Dig`; does **not** reopen the exact-address × STP nulls.

## Read alongside

In this repo:

- `HANDOFF_CURRENT.md`
- `JOINT_ADDRESS_STP_NONLINEAR_POC_V01_RECEIPT.md`
- `JOINT_ADDRESS_STP_ORDER_POC_V02_RECEIPT.md`
- `HANDOFF_NONCOMMUTING_DENDRITES.md`

In `anttiluode/Dig`:

- `RECEIVER_COLLAPSE_GATE.md`
- `receiver_collapse_cell1.py`
- `RECEIVER_COLLAPSE_CELL1_Q0_RECEIPT.md`
- `EXACT_L5_BRIDGE.md`
- `MULTIPORT_NEURON.md`

---

# What just happened

V23 has now produced repeated nulls for a specific claim:

> a learned local temporal synaptic state needs to remain attached to its exact optimized dendritic segment in order for the task to work.

That failed in:

```text
passive tree
balanced passive tree, 3 seeds
smooth local regenerative threshold toy
```

The strict post-training STP-tuple/address shuffle stayed essentially invariant.

Do **not** reinterpret the new Dig result as rescuing that claim.

Instead, Dig asked an orthogonal measurement question on the exact FCI/Hay `cell1.asc` morphology:

> If the same tiny source perturbations are observed from the soma alone versus a small distributed set of dendritic receivers, do the source locations remain equally distinguishable?

After rejecting two harness artifacts and using matched no-stimulus subtraction, the answer was clearly no.

Valid fixed-cell result:

```text
16 fixed source sites
same morphology
same passive-dendrite membrane model
same 0.02 nA / 0.5 ms perturbation

                                soma only      soma + 5 dendritic ports
entropy effective rank           3.8384               8.5159
participation rank               1.6211               2.6648
median pairwise cosine d         0.2065               0.4988
median nearest cosine d          0.00487              0.01626
```

Receiver jackknife:

```text
remove any one dendritic receiver:
entropy-rank ratio vs soma-only = 1.9309x .. 2.1179x

soma + one dendritic receiver:
entropy-rank ratio vs soma-only = 1.1723x .. 1.4406x
```

So no one lucky port carried the result.

Again: this is an expected kind of dendritic transfer / observation phenomenon, not a novelty claim.

---

# The useful correction

The previous experiments implicitly treated

```text
anatomical segment identity
```

as the candidate computational address.

The new measurement suggests a more disciplined coordinate:

```text
source i
  -> transfer responses to receiver set R
  -> normalized signature S_x(i | R,T)
```

where `x` is the operating state / mechanism regime and `T` is the observation horizon.

Then two physically distinct dendritic locations can be operationally close for a particular receiver if

```text
S_x(i | R,T) ~= S_x(j | R,T),
```

while adding receivers can split that equivalence.

This is not new mathematics. It is an observation-map / transfer-impedance / observability viewpoint applied consistently to the V23 question.

The important phrase from the earlier handoff now has an executable version:

> Different morphologies support different modes. Different local states deform those modes. Different receivers see different subsets of them.

For one fixed morphology, Q0 has now established the third clause operationally:

> **different receiver sets see different source distinctions.**

The second clause is the next test.

---

# Q1 — same anatomy, different operator

Freeze:

```text
cell1.asc morphology
16 source sites
6 receiver sites
stimulus
horizon
normalization
source-distance metric
```

Change only the realized dynamics / state.

For each condition `x`, measure

```text
S_x(i | R,T)
```

and its pairwise source geometry

```text
d_x(i,j) = distance(S_x(i), S_x(j)).
```

Then compare conditions.

The interesting claim is **not**

```text
active cell has bigger responses.
```

It is:

```text
same anatomy
+
different state / conductance regime
-> source relationships split, merge, rotate, or reorder
```

That would be a concrete measured version of

```text
state deforms effective causal geometry.
```

No cosmology required.

---

# Hard controls for Q1

1. **Gain-only control**  
   Normalize source signatures. A global/rescalable amplitude change is not geometry deformation.

2. **Fixed source/receiver control**  
   Never move sites between conditions.

3. **Matched baseline trajectory**  
   Each condition gets its own no-stimulus control from the same initialization.

4. **Distance-matrix comparison**  
   Report matrix correlation / Procrustes-like distortion / neighbour-order changes, not only effective rank.

5. **Mechanism ablation ladder**  
   Prefer author-released model mechanisms:

```text
P0  FCI passive dendrites
P1  NMDA operating regime on fixed morphology
P2  one validated active dendritic mechanism / holding state
P3  full active Hay cell on byte-identical cell1.asc
```

6. **No hand-written threshold rescue**  
   The smooth threshold toy already failed the exact-address gate. Do not invent another arbitrary nonlinearity just to bend the geometry.

---

# Relation to the exact-address × STP branch

If a later biological STP/address experiment is attempted, do **not** blindly shuffle temporal states over raw segments and assume every segment is an equally distinct address.

First measure the receiver-visible source geometry under the biological operating state.

Then a stronger test would distinguish:

```text
shuffle within nearly receiver-equivalent source classes
vs
shuffle across strongly receiver-distinct source classes
```

But this must be preregistered from a geometry measured **without using the downstream task result**. Otherwise it becomes post-hoc rescue.

The old strict raw-address shuffle remains a valid null for the model it tested.

---

# Current interpretation

What V23 can currently say is narrower and stronger than the old rhetoric:

```text
raw morphology != automatically useful computational address

soma projection can collapse much of the morphology's transfer structure

distributed receivers expose more of that structure

simple passive filtering and smooth threshold feedback
still do not force learned local temporal state to bind to exact address
```

The next genuinely interesting measurement is therefore not another bigger optimizer.

It is:

> **On byte-identical morphology, can a biologically grounded change of membrane/synaptic state deform the receiver-visible source geometry in a way that is more than gain scaling?**

If yes, then the old Clockfield intuition has a clean engineering descendant:

```text
state -> operator -> effective transfer geometry
```

If no, the state-deformation sentence loses force and receiver multiplicity remains the simpler surviving result.

## One-line handoff

> **Exact STP↔segment binding is still null. But Dig has now measured that source “address” is receiver-relative on the exact Hay morphology. Freeze that anatomy and test whether biological state changes the source-distance matrix itself.**
