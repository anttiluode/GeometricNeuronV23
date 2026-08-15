# Growth as adaptive sampling / acquiring new input views — literature collision

**Date:** 2026-08-15  
**Status:** literature map and hypothesis sharpening. **Not a novelty claim.**

## Seed intuition

A naive but useful question arose after the passive address × STP null:

> What if dendritic/spine growth is not mainly “more internal compute,” but a way for a neuron or dendritic branch to acquire a new viewpoint on the input — new synapses / new axonal streams when the currently sampled inputs are insufficient?

The broad idea is **not new**. In fact, several respectable papers get strikingly close. The useful remainder is to turn “viewpoint” into a measurable structural sampling problem and ask what is still missing.

---

## 1. Hedrick et al. 2022 is almost the literal biological version

Hedrick NG et al., *Learning binds new inputs into functional synaptic clusters via spinogenesis*, Nature Neuroscience 25:726–737 (2022). DOI: 10.1038/s41593-022-01086-6.

Longitudinal in-vivo two-photon imaging plus correlated EM in mouse motor cortex supports a concrete sequence:

```text
potentiated task-related local spine cluster
    -> nearby filopodial outgrowth
    -> local sampling of adjacent neuropil / candidate axonal partners
    -> successful co-active contacts stabilized
    -> new spines join the functional cluster
```

The especially important observation for the “new viewpoint” intuition is that **a majority of new spines contacted axons that had previously been unrepresented in those dendritic domains**.

So a defensible biological sentence is already:

> **Learning-related structural plasticity can locally sample candidate axons and bind previously unrepresented input streams into an existing functional dendritic cluster.**

This is stronger and more concrete than “growth adds capacity.” It is directly about acquiring new input streams.

Important limit: this paper studies new spines/filopodia around existing dendritic segments during motor learning, not arbitrary large-scale dendritic arbor growth in the adult cortex.

---

## 2. Pitcher et al. 2026 closes an even stranger loop: computation can instruct dendritic growth

Pitcher MN, Gonzales ASB, Habib R, Feller MB, *Retinal waves shape starburst amacrine cell dendrite development through a direction-selective dendritic computation*, Cell Reports 45:117476 (2026). DOI: 10.1016/j.celrep.2026.117476.

This is actual dendritic growth, in development rather than adult learning.

Developing starburst amacrine dendrites already compute the direction of spontaneous retinal waves. A nasal wave-propagation bias preferentially activates nasal-oriented dendrites, and that local direction-selective computation is converted into asymmetric dendritic growth. Perturbing the wave bias reduces the growth asymmetry.

The conceptual loop is therefore experimentally grounded:

```text
current dendritic computation
    -> detects structured activity
    -> biases where the dendrite grows
    -> changes the future morphology / sampling geometry
    -> changes future computation
```

This is extremely relevant to V23 because it says morphology need not be a fixed prior. **The computation itself can participate in constructing the morphology that will process later input.**

Again, this is not a V23 discovery: it is a 2026 peer-reviewed biological result.

---

## 3. Sehgal et al. 2025: branches are also allocation coordinates for new memories

Sehgal M et al., *Compartmentalized dendritic plasticity in the mouse retrosplenial cortex links contextual memories formed close in time*, Nature Neuroscience 28:602–615 (2025). DOI: 10.1038/s41593-025-01876-8.

Two contexts learned close in time preferentially reactivate overlapping dendritic segments, and new spine clusters for the two linked memories are preferentially allocated to the same dendritic segments. Reactivating the first-context dendrites is sufficient to bias memory linking.

So dendritic address is not merely a passive cable coordinate. It can be an **allocation coordinate** for future structural plasticity.

This is compatible with the adaptive-sampling view but does not itself show that new spines specifically acquire residual/previously missing information.

---

## 4. Levy & Baxter 2023 is a direct computational prior-art collision

Levy WB, Baxter RA, *Growing dendrites enhance a neuron’s computational power and memory capacity*, Neural Networks 164:275–309 (2023). DOI: 10.1016/j.neunet.2023.04.033.

Their algorithm combines dendritogenesis with adaptive synaptogenesis. New dendrites are added as novel experiences / latent mixture components accumulate; dendrites become feature clusters. They report enhanced memory capacity, reduced catastrophic interference, and mixture unmixing.

Therefore V23 cannot claim as new:

```text
grow dendrites when data complexity increases
growing dendrites as extra feature clusters
dendritogenesis to increase memory/capacity
data-driven dendrite creation in an artificial neuron
```

The interesting seam must be narrower.

---

## 5. “Viewpoint” translated into a falsifiable object

The useful residue is **adaptive measurement / input-channel acquisition**.

Suppose the current neuron/branch samples presynaptic features `x_S` and predicts target/task variable `y`:

```text
y_hat = f(x_S)
r = y - y_hat
```

A candidate new presynaptic stream `z_j` is useful only if it carries information not already represented by `x_S`.

Classical proxies include:

```text
|<r, z_j>|                       residual correlation
I(z_j ; y | x_S)                conditional mutual information
Delta task loss after adding j   direct marginal utility
```

Those are standard feature-selection / matching-pursuit / information-theoretic ideas; none is a novelty claim.

The biological twist suggested by Hedrick is that the proposal set is **not global**. A spine/filopodium samples axons physically available in nearby neuropil. Thus structural learning is a constrained search:

```text
current functional dendritic domain
    -> local candidate axons permitted by anatomy
    -> exploratory contacts
    -> local coactivity / utility test
    -> stabilize useful new stream; reject others
```

So “new viewpoint” should not mean an abstract arbitrary feature. It means a **new physically reachable input stream that adds conditional information to a local dendritic computation**.

---

## 6. Relation to today's nulls

Today's passive soma results do **not** imply dendritic structure is generally useless.

They establish narrower constraints:

```text
passive source->soma transfer is nearly separable
passive address × learned STP did not bind
Park's specific detailed history-state address was not privileged
```

TwinProp (Aizenbud et al. 2026 preprint) reports a different regime: intact active L5PC 99.4% on 4-bit parity, passive dendrites+NMDA 78.1%, soma-only 76.9%, no-NMDA 73.8%. Their interpretation is that **NMDA nonlinearities and voltage-gated dendritic conductances acting together on the morphology** provide the richer computation.

Therefore “nothing about shape survived” is too strong. What has failed so far is **passive / weakly coupled geometry as the special ingredient**.

---

## 7. Receiver idea: useful, but not an empty field

Starburst amacrine cells give a biological reason to care about local outputs: individual dendritic branches can carry direction-selective calcium/output signals that are absent or weakened in somatic voltage, and individual output synapses can be functionally compartmentalized.

But artificial multi-output neuron ideas already exist. For example Ding et al. (Knowledge-Based Systems 2024, DOI 10.1016/j.knosys.2024.111442) explicitly proposed a multi-input/multi-output dendritic neuron with a learnable matrix mapping dendrites to outputs. Vector-valued neural units and capsule-like representations are also old.

So do not claim:

```text
ANN units have never had multiple outputs
multi-output dendritic artificial neurons are new
```

A narrower question could still be worthwhile:

> Under a fixed state/parameter budget, does preserving **receiver-specific local branch information** change the utility or allocation rule of structural growth compared with pooling all branches through one scalar soma-like receiver?

That exact interaction requires another literature collision before building it.

---

## 8. Strong next hypothesis after the passive null

The next executable V23 gate is intentionally smaller:

> **Does a local voltage-dependent regenerative nonlinearity create mutual specialization between synaptic temporal dynamics and dendritic address where a passive tree did not?**

That is being tested separately in `joint_address_stp_nonlinear_poc.py`.

If even that minimal thresholded feedback remains shuffle-invariant, do not tune it to win. Move to a biologically grounded interacting-nonlinearity model (NMDA + active dendritic conductance), because TwinProp suggests that the combination—not passive geometry or one isolated nonlinearity—is the relevant regime.

Only after that should structural growth be added.

---

## 9. Candidate growth experiment, if the nonlinear gate earns it

A clean future factorial would separate three questions:

```text
A. can weights / STP adapt without new input channels?
B. can new synapses sample previously absent presynaptic streams?
C. can new dendritic subunits/branches create new local nonlinear contexts or receivers?
```

At a fixed cost budget, give the model a stream of tasks or mixture components. When residual error remains, allow either:

```text
control 1: add another synapse from an already represented input stream
control 2: add a synapse from a new candidate input stream
control 3: create a new dendritic subunit and populate it from local candidates
```

Then ask whether growth preferentially captures **conditional residual information**, whether the new input stream is genuinely previously unrepresented, and whether local nonlinear/receiver structure adds anything beyond ordinary sparse feature selection.

The required matched controls are severe because otherwise this reduces to “more parameters help.”

---

## Current sentence

> **Dendritic growth can be viewed as constrained structural sampling: an existing local computation can bias exploration of nearby candidate inputs, stabilize previously unrepresented streams that add useful information, and thereby change the future input basis of the neuron. Biology already demonstrates major pieces of this loop; the open question is what additional computational principle, if any, emerges from coupling that adaptive sampling to nonlinear dendritic address and receiver structure.**
