"""Regenerates every figure used in the probability/ notes.

Run from anywhere:  python probability/images/generate_figures.py
Requires: numpy, scipy, matplotlib
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

OUT = Path(__file__).resolve().parent
C = ["#2563eb", "#dc2626", "#16a34a", "#d97706", "#7c3aed", "#0891b2"]  # colour-blind-friendly-ish
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 110, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25,
    "axes.titlesize": 11, "axes.labelsize": 10, "legend.fontsize": 9,
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def stems(ax, x, p, color, label, offset=0.0, width=0.25):
    ax.bar(x + offset, p, width=width, color=color, alpha=0.85, label=label)


# ---------------------------------------------------------------- 01
def fig01():
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.4))
    x = np.arange(1, 7)
    ax[0].bar(x, [1 / 6] * 6, color=C[0])
    ax[0].set(title="PMF – fair die (discrete)", xlabel="x", ylabel="P(X = x)", ylim=(0, 0.3))
    ax[0].set_xticks(x)

    g = np.linspace(-4, 4, 400)
    ax[1].plot(g, stats.norm.pdf(g), color=C[0])
    m = (g >= -1) & (g <= 1)
    ax[1].fill_between(g[m], stats.norm.pdf(g[m]), color=C[1], alpha=0.5)
    ax[1].text(0, 0.1, "area = 0.68\n= P(−1 ≤ X ≤ 1)", ha="center", fontsize=9)
    ax[1].set(title="PDF – standard normal (continuous)", xlabel="x", ylabel="density f(x)")

    ax[2].plot(g, stats.norm.cdf(g), color=C[0])
    ax[2].axhline(0.5, color="grey", ls="--", lw=0.8)
    ax[2].axvline(0, color="grey", ls="--", lw=0.8)
    ax[2].set(title="CDF – F(x) = P(X ≤ x)", xlabel="x", ylabel="F(x)")
    save(fig, "01_pmf_pdf_cdf.png")


def fig01b():
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    g = np.linspace(-10, 10, 500)
    for s, c in [(1, C[0]), (3, C[1])]:
        ax[0].plot(g, stats.norm.pdf(g, 0, s), color=c, label=f"σ = {s}")
    ax[0].axvline(0, color="grey", ls="--", lw=0.8)
    ax[0].set(title="Same mean (0), different variance", xlabel="x", ylabel="density")
    ax[0].legend()

    vals = np.array([0, 10, 20, 50])
    probs = np.array([0.1, 0.2, 0.4, 0.3])
    ax[1].bar(vals, probs, width=3, color=C[2])
    ax[1].axvline((vals * probs).sum(), color=C[1], ls="--", lw=1.4)
    ax[1].text(26, 0.37, "E[X] = 25 (balance point)", color=C[1], fontsize=9)
    ax[1].set(title="Daily bonus: E[X] is where the bars balance", xlabel="bonus (₹)", ylabel="probability",
              xticks=vals, ylim=(0, 0.45))
    save(fig, "01_mean_variance.png")


# ---------------------------------------------------------------- 02
def fig02():
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.4))
    ax[0].bar([0, 1], [0.3, 0.7], color=C[0], width=0.4)
    ax[0].set(title="Bernoulli(p = 0.7)", xlabel="x", ylabel="P(X = x)", xticks=[0, 1])

    k = np.arange(0, 21)
    for (n, p), c in zip([(20, 0.2), (20, 0.5), (20, 0.8)], C):
        ax[1].plot(k, stats.binom.pmf(k, n, p), "o-", ms=3.5, color=c, label=f"n={n}, p={p}")
    ax[1].set(title="Binomial(n, p)", xlabel="number of successes k", ylabel="P(X = k)")
    ax[1].legend()

    k = np.arange(0, 21)
    for lam, c in zip([1, 4, 10], C):
        ax[2].plot(k, stats.poisson.pmf(k, lam), "o-", ms=3.5, color=c, label=f"λ = {lam}")
    ax[2].set(title="Poisson(λ)", xlabel="number of events k", ylabel="P(X = k)")
    ax[2].legend()
    save(fig, "02_bernoulli_binomial_poisson.png")


def fig02b():
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.4))
    k = np.arange(1, 16)
    for p, c in zip([0.2, 0.5], C):
        ax[0].plot(k, stats.geom.pmf(k, p), "o-", ms=3.5, color=c, label=f"p = {p}")
    ax[0].set(title="Geometric(p): trials until 1st success", xlabel="trial number k", ylabel="P(X = k)")
    ax[0].legend()

    k = np.arange(0, 41)
    for r, p, c in [(3, 0.3, C[0]), (10, 0.3, C[1])]:
        # scipy nbinom counts failures before r-th success; shift to "trials"
        ax[1].plot(k + r, stats.nbinom.pmf(k, r, p), "o-", ms=3, color=c, label=f"r={r}, p={p}")
    ax[1].set(title="Negative binomial: trials until r-th success", xlabel="trial number", ylabel="probability")
    ax[1].legend()

    k = np.arange(0, 11)
    ax[2].bar(k - 0.2, stats.hypergeom.pmf(k, 50, 20, 10), width=0.4, color=C[0], label="Hypergeometric\n(no replacement)")
    ax[2].bar(k + 0.2, stats.binom.pmf(k, 10, 20 / 50), width=0.4, color=C[3], label="Binomial\n(with replacement)")
    ax[2].set(title="Hypergeometric vs Binomial (N=50, K=20, n=10)", xlabel="k successes in sample", ylabel="probability")
    ax[2].legend()
    save(fig, "02_geometric_negbin_hypergeom.png")


def fig02c():
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
    n, p = 40, 0.5
    k = np.arange(0, n + 1)
    ax[0].bar(k, stats.binom.pmf(k, n, p), color=C[0], alpha=0.7, label="Binomial(40, 0.5)")
    g = np.linspace(0, n, 400)
    ax[0].plot(g, stats.norm.pdf(g, n * p, np.sqrt(n * p * (1 - p))), color=C[1], label="Normal(20, √10)")
    ax[0].set(title="Binomial → Normal (n large)", xlabel="k", ylabel="probability")
    ax[0].legend()

    n, p = 200, 0.02
    k = np.arange(0, 15)
    ax[1].bar(k - 0.2, stats.binom.pmf(k, n, p), width=0.4, color=C[0], label="Binomial(200, 0.02)")
    ax[1].bar(k + 0.2, stats.poisson.pmf(k, n * p), width=0.4, color=C[3], label="Poisson(λ = 4)")
    ax[1].set(title="Binomial → Poisson (n large, p small)", xlabel="k", ylabel="probability")
    ax[1].legend()
    save(fig, "02_approximations.png")


# ---------------------------------------------------------------- 03
def fig03():
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.4))
    g = np.linspace(-1, 6, 500)
    ax[0].plot(g, stats.uniform.pdf(g, 1, 4), color=C[0], label="Uniform(1, 5)")
    ax[0].plot(g, stats.triang.pdf(g, 0.5, 1, 4), color=C[1], label="Triangular(1, 3, 5)")
    ax[0].set(title="Uniform and Triangular", xlabel="x", ylabel="density")
    ax[0].legend()

    g = np.linspace(-8, 10, 600)
    for (m, s), c in zip([(0, 1), (0, 2), (3, 1)], C):
        ax[1].plot(g, stats.norm.pdf(g, m, s), color=c, label=f"μ={m}, σ={s}")
    ax[1].set(title="Normal(μ, σ)", xlabel="x", ylabel="density")
    ax[1].legend()

    g = np.linspace(0, 6, 500)
    for lam, c in zip([0.5, 1, 2], C):
        ax[2].plot(g, stats.expon.pdf(g, scale=1 / lam), color=c, label=f"λ = {lam}")
    ax[2].set(title="Exponential(λ)", xlabel="x", ylabel="density")
    ax[2].legend()
    save(fig, "03_uniform_normal_exponential.png")


def fig03b():
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    g = np.linspace(-4, 4, 600)
    ax[0].plot(g, stats.norm.pdf(g), color="black", lw=1.3)
    for lo, hi, c, lab in [(-3, 3, C[2], "99.7%"), (-2, 2, C[3], "95%"), (-1, 1, C[1], "68%")]:
        m = (g >= lo) & (g <= hi)
        ax[0].fill_between(g[m], stats.norm.pdf(g[m]), color=c, alpha=0.6, label=lab)
    ax[0].set(title="Empirical rule (68–95–99.7)", xlabel="z (std. devs from mean)", ylabel="density",
              xticks=range(-4, 5))
    ax[0].legend()

    # z-score example: exam mean 60, sd 10, score 80 -> z = 2
    g = np.linspace(20, 100, 500)
    ax[1].plot(g, stats.norm.pdf(g, 60, 10), color="black", lw=1.3)
    m = g >= 80
    ax[1].fill_between(g[m], stats.norm.pdf(g[m], 60, 10), color=C[1], alpha=0.7)
    ax[1].text(86, 0.012, "P(X ≥ 80)\n= 0.0228", fontsize=9, color=C[1])
    ax[1].set(title="Exam: μ = 60, σ = 10 → score 80 has z = 2", xlabel="score", ylabel="density")
    save(fig, "03_normal_empirical_zscore.png")


def fig03c():
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.4))
    g = np.linspace(0.001, 20, 600)
    for (a, th), c in zip([(1, 2), (2, 2), (5, 1), (9, 0.5)], C):
        ax[0].plot(g, stats.gamma.pdf(g, a, scale=th), color=c, label=f"α={a}, θ={th}")
    ax[0].set(title="Gamma(shape α, scale θ)", xlabel="x", ylabel="density", ylim=(0, 0.6))
    ax[0].legend()

    g = np.linspace(0.001, 5, 600)
    for s, c in zip([0.25, 0.5, 1.0], C):
        ax[1].plot(g, stats.lognorm.pdf(g, s), color=c, label=f"σ = {s}")
    ax[1].set(title="Log-normal(μ = 0, σ)", xlabel="x", ylabel="density", ylim=(0, 1.5))
    ax[1].legend()

    g = np.linspace(0.001, 3, 600)
    for k, c in zip([0.5, 1, 1.5, 5], C):
        ax[2].plot(g, stats.weibull_min.pdf(g, k), color=c, label=f"k = {k}")
    ax[2].set(title="Weibull(shape k, scale 1)", xlabel="x", ylabel="density", ylim=(0, 2))
    ax[2].legend()
    save(fig, "03_gamma_lognormal_weibull.png")


def fig03d():
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.8))
    g = np.linspace(0.001, 0.999, 600)
    for (a, b), c in zip([(0.5, 0.5), (1, 1), (2, 5), (5, 2), (5, 5), (20, 40)], C):
        ax[0].plot(g, stats.beta.pdf(g, a, b), color=c, label=f"α={a}, β={b}")
    ax[0].set(title="Beta(α, β) – lives on [0, 1]", xlabel="x (a proportion)", ylabel="density", ylim=(0, 7))
    ax[0].legend(ncol=2, loc="upper center")

    # Bayesian updating: prior Beta(2,2), 7 clicks out of 10 visits
    ax[1].plot(g, stats.beta.pdf(g, 2, 2), color=C[0], label="Prior: Beta(2, 2)")
    ax[1].plot(g, stats.beta.pdf(g, 2 + 7, 2 + 3), color=C[1], label="After 7 clicks / 10 visits:\nBeta(9, 5)")
    ax[1].plot(g, stats.beta.pdf(g, 2 + 70, 2 + 30), color=C[2], label="After 70 / 100:\nBeta(72, 32)")
    ax[1].set(title="Beta as a belief about a click-rate", xlabel="true click-rate p", ylabel="density")
    ax[1].legend()
    save(fig, "03_beta.png")


def fig03e():
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.4))
    g = np.linspace(1, 6, 600)
    for a, c in zip([0.5, 1, 2], C):
        ax[0].plot(g, stats.pareto.pdf(g, a), color=c, label=f"α = {a}")
    ax[0].set(title="Pareto (power-law, '80/20')", xlabel="x (minimum = 1)", ylabel="density", ylim=(0, 2))
    ax[0].legend()

    g = np.linspace(-6, 6, 600)
    ax[1].plot(g, stats.norm.pdf(g), color=C[0], label="Normal")
    ax[1].plot(g, stats.cauchy.pdf(g), color=C[1], label="Cauchy (heavy tails)")
    ax[1].plot(g, stats.laplace.pdf(g), color=C[2], label="Laplace")
    ax[1].set(title="Symmetric: light vs heavy tails", xlabel="x", ylabel="density")
    ax[1].legend(loc="upper left")

    g = np.linspace(0.001, 6, 600)
    ax[2].plot(g, stats.alpha.pdf(g, 1), color=C[4], label="alpha(a = 1)")
    ax[2].plot(g, stats.alpha.pdf(g, 3), color=C[5], label="alpha(a = 3)")
    ax[2].set(title="SciPy's 'alpha' distribution (rare)", xlabel="x", ylabel="density")
    ax[2].legend()
    save(fig, "03_heavy_tails_alpha.png")


# ---------------------------------------------------------------- 04
def fig04():
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.5))
    g = np.linspace(-5, 5, 600)
    ax[0].plot(g, stats.norm.pdf(g), color="black", ls="--", label="Normal (z)")
    for df, c in zip([1, 3, 10, 30], C):
        ax[0].plot(g, stats.t.pdf(g, df), color=c, label=f"t, df = {df}")
    ax[0].set(title="Student's t → Normal as df grows", xlabel="t", ylabel="density")
    ax[0].legend()

    g = np.linspace(0.001, 30, 600)
    for df, c in zip([1, 3, 5, 10, 20], C + [C[0]]):
        ax[1].plot(g, stats.chi2.pdf(g, df), color=c, label=f"df = {df}")
    ax[1].set(title="Chi-square(df)", xlabel="x", ylabel="density", ylim=(0, 0.5))
    ax[1].legend()

    g = np.linspace(0.001, 5, 600)
    for (d1, d2), c in zip([(2, 5), (5, 10), (10, 30), (30, 100)], C):
        ax[2].plot(g, stats.f.pdf(g, d1, d2), color=c, label=f"df1={d1}, df2={d2}")
    ax[2].set(title="F(df1, df2)", xlabel="x", ylabel="density")
    ax[2].legend()
    save(fig, "04_t_chi2_f.png")


def fig04b():
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.5))
    g = np.linspace(-5, 5, 600)
    for df, a_c in [(5, C[1]), (30, C[2])]:
        ax[0].plot(g, stats.t.pdf(g, df), color=a_c, label=f"t, df={df}")
    ax[0].plot(g, stats.norm.pdf(g), "k--", label="Normal")
    ax[0].set(xlim=(1.5, 5), ylim=(0, 0.15), title="Tails (zoom): t is heavier", xlabel="t", ylabel="density")
    ax[0].legend()

    # critical values vs df
    df = np.arange(2, 61)
    ax[1].plot(df, stats.t.ppf(0.975, df), color=C[0], label="t critical (95% two-sided)")
    ax[1].axhline(1.96, color="black", ls="--", label="z = 1.96")
    ax[1].set(title="95% critical value vs df", xlabel="degrees of freedom", ylabel="critical value")
    ax[1].legend()

    # chi2 as sum of squared standard normals
    rng = np.random.default_rng(0)
    z = rng.standard_normal((100_000, 3))
    q = (z ** 2).sum(axis=1)
    ax[2].hist(q, bins=80, density=True, color=C[0], alpha=0.5, label="simulated Z₁²+Z₂²+Z₃²")
    gg = np.linspace(0.001, 20, 500)
    ax[2].plot(gg, stats.chi2.pdf(gg, 3), color=C[1], label="Chi-square(3)")
    ax[2].set(xlim=(0, 20), title="Chi-square = sum of squared normals", xlabel="x", ylabel="density")
    ax[2].legend()
    save(fig, "04_relationships.png")


if __name__ == "__main__":
    for f in [fig01, fig01b, fig02, fig02b, fig02c, fig03, fig03b, fig03c, fig03d, fig03e,
              fig04, fig04b]:
        f()
    print("figures written to", OUT)
