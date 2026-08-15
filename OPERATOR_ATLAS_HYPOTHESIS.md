# GeometricNeuronV23 — operator atlas hypothesis

**Status:** candidate mechanism / bridge to test. Not a novelty claim.

This note is what remains after three prior-art collisions:

1. **Kellems et al. (2009)** already showed that a detailed/quasi-active dendritic neuron can have an enormous compartmental state while its subthreshold input -> chosen receiver map is reducible to a very small linear system.
2. **Branco, Clark & Häusser (2010)** showed that real dendrites can nevertheless discriminate the order/velocity of spatially sequenced inputs through location-dependent integration and NMDA-dependent nonlinearities.
3. **TwinProp / Aizenbud et al. (2026)** already show rich, increasingly high-dimensional internal dendritic voltage trajectories during harder optimized tasks, with strong NMDA involvement.

So V23 should not claim that dendrites are high-dimensional, that the soma can collapse internal state, or that nonlinear dendritic activity has high PCA rank.

The narrower question is different:

> **Can a neuron be locally low-order at any one operating state, yet globally hard to emulate because its local input/output operator changes across space and state?**

That is the candidate bridge between the old “state changes geometry” intuition and current neuron-complexity work.

---

## 1. One operator is not enough once local nonlinear state matters

For a linearized neuron around state `x`, write

```text
xdot = A_x x + B_x u
y    = C_x x
```

or, in a transfer/impedance picture,

```text
H_x(omega).
```

A passive or quasi-active model near rest may admit a very low-order approximation at the soma.

But with local voltage-dependent and history-dependent mechanisms,

```text
x_0 -> H_0
x_1 -> H_1
x_2 -> H_2
...
```

The global nonlinear system is therefore not described by one low-order transfer function. It moves through a **family of locally valid operators**.

Call that family, provisionally,

```text
OPERATOR ATLAS = { H_x : x in visited operating states }.
```

This is only a working name. Similar language exists in LPV, gain-scheduled, switched, Koopman and local-linear modeling, so novelty must not be inferred from the name.

---

## 2. Why NMDA makes this concrete

For a passive transfer operator `Z`, local voltage-dependent NMDA can be written schematically as

```text
v = Z [ i_external + I_N(v, g_N) ].
```

Linearizing around a momentary operating state gives an incremental local gain matrix `K_x` and

```text
Z_eff(x) = (I - Z K_x)^(-1) Z
```

under the sign convention used in the Dig derivation.

The important part is not the matrix formula itself. It is the dependency:

```text
morphology / cable geometry  -> Z
current local synaptic state -> K_x
                               |
                               v
                    current effective operator
```

Different dendritic regions can occupy different NMDA operating regimes at the same time.

So even if `Z` is highly reducible at the soma, the *collection*

```text
{ (I - Z K_x)^(-1) Z }
```

may be much richer.

Presynaptic STP adds another source of state dependence because the effective local drive itself depends on history.

---

## 3. A possible explanation of the Aizenbud / TwinProp split

Aizenbud's FCI is a **global emulation-difficulty** measure: a fixed temporal network must emulate the cell over many random input trajectories.

Kellems asks a different question: how many modes are needed to preserve a locally linearized source-to-receiver map.

TwinProp asks another: how much task capacity can be extracted after optimizing synaptic strength/location, and reports increasingly rich/high-rank internal dendritic voltage activity for harder tasks.

These facts suggest a testable decomposition:

```text
complex simulator dimension
    !=
linear receiver-visible order at one state
    !=
number/diversity of receiver-visible operators visited across states
    !=
optimized task capacity
```

The V23 bridge to test is the middle one:

> **Does FCI track the diversity of state-conditioned receiver operators better than it tracks one passive/quasi-active operator?**

If no, kill this bridge.

---

## 4. The cheap version does not require a full Jacobian first

A first approximation can use the existing passive `Z` and local NMDA susceptibility.

For each saved simulation snapshot `s`:

```text
1. record local V_i(s)
2. record local NMDA conductance state g_i(s)
3. compute local incremental gain k_i(s)
4. form diagonal/sparse K_s
5. estimate Z_eff(s)
```

Then choose source/receiver subsets and measure how much `Z_eff(s)` changes over visited states.

Possible summaries:

```text
operator distance:
    || H_s - H_t ||

receiver-signature distance:
    || H_s[:, receiver] - H_t[:, receiver] ||

operator-PCA / effective rank across snapshots

cluster count / regime count under held-out validation

change in Hankel spectrum after local linearization
```

None should be called intrinsic complexity until they predict something outside the data used to define them.

---

## 5. The strongest falsifier: every state is the same small system

Suppose after gain/delay normalization the state-conditioned receiver kernels all lie near one low-dimensional family:

```text
H_x(i,t) ~= a_i(x) * f(t - tau_i)
```

with state mainly changing scalar gains.

Then V23 does not get a rich operator atlas. The nonlinear system may still perform useful thresholding or local dendritic operations, but this particular explanation of FCI is weak.

Conversely, the interesting result would be:

```text
passive / AMPA:
    few receiver-visible shapes / operators

+ NMDA:
    many state-dependent source-to-receiver shapes

+ STP:
    additional history-conditioned operator diversity
```

with the increase predicting either FCI or task capacity across morphologies.

---

## 6. A quantitative object: operator-atlas dimension

Do not freeze this as a metric yet, but a simple prototype is:

For each operating snapshot `s`, vectorize a normalized receiver transfer object:

```text
q_s = vec( normalize(H_s) ).
```

Stack them:

```text
Q = [ q_1, q_2, ..., q_M ].
```

Then measure:

```text
effective rank(Q)
participation ratio(Q)
held-out reconstruction error versus atlas dimension
```

The important control is to remove trivial changes first:

```text
gain
mean firing / conductance level
simple global time shift
input amplitude
```

Otherwise “operator diversity” may simply measure changing overall excitation.

A more principled later version can use distances between balanced realizations / transfer functions rather than raw vectorized kernels.

---

## 7. Why the soma/local-receiver split matters here

The atlas may be small at the soma and large locally.

That would reproduce the receiver-collapse theme in a state-dependent way:

```text
local dendritic receiver:
    many distinguishable regimes

soma:
    compressed projection of those regimes
```

But FCI scores somatic/spike output, so any proposed complexity mechanism must eventually survive the soma/axon projection.

Therefore every local result owes this gate:

> Does the locally distinct regime cause a distinguishable future at the actual downstream receiver?

---

## 8. The “space and time orthogonal” question, translated again

In the passive limit, recent calculations suggest that soma transfer may be close to space/time separable or at least gain+delay separable:

```text
location -> gain + delay
```

If validated, the interesting computation begins where this factorization fails:

```text
location x current local state x recent history
        -> different temporal transfer shape
        -> different receiver future
```

So perhaps the useful question is not whether space and time are orthogonal.

It is:

> **When can the neuron's input/output map be factored into independent spatial and temporal pieces, and which mechanisms deliberately destroy that factorization?**

The failure of factorization is measurable.

---

## 9. Immediate experiment ladder

```text
O0  validate passive solver against exact NEURON model

O1  fit passive gain+delay separability at soma and local receivers

O2  reproduce Kellems-style low-order receiver reduction on one cell
    (or at minimum confirm rapid Hankel/transfer singular-value decay)

O3  add AMPA-only; measure state-conditioned transfer variation

O4  add rat NMDA; repeat

O5  add human NMDA bundle; repeat

O6  split NMDA conductance / kinetics / gamma

O7  add presynaptic STP; repeat

O8  compare operator-atlas measures against FCI across the released morphologies

O9  compare against TwinProp task difficulty / accuracy / dendritic-voltage PCA rank
```

Do **not** begin with O8. The mechanism must work inside one cell first.

---

## 10. Prior-art guardrail: TwinProp already has “rank increases with task difficulty”

The 2026 TwinProp preprint explicitly reports that more PCA components are required to explain dendritic voltage activity as parity-task dimensionality rises, together with increasing NMDA recruitment.

So V23 must not rename that result “operator rank.”

Our proposed object is different:

```text
TwinProp measurement:
    rank of internal voltage trajectories during a task

V23 candidate:
    diversity / order of local input-output operators across operating states
```

The two may correlate. If they collapse to the same information, V23 has added no mechanism.

TwinProp:
- https://www.biorxiv.org/content/10.64898/2026.06.08.730984v1.full

---

## 11. A current 2026 nonlinear-system-ID precedent

A 2026 study of CA3 -> CA1 dendritic transformations used Volterra-series system identification and reported that a second-order model could describe apical dendritic field-response dynamics with >94% accuracy, while basal dendrites required higher order for complete characterization.

- PubMed: https://pubmed.ncbi.nlm.nih.gov/41768319/

That is another warning not to claim that nonlinear transfer-kernel order is a new idea.

But it gives V23 a potentially useful established tool:

```text
first-order kernel  -> linear transfer
second/higher kernels -> interaction / history nonlinearity
```

A location- and receiver-resolved Volterra analysis could therefore be a second route to the same mechanism question if local-linear Jacobian analysis becomes awkward.

---

## 12. Kill conditions

```text
K0 passive transfer is not low-order after exact validation
   -> revise starting premise

K1 NMDA changes gain but not operator shape/order
   -> no operator-atlas expansion

K2 atlas dimension expands but does not survive soma projection
   -> local mechanism only, not FCI explanation

K3 atlas metric does not correlate with FCI across morphologies
   -> not the missing FCI mechanism

K4 atlas metric correlates with FCI but adds nothing beyond area/path/NMDA load
   -> redundant descriptor

K5 it predicts FCI but not optimized task capacity
   -> emulation-complexity result, not computational-power result
```

---

## Current sentence

> **A detailed dendrite may be easy to reduce at any one operating point yet hard to emulate globally if local nonlinear and history-bearing mechanisms make it move through many receiver-distinguishable low-order operators.**

That is now the mechanism worth trying to kill.