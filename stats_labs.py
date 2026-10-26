"""
Statistics labs: Lab 6 (B, C), Practical 6, and Sampling/CLT/Bootstrap exercises.
Run everything:  python stats_labs.py
Run one part:    python stats_labs.py lab6b | lab6c | practical6 | ex1 | ex2 | ex3 | ex4 | ex5
Each exercise reads the real Kaggle/UCI CSV if it is in the same folder
(train.csv, StudentPerformanceFactors.csv, OnlineRetail.csv, insurance.csv, StudentsPerformance.csv);
otherwise a synthetic stand-in with a similar shape is generated so the code runs.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

OUT = "outputs_stats"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(42)


def save(name):
    plt.tight_layout()
    plt.savefig(f"{OUT}/{name}.png", dpi=110)
    plt.close()


# =============================================================================
# LAB 6 - PART B: Covariance & Correlation
# =============================================================================
def lab6b(df=None):
    print("\n########## LAB 6 PART B: COVARIANCE & CORRELATION ##########")
    if df is None:
        n = 200
        area = rng.normal(1200, 300, n)
        df = pd.DataFrame({
            "area": area,
            "price": area * 5000 + rng.normal(0, 800000, n),
            "age": rng.integers(0, 30, n),
            "distance": rng.uniform(1, 25, n),
        })
        df["price"] -= df["distance"] * 60000
    # covariance: sign shows direction, magnitude depends on units
    print("Covariance matrix (sample, ddof=1):\n", df.cov().round(2))
    # correlation: unit-free, in [-1, 1]
    print("\nPearson correlation matrix:\n", df.corr().round(3))
    print("\nSpearman correlation matrix:\n", df.corr(method="spearman").round(3))

    # manual formula check:  cov(X,Y) = sum((x-xbar)(y-ybar)) / (n-1) ;  r = cov / (sx*sy)
    x, y = df["area"], df["price"]
    cov_manual = ((x - x.mean()) * (y - y.mean())).sum() / (len(x) - 1)
    r_manual = cov_manual / (x.std() * y.std())
    print(f"\nManual cov(area, price) = {cov_manual:.2f} | numpy = {np.cov(x, y)[0, 1]:.2f}")
    print(f"Manual r = {r_manual:.4f} | pandas = {x.corr(y):.4f}")

    def interpret(r):
        a = abs(r)
        s = ("very weak" if a < .2 else "weak" if a < .4 else "moderate" if a < .6
             else "strong" if a < .8 else "very strong")
        return f"{s} {'positive' if r > 0 else 'negative'}"

    for c in df.columns[1:]:
        r = df["area"].corr(df[c])
        print(f"area vs {c}: r={r:.3f} -> {interpret(r)}")

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=ax[0])
    ax[0].set_title("Correlation heatmap")
    sns.regplot(x="area", y="price", data=df, ax=ax[1], scatter_kws={"alpha": .5})
    ax[1].set_title(f"area vs price (r={r_manual:.2f})")
    save("lab6b_corr")


# =============================================================================
# LAB 6 - PART C: Hypothesis test for correlation (Pearson & Spearman)
# =============================================================================
def lab6c(df=None, alpha=0.05):
    print("\n########## LAB 6 PART C: HYPOTHESIS TESTING FOR CORRELATION ##########")
    if df is None:
        n = 150
        x = rng.normal(50, 10, n)
        df = pd.DataFrame({"x": x, "y": 0.6 * x + rng.normal(0, 8, n),
                           "z": np.exp(x / 20) + rng.normal(0, .3, n),   # monotonic, non-linear
                           "noise": rng.normal(0, 1, n)})
    pairs = [("x", "y"), ("x", "z"), ("x", "noise")]
    print("H0: rho = 0 (no correlation)   H1: rho != 0   alpha =", alpha)
    for a, b in pairs:
        r, p_r = stats.pearsonr(df[a], df[b])
        rho, p_s = stats.spearmanr(df[a], df[b])
        n = len(df)
        t = r * np.sqrt((n - 2) / (1 - r ** 2))            # t statistic for Pearson
        print(f"\n{a} vs {b}")
        print(f"  Pearson : r={r:.4f}, t={t:.3f}, p={p_r:.4g} -> "
              f"{'Reject H0' if p_r < alpha else 'Fail to reject H0'}")
        print(f"  Spearman: rho={rho:.4f}, p={p_s:.4g} -> "
              f"{'Reject H0' if p_s < alpha else 'Fail to reject H0'}")
        # 95% CI of Pearson r via Fisher z-transform
        z = np.arctanh(r); se = 1 / np.sqrt(n - 3)
        lo, hi = np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se)
        print(f"  95% CI for r: [{lo:.3f}, {hi:.3f}]   R^2 = {r ** 2:.3f}")
        # normality check helps choose Pearson vs Spearman
        print(f"  Shapiro p-values: {a}={stats.shapiro(df[a])[1]:.3f}, {b}={stats.shapiro(df[b])[1]:.3f}"
              "  (p<0.05 => prefer Spearman)")


# =============================================================================
# PRACTICAL 6: Chi-square test + One-way ANOVA (+ descriptive stats, plots, 1-sample t)
# =============================================================================
def practical6(df=None, alpha=0.05):
    print("\n########## PRACTICAL 6: CHI-SQUARE, ANOVA, DESCRIPTIVE, t-TEST ##########")
    if df is None:   # >=100 rows, numeric + categorical groups, before/after style values
        n = 300
        df = pd.DataFrame({
            "region": rng.choice(["North", "South", "East", "West"], n),
            "segment": rng.choice(["Basic", "Premium"], n, p=[.6, .4]),
            "sales_before": rng.normal(100, 15, n),
        })
        df["sales_after"] = df["sales_before"] + rng.normal(5, 10, n) + (df["region"] == "South") * 6
    num = "sales_after"

    # ---- Part B: descriptive statistics ----
    s = df[num]
    q1, q3 = s.quantile(.25), s.quantile(.75)
    print("\nPart B - Descriptive statistics of", num)
    print(f"Mean={s.mean():.3f} Median={s.median():.3f} Mode={s.round(0).mode()[0]:.0f}\n"
          f"Variance={s.var():.3f} Std={s.std():.3f} Range={s.max() - s.min():.3f} IQR={q3 - q1:.3f}")

    # ---- Part C: plots ----
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    sns.histplot(s, kde=True, ax=ax[0]); ax[0].set_title("Histogram")
    sns.boxplot(x="region", y=num, data=df, ax=ax[1]); ax[1].set_title("Boxplot by region")
    df["region"].value_counts().plot.bar(ax=ax[2]); ax[2].set_title("Bar chart: region counts")
    save("practical6_plots")

    # ---- Part D1: one-sample t-test ----
    mu0 = 100
    t, p = stats.ttest_1samp(s, mu0)
    print(f"\nOne-sample t-test: H0: mu = {mu0}  H1: mu != {mu0}")
    print(f"  t = {t:.4f}, p = {p:.4g} -> {'Reject H0' if p < alpha else 'Fail to reject H0'}")

    # ---- Chi-square test of independence ----
    ct = pd.crosstab(df["region"], df["segment"])
    chi2, p, dof, exp = stats.chi2_contingency(ct)
    print("\nChi-square test of independence (region x segment)")
    print("H0: variables are independent   H1: they are associated")
    print(ct)
    print(f"  chi2 = {chi2:.4f}, dof = {dof}, p = {p:.4g}")
    print(f"  min expected count = {exp.min():.2f} (should be >= 5)")
    print(f"  Decision: {'Reject H0 (associated)' if p < alpha else 'Fail to reject H0 (independent)'}")
    cramers_v = np.sqrt(chi2 / (ct.values.sum() * (min(ct.shape) - 1)))
    print(f"  Cramer's V (effect size) = {cramers_v:.3f}")

    # ---- One-way ANOVA ----
    groups = [g[num].values for _, g in df.groupby("region")]
    F, p = stats.f_oneway(*groups)
    print("\nOne-way ANOVA: mean", num, "across regions")
    print("H0: all group means equal   H1: at least one differs")
    print(f"  F = {F:.4f}, p = {p:.4g} -> {'Reject H0' if p < alpha else 'Fail to reject H0'}")
    print("  Levene (equal variance) p =", round(stats.levene(*groups)[1], 4),
          "| Kruskal-Wallis (non-parametric) p =", round(stats.kruskal(*groups)[1], 4))
    k, N = len(groups), len(df)
    ssb = sum(len(g) * (g.mean() - s.mean()) ** 2 for g in groups)
    sst = ((s - s.mean()) ** 2).sum()
    print(f"  eta^2 (effect size) = {ssb / sst:.3f}")
    if p < alpha:   # Tukey post-hoc (scipy >= 1.8)
        print("\nTukey HSD post-hoc:\n", stats.tukey_hsd(*groups))

    # paired t-test for before/after
    t, p = stats.ttest_rel(df["sales_after"], df["sales_before"])
    print(f"\nPaired t-test (before vs after): t={t:.3f}, p={p:.4g}")


# =============================================================================
# EXERCISE 1: House price - CLT & confidence intervals
# =============================================================================
def ex1():
    print("\n########## EXERCISE 1: HOUSE PRICES - CLT ##########")
    if os.path.exists("train.csv"):
        price = pd.read_csv("train.csv")["SalePrice"].dropna()
    else:
        price = pd.Series(rng.lognormal(12.0, 0.4, 1460)).rename("SalePrice")
    mu, sd = price.mean(), price.std(ddof=0)
    print(f"Population: mean={mu:,.0f} median={price.median():,.0f} std={sd:,.0f}")
    sizes = [30, 50, 100, 200]
    fig, ax = plt.subplots(1, 4, figsize=(18, 3.8))
    for a, n in zip(ax, sizes):
        means = np.array([price.sample(n).mean() for _ in range(2000)])
        se_emp, se_th = means.std(ddof=1), sd / np.sqrt(n)
        print(f"n={n:4d}: mean of means={means.mean():,.0f} | empirical SE={se_emp:,.0f} | "
              f"theoretical SE=sigma/sqrt(n)={se_th:,.0f}")
        sns.histplot(means, kde=True, ax=a); a.axvline(mu, color="r", ls="--")
        a.set_title(f"n={n}")
    save("ex1_sampling_distribution")
    # 95% CI from one sample
    smp = price.sample(100, random_state=1)
    ci = stats.t.interval(0.95, len(smp) - 1, smp.mean(), stats.sem(smp))
    print(f"95% t-CI from one sample (n=100): ({ci[0]:,.0f}, {ci[1]:,.0f}); true mean {mu:,.0f}")


# =============================================================================
# EXERCISE 2: Bootstrap - student performance
# =============================================================================
def ex2():
    print("\n########## EXERCISE 2: BOOTSTRAP ##########")
    if os.path.exists("StudentPerformanceFactors.csv"):
        scores = pd.read_csv("StudentPerformanceFactors.csv")["Exam_Score"].dropna()
    else:
        scores = pd.Series(np.clip(rng.normal(67, 4, 6500), 50, 101))
    print(f"Population mean={scores.mean():.3f} median={scores.median():.3f}")
    fig, ax = plt.subplots(1, 3, figsize=(15, 3.8))
    for a, n in zip(ax, [30, 50, 100]):
        smp = scores.sample(n, random_state=7).values
        boot = np.array([rng.choice(smp, n, replace=True).mean() for _ in range(5000)])
        lo, hi = np.percentile(boot, [2.5, 97.5])
        print(f"n={n:3d}: sample mean={smp.mean():.3f} median={np.median(smp):.3f} | "
              f"bootstrap mean={boot.mean():.3f} SE={boot.std():.3f} | 95% CI=({lo:.2f}, {hi:.2f}) | "
              f"pop mean inside CI: {lo <= scores.mean() <= hi}")
        sns.histplot(boot, kde=True, ax=a); a.axvline(scores.mean(), color="r", ls="--", label="population mean")
        a.set_title(f"Bootstrap distribution n={n}"); a.legend()
    save("ex2_bootstrap")


# =============================================================================
# EXERCISE 3: CLT with skewed transaction data
# =============================================================================
def ex3():
    print("\n########## EXERCISE 3: CLT ON SKEWED RETAIL DATA ##########")
    if os.path.exists("OnlineRetail.csv"):
        df = pd.read_csv("OnlineRetail.csv", encoding="ISO-8859-1")
    else:
        m = 20000
        df = pd.DataFrame({"Quantity": rng.integers(-5, 40, m), "UnitPrice": rng.lognormal(1, 1, m)})
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()      # 1. remove invalid
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]                  # 2. revenue
    pop = df["Revenue"]
    clip = pop.clip(upper=pop.quantile(.99))                          # only to make plot readable
    plt.figure(figsize=(6, 4)); sns.histplot(clip, bins=60, kde=True)
    plt.title("Population distribution of Revenue (clipped at 99th pct)"); save("ex3_population")
    print(f"Population mean={pop.mean():.2f}, std={pop.std():.2f}, skewness={stats.skew(pop):.2f}")
    for n in [10, 30, 100]:
        means = np.array([pop.sample(n).mean() for _ in range(5000)])
        se_emp, se_th = means.std(ddof=1), pop.std() / np.sqrt(n)
        sk = stats.skew(means)
        sh = stats.shapiro(means[:5000])[1]
        print(f"n={n:3d}: mean of means={means.mean():.2f} | SE emp={se_emp:.2f} theory={se_th:.2f} | "
              f"skew={sk:.2f} | Shapiro p={sh:.3g}")
        fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
        sns.histplot(means, kde=True, ax=ax[0]); ax[0].set_title(f"Sampling distribution n={n}")
        stats.probplot(means, plot=ax[1]); ax[1].set_title("Q-Q plot")
        save(f"ex3_sampling_n{n}")
    print("""
Why CLT works: the sample mean is a sum of n independent draws divided by n. Extreme values in a
skewed population are rare, so in any one sample they are averaged with many ordinary values.
As n grows, skewness of the mean shrinks roughly as skew/sqrt(n) and the distribution of the mean
approaches Normal(mu, sigma/sqrt(n)) regardless of the population's shape (finite variance required).
Heavily skewed data needs a larger n (>=100 here) than symmetric data (n~30).""")


# =============================================================================
# EXERCISE 4: Mean vs median as estimators
# =============================================================================
def ex4():
    print("\n########## EXERCISE 4: MEAN vs MEDIAN AS ESTIMATORS ##########")
    if os.path.exists("insurance.csv"):
        ch = pd.read_csv("insurance.csv")["charges"]
    else:
        ch = pd.Series(rng.lognormal(9, 0.9, 1338))
    print(f"Population mean={ch.mean():.1f} median={ch.median():.1f}")
    for n in [30, 50, 100]:
        means = np.empty(1000); meds = np.empty(1000)
        for i in range(1000):
            s = ch.sample(n).values; means[i] = s.mean(); meds[i] = np.median(s)
        print(f"n={n:3d}: Var(mean)={means.var():.1f}  Var(median)={meds.var():.1f} | "
              f"bias(mean wrt pop mean)={means.mean() - ch.mean():.1f}  "
              f"bias(median wrt pop median)={meds.mean() - ch.median():.1f}")
        fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
        sns.histplot(means, kde=True, ax=ax[0]); ax[0].axvline(ch.mean(), color="r", ls="--")
        ax[0].set_title(f"Sample means n={n}")
        sns.histplot(meds, kde=True, ax=ax[1], color="green"); ax[1].axvline(ch.median(), color="r", ls="--")
        ax[1].set_title(f"Sample medians n={n}")
        save(f"ex4_n{n}")
    print("""Conclusion: the sample mean is an unbiased estimator of the population mean. The median estimates
the population MEDIAN (different from the mean for skewed data). For near-normal data the mean has lower
variance (median variance ~ pi/2 x larger); for heavy-tailed/skewed data with outliers the median is
more robust. Compare estimators against the parameter they target.""")


# =============================================================================
# EXERCISE 5: Sampling distribution & coverage probability
# =============================================================================
def ex5():
    print("\n########## EXERCISE 5: COVERAGE PROBABILITY ##########")
    if os.path.exists("StudentsPerformance.csv"):
        ms = pd.read_csv("StudentsPerformance.csv")["math score"]
    else:
        ms = pd.Series(np.clip(rng.normal(66, 15, 1000), 0, 100).round())
    mu, sd = ms.mean(), ms.std(ddof=0)
    print(f"Population mean={mu:.2f} std={sd:.2f}")
    rows = []
    for n in [10, 30, 50, 100]:
        cover_t = 0; means = []; ses = []
        for _ in range(1000):
            s = ms.sample(n); m, se = s.mean(), s.std(ddof=1) / np.sqrt(n)
            means.append(m); ses.append(se)
            tcrit = stats.t.ppf(.975, n - 1)
            cover_t += (m - tcrit * se <= mu <= m + tcrit * se)
        rows.append({"n": n, "mean of sample means": np.mean(means), "avg SE": np.mean(ses),
                     "theoretical SE": sd / np.sqrt(n), "95% CI coverage": cover_t / 1000})
    print(pd.DataFrame(rows).round(4).to_string(index=False))
    print("Coverage should be close to 0.95; SE falls as 1/sqrt(n).")


ALL = dict(lab6b=lab6b, lab6c=lab6c, practical6=practical6, ex1=ex1, ex2=ex2, ex3=ex3, ex4=ex4, ex5=ex5)

if __name__ == "__main__":
    todo = sys.argv[1:] or list(ALL)
    for k in todo:
        ALL[k]()
    print(f"\nPlots saved in ./{OUT}/")
