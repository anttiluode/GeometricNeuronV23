# GeometricNeuronV23 — method

## 0. The method is part of the project

V23 is not just an architecture sketch. It is also a way of preventing the sketch from drifting into a story that cannot be falsified.

The working rule is:

> **Every interesting sentence must either point backward to established evidence or forward to an experiment that can kill it.**

This is the research analogue of a proof assistant / type checker.

A paper can supply an already-tested lemma. A code audit can establish what a model actually contains. A simulation can discharge a new mechanistic obligation. A null result can invalidate a dependent claim.

The repository should preserve that dependency structure.

---

## 1. Claim graph

### Claim C0 — local synaptic state contains recent-history information

Established ancestors:

- Tsodyks–Markram dynamic synapses;
- Maass & Markram dynamic memory buffers;
- Mongillo et al. activity-silent synaptic memory;
- Oesch & Diamond release-pool history.

V23 obligation:

```text
Given a chosen V23 local-state model,
show exactly what aspects of recent input history are recoverable from its state / next response.
```

Do not simply call `R` or `u` “time.”

### Claim C1 — geometry changes how local state becomes useful

Established ancestors:

- dendritic cable / Green functions;
- compartmentalization;
- nonlinear dendritic subunits;
- receiver-specific dendritic output.

V23 obligation:

```text
Hold local state dynamics fixed.
Change only placement / coupling geometry.
Show a measurable difference that cannot be reduced to gain or state count.
```

### Claim C2 — pairing temporal state with geometric address matters

This is the key interaction claim.

V23 obligation:

```text
same geometry
same state count
same parameter multiset
same inputs
same output budget

STRUCTURED placement
vs
SHUFFLED placement
```

If the two are equivalent, geometry and local temporal memory may both matter separately but V23 has not established a special interaction between them.

### Claim C3 — receiver-relative computation matters

Established ancestor:

- starburst amacrine cell: dendritic Ca direction selectivity can be absent from somatic voltage.

V23 obligation:

```text
define receiver set explicitly
show which distinctions survive / disappear under receiver projection
```

### Claim C4 — the mechanism provides useful artificial computation

V23 obligation:

```text
compare against matched baselines
not merely against a stateless perceptron
```

Possible matched baselines:

- same state dimension, dense recurrent matrix;
- same state dimension, random sparse graph;
- same state dimension, learned RNN/GRU;
- TCN with matched or reported parameter budget;
- reservoir with matched decay spectrum;
- graph network with fixed weights but no edge state.

### Claim C5 — V23 says something about biological neuron complexity

V23 obligation:

Keep separate:

```text
emulation difficulty
intrinsic state dimension
information available at a receiver
task capacity after optimization
```

Do not use one as a synonym for the others.

---

## 2. Local-state unit test: what does one synapse remember?

Use a minimal deterministic Tsodyks-Markram-style resource/facilitation model first.

One possible state:

```text
R(t)   available resource
u(t)   utilization / facilitation
```

Between events use the chosen canonical equations. At events update release and state exactly according to the selected model.

### Protocol A — paired-pulse age curve

```text
conditioning event at t=0
probe event at t=Delta
```

Sweep `Delta` logarithmically.

Record:

```text
R(Delta-)
u(Delta-)
probe released amount
probe postsynaptic conductance peak
```

Question:

```text
Can Delta be estimated from the local state / probe response?
Over what range?
With what ambiguity / noise sensitivity?
```

### Protocol B — history collision

Construct different prior spike histories with the same final inter-event interval.

Ask whether they produce the same state.

If not, the synapse is not merely an “age detector”; it carries a compressed statistic of a longer history.

That result is important and should replace any over-simple clock metaphor.

---

## 3. The first geometry test

Use a small fixed dendritic tree or graph with a known receiver.

Each contact gets identical local dynamics.

Measure source-to-receiver impulse responses:

```text
h[r <- i](t)
```

Then introduce the local edge state.

Compare events arriving at the same absolute time but at contacts with different internal histories.

The primitive measurement is:

```text
Delta y_r(t)
    = output difference caused by local-state difference at source i
```

Map this over locations.

This yields a local-state observability field:

```text
location i
    -> how visible is a perturbation of z_i at receiver r?
```

This is already useful even if no learning is used.

---

## 4. Structured-versus-shuffled test

Choose two or more local temporal phenotypes, for example:

```text
fast recovery
slow recovery
facilitating
depressing
```

Assign them across locations using a rule that can be stated before looking at task performance.

Examples:

```text
proximal vs distal
high- vs low-input-impedance region
high- vs low-transfer-to-receiver region
separate dendritic subtrees
```

Then compare:

```text
A. structured assignment
B. many random shuffles of the exact same labels
C. homogeneous mean-parameter control
```

Pre-register the statistic before running the large sweep.

Possible statistics:

- mutual information about recent input at receiver;
- linear separability of temporal classes;
- delayed XOR / context gating accuracy;
- receiver trajectory effective rank;
- task accuracy under a fixed readout;
- emulation error of a constrained surrogate.

The strongest result is not `A > C`; it is `A` outside the shuffle distribution of `B`.

---

## 5. Geometry controls

The phrase “geometry matters” is too easy to win unless geometry controls are harsh.

Use at least:

### G0 — same graph, permuted local state labels

Tests temporal-state/address pairing.

### G1 — degree-preserving rewiring

Preserve approximate local degree but alter paths / receiver transfer.

### G2 — response-matched surrogate graph

Fit a simpler graph to match basic source-to-receiver attenuation / latency statistics.

If V23 still wins, the useful structure is subtler than those marginals.

### G3 — remove geometry but preserve state dimension

Dense or recurrent baseline with the same number of state variables.

This tests whether the effect is simply “more memory.”

---

## 6. Receiver controls

Define receiver sets before scoring.

```text
R_soma       one global scalar
R_local      selected local branches
R_multi      several output ports jointly
```

For biological models, useful outputs may be:

```text
somatic voltage
spike output
local dendritic voltage
local calcium
local transmitter-release proxy
```

For artificial V23 models, the analogue can be multiple learned/read-only ports.

Do not let a richer receiver set win by simply giving the classifier more dimensions without matching downstream readout capacity.

---

## 7. Aizenbud / FCI-specific gate

The released FCI baseline is valuable because it already standardizes many things, but V23 should not confuse its omitted presynaptic STP with an error.

Treat it as an intervention opportunity.

On one exact morphology first:

```text
F0  released deterministic AMPA/NMDA conductance synapse

F1  restore a canonical presynaptic dynamic-resource mechanism
    same receptor kinetics
    same source spike trains

F2  dynamic mechanism with shuffled tau_rec/tau_fac across sites

F3  homogeneous dynamic mechanism with matched mean release
```

Before comparing any FCI-like surrogate difficulty:

match or report:

```text
mean excitatory charge / conductance budget
output firing rate
input rate
synapse count
receptor kinetics
```

Start with AMPA-only if the immediate question is STP × geometry. Add NMDA later.

### Why AMPA-only first?

Because NMDA introduces local voltage-dependent feedback. That is interesting, but it creates another interaction:

```text
local resource history
    -> released conductance
    -> local voltage
    -> Mg block / NMDA current
    -> state-dependent dendritic propagation
```

V23 should first establish the simpler interaction before adding this one.

---

## 8. Retina gate

Use the open starburst-amacrine model associated with Srivastava et al. 2022:

https://github.com/geoffder/spatiotemporal-starburst-model

The model already provides spatially separated sustained/transient bipolar inputs and records soma / terminal signals.

### R0 — reproduce native receiver dependence

Run the authors' motion conditions and quantify direction dependence at multiple receivers.

### R1 — temporal-kernel shuffle

Preserve the temporal-kernel multiset but permute sustained/transient identity across locations.

### R2 — local-history extension

Only after reproducing the fixed-kernel result, replace/add a history-dependent presynaptic mechanism and repeat structured-vs-shuffled tests.

This gives V23 a biologically grounded system where both receiver choice and spatial arrangement of temporal dynamics already matter.

---

## 9. Artificial benchmark ladder

Do not start with MNIST or static classification. V23 should be tested first on tasks that require the resource it claims to provide.

### T0 — interval discrimination

Two pulses; classify / regress interval.

Tests local temporal state only.

### T1 — location × interval conjunction

Same interval means different things at different spatial addresses.

Tests whether geometry/address and time interact.

### T2 — delayed XOR across separated branches

Two branch-local events with delay; output depends on their conjunction/history.

### T3 — context pulse + later local event

Global or branch context arrives first; later event must be interpreted differently depending on lingering state.

This is the clean artificial analogue of:

```text
old local/global state + present input -> different local future
```

### T4 — sequence task with source reuse / dendro-plexing

One temporal source appears at multiple contacts. Compare one-contact and multi-contact versions.

---

## 10. Baseline fairness

A V23 comparison should report at least:

```text
trainable parameter count
persistent state dimension
number of nonlinear state updates per step
input/output dimensionality
receiver dimensionality
compute cost
```

If V23 uses heterogeneous fixed time constants, compare to a baseline with the same time-constant spectrum but no geometry assignment.

If V23 uses learned geometry, compare to a recurrent model with a comparable number of learned connections.

If V23 uses multiport output, compare to a baseline with the same output bandwidth.

---

## 11. What to measure inside the model

Do not rely only on task accuracy.

Record:

```text
local state trajectories z_i(t)
source-to-receiver responses
state perturbation observability
receiver trajectory rank / spectrum
history decoding from local and global state
shuffled-vs-structured effect size
energy / update sparsity if relevant
```

Useful question:

```text
Which local histories remain causally alive at time t,
and at which receivers are they still distinguishable?
```

That is a more precise descendant of the older “wide present / pivot / local future” language.

---

## 12. Negative results we want

V23 should make room for clean losses.

Examples:

```text
STP helps but placement does not
    -> local memory result, not geometric-time result

structured placement helps only because mean gain differs
    -> normalization artefact

multiport readout helps but soma does not
    -> receiver result, not necessarily architecture result

NMDA creates the whole effect
    -> nonlinear dendrite result; narrow V23 accordingly

RNN with matched state dimension matches everything
    -> biological interpretation may remain interesting,
       but no AI architecture advantage established
```

These are successful experiments because they identify which dependency actually carries the phenomenon.

---

## 13. Research ledger format

For each new claim, add a small block:

```text
CLAIM:

SUPPORT ALREADY IN LITERATURE:

DERIVATION / INFERENCE:

UNTESTED ASSUMPTIONS:

CHEAPEST KILL TEST:

RESULT:

STATUS:
    open / narrowed / killed / survives
```

This is the V23 equivalent of a proof obligation.

It lets the repository stay imaginative without letting imagination quietly become evidence.