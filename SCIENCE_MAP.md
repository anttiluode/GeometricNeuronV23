# GeometricNeuronV23 — science map

This file is intentionally conservative. Each paper is here because it supports a specific piece of V23. None of these papers, individually, is evidence that the full V23 architecture is new or correct.

The project is strongest when it says:

```text
this piece is established here;
this other piece is established there;
this particular composition / intervention is what we still need to test.
```

---

## A. The abstraction we are extending

### McCulloch & Pitts (1943) — point / threshold neuron

Warren S. McCulloch & Walter Pitts, **A logical calculus of the ideas immanent in nervous activity**, *Bulletin of Mathematical Biophysics* 5, 115–133.

- DOI: https://doi.org/10.1007/BF02478259
- Publisher page: https://link.springer.com/article/10.1007/BF02478259

Why it matters here: this is the historical ancestor of the many-inputs / threshold-output abstraction. V23 is not arguing that it is useless. It is asking what is lost when a spatially extended, locally stateful biological cell is collapsed to that interface.

---

## B. Dendrites as nonlinear computational structure

### Mel (1993) — spatial organization and cluster sensitivity

Bartlett W. Mel, **Synaptic integration in an excitable dendritic tree**, *Journal of Neurophysiology* 70(3):1086–1101.

- DOI: https://doi.org/10.1152/jn.1993.70.3.1086

Why it matters: spatial arrangement of excitatory input on an active dendritic tree changes the response. Geometry is not merely decorative wiring.

### Schiller et al. (2000) — local NMDA spikes

Jackie Schiller, Guy Major, Helmut J. Koester, Yitzhak Schiller, **NMDA spikes in basal dendrites of cortical pyramidal neurons**, *Nature* 404:285–289.

- DOI: https://doi.org/10.1038/35005094
- Paper: https://www.nature.com/articles/35005094

Why it matters: clustered neighboring inputs can create spatially restricted dendritic nonlinear events whose somatic effect is a filtered projection of a local computation.

### Poirazi, Brannon & Mel (2003) — pyramidal neuron as two-layer network

Panayiota Poirazi, Terrence Brannon, Bartlett W. Mel, **Pyramidal neuron as two-layer neural network**, *Neuron* 37(6):989–999.

- DOI: https://doi.org/10.1016/S0896-6273(03)00149-1
- PubMed: https://pubmed.ncbi.nlm.nih.gov/12670427/

Companion paper:

- **Arithmetic of subthreshold synaptic summation in a model CA1 pyramidal cell**
- DOI: https://doi.org/10.1016/S0896-6273(03)00148-X

Why it matters: a detailed pyramidal cell can be usefully abstracted as multiple nonlinear dendritic subunits feeding a second stage rather than as a single immediate sum-and-threshold unit.

### Bicknell & Häusser (2021) — learning can exploit dendritic nonlinearities

Brendan A. Bicknell & Michael Häusser, **A synaptic learning rule for exploiting nonlinear dendritic computation**, *Neuron* 109(24):4001–4017.e10.

- DOI: https://doi.org/10.1016/j.neuron.2021.09.044
- PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC8691952/

Why it matters: dendritic cable/nonlinear structure is not only something to describe after the fact; a learning rule can exploit it for nonlinear spatiotemporal feature binding.

---

## C. Geometry as electrical coupling / compartmentalization

### Wybo, Stiefel & Torben-Nielsen (2013) — Green functions for dendrites

Willem A. M. Wybo, Klaus M. Stiefel, Benjamin Torben-Nielsen, **The Green's function formalism as a bridge between single- and multi-compartmental modeling**.

- DOI: https://doi.org/10.1007/s00422-013-0568-0
- PubMed: https://pubmed.ncbi.nlm.nih.gov/24037222/
- arXiv: https://arxiv.org/abs/1309.2382

Why it matters: it gives a rigorous source-location → time-dependent receiver-response language without requiring vague “geometry” metaphors.

### Wybo et al. (2019) — electrical compartmentalization

Willem A. M. Wybo, Benjamin Torben-Nielsen, Thomas Nevian, Marc-Oliver Gewaltig, **Electrical Compartmentalization in Neurons**, *Cell Reports* 26(7):1759–1773.e7.

- DOI: https://doi.org/10.1016/j.celrep.2019.01.074
- PubMed: https://pubmed.ncbi.nlm.nih.gov/30759388/

Why it matters: dendritic trees can be understood in terms of impedance-defined electrical compartments, and the effective compartment structure can change with input/conductance state.

### Beaulieu-Laroche et al. (2018) — direct human dendritic compartmentalization

Lou Beaulieu-Laroche et al., **Enhanced Dendritic Compartmentalization in Human Cortical Neurons**, *Cell* 175(3):643–651.e14.

- DOI: https://doi.org/10.1016/j.cell.2018.08.045
- PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC6197488/

Why it matters: direct human dendritic recordings show that morphology/biophysics can produce stronger electrical separation than in rat neurons. This is experimental physiology, not merely model geometry.

### Eyal et al. (2018) — many independent nonlinear subunits in human L2/3 models

Guy Eyal et al., **Human Cortical Pyramidal Neurons: From Spines to Spikes via Models**, *Frontiers in Cellular Neuroscience* 12:181.

- DOI: https://doi.org/10.3389/fncel.2018.00181
- Full text: https://www.frontiersin.org/journals/cellular-neuroscience/articles/10.3389/fncel.2018.00181/full

Why it matters: the models predict tens of independent local NMDA-spike subunits in human L2/3 pyramidal neurons and explicitly relate their independence to electrical separation.

### Wybo et al. (2021) — preserving dendro-somatic responses under reduction

Willem A. M. Wybo et al., **Data-driven reduction of dendritic morphologies with preserved dendro-somatic responses**, *eLife* 10:e60936.

- DOI: https://doi.org/10.7554/eLife.60936
- Full text: https://elifesciences.org/articles/60936

Why it matters: it shows that the computationally relevant morphology depends on the source/receiver transformation one intends to preserve; moving nonlinear synaptic inputs can require special care.

---

## D. Single-neuron complexity is already an active research program

### Beniaguev, Segev & London (2021) — detailed cortical neuron ≈ deep temporal network

David Beniaguev, Idan Segev, Michael London, **Single cortical neurons as deep artificial neural networks**, *Neuron* 109(17):2727–2739.e3.

- DOI: https://doi.org/10.1016/j.neuron.2021.07.002
- PubMed: https://pubmed.ncbi.nlm.nih.gov/34380016/

Why it matters: a detailed L5 pyramidal model required a multi-layer temporal DNN surrogate; dendritic morphology and NMDA receptor interactions were major contributors to the complexity.

### Aizenbud et al. (2026) — morphology + synaptic nonlinearities and FCI

Ido Aizenbud et al., **Dendritic morphology and synaptic nonlinearities enhance functional complexity in human cortical neurons**, *PNAS* 123(28):e2533168123.

- DOI: https://doi.org/10.1073/pnas.2533168123
- PNAS: https://www.pnas.org/doi/10.1073/pnas.2533168123
- PubMed: https://pubmed.ncbi.nlm.nih.gov/42412934/
- Code: https://github.com/ido4848/FCI

Why it matters: this is the closest direct empirical/modeling collision with the Geometric Neuron line. A fixed temporal network has more difficulty emulating some neurons than others; morphology and human synaptic parameters both contribute.

Important V23 correction from the released code: the standard `AMPANMDA_EMS.mod` keeps AMPA/NMDA conductance-state memory but omits the presynaptic recovered/unrecovered / depression / facilitation machinery described in the historical BBP comments.

Exact FCI source anchor:

- https://github.com/ido4848/FCI/blob/55826436751c03a32dfd39e91a48894869e1db57/simulating_neurons/neuron_models/rat/hay/Rat_L5b_PC_2_Hay_passive_dends_simple_soma/mods/AMPANMDA_EMS.mod

### Aizenbud et al. (2026 preprint) — TwinProp / task capacity

Ido Aizenbud, David Beniaguev, Noam Pnueli, Idan Segev, Michael London, **What can a neuron compute**.

- DOI: https://doi.org/10.64898/2026.06.08.730984
- bioRxiv: https://www.biorxiv.org/content/10.64898/2026.06.08.730984v1
- PubMed: https://pubmed.ncbi.nlm.nih.gov/42327113/

Why it matters: digital-twin gradients are used to optimize synaptic strengths and dendritic locations in a detailed neuron for actual tasks. This distinguishes **emulation difficulty** from **usable optimized task capacity**.

### Beniaguev et al. (2026) — dendro-plexing / multiple contacts per source

David Beniaguev, Sapir Shapira, Idan Segev, Michael London, **Dendro-plexing of Single Input Spikes via Multiple Synaptic Contacts Can Enhance Cortical Neuron Computation and Reduce Axonal Wiring**, *Journal of Neuroscience* 46(17):e0839242026.

- DOI: https://doi.org/10.1523/JNEUROSCI.0839-24.2026
- PubMed: https://pubmed.ncbi.nlm.nih.gov/41916758/

Why it matters: the same temporal source can be expressed at multiple spatial contacts, giving one input several dendritic transfer filters. That is directly relevant to V23's distinction between **temporal source identity** and **geometric contact address**.

---

## E. Synapses as local hidden-state machines

### Tsodyks, Pawelzik & Markram (1998) — dynamic synapses

Misha Tsodyks, Klaus Pawelzik, Henry Markram, **Neural networks with dynamic synapses**, *Neural Computation* 10(4):821–835.

- DOI: https://doi.org/10.1162/089976698300017502
- PubMed: https://pubmed.ncbi.nlm.nih.gov/9573407/

Why it matters: synaptic transmission depends on recent presynaptic history; depression/facilitation can be represented with local dynamical variables rather than fixed weights.

### Maass & Markram (2002) — “dynamic memory buffers”

Wolfgang Maass & Henry Markram, **Synapses as dynamic memory buffers**, *Neural Networks* 15(2):155–161.

- DOI: https://doi.org/10.1016/S0893-6080(01)00144-7
- PubMed: https://pubmed.ncbi.nlm.nih.gov/12022505/

Why it matters: the paper explicitly studies how a synapse's internal dynamical state stores information about the recent presynaptic spike train and exposes that information in subsequent postsynaptic responses.

### Mongillo, Barak & Tsodyks (2008) — activity-silent synaptic working memory

Gianluigi Mongillo, Omri Barak, Misha Tsodyks, **Synaptic theory of working memory**, *Science* 319(5869):1543–1546.

- DOI: https://doi.org/10.1126/science.1150769
- PubMed: https://pubmed.ncbi.nlm.nih.gov/18339943/

Why it matters: presynaptic residual calcium / facilitation can hold a latent memory trace that is later refreshed and read out by spiking. This is a direct scientific ancestor of the V23 “quiet local history waiting to be sampled by a later event” intuition.

### Oesch & Diamond (2011) — a real synapse computes with vesicle-pool state

Nicholas W. Oesch & Jeffrey S. Diamond, **Ribbon synapses compute temporal contrast and encode luminance in retinal rod bipolar cells**, *Nature Neuroscience* 14:1555–1561.

- DOI: https://doi.org/10.1038/nn.2945
- PubMed: https://pubmed.ncbi.nlm.nih.gov/22019730/
- PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC3225507/

Why it matters: depletion/replenishment state of the readily releasable vesicle pool shapes temporal contrast computation. A synapse is a local stateful transducer, not a passive scalar edge.

### James et al. (2019) — ribbon synapses carry amplitude and frequency codes

Ben James et al., **An amplitude code transmits information at a visual synapse**, *Nature Neuroscience* 22:1140–1147.

- DOI: https://doi.org/10.1038/s41593-019-0403-6
- PubMed: https://pubmed.ncbi.nlm.nih.gov/31110322/

Why it matters: a tiny synaptic junction does not force all information into a binary spike timing code. Retinal bipolar ribbon synapses can encode contrast in both release-event frequency and amplitude.

---

## F. The retina makes receiver choice and spatially arranged time constants explicit

### Euler, Detwiler & Denk (2002) — local computation can disappear at soma

Thomas Euler, Peter B. Detwiler, Winfried Denk, **Directionally selective calcium signals in dendrites of starburst amacrine cells**, *Nature* 418:845–852.

- DOI: https://doi.org/10.1038/nature00931
- Paper: https://www.nature.com/articles/nature00931
- PubMed: https://pubmed.ncbi.nlm.nih.gov/12192402/

Why it matters: individual dendritic branches behaved as independent direction-selective modules; dendritic Ca was direction selective while somatic voltage was not. Receiver choice can reveal or erase a computation.

### Srivastava et al. (2022) — temporal kernels are spatially arranged

Prerna Srivastava et al., **Spatiotemporal properties of glutamate input support direction selectivity in the dendrites of retinal starburst amacrine cells**, *eLife* 11:e81533.

- DOI: https://doi.org/10.7554/eLife.81533
- Full text: https://elifesciences.org/articles/81533
- Open model: https://github.com/geoffder/spatiotemporal-starburst-model

Why it matters: proximal glutamatergic inputs are more sustained and distal inputs more transient. This supplies an existing biological example in which **temporal response properties are correlated with geometric address**.

### Acarón Ledesma et al. (2024) — global context + local dendritic computation

Héctor Acarón Ledesma et al., **Dendritic mGluR2 and perisomatic Kv3 signaling regulate dendritic computation of mouse starburst amacrine cells**, *Nature Communications* 15:1819.

- DOI: https://doi.org/10.1038/s41467-024-46234-7
- Paper: https://www.nature.com/articles/s41467-024-46234-7

Why it matters: the perisomatic region integrates motion into a low-pass global depolarization while local dendrites combine that global state with local synaptic input to generate direction-selective local events. This is a concrete example of a slowly varying distributed state modulating what a later local input can do.

---

## G. A note on “Clockfield” language

The old Clockfield vocabulary is useful only after translation.

Do **not** infer from these papers that neurons contain a new physical time field.

The established mechanisms already give us a rigorous descendant:

```text
recent events
    -> local physical state variables
    -> different relaxation / recovery times
    -> later events sample those states
    -> geometry determines how the effects propagate
```

That is enough to speak operationally about a **field of local histories** or a **distribution of local ages**, as long as “field” means spatially distributed state variables and “age” means a derived coordinate of those states rather than a literal universal clock.

---

## H. What appears not to be established by the literature above

The papers above do **not** by themselves establish that:

- a V23 artificial layer will outperform standard recurrent architectures;
- spatially structured short-term-plasticity time constants are generally optimized by biological morphology;
- FCI increases when presynaptic STP is restored;
- receiver-relative emulation complexity is a standard accepted complexity metric;
- the V23 structured-vs-shuffled interaction is novel;
- any Clockfield physics claim follows from neuron dynamics.

Those remain experiments / literature-search obligations.

That distinction is the reason this bibliography exists.