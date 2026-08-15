# Joint synaptic address × STP — prior-art collision

**Date:** 2026-08-15  
**Status:** literature collision before building a discovery harness. **Not a novelty claim.**

## Candidate seam

After the Park branch narrowed, the remaining candidate is:

```text
fixed realistic dendritic morphology
    × jointly optimized synaptic address/location
    × jointly optimized presynaptic short-term dynamics
        U, tau_D, tau_F
```

with the scientific question:

> After optimization, do temporal synaptic parameters organize according to local receiver-transfer geometry in a reproducible way, and does that spatial assignment matter beyond the multiset of learned temporal parameters?

This note records what the first hard literature collision already kills.

---

# 1. Learned STP in a realistic dendritic neuron is old

Carvalho & Buonomano (2011) explicitly implemented learned short-term synaptic plasticity in a reconstructed layer-3 pyramidal neuron with active/passive conductances.

Their model had:

```text
104 dendritic compartments
242 dendritic segments
1000 randomly distributed background synapses
10 driving inputs
```

The driving inputs were placed **randomly on 10 of 16 quaternary branches** around the soma.

They learned synaptic weight and the STP parameter `U`; the realistic neuron showed lower forward/reverse discrimination error with learned STP than with fixed/random STP, and they included a shuffled learned-STP control.

They also explicitly discuss `tau_D` and `tau_F` plasticity. They tried more complex learning rules for these time constants; in that particular discrimination setting the added plasticity did not significantly improve performance, although they note tasks where time-constant tuning should matter.

Therefore V23 cannot claim:

```text
realistic dendrite + learned STP
realistic dendrite + learned U
shuffle learned STP across driving inputs
learning tau_D / tau_F in principle
```

as new.

Reference:
- Carvalho TP, Buonomano DV. (2011), *A novel learning rule for long-term plasticity of short-term synaptic plasticity enhances temporal processing*, Frontiers in Integrative Neuroscience 5:20. DOI: 10.3389/fnint.2011.00020.

Important remainder:

> Their driving synaptic locations were randomly assigned/fixed. They did **not** jointly optimize the locations together with the temporal STP parameters in the detailed morphology.

---

# 2. Optimized dendritic location in a detailed neuron is now explicit prior art

Aizenbud et al. (2026), `What can a neuron compute`, introduce TwinProp, which uses a differentiable digital twin of a detailed rat L5 pyramidal cell to optimize:

```text
synaptic strength
AND
synaptic dendritic location
```

under biological constraints.

They optimize those structural/strength degrees of freedom for naturalistic and Boolean tasks and map the solution back to the detailed neuron.

They explicitly frame their target as what computations can be realized through optimized synaptic strengths and dendritic locations, rather than a biological learning rule for acquiring them.

Their detailed synapse dynamics are taken from existing physiological parameterizations; the STP temporal parameters are not the jointly optimized degree of freedom in the TwinProp optimization described here.

Therefore V23 cannot claim:

```text
optimize synaptic location in a detailed morphology
jointly optimize location + synaptic strength
use task optimization to discover spatial connectivity on one neuron
```

as new.

Reference:
- Aizenbud I, Beniaguev D, Pnueli N, Segev I, London M. (2026), *What can a neuron compute*, bioRxiv 2026.06.08.730984. DOI: 10.64898/2026.06.08.730984.

---

# 3. Learning full temporal synapse profiles is now a live 2026 line

Buonomano, Soldado-Magraner, McDowell & Zhou (2026) explicitly propose synapses as multi-parameter learnable temporal computational elements and show that learned STP improves interval/counting and more complex temporal tasks.

The central premise therefore already exists:

```text
synapses can learn temporal dynamics, not only scalar strength
```

and learned temporal parameter identity matters to performance.

This is currently a preprint and should be treated as frontier evidence, not settled consensus.

Reference:
- Buonomano D, Soldado-Magraner S, McDowell J, Zhou S. (2026), *A computational theory of short-term synaptic plasticity: synapses learn to tell time*. Research Square preprint. DOI: 10.21203/rs.3.rs-9916271/v1.

---

# 4. Biology already contains spatial STP gradients

A learned spatial allocation cannot be interpreted in a vacuum because location-dependent STP already exists experimentally.

Grillo et al. (2018) showed in CA1 basal dendrites that presynaptic bouton size/release probability changes with dendritic distance, producing a gradient toward stronger short-term facilitation distally. Their compartmental model showed that this gradient tunes frequency-dependent dendritic integration.

So if an optimizer discovers:

```text
more facilitating synapses distally
```

that may be a rediscovery of known CA1 basal organization, not a new principle.

Reference:
- Grillo FW et al. (2018), *A Distance-Dependent Distribution of Presynaptic Boutons Tunes Frequency-Dependent Dendritic Integration*, Neuron 99:275–282.e3. DOI: 10.1016/j.neuron.2018.06.015.

Also, location-dependent STP gradients are not universal in direction across neuron compartments/types, so a raw proximal-distal rule is unlikely to be a universal principle.

---

# 5. Location-dependent learning rules are also old

Dendritic location has long been known to alter synaptic plasticity induction because the relevant local voltage/calcium signals differ along the tree.

For example, Letzkus, Kampa & Stuart (2006) show that the timing rule for STDP changes with dendritic location in layer-5 pyramidal neurons.

This is long-term plasticity rather than presynaptic STP, but it is an important guardrail:

```text
location × learning rule
```

is not itself new.

Reference:
- Letzkus JJ, Kampa BM, Stuart GJ. (2006), *Learning Rules for Spike Timing-Dependent Plasticity Depend on Dendritic Synapse Location*, Journal of Neuroscience 26:10420–10429. DOI: 10.1523/JNEUROSCI.2650-06.2006.

---

# 6. What this search did NOT find

In this literature pass I did **not** find a study closing all of the following simultaneously:

```text
1. one morphologically detailed neuron
2. synaptic dendritic address is a task-optimized variable
3. full presynaptic STP temporal dynamics are also task-optimized
4. location and temporal parameters are optimized jointly
5. the learned temporal-parameter multiset is shuffled over the learned
   locations as a matched causal control
6. the resulting allocation is analyzed against local transfer/impedance
   coordinates rather than only raw distance
```

This is a **search result, not a novelty certification**. There may be obscure work missed by the query set.

The closest collision is Carvalho & Buonomano 2011:

```text
realistic dendrite + learned STP + shuffle
BUT locations randomly assigned/fixed
```

and TwinProp 2026:

```text
realistic dendrite + learned address/strength
BUT STP temporal kinetics not jointly learned
```

That is why the seam remains worth a small experiment.

---

# 7. The first experiment must be smaller than the claim

Do **not** begin with 500 evolutionary restarts or a giant active L5 model.

Build a proof-of-concept whose only purpose is to answer:

> Can joint address × STP optimization produce an assignment effect that survives a strict post-training STP-label shuffle when the temporal-parameter multiset is held fixed?

Minimum factorial controls:

```text
A  fixed address, fixed STP
B  learned address, fixed STP
C  fixed address, learned STP
D  learned address, learned STP
E  D then shuffle learned STP labels across learned addresses
```

If

```text
D ~= E
```

then the specific address × temporal-dynamics interaction is weak; stop.

If

```text
D >> E
```

then ask whether the learned arrangement is predicted by:

```text
raw path distance
DC attenuation
transfer-kernel centroid / width
local input impedance
branch identity
active/nonlinear susceptibility
```

A spatial rule is only interesting if it survives controls for simpler coordinates.

---

# 8. Do not use the passive delay lemma as the target

The earlier rearrangement identity for transfer-kernel centroids is a useful linear null:

```text
mu(h_i * g_j) = mu(h_i) + mu(g_j)
```

but in the passive cells measured so far, morphology-induced somatic delay variation is only a few milliseconds while STP timescales span tens to hundreds/thousands of milliseconds.

So a large joint-assignment benefit should **not** be attributed to simple cable-delay matching without demonstrating the effect size.

The useful discovery target would be a stronger interaction involving attenuation, waveform shape, nonlinear dendritic recruitment, or state/history—not merely sorting delays.

---

# Current seam sentence

> **The surviving candidate is not “dendrites plus temporal synapses.” It is whether a detailed neuron's task-optimized synaptic addresses and task-optimized presynaptic temporal dynamics become mutually specialized, so that the same learned temporal-parameter multiset loses function when reassigned across the learned morphology.**

That is specific enough to test and narrow enough not to collide immediately with the papers found here.
