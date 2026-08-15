#!/usr/bin/env python3
"""Local-nonlinearity address x STP kill gate.

Synthetic mechanism experiment only.  Not biological evidence and not a
novelty claim.

This follows the passive-tree null in JOINT_ADDRESS_STP_ORDER_POC_V02_RECEIPT.
The spatial medium is the same small asymmetric RC tree, but each candidate
site now has two passive kernels:

    h_local[i]   source i -> voltage at i
    h_soma[i]    source i -> soma

The direct source->soma kernels are area normalized as before, removing the
trivial DC-gain advantage of proximal sites.  The *local* kernels are not
individually normalized; their differences in local input impedance are
retained.  A single global smooth threshold converts sufficiently large local
voltage into a regenerative current, which then propagates to the soma through
that site's soma kernel.

Thus the only new mechanism is:

    presynaptic STP -> local voltage -> thresholded local feedback -> soma

Question:
    Does this minimal voltage-dependent feedback make the exact learned
    STP-to-address assignment matter?

Decisive intervention:
    Within each afferent, shuffle complete learned (U,tauD,tauF) tuples over
    the already frozen hard addresses.  Preserve everything else.

Matched controls:
    - beta=0 linear tree (should reproduce near-shuffle-invariance)
    - nonlinear isopotential medium (all sites share identical local and soma
      kernels; address must then be exchangeable)

The threshold is calibrated *before training* from the median candidate-site
response to one canonical fixed-STP three-spike burst.  It is not fitted to the
task or to the eventual shuffle result.
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


# -----------------------------------------------------------------------------
# Spatial medium
# -----------------------------------------------------------------------------

def _tree_matrices(n_nodes: int = 31, dt: float = 1.0):
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
    return C, depth, edges, expm(A * dt)


def make_tree_kernels(
    n_nodes: int = 31,
    candidate_count: int = 18,
    kernel_len: int = 110,
    dt: float = 1.0,
):
    C, depth, edges, step = _tree_matrices(n_nodes, dt)

    possible = np.arange(3, n_nodes)
    candidate_count = min(candidate_count, len(possible))
    pick = np.linspace(0, len(possible) - 1, candidate_count).round().astype(int)
    sites = possible[pick]

    soma, local = [], []
    soma_raw_area, soma_centroid, local_peak = [], [], []
    tt = np.arange(kernel_len, dtype=float) * dt

    for site in sites:
        v = np.zeros(n_nodes, float)
        v[site] = 1.0 / C[site]  # unit charge impulse
        ys = np.empty(kernel_len, float)
        yl = np.empty(kernel_len, float)
        for t in range(kernel_len):
            ys[t] = v[0]
            yl[t] = v[site]
            v = step @ v

        ys = np.maximum(ys, 0.0)
        yl = np.maximum(yl, 0.0)
        area = float(ys.sum())
        if area <= 1e-15:
            raise RuntimeError(f"degenerate soma kernel at site {site}")
        soma_raw_area.append(area)
        ys = ys / area  # strict source->soma area normalization
        soma_centroid.append(float((tt * ys).sum()))
        local_peak.append(float(yl.max()))
        soma.append(ys)
        local.append(yl)

    soma = np.asarray(soma, np.float32)
    local = np.asarray(local, np.float32)

    # One global physical-unit rescaling only, not per-site normalization.  This
    # preserves relative local impedance while keeping thresholds O(1).
    med_peak = float(np.median(np.max(local, axis=1)))
    if med_peak <= 0:
        raise RuntimeError("bad local kernel scale")
    local_scaled = local / med_peak

    meta = dict(
        candidate_sites=sites.tolist(),
        depth={str(int(s)): int(depth[s]) for s in sites},
        soma_raw_area=soma_raw_area,
        soma_centroid=soma_centroid,
        local_peak_raw=local_peak,
        local_global_scale=med_peak,
        local_peak_scaled=np.max(local_scaled, axis=1).tolist(),
        edge_conductances=edges,
    )
    return soma, local_scaled.astype(np.float32), meta


def make_isopotential(soma: np.ndarray, local: np.ndarray):
    sm = soma.mean(axis=0, keepdims=True)
    sm /= sm.sum(axis=1, keepdims=True)
    lm = local.mean(axis=0, keepdims=True)
    return (
        np.repeat(sm, soma.shape[0], axis=0).astype(np.float32),
        np.repeat(lm, local.shape[0], axis=0).astype(np.float32),
    )


# -----------------------------------------------------------------------------
# STP and threshold calibration
# -----------------------------------------------------------------------------

def canonical_release(T: int = 90, U: float = 0.5, tauD: float = 252.5, tauF: float = 252.5):
    spikes = np.zeros(T, np.float64)
    for t in (10, 24, 44):
        spikes[t] = 1.0
    x = 1.0
    u = U
    dD = math.exp(-1.0 / tauD)
    dF = math.exp(-1.0 / tauF)
    rel = np.zeros(T, np.float64)
    for t in range(T):
        x = 1.0 - (1.0 - x) * dD
        u = U + (u - U) * dF
        if spikes[t]:
            u = u + U * (1.0 - u)
            rel[t] = u * x
            x = x * (1.0 - u)
    return rel


def calibrate_threshold(local: np.ndarray):
    """Global threshold from canonical fixed-STP burst, before any learning."""
    rel = canonical_release()
    peaks = []
    for k in local:
        v = np.convolve(rel, k, mode="full")[: len(rel)]
        peaks.append(float(v.max()))
    theta = float(np.median(peaks))
    # Width fixed to 12% of calibrated threshold.  No task fitting.
    slope = max(theta * 0.12, 1e-4)
    return theta, slope, peaks


# -----------------------------------------------------------------------------
# Balanced temporal-order task
# -----------------------------------------------------------------------------

def make_dataset(repeats: int, seed: int, T: int = 180):
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
                rank = c if label == 0 else 3 - c
                t0 = base + rank * spacing + int(jitter[c])
                t1 = t0 + 14 + int(burst_jitter[c, 0])
                t2 = t1 + 20 + int(burst_jitter[c, 1])
                for t in (t0, t1, t2):
                    if 0 <= t < T:
                        spikes[c, t] = 1.0
            X.append(spikes)
            Y.append(float(label))
    order = rng.permutation(len(Y))
    return torch.from_numpy(np.stack(X)[order]), torch.tensor(np.asarray(Y, np.float32)[order])


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


# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
class NonlinearAddressSTP(nn.Module):
    def __init__(
        self,
        soma_kernels: torch.Tensor,
        local_kernels: torch.Tensor,
        cfg: Config,
        theta: float,
        slope: float,
        beta: float,
        learn_location: bool,
        learn_stp: bool,
        fixed_idx=None,
    ):
        super().__init__()
        self.cfg = cfg
        self.theta = float(theta)
        self.slope = float(slope)
        self.beta = float(beta)
        self.register_buffer("soma_kernels", soma_kernels.clone())
        self.register_buffer("local_kernels", local_kernels.clone())
        self.register_buffer("contact_channel", cfg.contact_channel())

        Cn = cfg.contacts
        S = soma_kernels.shape[0]
        if fixed_idx is None:
            fixed_idx = torch.linspace(0, S - 1, Cn).round().long()
        self.register_buffer("fixed_idx", fixed_idx.clone().long())

        logits = torch.full((Cn, S), -1.5)
        logits[torch.arange(Cn), self.fixed_idx] = 1.5
        self.loc_logits = nn.Parameter(logits, requires_grad=learn_location)

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
            return F.one_hot(self.fixed_idx, num_classes=self.soma_kernels.shape[0]).float()
        if hard:
            idx = self.loc_logits.argmax(dim=1)
            return F.one_hot(idx, num_classes=self.soma_kernels.shape[0]).float()
        return F.softmax(self.loc_logits / self.temperature, dim=1)

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

    def forward(self, spikes4, hard_location=False, return_diag=False):
        rel = self.release_train(spikes4)  # [B,C,T]
        B, Cn, T = rel.shape
        S, K = self.soma_kernels.shape

        # First convolution: each contact evaluated at every candidate site's
        # local voltage.  Soft address optimization is therefore a mixture of
        # complete physical site responses, not a mixture of kernels before the
        # nonlinearity.
        nfft = 1
        while nfft < T + K - 1:
            nfft *= 2
        rr = torch.fft.rfft(rel, n=nfft, dim=-1)                 # [B,C,F]
        lk = torch.fft.rfft(self.local_kernels, n=nfft, dim=-1) # [S,F]
        vloc = torch.fft.irfft(rr[:, :, None, :] * lk[None, None, :, :], n=nfft, dim=-1)
        vloc = vloc[..., :T]                                    # [B,C,S,T]

        # Smooth regenerative current.  beta=0 is the exact linear control.
        regen = F.softplus((vloc - self.theta) / self.slope) * self.slope
        source = rel[:, :, None, :] + self.beta * regen

        # Second convolution: local direct+regenerative current propagates to
        # soma through that same site's transfer kernel.
        sr = torch.fft.rfft(source, n=nfft, dim=-1)
        sk = torch.fft.rfft(self.soma_kernels, n=nfft, dim=-1)
        ys = torch.fft.irfft(sr * sk[None, None, :, :], n=nfft, dim=-1)[..., :T]

        p = self.location_weights(hard=hard_location)  # [C,S]
        y = torch.einsum("bcst,cs->bt", ys, p)
        feat = torch.stack([y[:, a:b].mean(dim=1) for a, b in self.cfg.windows], dim=1)
        logits = feat @ self.decoder_w + self.decoder_bias

        if not return_diag:
            return logits, feat
        with torch.no_grad():
            # Diagnostics use hard/soft weighted mean gate occupancy.
            gate_occ = (vloc > self.theta).float().mean(dim=(0, 3))  # [C,S]
            weighted_occ = float((gate_occ * p).sum().item() / Cn)
            max_v = float(vloc.max().item())
        return logits, feat, dict(weighted_gate_occupancy=weighted_occ, max_local_voltage=max_v)


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


def fit_variant(soma_np, local_np, cfg, theta, slope, beta, variant, seed, Xtr, ytr, Xte, yte):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    soma = torch.tensor(soma_np, dtype=torch.float32)
    local = torch.tensor(local_np, dtype=torch.float32)

    if variant == "fixed":
        m = NonlinearAddressSTP(soma, local, cfg, theta, slope, beta, False, False)
        train_model(m, Xtr, ytr, 240, 0.03, 0.0)
        hard = m
    elif variant == "loc_only":
        m = NonlinearAddressSTP(soma, local, cfg, theta, slope, beta, True, False)
        train_model(m, Xtr, ytr, 360, 0.028)
        idx = m.loc_logits.argmax(dim=1).detach()
        hard = NonlinearAddressSTP(soma, local, cfg, theta, slope, beta, False, False, fixed_idx=idx)
        copy_stp_decoder(m, hard)
        train_model(hard, Xtr, ytr, 100, 0.018, 0.0)
    elif variant == "stp_only":
        m = NonlinearAddressSTP(soma, local, cfg, theta, slope, beta, False, True)
        train_model(m, Xtr, ytr, 360, 0.020, 0.0)
        hard = m
    elif variant == "joint":
        m = NonlinearAddressSTP(soma, local, cfg, theta, slope, beta, True, True)
        train_model(m, Xtr, ytr, 430, 0.020)
        idx = m.loc_logits.argmax(dim=1).detach()
        hard = NonlinearAddressSTP(soma, local, cfg, theta, slope, beta, False, True, fixed_idx=idx)
        copy_stp_decoder(m, hard)
        train_model(hard, Xtr, ytr, 150, 0.014, 0.0)
    else:
        raise ValueError(variant)

    with torch.no_grad():
        ltr, _ = hard(Xtr, hard_location=True)
        lte, _, diag = hard(Xte, hard_location=True, return_diag=True)
        U, d, f = hard.stp_values()
        loc = hard.fixed_idx.cpu().tolist()
        diversity = []
        for c in range(cfg.channels):
            a = c * cfg.contacts_per_channel
            diversity.append(len(set(loc[a:a + cfg.contacts_per_channel])))
        result = dict(
            variant=variant,
            seed=seed,
            beta=beta,
            train_acc=accuracy(ltr, ytr),
            test_acc=accuracy(lte, yte),
            train_loss=float(F.binary_cross_entropy_with_logits(ltr, ytr)),
            test_loss=float(F.binary_cross_entropy_with_logits(lte, yte)),
            hard_location=loc,
            unique_locations_per_afferent=diversity,
            U=U.cpu().tolist(), tauD=d.cpu().tolist(), tauF=f.cpu().tolist(),
            decoder_w=hard.decoder_w.cpu().tolist(),
            decoder_bias=float(hard.decoder_bias),
            **diag,
        )
    return hard, result


def shuffled_stp_losses(model, X, y, n_shuffle, seed):
    rng = np.random.default_rng(seed)
    bu = model.raw_u.detach().clone()
    bd = model.raw_d.detach().clone()
    bf = model.raw_f.detach().clone()
    groups = []
    for c in range(model.cfg.channels):
        a = c * model.cfg.contacts_per_channel
        groups.append(np.arange(a, a + model.cfg.contacts_per_channel))

    with torch.no_grad():
        base_logits, _, base_diag = model(X, hard_location=True, return_diag=True)
        base_loss = float(F.binary_cross_entropy_with_logits(base_logits, y))
        base_acc = accuracy(base_logits, y)
        rows = []
        for _ in range(n_shuffle):
            perm = np.arange(model.cfg.contacts)
            for g in groups:
                perm[g] = rng.permutation(g)
            p = torch.as_tensor(perm, dtype=torch.long)
            model.raw_u.copy_(bu[p]); model.raw_d.copy_(bd[p]); model.raw_f.copy_(bf[p])
            logits, _, diag = model(X, hard_location=True, return_diag=True)
            rows.append(dict(
                loss=float(F.binary_cross_entropy_with_logits(logits, y)),
                acc=accuracy(logits, y),
                gate=diag["weighted_gate_occupancy"],
            ))
        model.raw_u.copy_(bu); model.raw_d.copy_(bd); model.raw_f.copy_(bf)

    losses = np.asarray([r["loss"] for r in rows])
    accs = np.asarray([r["acc"] for r in rows])
    gates = np.asarray([r["gate"] for r in rows])
    return dict(
        baseline_loss=base_loss,
        baseline_acc=base_acc,
        baseline_gate_occupancy=base_diag["weighted_gate_occupancy"],
        n=n_shuffle,
        shuffled_loss_mean=float(losses.mean()),
        shuffled_loss_min=float(losses.min()),
        shuffled_loss_max=float(losses.max()),
        shuffled_acc_mean=float(accs.mean()),
        shuffled_acc_min=float(accs.min()),
        shuffled_acc_max=float(accs.max()),
        shuffled_gate_mean=float(gates.mean()),
        loss_increase_mean=float(losses.mean() - base_loss),
        loss_ratio_mean=float(losses.mean() / max(base_loss, 1e-12)),
        rows=rows,
    )


def run_medium(name, soma, local, args, theta, slope, beta):
    cfg = Config()
    Xtr, ytr = make_dataset(args.train_repeats, 1001, cfg.T)
    Xte, yte = make_dataset(args.test_repeats, 9001, cfg.T)
    results, shuffles = [], []
    for seed in range(args.seeds):
        for variant in ("fixed", "loc_only", "stp_only", "joint"):
            m, r = fit_variant(soma, local, cfg, theta, slope, beta, variant, seed, Xtr, ytr, Xte, yte)
            r["medium"] = name
            results.append(r)
            print("NL_RESULT", json.dumps(r, separators=(",", ":")))
            if variant == "joint":
                sh = shuffled_stp_losses(m, Xte, yte, args.shuffles, 60000 + seed)
                sh.update(medium=name, seed=seed, beta=beta)
                shuffles.append(sh)
                print("NL_SHUFFLE", json.dumps({k:v for k,v in sh.items() if k != "rows"}, separators=(",", ":")))
    return results, shuffles


def summarize(results, shuffles, medium, beta):
    out = dict(medium=medium, beta=beta, variants={}, joint_shuffle={})
    for variant in ("fixed", "loc_only", "stp_only", "joint"):
        rr = [r for r in results if r["medium"] == medium and r["beta"] == beta and r["variant"] == variant]
        out["variants"][variant] = dict(
            n=len(rr),
            test_acc_mean=float(np.mean([r["test_acc"] for r in rr])),
            test_loss_mean=float(np.mean([r["test_loss"] for r in rr])),
            gate_occupancy_mean=float(np.mean([r["weighted_gate_occupancy"] for r in rr])),
        )
    ss = [s for s in shuffles if s["medium"] == medium and s["beta"] == beta]
    out["joint_shuffle"] = dict(
        n_seeds=len(ss),
        baseline_loss_mean=float(np.mean([s["baseline_loss"] for s in ss])),
        shuffled_loss_mean=float(np.mean([s["shuffled_loss_mean"] for s in ss])),
        mean_loss_ratio=float(np.mean([s["loss_ratio_mean"] for s in ss])),
        baseline_acc_mean=float(np.mean([s["baseline_acc"] for s in ss])),
        shuffled_acc_mean=float(np.mean([s["shuffled_acc_mean"] for s in ss])),
        baseline_gate_mean=float(np.mean([s["baseline_gate_occupancy"] for s in ss])),
        shuffled_gate_mean=float(np.mean([s["shuffled_gate_mean"] for s in ss])),
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=1)
    ap.add_argument("--shuffles", type=int, default=40)
    ap.add_argument("--train-repeats", type=int, default=40)
    ap.add_argument("--test-repeats", type=int, default=100)
    ap.add_argument("--beta", type=float, default=2.0)
    ap.add_argument("--output", default="joint_address_stp_nonlinear_poc_result.json")
    args = ap.parse_args()

    torch.set_num_threads(2)
    soma, local, meta = make_tree_kernels()
    iso_soma, iso_local = make_isopotential(soma, local)
    theta, slope, canonical_peaks = calibrate_threshold(local)
    iso_theta, iso_slope, iso_peaks = calibrate_threshold(iso_local)
    meta.update(
        threshold=theta,
        threshold_slope=slope,
        canonical_local_response_peak=canonical_peaks,
        isopotential_threshold=iso_theta,
        isopotential_threshold_slope=iso_slope,
        isopotential_canonical_peak=iso_peaks,
    )

    all_r, all_s = [], []
    runs = [
        ("tree_linear", soma, local, theta, slope, 0.0),
        ("tree_nonlinear", soma, local, theta, slope, args.beta),
        ("isopotential_nonlinear", iso_soma, iso_local, iso_theta, iso_slope, args.beta),
    ]
    summaries = []
    for name, sk, lk, th, sl, beta in runs:
        r, s = run_medium(name, sk, lk, args, th, sl, beta)
        all_r += r; all_s += s
        summaries.append(summarize(all_r, all_s, name, beta))

    result = dict(
        status="synthetic local-nonlinearity mechanism gate; not biological evidence",
        nonlinearity="global smooth threshold on local passive voltage; regenerative current then propagates through same site's soma kernel",
        threshold_rule="median candidate-site response to canonical homogeneous fixed-STP burst, fixed before training",
        beta=args.beta,
        spatial_meta=meta,
        summaries=summaries,
        results=all_r,
        shuffles=all_s,
    )
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print("=== NONLINEAR POC SUMMARY ===")
    for s in summaries:
        print(json.dumps(s, indent=2))


if __name__ == "__main__":
    main()
