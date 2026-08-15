# GeometricNeuronV23

## Geometry with local state

**Status:** research program / prototype architecture, not a novelty claim and not yet a positive experimental result.

> **“Silliness” is a search mode, not a standard of evidence.**
>
> V23 is allowed to begin from odd intuitions. It is not allowed to keep them merely because they are beautiful. The point of this repository is to translate the intuition into mechanisms that already exist in neuroscience, connect those mechanisms correctly, and then build experiments in which the combined claim can fail.

GeometricNeuronV23 starts from a narrower and more serious version of the old Geometric Neuron intuition:

> **A biological connection is not just a weight. It can have a location, a local hidden state, a history-dependent response, and a receiver-dependent future. Geometry determines how those local states are coupled.**

The immediate scientific ancestors are not obscure. They include cable theory and Green-function dendritic transfer, nonlinear dendritic subunits, NMDA spikes, short-term synaptic plasticity, activity-silent synaptic memory, electrical compartmentalization, distributed dendritic readouts, and recent work measuring / optimizing the computational complexity of detailed cortical neurons.

The claim to earn is therefore **not** “biology secretly discovered V23.” The claim to earn is whether putting these established pieces together in the particular V23 way gives a useful artificial neuron or a better measurement of what a biological neuron is doing.

---

## 1. The point-neuron boundary we are crossing

McCulloch & Pitts gave us the enormously useful abstraction

```text
many inputs -> one unit -> one output
```

and most artificial neural networks still inherit that interface.

But several lines of neuroscience show that the interior of one biological neuron can itself contain useful computation:

```text
spatially addressed input
      |
      v
local dendritic / synaptic dynamics
      |
      +----> local output / release site
      |
      +----> other dendritic regions
      |
      +----> soma / axon
```

V23 treats the soma/axon as **one important receiver**, not automatically the definition of the whole computational object.

For a set of source locations `S` and receiver locations `R`, the linearized physical object is naturally multi-input / multi-output:

```text
H_R<-S(t)
```

with entries

```text
h[r <- i](t)
```

asking what a perturbation at source `i` does at receiver `r` after time `t`.

That is ordinary systems/cable language. The V23 step is to give each source/contact a local hidden state as well.

---

## 2. A synapse is not merely a weight

For synapse/contact `i`, write a local state

```text
z_i(t) = [
    receptor conductance state,
    release/resource state,
    facilitation state,
    calcium or other local state,
    ...
]
```

A presynaptic event does not simply multiply by `w_i`.

It arrives at a local physical state, **samples it**, changes it, and generates a current or release event whose effect then propagates through the cell.

Schematic:

```text
incoming event
    + local history z_i(t-)
    + local voltage v_i(t-)
        |
        v
local transmission / state update
        |
        v
current or release event
        |
        v
geometry-dependent propagation to receiver set R
```

This makes a useful distinction among four kinds of memory:

```text
1. cable / membrane memory
   capacitive relaxation + dendritic modes

2. receptor-kernel memory
   AMPA / NMDA / GABA conductance traces

3. synaptic resource memory
   depression / facilitation / recovery / release state

4. structural memory
   morphology, contact locations, long-term weights
```

The standard released Aizenbud FCI synapse contains (1), (2), and (4), but its normal `AMPANMDA_EMS` path omits the presynaptic recovered/unrecovered, utilization, depression and facilitation machinery of the older BBP probabilistic mechanism. In other words:

> **FCI keeps postsynaptic conductance-trace memory but removes presynaptic resource/release memory.**

That missing mechanism is a clean V23 experimental knob.

---

## 3. “Local time” without inventing a new clock

The phrase that motivated this version was roughly:

> a synapse can sit locally carrying an unfinished piece of recent history until a later network event reaches it, at which point that local history changes what rejoins the larger dynamics.

The scientific translation does not require literal frozen time.

For a simple depressing resource variable `R`, between release events:

```text
dR/dt = (1 - R) / tau_rec
```

so after a known release

```text
R(t) = 1 - [1 - R(t0+)] exp(-(t-t0)/tau_rec).
```

In this restricted case `R` is a monotone physical trace of elapsed time since the local event. With repeated inputs, it becomes a compressed summary of recent history rather than a unique timestamp.

The next event therefore does something very concrete:

```text
local history evolves quietly
        +
network event arrives
        ->
local history is sampled and updated
        ->
new contribution enters distributed dynamics
```

This is close to established descriptions of dynamic synapses as **memory buffers**, and to activity-silent working-memory models in which synaptic state is loaded and later read out by spiking.

The narrow WidePresent-style statement that survives is:

> **The past need not be stored as a ledger. Some consequences of the past simply have not relaxed yet. The instantaneous system state is a spatial distribution of differently aged physical traces.**

No special time field is required for that statement.

---

## 4. Geometry × local history

Let morphology / cable physics give a transfer kernel

```text
h[r <- i](t)
```

and let the local synapse carry state

```text
z_i(t).
```

Then the useful object is not only

```text
h[r <- i](t)
```

but something closer to

```text
h[r <- i](t ; z_i, x)
```

where `x` is the wider operating state of the cell.

A location matters because it determines at least three things:

```text
1. what inputs can reach the local state;
2. what electrical / biochemical operating conditions that state experiences;
3. where the resulting effect can propagate and which receivers can observe it.
```

This is the disciplined descendant of “geometry as time”:

> **spatial address determines which history-dependent state machine an event encounters and how the result becomes causally available elsewhere.**

The interesting question is therefore an interaction question, not a slogan:

```text
Does the pairing
    local temporal dynamics <-> geometric/electrical address
matter beyond either ingredient alone?
```

---

## 5. The retina gives a ground-truth receiver warning

Starburst amacrine cells make the receiver problem unavoidable.

Euler, Detwiler & Denk (2002) found that individual starburst dendritic branches carry direction-selective calcium signals while the somatic membrane voltage is not direction selective under the same stimulus. Later work shows a perisomatic/global voltage component combining with local dendritic input, and spatially varying bipolar-input kinetics along the dendrite.

So the same cell can contain a distinction that is obvious at one receiver and absent at another.

For V23:

```text
receiver set is part of the computational question
```

not a cosmetic logging choice.

The retina also supplies a literal **time-on-geometry** experiment: keep the same set of sustained/transient temporal kernels and shuffle only which dendritic locations receive them.

That motivates the V23 shuffle below.

---

## 6. First V23 architecture sketch

Do not freeze this API yet, but the minimal architecture should expose the biological ingredients separately.

For contact `i`:

```text
location:       p_i
long-term gain: w_i
local state:    z_i
local time constants / parameters: theta_i
```

For the morphology / geometry:

```text
G or A(x): state-dependent coupling / transfer operator
```

For an incoming event `u_i(t)`:

```text
(z_i(t+), q_i(t)) = Synapse(z_i(t-), u_i(t), v_i(t), theta_i)
```

then

```text
q(t) -> distributed state x(t) -> receiver outputs y_R(t).
```

A useful artificial simplification may begin with:

```text
edge state       Tsodyks-Markram-like R/u variables
local kernel     one or more leaky conductance states
geometry         sparse graph / delay / Green-kernel operator
receiver         one or several readout ports
```

Only later add voltage-dependent NMDA feedback or active dendrites.

V23 should remain modular enough that each mechanism can be removed without rewriting the model.

---

## 7. The decisive shuffle

Suppose every contact has a temporal parameter vector

```text
theta_i = [tau_rec, tau_fac, receptor taus, ...].
```

Use exactly the same morphology, inputs, weights, parameter multiset and state count.

Compare:

```text
STRUCTURED
    theta_i stays at its designed / learned / biological address

SHUFFLED
    theta_pi(i) is randomly permuted across the same addresses

HOMOGENEOUS
    all sites use a matched common parameter set
```

The important contrast is

```text
STRUCTURED - SHUFFLED.
```

It asks whether **the assignment of local temporal memory to geometry** matters.

That is far stronger than showing that “adding more state helps.”

---

## 8. Scientific method for V23: an obligation graph

This repo should be theorem-prover-ish about claims.

A claim is allowed only after the dependencies underneath it have been checked.

Example:

```text
CLAIM:
Geometry + local synaptic history provides a useful computational resource.

OWES:
  -> local state actually stores/readouts recent history
  -> effect survives matched mean gain / firing rate
  -> structured placement beats shuffled placement
  -> effect survives matched parameter/state count
  -> geometry ablation removes the advantage
  -> receiver choice is specified
  -> simple recurrent baseline does not explain the entire gain
```

A failed obligation narrows the claim; it does not need to be hidden.

The playful idea-generation mode and the claim standard are deliberately different things.

---

## 9. First experiment ladder

### V23-0 — one synapse, paired-pulse age readout

No morphology claim yet.

Use one dynamic synapse. Give one conditioning event, wait `Delta t`, give a probe event, and measure the probe response.

Test whether the local state and probe response carry recoverable information about `Delta t` over a useful range.

Controls:

```text
same receptor kernel without STP
matched mean response amplitude
multiple histories that share the same final interval
```

This establishes what the state actually remembers.

### V23-1 — one branch, stateful versus stateless edge

Put the synapse on a dendritic cable / graph. Compare:

```text
same geometry + deterministic receptor traces
same geometry + dynamic resource/facilitation state
```

Start AMPA-only or weakly voltage-dependent so STP is not immediately confounded by NMDA feedback.

### V23-2 — structured versus shuffled local time constants

Same multiset of `theta_i`; permute only their addresses.

If structured ≈ shuffled, do not claim a geometry/time interaction.

### V23-3 — geometry ablation

Preserve state count and local dynamics while destroying / randomizing the transfer geometry.

If the advantage survives, the resource is local state, not geometric placement.

### V23-4 — receiver test

Compare one scalar receiver with distributed receivers.

The open starburst-amacrine model is a particularly good gate because the biology already tells us that soma and dendritic output can expose different computations.

### V23-5 — add NMDA feedback

Only after the linear / STP interaction is understood, add voltage-dependent NMDA and ask whether local history changes which nonlinear operating regime is reached.

### V23-6 — task capacity

Only after the mechanism gates work, compare V23 against parameter/state-matched recurrent, TCN, reservoir and point-neuron baselines on temporal tasks.

Useful tasks should require history **and** spatial/address structure, otherwise the geometry is ornamental.

---

## 10. What would count as a real result?

A strong V23 result would look like:

> With the same number of states, same local dynamics, same parameter multiset, same input statistics and same receiver definition, a structured pairing of local history dynamics with geometry performs a task or preserves information that is degraded by shuffling that pairing; the effect is predicted by measurable local transfer/state quantities and survives simple baselines.

That is a claim worth keeping.

A weak result is merely:

```text
stateful model > stateless model
```

because recurrent state is already known to be useful.

---

## 11. Relationship to the earlier Geometric Neuron line

Earlier versions often asked whether geometry itself could become the neuron.

V23 is more specific:

```text
geometry is not the computation by itself

geometry constrains coupling
local mechanisms carry state
incoming events read/update that state
time exposes the coupling
receivers determine which distinctions are visible
```

So the working object is:

```text
GEOMETRIC NEURON V23
    = distributed local state
    + spatial/electrical coupling
    + event-driven state transitions
    + receiver-relative readout
```

This is still a Geometric Neuron. It is simply much closer to the mechanisms real neurons actually use.

---

## 12. Reading map

See [`SCIENCE_MAP.md`](SCIENCE_MAP.md) for the paper-by-paper foundation and [`METHOD.md`](METHOD.md) for claim obligations, ablations, and the initial benchmark plan.

The repository should become more ambitious in implementation while becoming **more precise in claims**.