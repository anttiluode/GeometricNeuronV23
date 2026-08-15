# GeometricNeuronV23 — space/time separability gate

**Status:** method / falsification note. Not a novelty claim.

This note grew from the question:

> Can space and time be “orthogonal” in a dendrite, and what would that mean operationally?

The useful answer is **not** a Minkowski analogy. It is a measurement question about whether **source location and temporal response can be separated** at a chosen receiver.

---

## 1. First correction: a passive cable is not a wave equation

For a uniform passive cable,

```text
tau_m * dV/dt = lambda^2 * d2V/dx2 - V
```

or

```text
dV/dt = D * d2V/dx2 - V/tau_m,
D = lambda^2 / tau_m.
```

This is a **diffusion-with-leak** equation. It is parabolic, not a finite-speed hyperbolic wave equation.

So a fitted delay that grows approximately linearly with distance does **not** by itself establish wave-like propagation or a causal cone.

For an infinite uniform cable, the impulse Green function has the form

```text
G(x,t) ∝ t^(-1/2)
         * exp[-x^2 tau_m/(4 lambda^2 t)]
         * exp[-t/tau_m].
```

Maximizing this response over time gives

```text
X = x/lambda

 t_peak / tau_m
      = (sqrt(1 + 4 X^2) - 1) / 4.
```

This has two limits:

```text
X << 1:
    t_peak ≈ (tau_m/2) X^2
    -> diffusive-looking x^2 scaling

X >> 1:
    t_peak ≈ (tau_m/2) X - tau_m/4
    -> approximately linear delay with distance
```

So **leak itself can make the ridge of a diffusive Green function look approximately ballistic at larger electrotonic distance** while the underlying PDE remains diffusive.

That gives a clean null for the recent passive-solver observation that fitted delay scales roughly as path length^1.

For a tapering/branched dendrite, the first coordinate to try is not raw Euclidean distance and not even raw path length, but approximate electrotonic path

```text
X_i ≈ integral_path ds / lambda(s).
```

### Gate S0

Before interpreting a fitted delay exponent, plot

```text
t_peak/tau_m  vs  X_i
```

and compare it with the simple cable prediction above.

If the four morphologies largely collapse after electrotonic normalization, then the apparent “space -> time” law is mostly classical cable theory. The residual around that collapse is the part worth explaining with branching, taper, soma load, active conductances, etc.

---

## 2. The useful replacement for “orthogonal”: separable

Choose a receiver `r` (initially the soma). For source location `i`, let

```text
H_r(i,t) = h[r <- i](t)
```

be the source-to-receiver impulse response.

The strongest possible space/time separation is

```text
H_r(i,t) = a(i) * f(t).
```

Then:

- space chooses only a gain `a(i)`;
- time chooses one common waveform `f(t)`;
- source location does not change temporal shape.

In matrix language (`source x time`), this is rank 1.

A graded inseparability score can therefore be borrowed directly from standard spatiotemporal receptive-field analysis:

```text
alpha_SVD = 1 - sigma_1^2 / sum_k sigma_k^2
```

where `sigma_k` are singular values of the source-by-time response matrix.

`alpha_SVD = 0` means exact separability.

But raw SVD mixes two different things:

1. a true change of waveform shape;
2. a simple time shift.

So V23 should also test a stronger **gain + delay** model.

---

## 3. Space may act approximately as a delay coordinate

A better passive null is

```text
h[r <- i](t) ≈ a_i * f(t - tau_i).
```

Equivalently in frequency space,

```text
H_i(omega)
    ≈ a_i * exp(-j omega tau_i) * F(omega).
```

Then location does two simple things at the receiver:

```text
where i is
    -> attenuation a_i
    -> delay tau_i
```

and does **not** otherwise change the temporal waveform.

This is much closer to the original intuition than a spacetime angle:

> spatial address can become a temporal translation at a receiver.

### Gate S1 — shift-separable fit

For every source:

1. fit gain `a_i`;
2. fit delay `tau_i`;
3. align the impulse responses by `tau_i`;
4. remove `a_i`;
5. recompute residual SVD rank / waveform error.

Report both:

```text
RAW INSEPARABILITY
    how much source and time are mixed before alignment

SHAPE INSEPARABILITY
    how much remains after the best gain + delay explanation
```

If shape inseparability is tiny at the soma, then passive dendritic geometry is being compressed there into almost nothing more than **weight + delay**.

That is an important negative result, not a disappointment.

---

## 4. Receiver collapse becomes measurable

The soma is only one projection.

Repeat the same analysis for

```text
R_soma
R_branch
R_multi
```

and for the full transfer matrix

```text
H_R<-S(t).
```

A tree can be highly structured internally while a particular receiver observes a nearly rank-1 projection.

This is consistent with the motivation behind impedance-kernel / reduced-compartment work: the number of spatial compartments needed depends on which source-to-receiver transformations and nonlinear computations one intends to preserve.

### Gate S2

Ask whether

```text
shape-rank(local receiver) >> shape-rank(soma)
```

for the same passive morphology.

If yes, the soma is performing a genuine **receiver collapse** of richer internal spatiotemporal structure.

---

## 5. A sequence-reversal consequence

This gives a very cheap test that connects directly to known dendritic sequence discrimination.

Take two locations `i,j`, deliver identical events separated by `Delta`, and compare

```text
A: i at 0,      j at Delta
B: j at 0,      i at Delta
```

First scale the two synapses so that their unitary somatic responses have matched gain.

Under the strict linear rank-1 model

```text
h_i(t) = a_i f(t)
h_j(t) = a_j f(t)
```

and after gain compensation, `A` and `B` become identical at the soma.

Therefore substantial order/direction sensitivity after unitary-gain matching requires at least one of:

```text
location-dependent waveform shape
location-dependent delay / dispersion
nonlinear local interaction (e.g. NMDA)
state/history dependence (e.g. STP)
active dendritic conductance
receiver-local interaction
```

Branco, Clark & Häusser (2010) already provide the biological ancestor: single cortical dendrites discriminate the direction and velocity of sequential synaptic activation, with dendritic impedance gradients and NMDA receptor activation as key mechanisms.

This means “space and time stop being separable” can be translated into an actual experiment:

> reverse a spatiotemporal path and ask whether the receiver can tell.

---

## 6. Why this is directly relevant to Aizenbud FCI

Aizenbud et al. (2026) show a morphology contribution to Functional Complexity Index under a common rat-synapse condition.

But that common excitatory synapse still contains voltage-dependent NMDA.

So the published morphology result does **not** isolate

```text
passive morphology only
```

from

```text
morphology-dependent organization of local NMDA feedback.
```

The recent passive-solver result, if it survives NEURON validation, makes the missing AMPA-only gate even more informative.

### Prediction

If passive soma transfer is almost gain+delay separable, then:

```text
AMPA-only morphology
```

should be much easier to collapse into a small temporal surrogate than

```text
same morphology + NMDA.
```

The interesting quantity may not be morphology itself but **how morphology makes local nonlinear/history-bearing processes nonseparable at the receiver**.

---

## 7. Experiment ladder

```text
S0  validate passive solver against NEURON on exact released cell
    same discretization / same parameters

S1  electrotonic collapse
    t_peak/tau_m vs integral ds/lambda(s)

S2  soma transfer dictionary
    raw SVD rank
    gain+delay fit
    post-alignment shape rank

S3  receiver test
    soma vs branch vs multiport transfer dictionaries

S4  mechanism ladder
    AMPA-only
    rat AMPA+NMDA
    human AMPA+NMDA
    active dendrites

S5  local-history ladder
    fixed receptor traces
    + presynaptic STP
    + heterogeneous / learned STP

S6  sequence reversal
    matched unitary soma gain
    IN vs OUT / i->j vs j->i
    sweep Delta and velocity

S7  ask whether nonseparability / sequence sensitivity predicts
    FCI or optimized task capacity better than area/path baselines
```

---

## 8. A stronger systems-theory extension: receiver-visible dynamic order

SVD of a source-by-time kernel is a useful cheap diagnostic, but there is a more rigorous systems question hiding underneath.

For a locally linearized model

```text
xdot = A x + B u
y    = C x
```

`B` says which internal directions sources can reach and `C` says which internal directions the chosen receiver can see.

The relevant dynamic states are therefore the ones that are **both reachable and observable**.

A block-Hankel matrix built from impulse responses, or an eigensystem-realization / balanced-truncation analysis, can estimate the receiver-visible dynamical order without caring how many compartments the simulator happened to use.

This is almost tailor-made for the V23 question:

```text
large morphological state dimension
        !=
large receiver-visible dynamic dimension
```

### Gate S8

Build the impulse-response Hankel spectrum for:

```text
passive soma
passive multiport
NMDA soma
NMDA multiport
STP + NMDA
```

If the passive soma has one/few dominant Hankel modes while NMDA/STP greatly expands the receiver-visible spectrum, that would give a classical systems-theory explanation for why a detailed morphology can look simple in one regime and hard to emulate in another.

Do not call this new mathematics. The possible contribution is applying the right established input/output complexity object to the Aizenbud/TwinProp setting.

---

## 9. Discovery-mode version

Poleg-Polsky (2026) is a useful methodological template: search a biologically constrained parameter space, collect many successful solutions, then cluster the mechanisms that repeatedly emerge.

For V23, allow jointly:

```text
synaptic location
synaptic strength
local temporal parameters (STP / receptor kinetics)
```

and optimize tasks requiring spatial order + time.

Then classify the repeated solutions by whether they implement:

```text
gain asymmetry
arrival-time alignment
temporal diversification
local nonlinear gating
history-conditioned gating
multi-receiver routing
```

Critical controls:

```text
isopotential morphology
delay-shuffled morphology
location-shuffled temporal parameters
same state count / same parameter multiset
same unitary receiver gain
same optimizer and search budget
```

If the same solution clusters appear in the isopotential/shuffled controls, they are optimizer/task geometry, not dendritic geometry.

---

## 10. About the “temporal angle” intuition

An angle can always be drawn after choosing units that convert time to length, but that angle is **not canonical** here.

For a true finite-speed trajectory one may draw a spacetime slope and interpret it as velocity. A passive dendritic impulse is different: it is a **distributed Green function**, not a worldline with a sharp front.

So do not use

```text
tortuosity angle
Minkowski interval
rapidity
computational light cone
```

as physics claims for the passive cable.

The invariant object we actually possess is better:

```text
source location
    -> transfer kernel over time
    -> receiver
```

and the scientific question is whether that kernel is separable, shift-separable, or genuinely space/time inseparable.

That is enough.

---

## Relevant literature

### Cable / transfer kernels

- Hellerstein (1968), **Passive membrane potentials: a generalization of the theory of electrotonus**. Biophysical Journal. DOI: https://doi.org/10.1016/S0006-3495(68)86493-8
- Wybo, Stiefel & Torben-Nielsen (2013), **The Green's function formalism as a bridge between single- and multi-compartmental modeling**. Biological Cybernetics. DOI: https://doi.org/10.1007/s00422-013-0568-0
- Wybo et al. (2021), **Data-driven reduction of dendritic morphologies with preserved dendro-somatic responses**. eLife. DOI: https://doi.org/10.7554/eLife.60936

### Spatial order becomes temporal computation

- Branco, Clark & Häusser (2010), **Dendritic discrimination of temporal input sequences in cortical neurons**. Science. DOI: https://doi.org/10.1126/science.1189664
- Branco & Häusser (2011), **Synaptic integration gradients in single cortical pyramidal cell dendrites**. Neuron. DOI: https://doi.org/10.1016/j.neuron.2011.02.006

### Current frontier around geometry / temporal synapses / search

- Aizenbud et al. (2026), **Dendritic morphology and synaptic nonlinearities enhance functional complexity in human cortical neurons**. PNAS. DOI: https://doi.org/10.1073/pnas.2533168123
- Aizenbud et al. (2026), **What can a neuron compute** (TwinProp preprint). DOI: https://doi.org/10.64898/2026.06.08.730984
- Buonomano et al. (2026), **A computational theory of short-term synaptic plasticity: synapses learn to tell time** (preprint). DOI: https://doi.org/10.21203/rs.3.rs-9916271/v1
- Poleg-Polsky (2026), **Machine learning discovers numerous new computational principles supporting elementary motion detection**. Nature Communications. DOI: https://doi.org/10.1038/s41467-026-70288-4

---

## Current research sentence

> **At a chosen receiver, ask how much spatial address can be factored into gain and delay, how much remains as true temporal-shape diversity, and which local nonlinear/history-bearing mechanisms create the failure of separability.**

That is the useful version of the space/time question for V23.