# Morphology as access geometry, not only transfer geometry

**Date:** 2026-08-15  
**Status:** conceptual reclassification anchored in established neurogeometry. **Not a novelty claim.**

Today's nulls mostly interrogated a fixed morphology as an **electrical transfer operator**:

```text
chosen synaptic site
    -> dendritic filtering / active transformation
    -> receiver
```

The growth discussion exposes a different role of morphology that those tests do not address:

```text
surrounding axons / boutons
    -> which synaptic contacts are physically possible
    -> which input streams the neuron can ever sample
```

Call these, provisionally:

```text
transfer geometry   = what the tree does to an already connected input
access geometry     = which inputs the tree can physically acquire
```

The labels are bookkeeping, not new scientific terms.

## Established prior art

Stepanyants, Chklovskii and colleagues developed the concept of **potential synapses**: sufficiently close axon–dendrite appositions that could be converted into actual contacts by spine growth.

Stepanyants et al., J Neurosci 2008, *Structural Plasticity of Circuits in Cortical Neuropil* (PMID 18716206) estimated that an average dendritic spine could choose among roughly 4–7 potential targets in rodents and 10–20 in primates in the systems they analyzed. Their framework explicitly treats local neurogeometry as a large reservoir of possible circuit rewiring.

Therefore the statement

> morphology constrains the set of presynaptic partners available to structural plasticity

is established neurogeometry, not V23 novelty.

Hedrick et al. 2022 then supplies a learning experiment compatible with this picture: nearby filopodia sample local neuropil for candidate axonal partners, and a majority of surviving new spines contact axons previously unrepresented in that dendritic domain.

Pitcher et al. 2026 supplies actual activity-dependent dendritic growth: a dendritic computation of retinal-wave direction biases subsequent outgrowth.

## Why today's passive null does not touch this

Suppose the soma transfer is nearly separable:

```text
H_soma<-i(t) ~= a_i f(t-tau_i).
```

That can make many already-connected sites electrically interchangeable at the soma.

But changing dendritic reach can still alter the *candidate input set*:

```text
C(morphology) = {axons/boutons close enough to become synaptic partners}.
```

Two morphologies can therefore have nearly identical passive receiver kernels for their existing synapses while exposing different sets of potential presynaptic variables.

Likewise, reducing a huge fixed compartmental neuron to a small receiver-visible state does not imply that the original arbor was irrelevant to which axons it could contact.

So do not collapse these two questions:

```text
Q1: does fixed geometry create rich online soma dynamics?
Q2: does geometry define a useful structural search/access space for connectivity?
```

Today's results are mostly negative for Q1 in the passive regime. They say almost nothing about Q2.

## The sharper computational analogy

Morphological/spine growth is closer to **adaptive sensor placement / feature acquisition** than to simply adding hidden state.

At any time the neuron has an observed feature set `x_S`. Growth changes the feasible candidate set and may add a new stream `z_j`:

```text
S -> S union {j}.
```

The useful question is not whether the new branch has an exotic transfer kernel. It is whether the new geometry gives access to information unavailable through the old synaptic set.

A strict test should therefore distinguish:

```text
more contacts to already represented axons
vs
new contacts to previously unrepresented axons
vs
new dendritic branch exposing a genuinely different candidate pool
```

and match total synapse/parameter/energy cost.

## Current reframing

> **The tree may be weak as a passive online temporal computer at one receiver yet important as a physical search manifold over possible connectivity.**

That statement is compatible with today's nulls and with established structural-plasticity literature.

The possible V23 contribution would have to go beyond the established potential-synapse concept: e.g. demonstrating a task-dependent law connecting local computation/error to where structural exploration occurs, what new conditional information is acquired, and whether local nonlinear/receiver context changes that acquisition policy.
