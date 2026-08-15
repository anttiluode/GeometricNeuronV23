#!/usr/bin/env python3
"""Balanced forward/reverse joint address x STP proof-of-concept.

This is a synthetic mechanism gate, not biological evidence and not a novelty
claim.  It replaces the imbalanced majority task in joint_address_stp_poc.py
with a balanced spatiotemporal forward-vs-reverse discrimination task.

Question
--------
Does jointly learning dendritic address and presynaptic STP create a specific
STP-to-address assignment that matters after training?

The decisive intervention is a within-afferent shuffle of complete learned
(U, tau_D, tau_F) tuples over already-frozen hard addresses.  The exact tuple
multiset, afferent identity, decoder, contact weights, and addresses are held
fixed.  An isopotential control must be shuffle-invariant.

No diversity reward is used: if the optimizer collapses locations, that is a
real negative result for this toy rather than something to tune away.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass

import numpy as np
from scipy.linalg import expm
import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------------- spatial medium ----------------

def make_passive_tree_kernels(
    n_nodes: int = 31,
    candidate_count: int = 18,
    kernel_len: int = 110,
    dt: float = 1.0,
):
    C = np.empty(n_nodes, float)
    leak = np.empty(n_nodes, float)
    depth = np.zeros(n_nodes, int)
    for i in range(n_nodes):
        if i:
            depth[i] = depth[(i - 1) // 2] + 1
        C[i] = 0.85 + 0.25 * (1.0 + math.sin(0.71 * i + 0.2)) / 2.0 + 0.025 * depth[i]
        leak[i] = 0.008 + 0.004 * (1.0 + math.cos(0.43 * i)) / 2.0

    G = np.zeros((n_nodes, n_nodes), float)
    edges = []
    for child in range(1, n_nodes):
        parent = (child - 1) // 2
        g = 0.055 * (0.86 ** max(depth[child] - 1, 0)) * (1.0 + 0.20 * math.sin(1.37 * child))
        g = max(g, 0.008)
        G[parent, parent] += g
        G[child, child] += g
        G[parent, child] -= g
        G[child, parent] -= g
        edges.append((int(parent), int(child), float(g)))

    A = -np.diag(1.0 / C) @ (G + np.diag(leak))
    step = expm(A * dt)

    possible = np.arange(3, n_nodes)
    candidate_count = min(candidate_count, len(possible))
    pick = np.linspace(0, len(possible) - 1, candidate_count).round().astype(int)
    sites = possible[pick]

    kernels, raw_areas, peaks, centroids = [], [], [], []
    for site in sites:
        v = np.zeros(n_nodes, float)
        v[site] = 1.0 / C[site]
        y = np.empty(kernel_len, float)
        for t in range(kernel_len):
            y[t] = v[0]
            v = step @ v
        y = np.maximum(y, 0.0)
        area = float(y.sum())
        if area <= 1e-15:
            raise RuntimeError(f"degenerate site {site}")
        raw_areas.append(area)
        y /= area  # strict area/DC normalization
        tt = np.arange(kernel_len, dtype=float) * dt
        kernels.append(y)
        peaks.append(float(tt[np.argmax(y)]))
        centroids.append(float((tt * y).sum()))

    meta = dict(
        candidate_sites=sites.tolist(),
        depth={str(int(s)): int(depth[s]) for s in sites},
        raw_kernel_area=raw_areas,
        normalized_peak_time=peaks,
        normalized_centroid=centroids,
        edge_conductances=edges,
    )
    return np.asarray(kernels, np.float32), meta


def make_isopotential_kernels(kernels: np.ndarray) -> np.ndarray:
    mean = kernels.mean(axis=0, keepdims=True)
    mean /= mean.sum(axis=1, keepdims=True)
    return np.repeat(mean, kernels.shape[0], axis=0).astype(np.float32)


# ---------------- balanced temporal task ----------------

def make_dataset(repeats: int, seed: int, T: int = 180):
    """Balanced 4-afferent FWD vs REV sequence discrimination.

    Each afferent emits the same three-spike burst.  What changes between the
    two classes is the relative order of the four afferent burst onsets.
    Global onset, tempo and local jitter vary trial-to-trial, so the stable cue
    is relative spatiotemporal order rather than one absolute timestamp.
    """
    rng = np.random.default_rng(seed)
    X, Y = [], []
    for label in (0, 1):
        for _ in range(repeats):
            spikes = np.zeros((4, T), np.float32)
            base = int(rng.integers(10, 26))
            spacing = int(rng.integers(17, 27))
            jitter = rng.integers(-3, 4, size=4)
            burst_jitter = rng.integers(-1, 2, size=(4, 2))
            for c in range(4):
                rank = c if label == 0 else (3 - c)
                t0 = base + rank * spacing + int(jitter[c])
                # Three events engage depression/facilitation while preserving
                # a simple FWD/REV stimulus family.
                t1 = t0 + 14 + int(burst_jitter[c, 0])
                t2 = t1 + 20 + int(burst_jitter[c, 1])
                for t in (t0, t1, t2):
                    if 0 <= t < T:
                        spikes[c, t] = 1.0
            X.append(spikes)
            Y.append(float(label))

    order = rng.permutation(len(Y))
    X = np.stack(X)[order]
    Y = np.asarray(Y, np.float32)[order]
    return torch.from_numpy(X), torch.from_numpy(Y)


@dataclass
class Config:
    channels: int = 4
    contacts_per_channel: int = 3
    T: int = 180
    windows: tuple = ((35, 65), (65, 95), (95, 125), (125, 160))

    @property
    def contacts(self):
        return self.channels * self.contacts_per_channel

    def contact_channel(self):
        return torch.arange(self.channels).repeat_interleave(self.contacts_per_channel)


class AddressSTP(nn.Module):
    def __init__(self, kernels, cfg, learn_location, learn_stp, fixed_idx=None):
        super().__init__()
        self.cfg = cfg
        self.register_buffer("kernels", kernels.clone())
        self.register_buffer("contact_channel", cfg.contact_channel())
        Cn = cfg.contacts
        S = kernels.shape[0]

        if fixed_idx is None:
            fixed_idx = torch.linspace(0, S - 1, Cn).round().long()
        self.register_buffer("fixed_idx", fixed_idx.clone().long())

        logits = torch.full((Cn, S), -1.5)
        logits[torch.arange(Cn), self.fixed_idx] = 1.5
        self.loc_logits = nn.Parameter(logits, requires_grad=learn_location)

        # A true fixed-STP arm is homogeneous. Learned-STP arms start with only
        # small seed-dependent heterogeneity.
        if learn_stp:
            ru = 0.12 * torch.randn(Cn)
            rd = 0.12 * torch.randn(Cn)
            rf = 0.12 * torch.randn(Cn)
        else:
            ru = torch.zeros(Cn)
            rd = torch.zeros(Cn)
            rf = torch.zeros(Cn)
        self.raw_u = nn.Parameter(ru, requires_grad=learn_stp)
        self.raw_d = nn.Parameter(rd, requires_grad=learn_stp)
        self.raw_f = nn.Parameter(rf, requires_grad=learn_stp)

        self.decoder_w = nn.Parameter(torch.zeros(len(cfg.windows)))
        self.decoder_bias = nn.Parameter(torch.tensor(0.0))
        self.temperature = 1.0

    def stp_values(self):
        U = 0.05 + 0.90 * torch.sigmoid(self.raw_u)
        tauD = 5.0 + 495.0 * torch.sigmoid(self.raw_d)
        tauF = 5.0 + 495.0 * torch.sigmoid(self.raw_f)
        return U, tauD, tauF

    def location_weights(self, hard=False):
        if not self.loc_logits.requires_grad:
            return F.one_hot(self.fixed_idx, num_classes=self.kernels.shape[0]).float()
        if hard:
            idx = self.loc_logits.argmax(dim=1)
            return F.one_hot(idx, num_classes=self.kernels.shape[0]).float()
        return F.softmax(self.loc_logits / self.temperature, dim=1)

    def effective_kernels(self, hard=False):
        return self.location_weights(hard=hard) @ self.kernels

    def release_train(self, spikes4):
        B, _, T = spikes4.shape
        Cn = self.cfg.contacts
        inp = spikes4[:, self.contact_channel, :]
        U, tauD, tauF = self.stp_values()
        U = U[None, :]
        dD = torch.exp(-1.0 / tauD)[None, :]
        dF = torch.exp(-1.0 / tauF)[None, :]
        x = torch.ones((B, Cn), device=spikes4.device)
        u = U.expand(B, -1)
        rel = []
        for t in range(T):
            x = 1.0 - (1.0 - x) * dD
            u = U + (u - U) * dF
            s = inp[:, :, t]
            u_event = u + s * U * (1.0 - u)
            r = s * u_event * x
            x = x * (1.0 - s * u_event)
            u = u_event
            rel.append(r)
        return torch.stack(rel, dim=-1)

    def forward(self, spikes4, hard_location=False):
        rel = self.release_train(spikes4)
        k = self.effective_kernels(hard=hard_location)
        nfft = 1
        need = rel.shape[-1] + k.shape[-1] - 1
        while nfft < need:
            nfft *= 2
        rr = torch.fft.rfft(rel, n=nfft, dim=-1)
        kk = torch.fft.rfft(k, n=nfft, dim=-1)
        yc = torch.fft.irfft(rr * kk[None, :, :], n=nfft, dim=-1)
        y = yc.sum(dim=1)[:, : self.cfg.T]
        feat = torch.stack([y[:, a:b].mean(dim=1) for a, b in self.cfg.windows], dim=1)
        logits = feat @ self.decoder_w + self.decoder_bias
        return logits, feat


def accuracy(logits, y):
    return float(((torch.sigmoid(logits) >= 0.5) == (y >= 0.5)).float().mean().item())


def train_model(model, X, y, steps, lr, entropy_weight=0.002):
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.Adam(params, lr=lr)
    for step in range(steps):
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


def copy_stp_decoder(src, dst):
    with torch.no_grad():
        dst.raw_u.copy_(src.raw_u)
        dst.raw_d.copy_(src.raw_d)
        dst.raw_f.copy_(src.raw_f)
        dst.decoder_w.copy_(src.decoder_w)
        dst.decoder_bias.copy_(src.decoder_bias)


def fit_variant(kernels_np, cfg, variant, seed, Xtr, ytr, Xte, yte):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    kernels = torch.tensor(kernels_np, dtype=torch.float32)

    if variant == "fixed":
        m = AddressSTP(kernels, cfg, False, False)
        train_model(m, Xtr, ytr, 260, 0.03, 0.0)
        hard = m
    elif variant == "loc_only":
        m = AddressSTP(kernels, cfg, True, False)
        train_model(m, Xtr, ytr, 420, 0.03)
        idx = m.loc_logits.argmax(dim=1).detach()
        hard = AddressSTP(kernels, cfg, False, False, fixed_idx=idx)
        copy_stp_decoder(m, hard)
        train_model(hard, Xtr, ytr, 120, 0.02, 0.0)
    elif variant == "stp_only":
        m = AddressSTP(kernels, cfg, False, True)
        train_model(m, Xtr, ytr, 420, 0.022, 0.0)
        hard = m
    elif variant == "joint":
        m = AddressSTP(kernels, cfg, True, True)
        train_model(m, Xtr, ytr, 500, 0.022)
        idx = m.loc_logits.argmax(dim=1).detach()
        hard = AddressSTP(kernels, cfg, False, True, fixed_idx=idx)
        copy_stp_decoder(m, hard)
        train_model(hard, Xtr, ytr, 180, 0.016, 0.0)
    else:
        raise ValueError(variant)

    with torch.no_grad():
        ltr, _ = hard(Xtr, hard_location=True)
        lte, _ = hard(Xte, hard_location=True)
        U, d, f = hard.stp_values()
        loc = hard.fixed_idx.cpu().tolist()
        diversity = []
        for c in range(cfg.channels):
            a = c * cfg.contacts_per_channel
            diversity.append(len(set(loc[a:a + cfg.contacts_per_channel])))
        result = dict(
            variant=variant,
            seed=seed,
            train_acc=accuracy(ltr, ytr),
            test_acc=accuracy(lte, yte),
            train_loss=float(F.binary_cross_entropy_with_logits(ltr, ytr)),
            test_loss=float(F.binary_cross_entropy_with_logits(lte, yte)),
            hard_location=loc,
            unique_locations_per_afferent=diversity,
            U=U.cpu().tolist(),
            tauD=d.cpu().tolist(),
            tauF=f.cpu().tolist(),
            decoder_w=hard.decoder_w.cpu().tolist(),
            decoder_bias=float(hard.decoder_bias),
        )
    return hard, result


def shuffled_stp_losses(model, X, y, n_shuffle, seed):
    rng = np.random.default_rng(seed)
    base_u = model.raw_u.detach().clone()
    base_d = model.raw_d.detach().clone()
    base_f = model.raw_f.detach().clone()
    groups = []
    for c in range(model.cfg.channels):
        a = c * model.cfg.contacts_per_channel
        groups.append(np.arange(a, a + model.cfg.contacts_per_channel))

    with torch.no_grad():
        base_logits, _ = model(X, hard_location=True)
        base_loss = float(F.binary_cross_entropy_with_logits(base_logits, y))
        base_acc = accuracy(base_logits, y)
        rows = []
        for _ in range(n_shuffle):
            perm = np.arange(model.cfg.contacts)
            for g in groups:
                perm[g] = rng.permutation(g)
            p = torch.as_tensor(perm, dtype=torch.long)
            model.raw_u.copy_(base_u[p])
            model.raw_d.copy_(base_d[p])
            model.raw_f.copy_(base_f[p])
            logits, _ = model(X, hard_location=True)
            rows.append(dict(
                loss=float(F.binary_cross_entropy_with_logits(logits, y)),
                acc=accuracy(logits, y),
            ))
        model.raw_u.copy_(base_u)
        model.raw_d.copy_(base_d)
        model.raw_f.copy_(base_f)

    losses = np.asarray([r["loss"] for r in rows])
    accs = np.asarray([r["acc"] for r in rows])
    return dict(
        baseline_loss=base_loss,
        baseline_acc=base_acc,
        n=n_shuffle,
        shuffled_loss_mean=float(losses.mean()),
        shuffled_loss_min=float(losses.min()),
        shuffled_loss_max=float(losses.max()),
        shuffled_acc_mean=float(accs.mean()),
        shuffled_acc_min=float(accs.min()),
        shuffled_acc_max=float(accs.max()),
        loss_increase_mean=float(losses.mean() - base_loss),
        loss_ratio_mean=float(losses.mean() / max(base_loss, 1e-12)),
        rows=rows,
    )


def run_medium(name, kernels_np, args):
    cfg = Config()
    Xtr, ytr = make_dataset(args.train_repeats, 1001, cfg.T)
    Xte, yte = make_dataset(args.test_repeats, 9001, cfg.T)
    results, shuffles = [], []
    for seed in range(args.seeds):
        for variant in ("fixed", "loc_only", "stp_only", "joint"):
            model, r = fit_variant(kernels_np, cfg, variant, seed, Xtr, ytr, Xte, yte)
            r["medium"] = name
            results.append(r)
            print("ORDER_RESULT", json.dumps(r, separators=(",", ":")))
            if variant == "joint":
                sh = shuffled_stp_losses(model, Xte, yte, args.shuffles, 70000 + seed)
                sh.update(medium=name, seed=seed)
                shuffles.append(sh)
                print("ORDER_SHUFFLE", json.dumps({k: v for k, v in sh.items() if k != "rows"}, separators=(",", ":")))
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
    ap.add_argument("--seeds", type=int, default=1)
    ap.add_argument("--shuffles", type=int, default=40)
    ap.add_argument("--train-repeats", type=int, default=64)
    ap.add_argument("--test-repeats", type=int, default=160)
    ap.add_argument("--output", default="joint_address_stp_order_poc_result.json")
    args = ap.parse_args()

    torch.set_num_threads(2)
    tree, meta = make_passive_tree_kernels()
    iso = make_isopotential_kernels(tree)
    all_results, all_shuffles = [], []
    for name, k in (("tree", tree), ("isopotential", iso)):
        r, s = run_medium(name, k, args)
        all_results += r
        all_shuffles += s

    summaries = [summarize(all_results, all_shuffles, m) for m in ("tree", "isopotential")]
    payload = dict(
        status="balanced synthetic mechanism gate; not biological evidence",
        task="balanced 4-afferent forward-vs-reverse burst-order discrimination",
        literature_guardrail="Carvalho & Buonomano 2011 FWD/REV spatiotemporal discrimination lineage",
        spatial_control="area-normalized passive tree; isopotential identical mean kernel",
        shuffle_control="within-afferent complete learned STP tuple shuffle over frozen hard addresses",
        kernel_meta=meta,
        summaries=summaries,
        results=all_results,
        shuffles=all_shuffles,
    )
    with open(args.output, "w") as f:
        json.dump(payload, f, indent=2)
    print("=== ORDER POC SUMMARY ===")
    for s in summaries:
        print(json.dumps(s, indent=2))


if __name__ == "__main__":
    main()
