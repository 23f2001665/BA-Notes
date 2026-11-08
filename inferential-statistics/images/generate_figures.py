"""Regenerates every figure used in the inferential-statistics/ notes.

Run from anywhere:  python inferential-statistics/images/generate_figures.py
Requires: numpy, scipy, matplotlib
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

OUT = Path(__file__).resolve().parent
C = ["#2563eb", "#dc2626", "#16a34a", "#d97706", "#7c3aed", "#0891b2"]
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 110, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25,
    "axes.titlesize": 11, "axes.labelsize": 10, "legend.fontsize": 9,
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------------------ 01
def fig01():
    """Four probability sampling schemes on a population of 10x10 points in 4 groups."""
    rng = np.random.default_rng(4)
    gx, gy = np.meshgrid(np.arange(10), np.arange(10))
    x, y = gx.ravel(), gy.ravel()
    group = (x >= 5).astype(int) + 2 * (y >= 5).astype(int)        # four 5x5 blocks (strata/clusters)
    idx = np.arange(100)
    schemes = {}
    schemes["Simple random\n(every unit equally likely)"] = rng.choice(idx, 12, replace=False)
    schemes["Stratified\n(3 random from each group)"] = np.concatenate(
        [rng.choice(idx[group == g], 3, replace=False) for g in range(4)])
    chosen = rng.choice(4, 1)[0]
    # cluster = whole small blocks of 5 rows/columns; pick 2 of 20 row-segments of 5
    seg = (y * 2 + (x >= 5))                                          # 20 segments of 5 points
    pick = rng.choice(20, 2, replace=False)
    schemes["Cluster\n(whole groups chosen at random)"] = idx[np.isin(seg, pick)]
    schemes["Systematic\n(every 8th unit)"] = idx[3::8]
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.5))
    for a, (title, sel) in zip(ax, schemes.items()):
        a.scatter(x, y, c=[["#9ca3af", "#fca5a5", "#93c5fd", "#86efac"][g] for g in group], s=55, zorder=2)
        a.scatter(x[sel], y[sel], s=130, facecolors="none", edgecolors="black", linewidths=2, zorder=3)
        a.set(title=title, xticks=[], yticks=[])
        a.grid(False)
        a.spines[["left", "bottom"]].set_visible(False)
    save(fig, "01_sampling_methods.png")


def fig01b():
    """Bigger sample does not cure bias."""
    rng = np.random.default_rng(2)
    mu_true = 100
    pop = rng.lognormal(np.log(80), 0.6, 200_000)
    mu_true = pop.mean()
    ns = np.array([10, 30, 100, 300, 1000, 3000, 10000, 30000])
    random_est, biased_est = [], []
    w = pop ** 1.0 / (pop ** 1.0).sum()           # high spenders more likely to respond
    for n in ns:
        random_est.append(rng.choice(pop, n).mean())
        biased_est.append(rng.choice(pop, n, p=w).mean())
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(ns, random_est, "o-", color=C[2], label="random sample")
    ax.plot(ns, biased_est, "o-", color=C[1], label="self-selected (big spenders over-represented)")
    ax.axhline(mu_true, color="black", ls="--", lw=1.2, label=f"true mean = {mu_true:.0f}")
    ax.set(xscale="log", xlabel="sample size n", ylabel="sample mean order value (₹)",
           title="More data shrinks random error, not bias")
    ax.legend()
    save(fig, "01_bias_vs_size.png")


# ------------------------------------------------------------------ 02
def fig02():
    """CLT grid: three population shapes x increasing n."""
    rng = np.random.default_rng(0)
    pops = [("Exponential (skewed)", lambda sz: rng.exponential(1, sz)),
            ("Uniform (flat)", lambda sz: rng.uniform(0, 1, sz)),
            ("Bimodal", lambda sz: np.where(rng.random(sz) < 0.5, rng.normal(0, 0.4, sz), rng.normal(3, 0.4, sz)))]
    ns = [1, 2, 5, 30]
    fig, ax = plt.subplots(3, 4, figsize=(12, 7), sharey="row")
    for r, (name, draw) in enumerate(pops):
        for c, n in enumerate(ns):
            m = draw((20000, n)).mean(axis=1)
            ax[r, c].hist(m, bins=50, density=True, color=C[0], alpha=0.65)
            g = np.linspace(m.min(), m.max(), 300)
            if n > 1:
                ax[r, c].plot(g, stats.norm.pdf(g, m.mean(), m.std()), color=C[1], lw=1.4)
            ax[r, c].set_title(f"n = {n}" if r == 0 else "", fontsize=10)
            ax[r, c].set_yticks([])
        ax[r, 0].set_ylabel(name, fontsize=10)
    fig.suptitle("Sampling distribution of the mean: whatever the population, it approaches a normal bell (red)", y=1.0)
    save(fig, "02_clt_grid.png")


def fig02b():
    rng = np.random.default_rng(1)
    fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.5))
    n = np.arange(1, 401)
    ax[0].plot(n, 12 / np.sqrt(n), color=C[0])
    ax[0].axvline(36, color="grey", ls="--", lw=1)
    ax[0].text(40, 6, "n = 36 → SE = 2", fontsize=9)
    ax[0].set(title="Standard error = σ/√n (σ = 12)", xlabel="sample size n", ylabel="SE of x̄")
    k = np.arange(1, 2001)
    for c in C[:4]:
        ax[1].plot(k, np.cumsum(rng.random(k.size) < 0.5) / k, color=c, lw=1)
    ax[1].axhline(0.5, color="black", lw=0.8)
    ax[1].set(xscale="log", ylim=(0.2, 0.8), title="Law of large numbers: fair coin",
              xlabel="number of tosses", ylabel="proportion of heads")
    # sampling distribution of p-hat
    p, nn = 0.3, 200
    g = np.linspace(0.18, 0.42, 400)
    ax[2].plot(g, stats.norm.pdf(g, p, np.sqrt(p * (1 - p) / nn)), color=C[0])
    m = g >= 0.35
    ax[2].fill_between(g[m], stats.norm.pdf(g[m], p, np.sqrt(p * (1 - p) / nn)), color=C[1], alpha=0.6)
    ax[2].text(0.352, 3, "P(p̂ ≥ 0.35)\n≈ 0.061", fontsize=9)
    ax[2].set(title="Sampling distribution of p̂ (p = 0.3, n = 200)", xlabel="sample proportion p̂", ylabel="density")
    save(fig, "02_se_lln_phat.png")


def fig02c():
    """Sampling distribution of x-bar with the worked example shaded."""
    fig, ax = plt.subplots(figsize=(7.5, 3.5))
    g = np.linspace(30, 50, 500)
    ax.plot(g, stats.norm.pdf(g, 40, 12), color="grey", label="individual deliveries: mean 40, SD 12")
    ax.plot(g, stats.norm.pdf(g, 40, 2), color=C[0], lw=2, label="sample means, n = 36: mean 40, SE 2")
    m = g >= 43
    ax.fill_between(g[m], stats.norm.pdf(g[m], 40, 2), color=C[1], alpha=0.6)
    ax.text(43.3, 0.05, "P(x̄ > 43) = 0.067", color=C[1], fontsize=9)
    ax.set(title="Averages vary far less than individual values", xlabel="delivery time (min)", ylabel="density")
    ax.legend(loc="upper left")
    save(fig, "02_individual_vs_mean.png")


# ------------------------------------------------------------------ 03
def fig03():
    """CI coverage: 50 intervals, ~95% cover the true mean."""
    rng = np.random.default_rng(11)
    mu, sd, n, reps = 50, 10, 25, 50
    fig, ax = plt.subplots(figsize=(7.5, 6))
    miss = 0
    for i in range(reps):
        s = rng.normal(mu, sd, n)
        m, se = s.mean(), s.std(ddof=1) / np.sqrt(n)
        h = stats.t.ppf(0.975, n - 1) * se
        ok = (m - h <= mu <= m + h)
        miss += (not ok)
        ax.plot([m - h, m + h], [i, i], color=C[0] if ok else C[1], lw=2)
        ax.plot(m, i, "o", color=C[0] if ok else C[1], ms=3)
    ax.axvline(mu, color="black", lw=1.2, label="true mean μ = 50")
    ax.set(title=f"50 different samples, 50 different 95% intervals — {miss} miss μ (red)",
           xlabel="value", ylabel="sample number", yticks=[])
    ax.legend(loc="upper right")
    save(fig, "03_ci_coverage.png")


def fig03b():
    fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.5))
    # bias/variance of estimators
    g = np.linspace(-6, 10, 600)
    ax[0].plot(g, stats.norm.pdf(g, 2, 0.6), color=C[2], label="unbiased, low variance")
    ax[0].plot(g, stats.norm.pdf(g, 2, 1.6), color=C[0], label="unbiased, high variance")
    ax[0].plot(g, stats.norm.pdf(g, 4.2, 0.6), color=C[1], label="biased, low variance")
    ax[0].axvline(2, color="black", ls="--", lw=1)
    ax[0].text(2.1, 0.62, "true θ", fontsize=9)
    ax[0].set(title="Estimators: bias vs variance", xlabel="estimate", ylabel="density", ylim=(0, 0.72))
    ax[0].legend(fontsize=8, loc="upper left")
    # t vs z interval multiplier
    n = np.arange(2, 101)
    ax[1].plot(n, stats.t.ppf(0.975, n - 1), color=C[0], label="t critical value")
    ax[1].axhline(1.96, color="black", ls="--", lw=1, label="z = 1.96")
    ax[1].set(title="95% multiplier: t shrinks to z as n grows", xlabel="sample size n", ylabel="critical value")
    ax[1].legend()
    # sample size for proportion
    E = np.linspace(0.01, 0.1, 200)
    for p, c in [(0.5, C[1]), (0.3, C[0]), (0.1, C[2])]:
        ax[2].plot(E * 100, 1.96 ** 2 * p * (1 - p) / E ** 2, color=c, label=f"p = {p}")
    ax[2].set(yscale="log", title="Sample size needed for a 95% margin of error E",
              xlabel="margin of error E (percentage points)", ylabel="required n")
    ax[2].legend()
    save(fig, "03_estimators_and_n.png")


def fig03c():
    """Width of CI: effect of confidence level and n."""
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    n = np.arange(5, 301)
    for lev, c in [(0.90, C[2]), (0.95, C[0]), (0.99, C[1])]:
        ax.plot(n, 2 * stats.t.ppf(1 - (1 - lev) / 2, n - 1) * 10 / np.sqrt(n), color=c, label=f"{int(lev*100)}% confidence")
    ax.set(title="CI width for a mean (s = 10)", xlabel="sample size n", ylabel="width of interval")
    ax.legend()
    save(fig, "03_ci_width.png")


# ------------------------------------------------------------------ 04
def fig04():
    """Null distribution, rejection regions, and the p-value for z = 2."""
    g = np.linspace(-4, 4, 600)
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 3.6))
    ax[0].plot(g, stats.norm.pdf(g), color="black")
    for lo, hi in [(-4, -1.96), (1.96, 4)]:
        m = (g >= lo) & (g <= hi)
        ax[0].fill_between(g[m], stats.norm.pdf(g[m]), color=C[1], alpha=0.6)
    ax[0].text(0, 0.1, "do not reject H₀\n(95%)", ha="center")
    ax[0].text(2.3, 0.07, "reject\n2.5%", ha="center", color=C[1], fontsize=9)
    ax[0].text(-2.3, 0.07, "reject\n2.5%", ha="center", color=C[1], fontsize=9)
    ax[0].set(title="Two-tailed test at α = 0.05: critical values ±1.96", xlabel="z (if H₀ is true)", ylabel="density")

    ax[1].plot(g, stats.norm.pdf(g), color="black")
    for lo, hi in [(-4, -2), (2, 4)]:
        m = (g >= lo) & (g <= hi)
        ax[1].fill_between(g[m], stats.norm.pdf(g[m]), color=C[0], alpha=0.6)
    ax[1].axvline(2, color=C[0], ls="--")
    ax[1].text(2.1, 0.2, "observed z = 2", color=C[0], fontsize=9)
    ax[1].text(0, 0.1, "p-value = 0.0455\n= both shaded tails", ha="center")
    ax[1].set(title="p-value: how extreme is the data if H₀ is true?", xlabel="z (if H₀ is true)")
    save(fig, "04_rejection_and_pvalue.png")


def fig04b():
    """Type I / Type II error and power."""
    mu0, mu1, se = 30, 32, 1.0
    g = np.linspace(25, 37, 800)
    crit_hi, crit_lo = mu0 + 1.96 * se, mu0 - 1.96 * se
    fig, ax = plt.subplots(figsize=(8.5, 3.9))
    ax.plot(g, stats.norm.pdf(g, mu0, se), color=C[0], lw=2, label="H₀ true: μ = 30")
    ax.plot(g, stats.norm.pdf(g, mu1, se), color=C[2], lw=2, label="H₁ true: μ = 32")
    m = g >= crit_hi
    ax.fill_between(g[m], stats.norm.pdf(g[m], mu0, se), color=C[1], alpha=0.7, label="α: Type I error (2.5% per tail)")
    m = g <= crit_lo
    ax.fill_between(g[m], stats.norm.pdf(g[m], mu0, se), color=C[1], alpha=0.7)
    m = (g > crit_lo) & (g < crit_hi)
    ax.fill_between(g[m], stats.norm.pdf(g[m], mu1, se), color=C[3], alpha=0.45, label="β: Type II error = 0.48")
    ax.axvline(crit_hi, color="black", ls="--", lw=1)
    ax.axvline(crit_lo, color="black", ls="--", lw=1)
    ax.text(crit_hi + 0.15, 0.2, "reject H₀ →", fontsize=9)
    ax.set(title="Error types and power (n = 49, σ = 7, power = 1 − β ≈ 0.52)", xlabel="sample mean x̄", ylabel="density")
    ax.legend(loc="upper left", fontsize=8)
    save(fig, "04_errors_power.png")


def fig04c():
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))
    n = np.arange(5, 301)
    for delta, c in [(1, C[1]), (2, C[0]), (3, C[2])]:
        se = 7 / np.sqrt(n)
        power = stats.norm.sf(1.96 - delta / se) + stats.norm.cdf(-1.96 - delta / se)
        ax[0].plot(n, power, color=c, label=f"true shift = {delta} min")
    ax[0].axhline(0.8, color="grey", ls="--", lw=1)
    ax[0].set(title="Power rises with n and with effect size (σ = 7)", xlabel="sample size n", ylabel="power")
    ax[0].legend(loc="lower right")
    d = np.linspace(0, 5, 200)
    for a, c in [(0.01, C[1]), (0.05, C[0]), (0.10, C[2])]:
        zc = stats.norm.ppf(1 - a / 2)
        ax[1].plot(d, stats.norm.sf(zc - d / 1) + stats.norm.cdf(-zc - d / 1), color=c, label=f"α = {a}")
    ax[1].set(title="Power vs shift (n = 49): lower α, lower power", xlabel="true shift μ − μ₀ (min)", ylabel="power")
    ax[1].legend(loc="lower right")
    save(fig, "04_power_curves.png")


if __name__ == "__main__":
    for f in [fig01, fig01b, fig02, fig02b, fig02c, fig03, fig03b, fig03c, fig04, fig04b, fig04c]:
        f()
    print("figures written to", OUT)
