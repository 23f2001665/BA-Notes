"""Regenerates every figure used in the descriptive-statistics/ notes.

Run from anywhere:  python descriptive-statistics/images/generate_figures.py
Requires: numpy, scipy, matplotlib >= 3.10
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

# The running salary example (₹ thousand per month): nine typical staff + one founder
SAL = np.array([28, 30, 32, 33, 35, 36, 38, 40, 45, 300.])


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig01():
    """Mean vs median vs mode on symmetric, right-skewed and left-skewed data."""
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.5))
    g = np.linspace(-3.5, 3.5, 500)
    cases = [
        ("Symmetric: mean = median = mode", stats.norm(0, 1), 0.0, 0.0, 0.0, g),
        ("Right-skewed: mode < median < mean", stats.gamma(2, scale=1), None, None, None,
         np.linspace(0, 10, 500)),
        ("Left-skewed: mean < median < mode", None, None, None, None, np.linspace(-10, 0, 500)),
    ]
    # symmetric
    d = stats.norm(0, 1)
    ax[0].plot(g, d.pdf(g), color="black")
    ax[0].axvline(0, color=C[1], lw=2, label="mean = median = mode")
    ax[0].set(title=cases[0][0], xlabel="value", ylabel="density")
    ax[0].legend()
    # right skew
    d = stats.gamma(2, scale=1); x = cases[1][5]
    ax[1].plot(x, d.pdf(x), color="black")
    ax[1].axvline(1.0, color=C[2], lw=2, label="mode = 1")
    ax[1].axvline(d.median(), color=C[0], lw=2, ls="--", label=f"median = {d.median():.2f}")
    ax[1].axvline(d.mean(), color=C[1], lw=2, ls=":", label="mean = 2")
    ax[1].set(title=cases[1][0], xlabel="value")
    ax[1].legend()
    # left skew (mirror)
    x = cases[2][5]
    ax[2].plot(x, d.pdf(-x), color="black")
    ax[2].axvline(-1.0, color=C[2], lw=2, label="mode = −1")
    ax[2].axvline(-d.median(), color=C[0], lw=2, ls="--", label=f"median = {-d.median():.2f}")
    ax[2].axvline(-d.mean(), color=C[1], lw=2, ls=":", label="mean = −2")
    ax[2].set(title=cases[2][0], xlabel="value")
    ax[2].legend(loc="upper left")
    save(fig, "01_mean_median_mode.png")


def fig01b():
    """Salary data: the mean is dragged by the outlier, the median is not."""
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.2), gridspec_kw={"width_ratios": [1.3, 1]})
    y = np.zeros_like(SAL)
    ax[0].scatter(SAL, y, s=60, color=C[0], zorder=3)
    ax[0].axvline(np.mean(SAL), color=C[1], lw=2, label=f"mean = {np.mean(SAL):.1f}")
    ax[0].axvline(np.median(SAL), color=C[2], lw=2, ls="--", label=f"median = {np.median(SAL):.1f}")
    ax[0].set(title="Ten salaries (₹ thousand/month): one founder at 300",
              xlabel="salary (₹ thousand)", yticks=[], ylim=(-0.5, 0.8))
    ax[0].legend(loc="upper center", ncol=2)

    lab = ["mean", "median", "10% trimmed\nmean"]
    from scipy.stats import trim_mean
    with_ = [SAL.mean(), np.median(SAL), trim_mean(SAL, 0.1)]
    without = [SAL[:-1].mean(), np.median(SAL[:-1]), trim_mean(SAL[:-1], 0.1)]
    x = np.arange(3)
    ax[1].bar(x - 0.2, with_, width=0.4, color=C[1], label="with the 300")
    ax[1].bar(x + 0.2, without, width=0.4, color=C[2], label="without it")
    ax[1].set_xticks(x, lab)
    ax[1].set(title="How much does one outlier move each?", ylabel="₹ thousand")
    ax[1].legend()
    save(fig, "01_outlier_effect.png")


def fig02():
    """Same mean, different spread; and the IQR vs SD under an outlier."""
    rng = np.random.default_rng(3)
    a = rng.normal(50, 3, 60)
    b = rng.normal(50, 12, 60)
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.4))
    ax[0].scatter(a, np.full_like(a, 1) + rng.uniform(-0.12, 0.12, a.size), color=C[0], s=18, alpha=0.8)
    ax[0].scatter(b, np.full_like(b, 0) + rng.uniform(-0.12, 0.12, b.size), color=C[1], s=18, alpha=0.8)
    ax[0].axvline(50, color="grey", ls="--", lw=1)
    ax[0].set(yticks=[0, 1], yticklabels=["Store B\n(SD ≈ 12)", "Store A\n(SD ≈ 3)"],
              xlabel="daily sales (₹ thousand)", title="Same mean (50), very different spread")

    labels = ["Range", "SD", "IQR", "MAD"]
    with_ = [np.ptp(SAL), SAL.std(ddof=1), np.subtract(*np.percentile(SAL, [75, 25])),
             np.median(abs(SAL - np.median(SAL)))]
    s9 = SAL[:-1]
    without = [np.ptp(s9), s9.std(ddof=1), np.subtract(*np.percentile(s9, [75, 25])),
               np.median(abs(s9 - np.median(s9)))]
    x = np.arange(4)
    ax[1].bar(x - 0.2, with_, width=0.4, color=C[1], label="with the 300")
    ax[1].bar(x + 0.2, without, width=0.4, color=C[2], label="without it")
    ax[1].set_xticks(x, labels)
    ax[1].set_yscale("log")
    ax[1].set(title="Resistance to an outlier (log scale)", ylabel="value (₹ thousand)")
    ax[1].legend()
    save(fig, "02_spread.png")


def fig03():
    """Skewness and kurtosis gallery."""
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
    g = np.linspace(0, 12, 600)
    ax[0].plot(-g + 12, stats.gamma.pdf(g, 2), color=C[1], label="negative skew")
    ax[0].plot(np.linspace(-3, 3, 600) + 6, stats.norm.pdf(np.linspace(-3, 3, 600)), color=C[0],
               label="zero skew")
    ax[0].plot(g, stats.gamma.pdf(g, 2), color=C[2], label="positive skew")
    ax[0].set(title="Skewness: which tail is longer?", xlabel="value", ylabel="density")
    ax[0].legend()

    z = np.linspace(-5, 5, 800)
    sd_t = np.sqrt(5 / 3)       # t(5) has variance 5/3
    sd_u = np.sqrt(1 / 12)
    ax[1].plot(z, stats.uniform.pdf(z, -np.sqrt(3), 2 * np.sqrt(3)), color=C[2], label="Uniform (excess kurt −1.2)")
    ax[1].plot(z, stats.norm.pdf(z), color=C[0], label="Normal (excess kurt 0)")
    ax[1].plot(z, stats.t.pdf(z * sd_t, 5) * sd_t, color=C[1], label="t(5) rescaled to SD 1 (excess kurt 6)")
    ax[1].plot(z, stats.laplace.pdf(z * np.sqrt(2)) * np.sqrt(2), color=C[3], label="Laplace (excess kurt 3)")
    ax[1].set(title="Kurtosis: same variance (1), different tails & peak", xlabel="standardised value",
              ylabel="density", ylim=(0, 1.0))
    ax[1].legend(loc="upper right", fontsize=8)
    save(fig, "03_skew_kurtosis.png")


def fig03b():
    """Skewness of the sample mean falls like 1/sqrt(n) (link to CLT)."""
    rng = np.random.default_rng(1)
    ns = np.array([2, 5, 10, 20, 30, 50, 100, 200, 500])
    sim = [stats.skew(rng.exponential(1, (20000, n)).mean(axis=1)) for n in ns]
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.4))
    ax[0].plot(ns, sim, "o", color=C[0], label="simulated")
    ax[0].plot(ns, 2 / np.sqrt(ns), "-", color=C[1], label="theory: 2/√n")
    ax[0].set(xscale="log", title="Skewness of the sample mean of exponential data",
              xlabel="sample size n", ylabel="skewness of x̄")
    ax[0].legend()
    m = rng.exponential(1, (20000, 5)).mean(axis=1)
    m2 = rng.exponential(1, (20000, 100)).mean(axis=1)
    ax[1].hist(m, bins=60, density=True, alpha=0.55, color=C[1], label="n = 5 (skew ≈ 0.9)")
    ax[1].hist(m2, bins=60, density=True, alpha=0.55, color=C[0], label="n = 100 (skew ≈ 0.2)")
    ax[1].set(title="Averages become symmetric as n grows", xlabel="sample mean", ylabel="density")
    ax[1].legend()
    save(fig, "03_skew_vs_n.png")


def fig04():
    """Box plot with Tukey fences + z-score masking."""
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.4))
    q1, q3 = np.percentile(SAL, [25, 75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    ax[0].boxplot(SAL, orientation="horizontal", widths=0.5, flierprops=dict(markerfacecolor=C[1], markeredgecolor=C[1]))
    ax[0].axvline(hi, color=C[1], ls="--", lw=1, label=f"upper fence = {hi:.1f}")
    ax[0].axvline(lo, color=C[3], ls="--", lw=1, label=f"lower fence = {lo:.1f}")
    ax[0].set(yticks=[], xlabel="salary (₹ thousand)", title="Five-number summary & Tukey fences")
    ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.0), frameon=True)
    ax[0].set_ylim(0.3, 1.9)

    z_all = (SAL - SAL.mean()) / SAL.std(ddof=1)
    rest = SAL[:-1]
    z_rest = (SAL - rest.mean()) / rest.std(ddof=1)
    ax[1].bar(["z-score using\nall 10 values", "z-score using the\nother 9 values"],
              [z_all[-1], z_rest[-1]], color=[C[0], C[1]])
    ax[1].axhline(3, color="grey", ls="--", lw=1)
    ax[1].text(0.5, 8, "dashed line: common cut-off |z| = 3", ha="center", fontsize=9, color="grey")
    for i, v in enumerate([z_all[-1], z_rest[-1]]):
        ax[1].text(i, v + 1, f"{v:.1f}", ha="center", fontweight="bold")
    ax[1].set(title="Masking: the outlier inflates the SD it is judged by", ylabel="z-score of 300")
    save(fig, "04_fences_masking.png")


def fig04b():
    """Percentile / quantile illustration on a skewed sample."""
    rng = np.random.default_rng(5)
    x = rng.lognormal(3.4, 0.5, 2000)
    qs = np.percentile(x, [5, 25, 50, 75, 95])
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    ax.hist(x, bins=60, color=C[0], alpha=0.5)
    for q, p in zip(qs, [5, 25, 50, 75, 95]):
        ax.axvline(q, color=C[1], lw=1.4)
        ax.text(q, ax.get_ylim()[1] * 0.95, f"P{p}\n{q:.0f}", ha="center", va="top", fontsize=8.5, color=C[1])
    ax.set(title="Percentiles split the data into equal-count slices", xlabel="order value (₹)", ylabel="count")
    save(fig, "04_percentiles.png")


if __name__ == "__main__":
    for f in [fig01, fig01b, fig02, fig03, fig03b, fig04, fig04b]:
        f()
    print("figures written to", OUT)
