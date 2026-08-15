# GeometricNeuronV23 — CURRENT HANDOFF

**Updated:** 2026-08-15, fifth pass — **Park calibration reached a data-driven stopping point**

**Status:** active falsification/discovery program. Nothing here is a novelty claim.

## Read in this order

1. `PARK_APICAL_STATE_SHUFFLE_RECEIPT.md` — latest cheap geometry × history kill gate.
2. `PARK_APICAL_I1_CORRECTION.md` — correct distal-apical receiver analysis; supersedes the mixed apical/basal I1 interpretation.
3. `PARK_HISTORY_CAUSAL_RECEIPT.md` — channel-history causal controls, corrected to distal apical receivers.
4. `PARK_TWO_COMPARTMENT_CONTROL_RECEIPT.md` — author-released minimal control; detailed morphology is not required for the broad Park phenotype.
5. `PARK_P0_EXECUTION_RECEIPT.md` — exact supplement execution/provenance and failed phase-table reproduction kept intact.
6. `GEOMETRY_STATE_COMMUTATOR_V02.md`, `FULL_STATE_GEOMETRY_HISTORY_DECOMPOSITION.md`, `CHRONOLOGY_LOCALITY.md` — mathematical nulls / possible later closure tools.
7. `chronology_probe.py`, `chronology_decompose.py`, `geometry_state_commutator_v02.py` — analysis utilities.
8. `OPERATOR_ATLAS_HYPOTHESIS.md`, `SPACETIME_SEPARABILITY_GATE.md` — upstream lineage.

The original `GEOMETRY_STATE_COMMUTATOR.md` / `geometry_state_commutator.py` are v0.1 shorthand. Prefer v0.2.

---

# Executive status

The Park 2025 branch did what a calibration branch should do: it **removed most of the exciting interpretation before we spent heavily on it**.

What survives:

```text
local history matters strongly                         YES
soma-dendrite coupling matters                         YES
state-conditioned distal accessibility exists          YES
correct distal-apical small-signal state effect         MODEST (~10-12%)
detailed history-state address strongly enhances it     NO
detailed tree required for broad accelerometer motif    NO
```

Therefore:

> **Do not make the full Park Jacobian / Magnus decomposition the next discovery bet.**

It remains available as a closure analysis, but the cheaper controls have already made the core mechanism look much closer to **local history + coupling** than to a special detailed-morphology chronology.

The next discovery effort should move to the narrower literature seam around **joint synaptic address × temporal dynamics optimization**, after one more hard prior-art collision.

---

# 1. Original mathematical hypothesis, now downgraded

The candidate was:

> Local history makes the neuron's incremental operator vary in time, and morphology determines whether the resulting chronological transformations remain distinguishable at a chosen receiver.

For a compartment model:

```text
A(t) = S + Q(t)
```

and exactly:

```text
[A_a,A_b]
 = [S,Q_b-Q_a] + [Q_a,Q_b].
```

Bookkeeping:

```text
[S,Q_b-Q_a]     morphology × changing-local-state chronology
[Q_a,Q_b]       intrinsic local chronology possible in a point neuron
```

This algebra remains correct and useful. But Park no longer gives strong empirical reason to expect the first term to be a large hidden discovery mechanism in this phenomenon.

---

# 2. Exact Park code was executed

The exact public Supplementary Software 1 was fetched from Springer Nature, compiled, and run under Python 3.10 / NEURON 8.2.2.

Successful provenance / execution runs include:

```text
supplement fetch/inspect       31872229100
phenotype reproduction        31872543670
500-um receiver census        31872658435
stored table replay           31872817613
I0 state-conditioned impedance 31872873718
I1 source-normalized impedance  31873026312
I1 heterogeneity audit          31873287254
channel-history controls        31873317216
apical-only I1 correction       31873436618
apical state-address shuffle    31873551235
apical causal audit             31873584518
```

Package rough edges and failed reproduction details are preserved in `PARK_P0_EXECUTION_RECEIPT.md`. No active channel equation was edited to make the model run.

---

# 3. The important anatomical correction

The primary Park paper concerns **distal apical dendrites**. The first V23 receiver shell had been selected by path distance alone and accidentally pooled `apic[]` with basal `dend[]` sections.

That mattered enormously.

The old mixed-shell 1-Hz extended result appeared to show:

```text
distal normalized success/failure     ~2.116 x
distal-specific diff-of-diff           ~2.200 x
```

The literature-correct apical-only rerun gives:

```text
proximal apical receivers    n=5
distal apical receivers      n=8

1-Hz extended:
soma input ratio             1.1235 x
proximal normalized          1.0329 x
distal normalized            1.1443 x
distal-specific              1.1079 x

10-Hz distal-specific        1.1182 x
```

So the dramatic ~2.2x effect was largely a receiver-definition / weak-basal-visibility artifact. The corrected biologically relevant effect is modest.

This correction is frozen in `PARK_APICAL_I1_CORRECTION.md`.

---

# 4. Channel history is nevertheless causally real

On the correct eight distal-apical receivers, baseline widefield gives:

```text
SSSFSFSFSFSFS
```

consensus over 13 somatic spikes.

### Remove slow NaV inactivation drive

Released `na3.mod` allows the slow-inactivation drive to be disabled by setting the relevant asymptote to 1 while retaining the Na current and fast gates.

Result:

```text
13 somatic spikes
8/8 distal-apical receivers: SSSSSSSSSSSSS
```

No failures remain.

### Remove A-type Kv conductance

Result:

```text
9 somatic spikes
8/8 distal-apical receivers: SSSSSSSSS
```

Again no failures.

Therefore the known Park history mechanisms genuinely control the finite-amplitude distal-apical phenotype. See `PARK_HISTORY_CAUSAL_RECEIPT.md`.

What they do **not** establish is a special role for detailed morphology.

---

# 5. Park's own two-compartment model is the strongest conceptual control

Exact Supplementary Software 2 was also fetched/executed.

The author-released coarse system has approximately:

```text
one soma compartment
one dendrite compartment
one coupling edge
one dendritic adaptation/recovery variable
```

and already generates a transient dendritic-spike window while soma spiking continues.

V23 controls:

```text
freeze dendritic recovery u2
    -> closing of the transient window disappears

remove soma-dendrite coupling
    -> soma drive no longer produces stimulus-related dendritic events
```

So the broad Park logic is already:

```text
local history + coupling -> history-conditioned accessibility
```

without a detailed tree.

This means the detailed morphology had to earn something **above** the qualitative phenotype. See `PARK_TWO_COMPARTMENT_CONTROL_RECEIPT.md`.

---

# 6. Direct apical history-state address shuffle: mostly negative

This was the decisive cheap gate before full Magnus.

At each fixed baseline snapshot:

```text
receiver        distal apic[] 490-510 um, n=8
source          soma
frequency       1 Hz
metric          extended impedance, normalized by soma input
apical segments 537
shuffle bins    50 um path-distance bins
seeds           10 fixed seeds
```

The exact gate-state multiset was preserved. Only address changed.

Baseline real spatial assignment:

```text
success/failure ratio = 1.1443439 x
```

### Slow NaV state address

Path-bin shuffles:

```text
mean   1.1397866
range  1.1393221 - 1.1403098
```

The real assignment is slightly larger, but only by about 0.0046 ratio units. This is tiny.

### A-type state address

Path-bin shuffles:

```text
mean   1.1639469
range  1.1488663 - 1.1778896
```

**All ten shuffles produce a larger contrast than the real assignment.**

### Joint slow-NaV + A-type

```text
mean   1.1606086
range  1.1452640 - 1.1748900
```

Again all ten are at or above the real assignment.

Interpretation:

> The real detailed apical history-state address is not strongly responsible for the measured operator contrast; for A-type state it certainly is not arranged to maximize that contrast.

This is only a snapshot/local-linearization test and not a finite-amplitude shuffled trajectory. But it is sufficiently negative that the expensive full chronology decomposition no longer has priority as a discovery experiment.

See `PARK_APICAL_STATE_SHUFFLE_RECEIPT.md`.

---

# 7. Park branch verdict

Do **not** claim:

```text
detailed dendritic geometry creates the spike-rate accelerometer
history-state spatial address strongly amplifies the Park transfer contrast
Park validates the GeometricNeuron chronology hypothesis
```

The earned statement is narrower:

> **Park validates a powerful local-history-plus-coupling mechanism. The detailed apical tree produces a modest state-conditioned transfer difference, but our direct path-matched address shuffle does not reveal a strong privileged spatial organization of the identified history gates for that metric.**

This does not globally falsify morphology × history in neurons. It says **Park is not the strong calibration win we hoped it might be**.

The correct stopping action is to move the discovery budget elsewhere unless a new Park-specific prediction appears.

---

# 8. Optional closure, not next priority

The full machinery still exists:

```text
short-window A(t)
direct Phi
Omega_1
Omega_2
Omega_2^geom vs Omega_2^local
physical source / receiver projections
```

It could quantify exactly how much pairwise chronology is local versus morphology-dependent.

But if run now it should be labelled **mechanistic closure**, not a discovery hunt. The cheap empirical gates already bound the likely payoff.

---

# 9. Next discovery seam: joint address × temporal synapse dynamics

Current literature collision has already killed several broad claims:

```text
morphology matters for neuron computation                 prior art
learn STP temporal parameters                             prior art
learn synaptic location / strength in detailed neuron     TwinProp 2026
learn STP in a realistic multicompartment neuron          Carvalho/Buonomano 2011 lineage
optimize morphology/channel distribution for sequence     Torben-Nielsen/Stiefel 2009
```

The candidate unclosed intersection is narrower:

```text
fixed realistic morphology
    x jointly trainable synaptic ADDRESS
    x jointly trainable presynaptic STP dynamics
        (U, tau_D, tau_F)
```

and then ask whether learned temporal dynamics organize by **receiver transfer geometry** rather than simply by raw distance.

Required controls before any claim:

```text
learned address + fixed STP
fixed address + learned STP
learned all, then shuffle learned STP labels across addresses
path-distance-matched STP shuffle
isopotential / response-matched morphology control
same parameter/state budget
```

The passive delay-pairing/rearrangement lemma remains only a null because passive cable-delay spread is small relative to normal STP time scales.

Before writing the optimization harness, collide the exact joint seam once more with primary literature.

---

# Current decision

> **Park branch: stop escalation. Preserve it as a clean negative/narrowing result.**

> **Next: literature collision on joint synaptic address × full STP dynamics in a fixed realistic morphology. If still open, build the smallest runnable optimization harness with a shuffle control before writing more theory.**

This is the handoff state.
