# Receiver-visible order — prior-art collision and the narrower V23 question

**Status:** correction / narrowing note.

`SPACETIME_SEPARABILITY_GATE.md` proposed using controllability/observability, Hankel singular values, balanced truncation or related realization tools to estimate how much dynamical structure is visible at a chosen receiver.

That is a good tool choice, but **it is not a new application to detailed dendritic neurons**.

## 1. The prior art is unusually direct

Kellems, Roos, Xiao & Cox (2009), *Low-dimensional, morphologically accurate models of subthreshold membrane potential*, already posed almost exactly the receiver-reduction problem:

> preserve highly detailed, spatially distributed synaptic input while reproducing membrane potential accurately at a small number of places, such as the action-potential initiation site.

They linearized detailed active cells around rest to obtain quasi-active systems and then applied **Balanced Truncation** and transfer-function approximation.

- DOI: https://doi.org/10.1007/s10827-008-0134-2
- PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC2756789/

The result is stronger than a vague precedent.

For their forked-cell example:

```text
full quasi-active dimension = 1204
Hankel singular values decay rapidly
sigma_n < machine epsilon for n > 65
~5 digits of soma-potential accuracy with only 12 HSV modes
```

For a much larger CA1 cell they report a 41,364-state quasi-active model reduced to about 15 states for ~5-digit agreement; at finer discretization, 165,330 states again reduced to about 15 for similar accuracy.

So this claim is **already established in an important regime**:

> a morphology may contain an enormous simulator state while the source-to-chosen-receiver subthreshold map has very low effective input/output order.

That is classical systems theory applied to detailed neurons, not V23 novelty.

Two follow-ups push the same direction:

### Kellems et al. (2010) — nonlinear spiking reduction

Anthony R. Kellems et al., *Morphologically accurate reduced order modeling of spiking neurons*, Journal of Computational Neuroscience 28:477–494.

- DOI: https://doi.org/10.1007/s10827-010-0229-4

Uses POD / DEIM-style reduction of nonlinear neuron dynamics while retaining morphological input structure.

### Hedrick & Cox (2013) — structure-preserving reduction

Kyle R. Hedrick & Steven J. Cox, *Structure-preserving model reduction of passive and quasi-active neurons*, Journal of Computational Neuroscience.

- DOI: https://doi.org/10.1007/s10827-012-0403-y

Develops reductions that retain passive/quasi-active circuit structure and spatial specificity.

Therefore V23 should **not** claim discovery of “receiver collapse,” low receiver-visible order, Hankel analysis of dendrites, or the idea that many compartments can collapse to a small dynamical system at the soma.

---

## 2. What remains open for V23

The interesting question shifts one level upward:

> **Which biological mechanisms make the receiver-visible map stop being low-order / separable, and does that increase predict FCI or usable task capacity?**

The Kellems result is mostly a linearized/quasi-active input-output result around an operating point. Aizenbud's FCI is driven by a detailed nonlinear cell under distributed time-varying synaptic bombardment, and their own experiments implicate morphology plus voltage-dependent NMDA.

So define a mechanism ladder:

```text
P0  passive cable
Q0  quasi-active / linearized conductances
A0  AMPA-only distributed synapses
N0  + NMDA voltage feedback
S0  + presynaptic short-term state
D0  + active dendritic spikes / channels
```

For each rung and each receiver set, measure the simplest object that is valid for that regime.

### Linear / locally linear regime

Use:

```text
impulse-response dictionary
transfer functions
Hankel singular values
balanced / minimal realization order
```

### Nonlinear / state-dependent regime

Use local linearizations over many operating states:

```text
x -> J_x -> H_x
```

and measure how much the receiver-visible transfer family itself changes with state.

A useful empirical quantity is a **state-conditioned transfer expansion**:

```text
Delta_order(mechanism)
    = receiver-visible order with mechanism
      - receiver-visible order of matched passive/quasi-active baseline
```

Do not freeze this definition until the measurement is stress-tested.

The scientific question is whether a morphology with high Aizenbud FCI also shows large expansion of receiver-visible dynamics when NMDA / local history / active dendrites are enabled.

If not, kill the bridge.

---

## 3. A cleaner descendant of the “temporal angle” intuition

There *is* an angle in the passive solver that is physically useful, but it is not

```text
atan(path distance / Euclidean distance)
```

and it is not a Minkowski rapidity.

For each source `i` and receiver `r`, the frequency-domain transfer is complex:

```text
H_ri(omega) = |H_ri(omega)| exp(j phi_ri(omega)).
```

The ordinary complex phase

```text
phi_ri(omega) = arg H_ri(omega)
```

is a real, measurable **temporal phase angle**.

Its derivative gives group delay:

```text
tau_g(i, omega) = - d phi_ri / d omega.
```

This gives the user's intuition a disciplined translation:

```text
spatial address
    -> frequency-dependent phase lag
    -> frequency-dependent delay at the receiver
```

If

```text
phi_i(omega) ~= -omega * tau_i + constant
```

then the source is close to a pure delay relative to a common transfer shape.

If `tau_g(i,omega)` varies strongly with frequency, the cable is dispersive and one scalar “velocity” or “temporal angle” is not enough.

### Gate P1 — phase-linearity test

For every source:

1. unwrap phase of `H_i(omega)`;
2. fit its best linear phase;
3. compute group-delay variation across the trusted frequency band;
4. compare across location, electrotonic path and branch identity;
5. repeat soma vs local receivers.

This is more informative than assigning one path/space angle to a pair of sites.

---

## 4. Another correction to the passive p ~= 1 observation

The standard passive cable equation is diffusion with leak:

```text
tau_m V_t = lambda^2 V_xx - V.
```

For an infinite uniform cable, the impulse Green function is proportional to

```text
G(x,t)
  ~ t^(-1/2)
    exp[-x^2 tau_m/(4 lambda^2 t)]
    exp[-t/tau_m].
```

Let

```text
X = x/lambda.
```

The time of the response peak is

```text
t_peak/tau_m
    = (sqrt(1 + 4 X^2) - 1)/4.
```

Therefore:

```text
X << 1:
    t_peak ~ (tau_m/2) X^2

X >> 1:
    t_peak ~ (tau_m/2) X - tau_m/4.
```

So an approximately linear `delay ~ distance` relation can arise from a **leaky diffusive cable** at sufficiently large electrotonic distance. It is not evidence that the passive dendrite has turned into a finite-speed wave equation.

This makes the next comparison obvious:

```text
raw path distance fit
vs
electrotonic X = integral ds/lambda(s)
vs
uniform-cable t_peak(X) null
```

The interesting information is the residual after the cable null, not the fitted exponent by itself.

---

## 5. Sequence reversal is still a useful nonlinear gate

Branco, Clark & Häusser (2010), *Dendritic discrimination of temporal input sequences in cortical neurons* (Science), showed that single cortical dendrites are sensitive to the order and velocity of sequential synaptic activation.

- DOI: https://doi.org/10.1126/science.1189664
- PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC6354899/

For V23, first match the unitary receiver amplitude of the stimulated sites. Otherwise a trivial spatial gain asymmetry can itself create order-sensitive output in a thresholded/nonlinear readout.

Then compare:

```text
i -> j
j -> i
```

under:

```text
passive
AMPA-only
NMDA
STP
NMDA + STP
active dendrite
```

The increase in order sensitivity relative to the passive gain+delay prediction is a direct measurement of **space/time inseparability created by local mechanisms**.

---

## 6. The current V23 seam

Put the prior-art collision and the current 2026 work together:

```text
Kellems/Cox:
    detailed morphology can collapse to very low receiver-visible order
    in subthreshold/quasi-active regimes

Branco/Hausser:
    dendrites can nevertheless discriminate temporal order through
    spatial gradients + local nonlinear mechanisms

Aizenbud:
    morphology + NMDA increase black-box functional complexity

Buonomano et al. 2026:
    synaptic temporal dynamics can themselves be learned and shuffled;
    learned STP supports timing tasks

TwinProp:
    synaptic location and strength can be optimized in a detailed neuron
```

The narrow missing experiment is therefore not

> “does geometry contain time?”

It is:

> **Starting from a morphology whose linear input/output map is strongly reducible, which local nonlinear/history-bearing mechanisms inflate the receiver-visible spatiotemporal map, and can the location of that inflation be predicted from geometry?**

Then, only if that works:

> **Can jointly optimizing synaptic location and local temporal dynamics exploit that inflation for task capacity?**

That is where V23 should dig next.

---

## 7. Kill conditions

```text
K0  Claude passive solver fails exact NEURON validation
    -> discard current separability numbers

K1  electrotonic cable null explains delay scaling
    -> discard wave/velocity interpretation

K2  post-gain+delay shape diversity is tiny at every receiver
    -> passive geometry is mostly a weighting/delay device

K3  NMDA/STP do not substantially expand state-conditioned transfer diversity
    -> no nonlinear rank-inflation mechanism

K4  expansion does not predict FCI or optimized task performance
    -> interesting dynamics, not the missing complexity mechanism

K5  matched RNN/reservoir reproduces the same gain at equal state/compute budget
    -> no artificial-architecture advantage
```

A killed rung is useful. It tells us exactly which part of the old intuition survives.