"""Regenerates every figure used in the inferential-statistics/ notes.

Run from anywhere:  python inferential-statistics/images/generate_figures.py
Requires: numpy, scipy (>= 1.12 for irwinhall), matplotlib (>= 3.10)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

OUT = Path(__file__).resolve().parent
C = ["#2563eb", "#dc2626", "#16a34a", "#d97706", "#7c3aed", "#0891b2"]
N = stats.norm
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 110, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25,
    "axes.titlesize": 11, "axes.labelsize": 10, "legend.fontsize": 9,
})
DELIVERY = np.array([32, 35, 29, 38, 31, 34, 36, 30, 33, 37.])      # running t-test example
ORDERS_PER_HOUR = np.array([3, 5, 2, 4, 6, 3, 4, 5, 2, 6])           # Poisson example
UNIF_SAMPLE = np.array([3.1, 7.4, 5.9, 9.2, 1.8])                    # Uniform(0, theta) example


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# =============================================================== 01 sampling
def fig01a():
    rng = np.random.default_rng(4)
    gx, gy = np.meshgrid(np.arange(10), np.arange(10))
    x, y = gx.ravel(), gy.ravel()
    group = (x >= 5).astype(int) + 2 * (y >= 5).astype(int)
    idx = np.arange(100)
    schemes = {
        "Simple random\n(every unit equally likely)": rng.choice(idx, 12, replace=False),
        "Stratified\n(3 random from each group)": np.concatenate(
            [rng.choice(idx[group == g], 3, replace=False) for g in range(4)]),
    }
    seg = y * 2 + (x >= 5)
    schemes["Cluster\n(whole groups chosen at random)"] = idx[np.isin(seg, rng.choice(20, 2, replace=False))]
    schemes["Systematic\n(every 8th unit)"] = idx[3::8]
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.5))
    for a, (title, sel) in zip(ax, schemes.items()):
        a.scatter(x, y, c=[["#9ca3af", "#fca5a5", "#93c5fd", "#86efac"][g] for g in group], s=55, zorder=2)
        a.scatter(x[sel], y[sel], s=130, facecolors="none", edgecolors="black", linewidths=2, zorder=3)
        a.set(title=title, xticks=[], yticks=[]); a.grid(False)
        a.spines[["left", "bottom"]].set_visible(False)
    save(fig, "01_sampling_methods.png")


def fig01b():
    rng = np.random.default_rng(2)
    pop = rng.lognormal(np.log(80), 0.6, 200_000)
    mu_true = pop.mean()
    ns = np.array([10, 30, 100, 300, 1000, 3000, 10000, 30000])
    w = pop / pop.sum()
    r = [rng.choice(pop, n).mean() for n in ns]
    b = [rng.choice(pop, n, p=w).mean() for n in ns]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(ns, r, "o-", color=C[2], label="random sample")
    ax.plot(ns, b, "o-", color=C[1], label="self-selected (big spenders over-represented)")
    ax.axhline(mu_true, color="black", ls="--", lw=1.2, label=f"true mean = {mu_true:.0f}")
    ax.set(xscale="log", xlabel="sample size n", ylabel="sample mean order value (₹)",
           title="More data shrinks random error, not bias")
    ax.legend()
    save(fig, "01_bias_vs_size.png")


# ======================================================== 02 sampling distributions
def fig02a():
    """The idea: population -> many samples -> distribution of x-bar."""
    rng = np.random.default_rng(5)
    pop = rng.gamma(4, 10, 500_000)                    # skewed delivery-time-like population, mean 40
    mu, sd = pop.mean(), pop.std()
    n = 30
    means = rng.choice(pop, (10000, n)).mean(axis=1)
    fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.5))
    ax[0].hist(pop, bins=80, density=True, color="grey", alpha=0.6)
    ax[0].axvline(mu, color=C[1], lw=1.5)
    ax[0].set(title=f"Population: μ = {mu:.0f}, σ = {sd:.0f}", xlabel="x", ylabel="density")
    for i in range(5):
        smp = rng.choice(pop, n)
        ax[1].scatter(smp, np.full(n, i), s=10, alpha=0.7, color=C[i % 5])
        ax[1].plot(smp.mean(), i, "k|", ms=18, mew=2)
    ax[1].axvline(mu, color=C[1], lw=1.5)
    ax[1].set(title="Five samples of n = 30 (black tick = each x̄)", xlabel="x", yticks=range(5),
              yticklabels=[f"sample {i+1}" for i in range(5)])
    ax[2].hist(means, bins=60, density=True, color=C[0], alpha=0.6)
    g = np.linspace(means.min(), means.max(), 300)
    ax[2].plot(g, N.pdf(g, mu, sd / np.sqrt(n)), color=C[1])
    ax[2].axvline(mu, color=C[1], lw=1.2)
    ax[2].set(title=f"10,000 values of x̄: mean {means.mean():.1f}, SD {means.std():.1f} (σ/√n = {sd/np.sqrt(n):.1f})",
              xlabel="x̄")
    save(fig, "02_sampling_distribution_idea.png")


def fig02b():
    fig, ax = plt.subplots(figsize=(7.5, 3.5))
    g = np.linspace(10, 70, 600)
    ax.plot(g, N.pdf(g, 40, 12), color="grey", label="individual deliveries: mean 40, SD 12")
    ax.plot(g, N.pdf(g, 40, 2), color=C[0], lw=2, label="sample means, n = 36: mean 40, SE 2")
    m = g >= 43
    ax.fill_between(g[m], N.pdf(g[m], 40, 2), color=C[1], alpha=0.6)
    ax.text(43.3, 0.05, "P(x̄ > 43) = 0.067", color=C[1], fontsize=9)
    ax.set(title="Averages vary far less than individual values", xlabel="delivery time (min)", ylabel="density")
    ax.legend(loc="upper left")
    save(fig, "02_individual_vs_mean.png")


def fig02c():
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.5))
    n = np.arange(1, 401)
    ax[0].plot(n, 12 / np.sqrt(n), color=C[0])
    ax[0].axvline(36, color="grey", ls="--", lw=1)
    ax[0].text(40, 6, "n = 36 → SE = 2", fontsize=9)
    ax[0].set(title="Standard error = σ/√n (σ = 12)", xlabel="sample size n", ylabel="SE of x̄")
    p, nn = 0.3, 200
    se = np.sqrt(p * (1 - p) / nn)
    g = np.linspace(0.18, 0.42, 400)
    ax[1].plot(g, N.pdf(g, p, se), color=C[0])
    m = g >= 0.35
    ax[1].fill_between(g[m], N.pdf(g[m], p, se), color=C[1], alpha=0.6)
    ax[1].text(0.352, 3, "P(p̂ ≥ 0.35)\n≈ 0.061", fontsize=9)
    ax[1].set(title="Sampling distribution of p̂ (p = 0.3, n = 200)", xlabel="sample proportion p̂", ylabel="density")
    save(fig, "02_se_and_phat.png")


def fig02d():
    """s^2 ~ chi-square, t-statistic ~ t, and x-bar independent of s^2 only for normal data."""
    rng = np.random.default_rng(8)
    fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.6))
    n, sigma = 10, 1.0
    x = rng.normal(0, sigma, (100000, n))
    q = (n - 1) * x.var(axis=1, ddof=1) / sigma ** 2
    ax[0].hist(q, bins=80, density=True, color=C[0], alpha=0.55, label="simulated (n−1)s²/σ²")
    g = np.linspace(0.01, 30, 400)
    ax[0].plot(g, stats.chi2.pdf(g, n - 1), color=C[1], label="Chi-square(9)")
    ax[0].set(xlim=(0, 30), title="(n − 1)s²/σ² follows χ² (normal data, n = 10)", xlabel="value", ylabel="density")
    ax[0].legend()
    n = 5
    x = rng.normal(0, 1, (200000, n))
    t = x.mean(axis=1) / (x.std(axis=1, ddof=1) / np.sqrt(n))
    z = x.mean(axis=1) / (1 / np.sqrt(n))
    g = np.linspace(-6, 6, 500)
    ax[1].hist(t, bins=np.linspace(-6, 6, 100), density=True, color=C[0], alpha=0.5, label="simulated T (σ estimated by s)")
    ax[1].plot(g, stats.t.pdf(g, n - 1), color=C[1], label="t, df = 4")
    ax[1].plot(g, N.pdf(g), color="black", ls="--", label="normal (σ known)")
    ax[1].set(xlim=(-6, 6), title="Estimating σ fattens the tails (n = 5)", xlabel="value")
    ax[1].legend(fontsize=8, loc="upper left")
    xn = rng.normal(0, 1, (4000, 5)); xe = rng.exponential(1, (4000, 5))
    ax[2].scatter(xe.mean(1), xe.var(1, ddof=1), s=4, color=C[1], alpha=0.35,
                  label=f"exponential data (corr {np.corrcoef(xe.mean(1), xe.var(1, ddof=1))[0,1]:.2f})")
    ax[2].scatter(xn.mean(1) + 3, xn.var(1, ddof=1), s=4, color=C[0], alpha=0.35,
                  label=f"normal data, shifted +3 (corr {np.corrcoef(xn.mean(1), xn.var(1, ddof=1))[0,1]:.2f})")
    ax[2].set(title="x̄ and s² are independent only for normal data", xlabel="x̄", ylabel="s²", ylim=(0, 6))
    ax[2].legend(fontsize=8, loc="upper right")
    save(fig, "02_variance_t_independence.png")


# ============================================================ 03 LLN and CLT
def fig03a():
    rng = np.random.default_rng(3)
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))
    k = np.arange(1, 5001)
    for c in C[:5]:
        ax[0].plot(k, np.cumsum(rng.integers(1, 7, k.size)) / k, color=c, lw=1)
    ax[0].axhline(3.5, color="black", lw=1)
    ax[0].set(xscale="log", title="Law of large numbers: running average of die rolls → 3.5",
              xlabel="number of rolls", ylabel="running average", ylim=(1.5, 5.5))
    n = np.arange(10, 801, 10)
    eps = 0.05
    cheb = np.minimum(1, 0.25 / (n * eps ** 2))
    exact = np.array([2 * stats.binom.sf(np.floor(m * (0.5 + eps)), m, 0.5) -
                      (stats.binom.pmf(m * 0.5 + m * eps, m, 0.5) * 2 if (m * eps) % 1 == 0 else 0) for m in n])
    ax[1].plot(n, cheb, color=C[1], label="Chebyshev bound  σ²/(nε²)")
    ax[1].plot(n, exact, color=C[0], label="exact P(|p̂ − 0.5| > 0.05)")
    ax[1].set(title="Fair coin: how fast does p̂ concentrate? (ε = 0.05)", xlabel="number of tosses n",
              ylabel="probability of being off by more than ε", ylim=(0, 1.05))
    ax[1].legend()
    save(fig, "03_lln.png")


def fig03b():
    """Sum of n uniforms (exact Irwin-Hall), standardised, vs the standard normal."""
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.2), sharey=True)
    z = np.linspace(-4, 4, 800)
    for a, n in zip(ax, [1, 2, 3, 12]):
        sd = np.sqrt(n / 12)
        a.plot(z, stats.irwinhall.pdf(n / 2 + sd * z, n) * sd, color=C[0], lw=2, label="exact")
        a.plot(z, N.pdf(z), color=C[1], ls="--", label="normal")
        a.set(title=f"sum of n = {n} uniform(0,1)", xlabel="standardised sum")
    ax[0].set_ylabel("density"); ax[0].legend()
    save(fig, "03_sum_of_uniforms.png")


def fig03c():
    """Sum of n exponentials = Gamma(n): exact skewed density approaches the normal slowly."""
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.2), sharey=True)
    z = np.linspace(-4, 5, 800)
    for a, n in zip(ax, [1, 3, 10, 50]):
        a.plot(z, stats.gamma.pdf(n + np.sqrt(n) * z, n) * np.sqrt(n), color=C[0], lw=2, label="exact Gamma(n)")
        a.plot(z, N.pdf(z), color=C[1], ls="--", label="normal")
        a.set(title=f"sum of n = {n} exponentials", xlabel="standardised sum", xlim=(-4, 5))
    ax[0].set_ylabel("density"); ax[0].legend()
    save(fig, "03_sum_of_exponentials.png")


def fig03d():
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
                ax[r, c].plot(g, N.pdf(g, m.mean(), m.std()), color=C[1], lw=1.4)
            ax[r, c].set_title(f"n = {n}" if r == 0 else "", fontsize=10)
            ax[r, c].set_yticks([])
        ax[r, 0].set_ylabel(name, fontsize=10)
    fig.suptitle("Sampling distribution of the mean: whatever the population, it approaches a normal bell (red)", y=1.0)
    save(fig, "03_clt_grid.png")


def kd_cont(cdf, mu, sd):
    xs = np.linspace(-6, 6, 24001)
    return np.max(np.abs(cdf(mu + sd * xs) - N.cdf(xs)))


def kd_binom(n, p):
    k = np.arange(0, n + 1)
    z = (k - n * p) / np.sqrt(n * p * (1 - p))
    return max(np.max(np.abs(stats.binom.cdf(k, n, p) - N.cdf(z))),
               np.max(np.abs(stats.binom.cdf(k - 1, n, p) - N.cdf(z))))


def fig03e():
    ns = np.unique(np.round(np.logspace(0, 3, 25)).astype(int))
    nsu = ns[ns <= 100]
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 3.9))
    ax[0].plot(ns, [kd_cont(lambda t: stats.gamma.cdf(t, n), n, np.sqrt(n)) for n in ns], "o-", ms=3.5, color=C[1],
               label="Exponential (skew 2)")
    ax[0].plot(ns, [kd_binom(n, 0.5) for n in ns], "o-", ms=3.5, color=C[0], label="Bernoulli(0.5), discrete")
    ax[0].plot(ns, [kd_binom(n, 0.1) for n in ns], "o-", ms=3.5, color=C[3], label="Bernoulli(0.1), skewed + discrete")
    ax[0].plot(nsu, [kd_cont(lambda t: stats.irwinhall.cdf(t, n), n / 2, np.sqrt(n / 12)) for n in nsu], "o-", ms=3.5,
               color=C[2], label="Uniform (skew 0)")
    ref = np.array([1, 1000])
    ax[0].plot(ref, 0.4 / np.sqrt(ref), color="grey", ls="--", lw=1, label="reference: 0.4/√n")
    ax[0].plot(ref, 0.06 / ref, color="grey", ls=":", lw=1, label="reference: 0.06/n")
    ax[0].set(xscale="log", yscale="log", title="Worst-case error of the normal approximation",
              xlabel="number of summands n", ylabel="max |F_n(x) − Φ(x)|")
    ax[0].legend(fontsize=8)
    # skewness of mean: correction term
    z = np.linspace(-3.5, 4, 600)
    n = 10
    gam = 2 / np.sqrt(n)
    exact = stats.gamma.cdf(n + np.sqrt(n) * z, n)
    edge = N.cdf(z) - gam / 6 * (z ** 2 - 1) * N.pdf(z)
    ax[1].plot(z, exact - N.cdf(z), color=C[1], lw=2, label="exact − normal")
    ax[1].plot(z, edge - N.cdf(z), color=C[0], ls="--", lw=2, label="Edgeworth skewness term")
    ax[1].axhline(0, color="black", lw=0.8)
    ax[1].set(title="Why skewed data converge slowly (exponential, n = 10)", xlabel="z", ylabel="CDF error")
    ax[1].legend()
    save(fig, "03_convergence_rate.png")


def fig03f():
    """Worked example: mean order value of lognormal (skewed) data, n = 10 vs 400."""
    rng = np.random.default_rng(0)
    ln = stats.lognorm(0.6, scale=80)
    mu, sd = ln.mean(), ln.std()
    fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.5))
    g = np.linspace(0, 400, 600)
    ax[0].plot(g, ln.pdf(g), color="grey")
    ax[0].axvline(mu, color=C[1])
    ax[0].set(title=f"Order values: mean {mu:.0f}, SD {sd:.0f}, skew 2.3", xlabel="₹", ylabel="density", xlim=(0, 400))
    for a, n in zip(ax[1:], [10, 400]):
        m = rng.lognormal(np.log(80), 0.6, (40000, n)).mean(axis=1)
        se = sd / np.sqrt(n)
        a.hist(m, bins=70, density=True, color=C[0], alpha=0.55)
        g = np.linspace(m.min(), m.max(), 400)
        a.plot(g, N.pdf(g, mu, se), color=C[1], lw=1.6, label="normal (CLT)")
        a.axvline(mu, color="black", lw=0.8)
        a.set(title=f"Mean of n = {n}: skew {stats.skew(m):.2f}", xlabel="x̄")
        a.legend()
    save(fig, "03_clt_orders.png")


def fig03g():
    rng = np.random.default_rng(6)
    fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.5))
    g = np.linspace(-12, 12, 800)
    c1 = rng.standard_cauchy(100000)
    c100 = rng.standard_cauchy((100000, 100)).mean(axis=1)
    ax[0].hist(c1, bins=np.linspace(-12, 12, 100), density=True, color=C[0], alpha=0.5, label="n = 1")
    ax[0].hist(c100, bins=np.linspace(-12, 12, 100), density=True, color=C[1], alpha=0.5, label="mean of n = 100")
    ax[0].plot(g, stats.cauchy.pdf(g), color="black", lw=1)
    ax[0].set(title="Cauchy: averaging changes nothing", xlabel="value", ylabel="density", xlim=(-12, 12))
    ax[0].legend()
    p15 = (rng.pareto(1.5, (20000, 1000)) + 1).mean(axis=1)
    ax[1].hist(p15, bins=np.linspace(0, 12, 90), density=True, color=C[3], alpha=0.65)
    gg = np.linspace(0, 12, 300)
    ax[1].plot(gg, N.pdf(gg, p15.mean(), p15.std()), color="black", ls="--", label="normal with same mean/SD")
    ax[1].set(title="Pareto α = 1.5 (infinite variance): n = 1000\nmeans still skewed", xlabel="x̄")
    ax[1].legend(fontsize=8)
    p4 = (rng.pareto(4, (20000, 100)) + 1).mean(axis=1)
    ax[2].hist(p4, bins=70, density=True, color=C[2], alpha=0.65)
    gg = np.linspace(p4.min(), p4.max(), 300)
    ax[2].plot(gg, N.pdf(gg, p4.mean(), p4.std()), color="black", ls="--", label="normal with same mean/SD")
    ax[2].set(title="Pareto α = 4 (finite variance): n = 100\nmeans nearly normal", xlabel="x̄")
    ax[2].legend(fontsize=8)
    save(fig, "03_clt_failure.png")


# ========================================================== 04 parameter estimation
def fig04a():
    rng = np.random.default_rng(1)
    n = 25
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
    for a, (name, gen) in zip(ax, [("Normal data", lambda: rng.normal(0, 1, (100000, n))),
                                   ("Laplace (heavy-tailed) data", lambda: rng.laplace(0, 1 / np.sqrt(2), (100000, n)))]):
        x = gen()
        mean, med = x.mean(1), np.median(x, 1)
        bins = np.linspace(-0.6, 0.6, 90)
        a.hist(mean, bins=bins, density=True, alpha=0.5, color=C[0], label=f"sample mean (var {mean.var():.3f})")
        a.hist(med, bins=bins, density=True, alpha=0.5, color=C[1], label=f"sample median (var {med.var():.3f})")
        a.set(title=f"{name}: which estimator of the centre is tighter?", xlabel="estimate (true centre = 0)")
        a.legend(fontsize=8)
    save(fig, "04_mean_vs_median.png")


def fig04b():
    rng = np.random.default_rng(1)
    n = 10
    x = rng.normal(0, 1, (200000, n))
    ss = ((x - x.mean(1, keepdims=True)) ** 2).sum(1)
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
    bins = np.linspace(0, 3.5, 90)
    for dv, c in [(n - 1, C[0]), (n, C[3]), (n + 1, C[1])]:
        ax[0].hist(ss / dv, bins=bins, density=True, histtype="step", lw=2, color=c, label=f"divide by {dv}")
    ax[0].axvline(1, color="black", ls="--", lw=1)
    ax[0].set(title="Sampling distributions of three variance estimators (σ² = 1, n = 10)", xlabel="estimate")
    ax[0].legend()
    d = np.linspace(7, 14, 100)
    bias2 = ((n - 1) / d - 1) ** 2
    var = 2 * (n - 1) / d ** 2
    ax[1].plot(d, bias2 + var, color=C[1], lw=2, label="MSE")
    ax[1].plot(d, var, color=C[0], label="variance")
    ax[1].plot(d, bias2, color=C[3], label="bias²")
    ax[1].axvline(n - 1, color="grey", ls=":", lw=1); ax[1].axvline(n + 1, color="grey", ls=":", lw=1)
    ax[1].text(n - 1, 0.215, "n−1\n(unbiased)", ha="center", fontsize=8)
    ax[1].text(n + 1, 0.19, "n+1\n(min MSE)", ha="center", fontsize=8)
    ax[1].set(title="Bias–variance trade-off for the divisor (n = 10)", xlabel="divisor", ylabel="value (σ = 1)")
    ax[1].legend(loc="center right")
    save(fig, "04_variance_divisors.png")


def fig04c():
    y = ORDERS_PER_HOUR
    lam = np.linspace(1.5, 8, 500)
    ll = np.array([stats.poisson.logpmf(y, l).sum() for l in lam])
    fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.5))
    L = np.exp(ll - ll.max())
    ax[0].plot(lam, L, color=C[0], lw=2)
    ax[0].axvline(y.mean(), color=C[1], ls="--"); ax[0].text(y.mean() + 0.1, 0.1, "MLE λ̂ = 4", color=C[1], fontsize=9)
    ax[0].set(title="Likelihood L(λ) / max L (n = 10 hours)", xlabel="λ (orders per hour)", ylabel="relative likelihood")
    for k, c in [(1, C[0]), (4, C[2]), (16, C[3])]:
        lk = np.array([stats.poisson.logpmf(np.tile(y, k), l).sum() for l in lam])
        ax[1].plot(lam, lk - lk.max(), color=c, lw=2, label=f"n = {10 * k}")
    ax[1].set(ylim=(-8, 0.3), title="Log-likelihood: more data = sharper peak", xlabel="λ",
              ylabel="log-likelihood − max")
    ax[1].legend()
    se = np.sqrt(y.mean() / len(y))
    ax[2].plot(lam, ll - ll.max(), color=C[0], lw=2, label="log-likelihood (n = 10)")
    ax[2].plot(lam, -0.5 * ((lam - y.mean()) / se) ** 2, color=C[1], ls="--", label="quadratic using SE = √(λ̂/n)")
    ax[2].set(ylim=(-8, 0.3), title="Curvature at the peak gives the standard error", xlabel="λ")
    ax[2].legend()
    save(fig, "04_likelihood_poisson.png")


def fig04d():
    x = DELIVERY
    n = len(x)
    mu = np.linspace(30, 37, 300)
    sg = np.linspace(1.5, 7, 300)
    M, S = np.meshgrid(mu, sg)
    ll = -n * np.log(S) - ((x[:, None, None] - M) ** 2).sum(0) / (2 * S ** 2)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    cs = ax[0].contour(M, S, ll - ll.max(), levels=[-16, -9.2, -4.6, -1.92, -0.5], colors=[C[0]])
    ax[0].clabel(cs, fmt={-0.5: "-0.5", -1.92: "-1.92", -4.6: "-4.6", -9.2: "-9.2", -16: "-16"}, fontsize=8)
    mle = np.sqrt(((x - x.mean()) ** 2).mean())
    ax[0].plot(x.mean(), mle, "o", color=C[1], label=f"MLE: μ̂ = {x.mean():.1f}, σ̂ = {mle:.2f}")
    ax[0].plot(x.mean(), x.std(ddof=1), "s", color=C[2], label=f"unbiased: s = {x.std(ddof=1):.2f}")
    ax[0].set(title="Log-likelihood surface of a normal model (10 delivery times)", xlabel="μ", ylabel="σ")
    ax[0].legend(fontsize=8, loc="upper right")
    # profile for mu
    prof = np.array([-n * np.log(np.sqrt(((x - m) ** 2).mean())) - n / 2 for m in mu])
    ax[1].plot(mu, prof - prof.max(), color=C[0], lw=2)
    ax[1].axhline(-1.92, color="grey", ls="--", lw=1)
    ax[1].text(30.1, -1.6, "−1.92: approx. 95% likelihood interval", fontsize=8, color="grey")
    ax[1].set(ylim=(-8, 0.5), title="Profile log-likelihood for μ", xlabel="μ", ylabel="log-likelihood − max")
    save(fig, "04_normal_loglik.png")


def fig04e():
    rng = np.random.default_rng(1)
    u = UNIF_SAMPLE
    n = len(u)
    th = np.linspace(5, 20, 600)
    L = np.where(th >= u.max(), th ** (-float(n)), 0)
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
    ax[0].plot(th, L / L.max(), color=C[0], lw=2)
    ax[0].axvline(u.max(), color=C[1], ls="--"); ax[0].text(u.max() + 0.2, 0.5, "MLE = max = 9.2", color=C[1])
    ax[0].set(title="Uniform(0, θ): likelihood is zero below max(x), then decreasing", xlabel="θ",
              ylabel="relative likelihood")
    th0, n = 10, 5
    s = rng.uniform(0, th0, (200000, n))
    bins = np.linspace(2, 20, 100)
    for e, c, lab in [(2 * s.mean(1), C[1], "method of moments 2x̄"), (s.max(1), C[3], "MLE: max (biased low)"),
                      ((n + 1) / n * s.max(1), C[2], "bias-corrected max")]:
        ax[1].hist(e, bins=bins, density=True, histtype="step", lw=2, color=c,
                   label=f"{lab}: MSE {((e - th0) ** 2).mean():.1f}")
    ax[1].axvline(th0, color="black", ls="--", lw=1)
    ax[1].set(title="Three estimators of θ = 10 (n = 5)", xlabel="estimate")
    ax[1].legend(fontsize=8)
    save(fig, "04_uniform_estimators.png")


def fig04f():
    rng = np.random.default_rng(2)
    lam = 0.5
    fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.5))
    for a, n in zip(ax, [5, 20, 200]):
        lh = 1 / rng.exponential(1 / lam, (100000, n)).mean(axis=1)
        a.hist(lh, bins=np.linspace(0, 1.4, 100), density=True, color=C[0], alpha=0.55)
        g = np.linspace(0.01, 1.4, 400)
        a.plot(g, N.pdf(g, lam, lam / np.sqrt(n)), color=C[1], lw=1.6, label="asymptotic N(λ, λ/√n)")
        a.axvline(lam, color="black", lw=0.8)
        a.set(title=f"n = {n}: mean of λ̂ = {lh.mean():.3f}", xlabel="λ̂ = 1/x̄", xlim=(0, 1.4))
        a.legend(fontsize=8)
    save(fig, "04_mle_asymptotics.png")


def fig04g():
    rng = np.random.default_rng(3)
    ns = np.unique(np.round(np.logspace(1, 3, 12)).astype(int))
    mean_r, med_r = [], []
    for n in ns:
        x = rng.normal(0, 1, (4000, n))
        mean_r.append(np.sqrt((x.mean(1) ** 2).mean()))
        med_r.append(np.sqrt((np.median(x, 1) ** 2).mean()))
    fig, ax = plt.subplots(figsize=(6.6, 3.7))
    ax.plot(ns, mean_r, "o-", color=C[0], label="sample mean")
    ax.plot(ns, med_r, "o-", color=C[1], label="sample median")
    ax.plot(ns, 1 / np.sqrt(ns), color="black", ls="--", label="Cramér–Rao bound 1/√n")
    ax.set(xscale="log", yscale="log", title="Error (RMSE) of estimating a normal mean",
           xlabel="sample size n", ylabel="root mean squared error")
    ax.legend()
    save(fig, "04_cramer_rao.png")


# ============================================================ 05 confidence intervals
def fig05a():
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
        col = C[0] if ok else C[1]
        ax.plot([m - h, m + h], [i, i], color=col, lw=2); ax.plot(m, i, "o", color=col, ms=3)
    ax.axvline(mu, color="black", lw=1.2, label="true mean μ = 50")
    ax.set(title=f"50 different samples, 50 different 95% intervals — {miss} miss μ (red)",
           xlabel="value", ylabel="sample number", yticks=[])
    ax.legend(loc="upper right")
    save(fig, "05_ci_coverage.png")


def fig05b():
    fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.5))
    n = np.arange(2, 101)
    ax[0].plot(n, stats.t.ppf(0.975, n - 1), color=C[0], label="t critical value")
    ax[0].axhline(1.96, color="black", ls="--", lw=1, label="z = 1.96")
    ax[0].set(title="95% multiplier: t shrinks to z as n grows", xlabel="sample size n", ylabel="critical value")
    ax[0].legend()
    n2 = np.arange(5, 301)
    for lev, c in [(0.90, C[2]), (0.95, C[0]), (0.99, C[1])]:
        ax[1].plot(n2, 2 * stats.t.ppf(1 - (1 - lev) / 2, n2 - 1) * 10 / np.sqrt(n2), color=c, label=f"{int(lev*100)}% confidence")
    ax[1].set(title="CI width for a mean (s = 10)", xlabel="sample size n", ylabel="width of interval")
    ax[1].legend()
    E = np.linspace(0.01, 0.1, 200)
    for p, c in [(0.5, C[1]), (0.3, C[0]), (0.1, C[2])]:
        ax[2].plot(E * 100, 1.96 ** 2 * p * (1 - p) / E ** 2, color=c, label=f"p = {p}")
    ax[2].set(yscale="log", title="Sample size for a 95% margin of error E", xlabel="margin of error E (points)",
              ylabel="required n")
    ax[2].legend()
    save(fig, "05_width_and_sample_size.png")


def fig05c():
    n, z = 30, 1.96
    ps = np.linspace(0.02, 0.98, 481)
    k = np.arange(n + 1)
    ph = k / n
    se = np.sqrt(ph * (1 - ph) / n)
    wald = (ph - z * se, ph + z * se)
    c = (ph + z * z / (2 * n)) / (1 + z * z / n)
    h = z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    wil = (c - h, c + h)
    cp = (np.where(k == 0, 0, stats.beta.ppf(0.025, np.maximum(k, 1), n - k + 1)),
          np.where(k == n, 1, stats.beta.ppf(0.975, k + 1, np.maximum(n - k, 1))))
    fig, ax = plt.subplots(figsize=(8.5, 3.9))
    for (lo, hi), col, lab in [(wald, C[1], "Wald  p̂ ± 1.96·SE"), (wil, C[2], "Wilson"), (cp, C[0], "Clopper–Pearson (exact)")]:
        cov = np.array([stats.binom.pmf(k, n, p)[(lo <= p) & (p <= hi)].sum() for p in ps])
        ax.plot(ps, cov, color=col, lw=1.3, label=lab)
    ax.axhline(0.95, color="black", ls="--", lw=1)
    ax.set(ylim=(0.75, 1.0), title="Actual coverage of nominal 95% intervals for a proportion (n = 30)",
           xlabel="true proportion p", ylabel="actual coverage")
    ax.legend(loc="lower center", ncol=3, fontsize=8)
    save(fig, "05_proportion_coverage.png")


def fig05d():
    rng = np.random.default_rng(4)
    ns = [3, 5, 10, 20, 30, 100]
    zc = [1 - 2 * stats.t.sf(1.96, n - 1) for n in ns]
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
    x = np.arange(len(ns))
    ax[0].bar(x - 0.2, zc, width=0.4, color=C[1], label="x̄ ± 1.96·s/√n  (wrong multiplier)")
    ax[0].bar(x + 0.2, [0.95] * len(ns), width=0.4, color=C[0], label="x̄ ± t*·s/√n  (correct)")
    ax[0].set_xticks(x, [f"n={n}" for n in ns]); ax[0].axhline(0.95, color="black", ls="--", lw=1)
    ax[0].set(ylim=(0.7, 1.06), title="Using z instead of t undercovers for small n", ylabel="actual coverage")
    ax[0].legend(fontsize=8, loc="upper center", ncol=2)
    for i, v in enumerate(zc):
        ax[0].text(i - 0.2, v + 0.004, f"{v:.3f}", ha="center", fontsize=8)
    boot = np.array([np.median(rng.choice(DELIVERY, DELIVERY.size)) for _ in range(10000)])
    lo, hi = np.percentile(boot, [2.5, 97.5])
    ax[1].hist(boot, bins=np.arange(29.75, 38.25, 0.5), density=True, color=C[0], alpha=0.6)
    ax[1].axvline(lo, color=C[1], ls="--"); ax[1].axvline(hi, color=C[1], ls="--")
    ax[1].axvline(np.median(DELIVERY), color="black")
    ax[1].set(title=f"Bootstrap distribution of the median: 95% CI ({lo:.1f}, {hi:.1f})", xlabel="resampled median")
    save(fig, "05_t_vs_z_and_bootstrap.png")


# ============================================================ 06 hypothesis testing
def fig06a():
    g = np.linspace(-4, 4, 600)
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 3.6))
    ax[0].plot(g, N.pdf(g), color="black")
    for lo, hi in [(-4, -1.96), (1.96, 4)]:
        m = (g >= lo) & (g <= hi)
        ax[0].fill_between(g[m], N.pdf(g[m]), color=C[1], alpha=0.6)
    ax[0].text(0, 0.1, "do not reject H₀\n(95%)", ha="center")
    ax[0].text(2.3, 0.07, "reject\n2.5%", ha="center", color=C[1], fontsize=9)
    ax[0].text(-2.3, 0.07, "reject\n2.5%", ha="center", color=C[1], fontsize=9)
    ax[0].set(title="Two-tailed test at α = 0.05: critical values ±1.96", xlabel="z (if H₀ is true)", ylabel="density")
    ax[1].plot(g, N.pdf(g), color="black")
    for lo, hi in [(-4, -2), (2, 4)]:
        m = (g >= lo) & (g <= hi)
        ax[1].fill_between(g[m], N.pdf(g[m]), color=C[0], alpha=0.6)
    ax[1].axvline(2, color=C[0], ls="--")
    ax[1].text(2.1, 0.2, "observed z = 2", color=C[0], fontsize=9)
    ax[1].text(0, 0.1, "p-value = 0.0455\n= both shaded tails", ha="center")
    ax[1].set(title="p-value: how extreme is the data if H₀ is true?", xlabel="z (if H₀ is true)")
    save(fig, "06_rejection_and_pvalue.png")


def fig06b():
    mu0, mu1, se = 30, 32, 1.0
    g = np.linspace(25, 37, 800)
    chi, clo = mu0 + 1.96 * se, mu0 - 1.96 * se
    fig, ax = plt.subplots(figsize=(8.5, 3.9))
    ax.plot(g, N.pdf(g, mu0, se), color=C[0], lw=2, label="H₀ true: μ = 30")
    ax.plot(g, N.pdf(g, mu1, se), color=C[2], lw=2, label="H₁ true: μ = 32")
    m = g >= chi
    ax.fill_between(g[m], N.pdf(g[m], mu0, se), color=C[1], alpha=0.7, label="α: Type I error (2.5% per tail)")
    m = g <= clo
    ax.fill_between(g[m], N.pdf(g[m], mu0, se), color=C[1], alpha=0.7)
    m = (g > clo) & (g < chi)
    ax.fill_between(g[m], N.pdf(g[m], mu1, se), color=C[3], alpha=0.45, label="β: Type II error = 0.48")
    ax.axvline(chi, color="black", ls="--", lw=1); ax.axvline(clo, color="black", ls="--", lw=1)
    ax.text(chi + 0.15, 0.2, "reject H₀ →", fontsize=9)
    ax.set(title="Error types and power (n = 49, σ = 7, power = 1 − β ≈ 0.52)", xlabel="sample mean x̄", ylabel="density")
    ax.legend(loc="upper left", fontsize=8)
    save(fig, "06_errors_power.png")


def fig06c():
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))
    n = np.arange(5, 301)
    for delta, c in [(1, C[1]), (2, C[0]), (3, C[2])]:
        se = 7 / np.sqrt(n)
        ax[0].plot(n, N.sf(1.96 - delta / se) + N.cdf(-1.96 - delta / se), color=c, label=f"true shift = {delta} min")
    ax[0].axhline(0.8, color="grey", ls="--", lw=1)
    ax[0].set(title="Power rises with n and with effect size (σ = 7)", xlabel="sample size n", ylabel="power")
    ax[0].legend(loc="lower right")
    d = np.linspace(0, 5, 200)
    for a, c in [(0.01, C[1]), (0.05, C[0]), (0.10, C[2])]:
        zc = N.ppf(1 - a / 2)
        ax[1].plot(d, N.sf(zc - d) + N.cdf(-zc - d), color=c, label=f"α = {a}")
    ax[1].set(title="Power vs shift (n = 49): lower α, lower power", xlabel="true shift μ − μ₀ (min)", ylabel="power")
    ax[1].legend(loc="lower right")
    save(fig, "06_power_curves.png")


def fig06d():
    rng = np.random.default_rng(9)
    reps = 100000
    x0 = rng.normal(30, 7, (reps, 49)).mean(axis=1)
    p0 = 2 * N.sf(np.abs((x0 - 30) / 1))
    x1 = rng.normal(32, 7, (reps, 49)).mean(axis=1)
    p1 = 2 * N.sf(np.abs((x1 - 30) / 1))
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.5), sharey=True)
    ax[0].hist(p0, bins=20, range=(0, 1), density=True, color=C[0], alpha=0.7)
    ax[0].axhline(1, color="black", lw=1, ls="--")
    ax[0].set(title="H₀ true: p-values are uniform on [0, 1]\n(5% fall below 0.05)", xlabel="p-value", ylabel="density")
    ax[1].hist(p1, bins=20, range=(0, 1), density=True, color=C[2], alpha=0.7)
    ax[1].axhline(1, color="black", lw=1, ls="--")
    ax[1].set(title=f"H₁ true (shift 2): p-values pile up near 0\n({(p1 < 0.05).mean():.0%} fall below 0.05 = power)", xlabel="p-value")
    save(fig, "06_pvalue_distribution.png")


if __name__ == "__main__":
    for f in [fig01a, fig01b, fig02a, fig02b, fig02c, fig02d, fig03a, fig03b, fig03c, fig03d, fig03e, fig03f,
              fig03g, fig04a, fig04b, fig04c, fig04d, fig04e, fig04f, fig04g, fig05a, fig05b, fig05c, fig05d,
              fig06a, fig06b, fig06c, fig06d]:
        f()
    print("figures written to", OUT)
