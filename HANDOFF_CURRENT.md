# GeometricNeuronV23 — CURRENT HANDOFF

**Updated:** 2026-08-15, seventh pass — passive and synthetic nonlinear address × STP gates closed; next online gate must be biological

**Status:** active falsification/discovery program. Nothing here is a novelty claim.

## Read in this order

1. `JOINT_ADDRESS_STP_NONLINEAR_POC_V01_RECEIPT.md` — current result: local nonlinear feedback helps the task but exact STP→address shuffle remains null.
2. `JOINT_ADDRESS_STP_ORDER_POC_V02_RECEIPT.md` — strongest passive-tree result: three-seed strict shuffle null.
3. `GROWTH_AS_ADAPTIVE_SAMPLING_COLLISION.md` — literature collision for dendritic/spine growth as acquiring new input streams.
4. `MORPHOLOGY_AS_ACCESS_GEOMETRY.md` — separates online transfer geometry from geometry of physically reachable synaptic partners.
5. `JOINT_ADDRESS_STP_COLLISION.md` — prior-art boundary around joint address × full STP.
6. `PARK_APICAL_STATE_SHUFFLE_RECEIPT.md`, `PARK_APICAL_I1_CORRECTION.md`, `PARK_HISTORY_CAUSAL_RECEIPT.md`, `PARK_TWO_COMPARTMENT_CONTROL_RECEIPT.md` — Park calibration / negative narrowing.
7. `GEOMETRY_STATE_COMMUTATOR_V02.md`, `FULL_STATE_GEOMETRY_HISTORY_DECOMPOSITION.md`, `CHRONOLOGY_LOCALITY.md` — mathematical nulls, now closure tools rather than discovery priority.

---

# Executive status

Two different geometry hypotheses have now been separated.

## A. Fixed morphology as an online soma transfer machine

Current evidence is negative for **exact address × local temporal-state specialization** in the regimes tested so far:

```text
passive soma transfer dictionary             nearly separable
Park detailed history-state address          not privileged for tested metric
passive address × learned STP                 strict shuffle null
balanced passive address × STP, 3 seeds       strict shuffle null
smooth local voltage feedback × STP           strict shuffle null
```

The strongest passive address × STP result remains:

```text
balanced forward/reverse task
3 independent seeds
60 strict within-afferent STP-tuple shuffles per seed

TREE:
fixed loss mean               0.5493544   acc 1.0
location-only                 0.2873722   acc 1.0
STP-only                      0.2771257   acc 1.0
joint                         0.1240620   acc 1.0

joint shuffle loss ratio      1.0000005806
baseline/shuffled acc         1.0 / 1.0
```

The new nonlinear kill-gate made the toy task much easier but did not create address binding:

```text
tree nonlinear, beta=2, one seed, 40 shuffles

joint baseline loss           0.00087783398
joint shuffled loss mean      0.00087751875
joint shuffle loss ratio      0.9996408992
baseline/shuffled acc         1.0 / 1.0
```

So spatial filtering, local nonlinear feedback and temporal synaptic state can all be useful while still **not becoming mutually specialized by exact address**.

Do not tune the passive task, threshold, `beta`, or diversity rewards to manufacture a placement effect.

## B. Morphology as access/search geometry

The growth discussion exposes a role today's electrical nulls do not test:

```text
morphology -> which axons/boutons are physically reachable
           -> which new input streams structural plasticity can acquire
```

This is established neurogeometry territory (`potential synapses`; Stepanyants/Chklovskii) and established structural plasticity, not a novelty claim.

Hedrick et al. 2022 is strikingly close to the naive “new viewpoint” intuition: learning-related filopodia locally sample adjacent neuropil for candidate axonal partners, and a majority of surviving new spines contact axons previously unrepresented in those dendritic domains.

Pitcher et al. 2026 provides actual growth feedback: developing starburst dendrites compute retinal-wave direction, and that local computation biases subsequent dendritic growth.

Thus the tree can be weak as a passive temporal operator at one receiver while still being important as a **physical search manifold over possible connectivity**.

---

# Park branch: stopped correctly

Exact Park 2025 public software was fetched, compiled and executed in NEURON.

What survived:

```text
local history matters strongly                         YES
soma-dendrite coupling matters                         YES
state-conditioned distal accessibility exists          YES
correct distal-apical small-signal state effect         MODEST (~10-12%)
detailed history-state address strongly enhances it     NO
detailed tree required for broad accelerometer motif    NO
```

The author-released two-compartment model already produces the qualitative history-dependent window. Path-distance-matched apical state-address shuffles did not show the real detailed arrangement to be privileged. Therefore the full Jacobian/Magnus decomposition remains optional mechanistic closure, not the next discovery bet.

---

# Joint address × STP prior-art boundary

Already occupied:

```text
realistic dendrite + learned STP                  Carvalho & Buonomano 2011
learned STP shuffle                               Carvalho & Buonomano 2011 / later work
learn full temporal STP parameters                Buonomano et al. 2026 preprint
optimize synaptic location + strength             TwinProp 2026 preprint
biological spatial STP gradients                  established
```

Still not found in the literature pass as one closed package:

```text
realistic morphology
x jointly optimized synaptic address
x jointly optimized full presynaptic STP kinetics
x strict post-training temporal-tuple/address shuffle
x analysis against receiver-transfer coordinates
```

But the executed synthetic gates now say **do not port the passive or smooth-threshold versions straight to a huge realistic cell**. Neither passive filtering nor the simple regenerative feedback produced the interaction.

---

# Important correction to the too-negative interpretation

Today's results do **not** justify saying “dendritic shape is useless.”

TwinProp's 2026 preprint reports on 4-bit parity:

```text
intact L5PC                         99.4%
passive dendrites, NMDA retained    78.1%
soma-only, channels+NMDA retained   76.9%
no NMDA, channels retained          73.8%
LIF                                 68.8%
```

Their interpretation is interaction: **NMDA synaptic nonlinearities + voltage-gated dendritic conductances acting on morphology**. Neither passive morphology+NMDA nor voltage-gated channels without NMDA is enough.

So the earned negative is narrower:

> passive / nearly separable geometry and a simple smooth local-voltage feedback do not create strong exact address × temporal-state binding in our tests.

The biologically interacting regime remains live.

---

# Synthetic local-nonlinearity branch: now closed

`joint_address_stp_nonlinear_poc.py` added the smallest possible mechanism that could break passive separability without pretending to be a biological NMDA model.

For every candidate site it computed:

```text
source -> same-site local voltage kernel
source -> soma transfer kernel
```

and then:

```text
STP release
 -> local voltage
 -> global smooth threshold / regenerative current
 -> propagation from that same site to soma
```

The threshold was calibrated before training from a canonical homogeneous fixed-STP burst.

GitHub Actions run:

```text
31883664252
```

completed successfully. The decisive nonlinear-tree result was:

```text
baseline joint loss        0.00087783398
shuffle mean loss          0.00087751875
shuffle loss ratio         0.9996408992
baseline/shuffle acc       1.0 / 1.0
```

The matched isopotential nonlinear control was exactly shuffle-invariant (`0.9999998597`).

Verdict:

> **LOCAL-SMOOTH-THRESHOLD NO ADDRESS×STP ADVANTAGE.**

This branch obeys its preregistered stop condition. Do not sweep `beta` or threshold looking for a win.

---

# Next online-computation gate: biological interaction, not more toy tuning

If the address × local-history idea is going to survive as an online dendritic computation, the next test should include the interaction class that current realistic-neuron work says matters:

```text
NMDA voltage dependence
+
active dendritic conductance / branch event
+
real morphology
+
local history-bearing synaptic state
```

The important control remains unchanged:

```text
same morphology
same afferents
same learned/fixed STP multiset
same total parameter/state budget
same task

STRUCTURED: temporal tuples at their trained/assigned addresses
SHUFFLED:   the exact tuples reassigned among matched addresses
```

Before implementing this, collide the exact mechanism against primary literature and identify the smallest public model in which the NMDA × active-conductance interaction is already validated. Prefer an existing author model over hand-writing another pseudo-biological threshold.

The useful question is no longer “can nonlinearity help?” It plainly can. It is:

> **Does a biologically grounded state-dependent dendritic event make the identity of a local temporal synaptic state inseparable from the electrical address at which it lives?**

If the answer is again no, stop pushing this online-address-binding branch and move more attention to receiver multiplicity and access/growth geometry.

---

# Growth / “new viewpoint” idea

The broad idea already has strong prior art.

### Hedrick et al. 2022, Nature Neuroscience

```text
existing task-related cluster potentiates
 -> local filopodia grow
 -> sample nearby neuropil / candidate axons
 -> co-active contacts stabilize
 -> majority of new spines contact axons previously unrepresented in the domain
```

This is almost a literal biological “acquire another input stream” mechanism.

### Pitcher et al. 2026, Cell Reports

Developing starburst dendrites decode the propagation direction of retinal waves and convert that computation into biased dendritic growth. Thus:

```text
current computation -> growth direction -> future morphology -> future computation
```

### Levy & Baxter 2023, Neural Networks

Direct computational collision: dendritogenesis + adaptive synaptogenesis, with dendrites added as novel experiences/latent mixture components accumulate; improved capacity / reduced catastrophic interference / mixture unmixing.

Therefore do not claim “grow dendrites for new data/views” as new.

The sharper possible question is:

> **Does local computation/error control structural exploration so that growth acquires physically reachable input streams carrying conditional information missing from the current local representation, and does nonlinear dendritic/receiver context change that acquisition policy?**

That needs another literature collision before an expensive build.

---

# Transfer geometry vs access geometry

Keep these separate:

```text
transfer geometry
    what morphology does to an already connected signal

access geometry
    which presynaptic signals morphology makes physically connectable
```

Stepanyants et al. 2008 estimated multiple potential synaptic targets within spine reach in cortical/hippocampal neuropil and treated this geometry as a reservoir for structural rewiring. So access geometry is established.

Today's electrical nulls bear mainly on transfer geometry. They do **not** show that arbor geometry is irrelevant to connectivity opportunity.

---

# Receiver hypothesis: still interesting but crowded

Starburst amacrine biology strongly supports receiver-relative local computation: branch calcium/output can be direction selective even when somatic voltage is not.

But do not claim ANN units universally have one scalar output. Multi-output dendritic artificial neurons already exist, as do vector-valued units and many multi-branch/multi-head architectures.

A narrower future test could hold total state and parameter budget fixed and compare:

```text
one pooled soma-like receiver
vs
K receiver-specific local branch projections
```

then ask whether structural growth becomes more useful when newly acquired branch information is not immediately collapsed through one output bottleneck.

This exact intersection needs prior-art collision before execution.

---

# Current decision tree

```text
1. Synthetic threshold gate is CLOSED NULL.
   Do not tune it.

2. Online address-binding branch:
      literature-collide and, only if warranted, run the smallest public
      real-morphology model containing NMDA voltage dependence + active
      dendritic conductance/branch events + local temporal synaptic state.

3. If that biological interaction also gives strict shuffle ~= 1:
      stop escalating address × STP as the main discovery bet.

4. In parallel, keep growth/access geometry separate:
      morphology may matter by changing what the neuron can connect to,
      not because passive soma transfer is rich.

5. Before building a growth+multi-receiver architecture, collide the exact
   intersection against structural-plasticity and multi-output-neuron literature.
```

## Current one-line state

> **Passive filtering and a smooth local regenerative nonlinearity both failed to bind learned temporal synapse state to exact dendritic address. The next online gate must be a real NMDA × active-dendrite interaction; separately, morphology remains live as access/search geometry and receiver-relative computation.**
