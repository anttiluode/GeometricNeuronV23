#!/usr/bin/env python3
"""Joint synaptic address x short-term-plasticity proof-of-concept.

PURPOSE
-------
This is a *software / mechanism smoke test*, not a biological result and not a
novelty claim.  It asks whether a strict post-training STP-label shuffle can
detect mutual specialization between temporal synaptic dynamics and a fixed
spatial transfer medium.

The medium is a small asymmetric passive RC tree.  Each candidate synaptic site
has a soma impulse-response kernel derived from the exact linear tree dynamics.
Every kernel is area-normalized before learning, deliberately removing the
trivial DC-gain advantage of choosing a proximal site.  Location can therefore
matter only through temporal kernel shape/delay.

There are four afferent channels and three contacts per channel.  Contacts of a
given afferent receive *identical spike trains*.  Thus shuffling complete STP
parameter tuples among the three contacts of the same afferent preserves:

    - presynaptic feature identity
    - learned hard dendritic addresses
    - the exact multiset of learned STP parameter tuples
    - the decoder

and changes only which temporal synapse sits at which address.

A matched isopotential control replaces every spatial kernel by the same mean
kernel.  In that control, within-afferent STP-label shuffling must be exactly
irrelevant (up to numerical roundoff), because equal-weight contacts with the
same input and same spatial kernel are exchangeable.

STP uses a standard Tsodyks-Markram-like depression/facilitation update with
learnable U, tau_D, tau_F.  The implementation is a differentiable toy, not a
claim to reproduce any specific biological synapse.

The task is a small interval/majority classification problem.  It is chosen to
exercise temporal synapses; it is not claimed to model behavior.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from itertools import product

import numpy as np
from scipy.linalg import expm
import torch
import torch.nn as nn
import torch.nn.functional as F


# --------------------------- spatial medium ---------------------------

def make_passive_tree_kernels(
    n_nodes: int = 31,
    candidate_count: int = 18,
    kernel_len: int = 100,
    dt: float = 1.0,
) -> tuple[np.ndarray, dict]:
    """Return area-normalized soma kernels for sites on an asymmetric RC tree."""
    # Binary-tree topology with deterministic heterogeneous electrical geometry.
    C = np.empty(n_nodes, float)
    leak = np.empty(n_nodes, float)
    depth = np.zeros(n_nodes, int)
    for i in range(n_nodes):
        if i:
            depth[i] = depth[(i - 1) // 2] + 1
        # Smooth but nonuniform capacitance/leak; positive and deterministic.
        C[i] = 0.85 + 0.25 * (1.0 + math.sin(0.71 * i + 0.2)) / 2.0 + 0.025 * depth[i]
        leak[i] = 0.008 + 0.004 * (1.0 + math.cos(0.43 * i)) / 2.0

    G = np.zeros((n_nodes, n_nodes), float)
    edge_g = []
    for child in range(1, n_nodes):
        parent = (child - 1) // 2
        # Axial coupling decreases mildly with depth and alternates between limbs.
        g = 0.055 * (0.86 ** max(depth[child] - 1, 0)) * (1.0 + 0.20 * math.sin(1.37 * child))
        g = max(g, 0.008)
        edge_g.append((parent, child, g))
        G[parent, parent] += g
        G[child, child] += g
        G[parent, child] -= g
        G[child, parent] -= g

    A = -np.diag(1.0 / C) @ (G + np.diag(leak))
    step = expm(A * dt)

    # Candidate sites emphasize non-somatic and distal/intermediate addresses.
    possible = np.arange(3, n_nodes)
    if candidate_count > len(possible):
        candidate_count = len(possible)
    pick = np.linspace(0, len(possible) - 1, candidate_count).round().astype(int)
    sites = possible[pick]

    kernels = []
    raw_areas = []
    peak_times = []
    centroids = []
    for site in sites:
        # Unit charge impulse: dv = C^-1 e_site.
        v = np.zeros(n_nodes, float)
        v[site] = 1.0 / C[site]
        y = np.empty(kernel_len, float)
        for t in range(kernel_len):
            y[t] = v[0]
            v = step @ v
        # Tiny early numerical values can be ~0; kernel should be positive here.
        y = np.maximum(y, 0.0)
        area = float(y.sum())
        if area <= 1e-15:
            raise RuntimeError(f"degenerate site {site}")
        raw_areas.append(area)
        y = y / area  # strict DC/area normalization
        tt = np.arange(kernel_len, dtype=float) * dt
        kernels.append(y)
        peak_times.append(float(tt[np.argmax(y)]))
        centroids.append(float((tt * y).sum()))

    meta = dict(
        n_nodes=n_nodes,
        candidate_sites=sites.tolist(),
        depth={str(int(s)): int(depth[s]) for s in sites},
        raw_kernel_area=raw_areas,
        normalized_peak_time=peak_times,
        normalized_centroid=centroids,
        edge_conductances=[(int(a), int(b), float(g)) for a, b, g in edge_g],
    )
    return np.asarray(kernels, np.float32), meta


def make_isopotential_kernels(kernels: np.ndarray) -> np.ndarray:
    mean = kernels.mean(axis=0, keepdims=True)
    mean /= mean.sum(axis=1, keepdims=True)
    return np.repeat(mean, kernels.shape[0], axis=0).astype(np.float32)


# --------------------------- task ---------------------------

def make_dataset(repeats: int, seed: int, T: int = 160) -> tuple[torch.Tensor, torch.Tensor]:
    """Four afferents encode short/long inter-spike intervals; classify majority-long."""
    rng = np.random.default_rng(seed)
    X = []
    Y = []
    base = np.asarray([12, 20, 28, 36])
    short = 18
    long = 62
    for bits in product([0, 1], repeat=4):
        target = 1.0 if sum(bits) >= 2 else 0.0
        for _ in range(repeats):
            spikes = np.zeros((4, T), np.float32)
            jitter = rng.integers(-3, 4, size=4)
            for c, bit in enumerate(bits):
                t0 = int(base[c] + jitter[c])
                isi = long if bit else short
                # Three spikes: the second probes interval state, the third probes
                # how that state was transformed by the second.
                ts = [t0, t0 + isi, t0 + isi + 18]
                for t in ts:
                    if 0 <= t < T:
                        spikes[c, t] = 1.0
            X.append(spikes)
            Y.append(target)
    return torch.from_numpy(np.stack(X)), torch.tensor(Y, dtype=torch.float32)


@dataclass
class Config:
    channels: int = 4
    contacts_per_channel: int = 3
    T: int = 160
    read_start: int = 82
    read_end: int = 142

    @property
    def contacts(self) -> int:
        return self.channels * self.contacts_per_channel

    def contact_channel(self) -> torch.Tensor:
        return torch.arange(self.channels).repeat_interleave(self.contacts_per_channel)


# --------------------------- differentiable synapses ---------------------------
class AddressSTP(nn.Module):
    def __init__(
        self,
        kernels: torch.Tensor,
        cfg: Config,
        learn_location: bool,
        learn_stp: bool,
        fixed_idx: torch.Tensor | None = None,
    ):
        super().__init__()
        self.cfg = cfg
        self.register_buffer("kernels", kernels.clone())  # [S,K]
        self.register_buffer("contact_channel", cfg.contact_channel())
        C = cfg.contacts
        S = kernels.shape[0]

        if fixed_idx is None:
            # Deterministic broad initial coverage.
            fixed_idx = torch.linspace(0, S - 1, C).round().long()
        self.register_buffer("fixed_idx", fixed_idx.clone().long())

        # Initialize logits close to the broad fixed layout, but not exactly one-hot.
        logits = torch.full((C, S), -1.5)
        logits[torch.arange(C), self.fixed_idx] = 1.5
        self.loc_logits = nn.Parameter(logits, requires_grad=learn_location)

        # Parametrization maps raw values into biologically plausible broad ranges.
        # Different contacts start slightly different so the optimizer can specialize.
        g = torch.Generator().manual_seed(12345)
        self.raw_u = nn.Parameter(0.15 * torch.randn(C, generator=g), requires_grad=learn_stp)
        self.raw_d = nn.Parameter(0.15 * torch.randn(C, generator=g), requires_grad=learn_stp)
        self.raw_f = nn.Parameter(0.15 * torch.randn(C, generator=g), requires_grad=learn_stp)

        self.decoder_scale = nn.Parameter(torch.tensor(12.0))
        self.decoder_bias = nn.Parameter(torch.tensor(-0.2))
        self.temperature = 1.0

    def stp_values(self):
        U = 0.05 + 0.90 * torch.sigmoid(self.raw_u)
        tauD = 5.0 + 495.0 * torch.sigmoid(self.raw_d)
        tauF = 5.0 + 495.0 * torch.sigmoid(self.raw_f)
        return U, tauD, tauF

    def location_weights(self, hard: bool = False):
        if not self.loc_logits.requires_grad:
            return F.one_hot(self.fixed_idx, num_classes=self.kernels.shape[0]).float()
        if hard:
            idx = self.loc_logits.argmax(dim=1)
            return F.one_hot(idx, num_classes=self.kernels.shape[0]).float()
        return F.softmax(self.loc_logits / self.temperature, dim=1)

    def effective_kernels(self, hard: bool = False):
        return self.location_weights(hard=hard) @ self.kernels

    def release_train(self, spikes4: torch.Tensor):
        """Return released efficacy events [B,C,T]."""
        B, _, T = spikes4.shape
        C = self.cfg.contacts
        input_spikes = spikes4[:, self.contact_channel, :]  # [B,C,T]
        U, tauD, tauF = self.stp_values()
        U = U[None, :]
        dD = torch.exp(-1.0 / tauD)[None, :]
        dF = torch.exp(-1.0 / tauF)[None, :]
        x = torch.ones((B, C), device=spikes4.device)
        u = U.expand(B, -1)
        rel = []
        for t in range(T):
            # Recovery during the one-ms interval preceding this event bin.
            x = 1.0 - (1.0 - x) * dD
            u = U + (u - U) * dF
            s = input_spikes[:, :, t]
            u_event = u + s * U * (1.0 - u)
            r = s * u_event * x
            x = x * (1.0 - s * u_event)
            u = u_event
            rel.append(r)
        return torch.stack(rel, dim=-1)

    def forward(self, spikes4: torch.Tensor, hard_location: bool = False):
        rel = self.release_train(spikes4)  # [B,C,T]
        k = self.effective_kernels(hard=hard_location)  # [C,K]
        nfft = 1
        need = rel.shape[-1] + k.shape[-1] - 1
        while nfft < need:
            nfft *= 2
        rr = torch.fft.rfft(rel, n=nfft, dim=-1)
        kk = torch.fft.rfft(k, n=nfft, dim=-1)
        y_contacts = torch.fft.irfft(rr * kk[None, :, :], n=nfft, dim=-1)
        y = y_contacts.sum(dim=1)[:, : self.cfg.T]
        # Fixed physical readout: mean soma response in one late temporal window.
        feat = y[:, self.cfg.read_start : self.cfg.read_end].mean(dim=1)
        logits = self.decoder_scale * feat + self.decoder_bias
        return logits, feat


# --------------------------- training / evaluation ---------------------------
def accuracy(logits, y):
    return float(((torch.sigmoid(logits) >= 0.5) == (y >= 0.5)).float().mean().item())


def train_model(model, X, y, steps: int, lr: float, entropy_weight: float = 0.002):
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.Adam(params, lr=lr)
    for step in range(steps):
        # Anneal spatial softmax only if location is trainable.
        if model.loc_logits.requires_grad:
            frac = step / max(steps - 1, 1)
            model.temperature = 1.0 * (0.12 ** frac)
        opt.zero_grad(set_to_none=True)
        logits, _ = model(X)
        loss = F.binary_cross_entropy_with_logits(logits, y)
        if model.loc_logits.requires_grad:
            p = F.softmax(model.loc_logits / model.temperature, dim=1)
            ent = -(p * torch.log(p + 1e-12)).sum(dim=1).mean()
            loss = loss + entropy_weight * ent
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 5.0)
        opt.step()
    return model


def copy_stp_and_decoder(src: AddressSTP, dst: AddressSTP):
    with torch.no_grad():
        dst.raw_u.copy_(src.raw_u)
        dst.raw_d.copy_(src.raw_d)
        dst.raw_f.copy_(src.raw_f)
        dst.decoder_scale.copy_(src.decoder_scale)
        dst.decoder_bias.copy_(src.decoder_bias)


def fit_variant(kernels_np, cfg, variant: str, seed: int, Xtr, ytr, Xte, yte):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    kernels = torch.tensor(kernels_np, dtype=torch.float32)

    if variant == "fixed":
        m = AddressSTP(kernels, cfg, False, False)
        # Only decoder is trainable.
        train_model(m, Xtr, ytr, 180, 0.03, 0.0)
        hard = m
    elif variant == "loc_only":
        m = AddressSTP(kernels, cfg, True, False)
        train_model(m, Xtr, ytr, 320, 0.035)
        idx = m.loc_logits.argmax(dim=1).detach()
        hard = AddressSTP(kernels, cfg, False, False, fixed_idx=idx)
        copy_stp_and_decoder(m, hard)
        train_model(hard, Xtr, ytr, 100, 0.02, 0.0)
    elif variant == "stp_only":
        m = AddressSTP(kernels, cfg, False, True)
        train_model(m, Xtr, ytr, 320, 0.025, 0.0)
        hard = m
    elif variant == "joint":
        m = AddressSTP(kernels, cfg, True, True)
        train_model(m, Xtr, ytr, 380, 0.025)
        idx = m.loc_logits.argmax(dim=1).detach()
        # Hard-address refinement: location frozen; temporal synapses may adapt to
        # the address they actually occupy. This avoids reporting a soft-mixture win.
        hard = AddressSTP(kernels, cfg, False, True, fixed_idx=idx)
        copy_stp_and_decoder(m, hard)
        train_model(hard, Xtr, ytr, 140, 0.018, 0.0)
    else:
        raise ValueError(variant)

    with torch.no_grad():
        ltr, _ = hard(Xtr, hard_location=True)
        lte, _ = hard(Xte, hard_location=True)
        result = dict(
            variant=variant,
            seed=seed,
            train_acc=accuracy(ltr, ytr),
            test_acc=accuracy(lte, yte),
            train_loss=float(F.binary_cross_entropy_with_logits(ltr, ytr)),
            test_loss=float(F.binary_cross_entropy_with_logits(lte, yte)),
            hard_location=hard.fixed_idx.cpu().tolist(),
        )
        U, d, f = hard.stp_values()
        result["U"] = U.cpu().tolist()
        result["tauD"] = d.cpu().tolist()
        result["tauF"] = f.cpu().tolist()
    return hard, result


def shuffled_stp_losses(model: AddressSTP, X, y, n_shuffle: int, seed: int):
    """Within-afferent tuple shuffle: preserves inputs, addresses, decoder, tuple multiset."""
    rng = np.random.default_rng(seed)
    base_u = model.raw_u.detach().clone()
    base_d = model.raw_d.detach().clone()
    base_f = model.raw_f.detach().clone()
    groups = []
    for c in range(model.cfg.channels):
        start = c * model.cfg.contacts_per_channel
        groups.append(np.arange(start, start + model.cfg.contacts_per_channel))

    with torch.no_grad():
        base_logits, _ = model(X, hard_location=True)
        base_loss = float(F.binary_cross_entropy_with_logits(base_logits, y))
        base_acc = accuracy(base_logits, y)
        rows = []
        for s in range(n_shuffle):
            perm = np.arange(model.cfg.contacts)
            for g in groups:
                perm[g] = rng.permutation(g)
            p = torch.as_tensor(perm, dtype=torch.long)
            model.raw_u.copy_(base_u[p])
            model.raw_d.copy_(base_d[p])
            model.raw_f.copy_(base_f[p])
            logits, _ = model(X, hard_location=True)
            rows.append(dict(loss=float(F.binary_cross_entropy_with_logits(logits, y)), acc=accuracy(logits, y)))
        model.raw_u.copy_(base_u)
        model.raw_d.copy_(base_d)
        model.raw_f.copy_(base_f)

    losses = np.array([r["loss"] for r in rows])
    accs = np.array([r["acc"] for r in rows])
    return dict(
        baseline_loss=base_loss,
        baseline_acc=base_acc,
        n=n_shuffle,
        shuffled_loss_mean=float(losses.mean()),
        shuffled_loss_median=float(np.median(losses)),
        shuffled_loss_min=float(losses.min()),
        shuffled_loss_max=float(losses.max()),
        shuffled_acc_mean=float(accs.mean()),
        shuffled_acc_min=float(accs.min()),
        shuffled_acc_max=float(accs.max()),
        loss_increase_mean=float(losses.mean() - base_loss),
        loss_ratio_mean=float(losses.mean() / max(base_loss, 1e-12)),
        rows=rows,
    )


def run_medium(name: str, kernels_np: np.ndarray, args):
    cfg = Config()
    Xtr, ytr = make_dataset(repeats=args.train_repeats, seed=1001, T=cfg.T)
    Xte, yte = make_dataset(repeats=args.test_repeats, seed=9001, T=cfg.T)
    results = []
    shuffles = []
    for seed in range(args.seeds):
        for variant in ("fixed", "loc_only", "stp_only", "joint"):
            model, r = fit_variant(kernels_np, cfg, variant, seed, Xtr, ytr, Xte, yte)
            r["medium"] = name
            results.append(r)
            print("POC_RESULT", json.dumps(r, separators=(",", ":")))
            if variant == "joint":
                sh = shuffled_stp_losses(model, Xte, yte, args.shuffles, seed=50000 + seed)
                sh.update(medium=name, seed=seed)
                shuffles.append(sh)
                print("POC_SHUFFLE", json.dumps({k: v for k, v in sh.items() if k != "rows"}, separators=(",", ":")))
    return results, shuffles


def summarize(results, shuffles, medium):
    out = {"medium": medium, "variants": {}, "joint_shuffle": {}}
    for variant in ("fixed", "loc_only", "stp_only", "joint"):
        rr = [r for r in results if r["medium"] == medium and r["variant"] == variant]
        out["variants"][variant] = dict(
            n=len(rr),
            test_acc_mean=float(np.mean([r["test_acc"] for r in rr])),
            test_acc_min=float(np.min([r["test_acc"] for r in rr])),
            test_acc_max=float(np.max([r["test_acc"] for r in rr])),
            test_loss_mean=float(np.mean([r["test_loss"] for r in rr])),
        )
    ss = [s for s in shuffles if s["medium"] == medium]
    out["joint_shuffle"] = dict(
        n_seeds=len(ss),
        baseline_loss_mean=float(np.mean([s["baseline_loss"] for s in ss])),
        shuffled_loss_mean_across_seeds=float(np.mean([s["shuffled_loss_mean"] for s in ss])),
        mean_loss_increase=float(np.mean([s["loss_increase_mean"] for s in ss])),
        mean_loss_ratio=float(np.mean([s["loss_ratio_mean"] for s in ss])),
        baseline_acc_mean=float(np.mean([s["baseline_acc"] for s in ss])),
        shuffled_acc_mean=float(np.mean([s["shuffled_acc_mean"] for s in ss])),
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--shuffles", type=int, default=60)
    ap.add_argument("--train-repeats", type=int, default=4)
    ap.add_argument("--test-repeats", type=int, default=10)
    ap.add_argument("--output", default="joint_address_stp_poc_result.json")
    args = ap.parse_args()

    torch.set_num_threads(2)
    tree, meta = make_passive_tree_kernels()
    iso = make_isopotential_kernels(tree)

    all_results = []
    all_shuffles = []
    for name, k in (("tree", tree), ("isopotential", iso)):
        r, s = run_medium(name, k, args)
        all_results += r
        all_shuffles += s

    summaries = [summarize(all_results, all_shuffles, m) for m in ("tree", "isopotential")]
    result = dict(
        status="software/mechanism proof-of-concept; not biological evidence",
        task="4-afferent short/long interval majority; 3 equal-weight contacts per afferent",
        spatial_control="all tree kernels area-normalized; isopotential uses identical mean kernel",
        shuffle_control="within-afferent shuffle of complete learned (U,tauD,tauF) tuples over fixed learned hard addresses",
        kernel_meta=meta,
        summaries=summaries,
        results=all_results,
        shuffles=all_shuffles,
    )
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print("=== POC SUMMARY ===")
    for s in summaries:
        print(json.dumps(s, indent=2))


if __name__ == "__main__":
    main()
