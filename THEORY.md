# Theory Notes

## 1. Statistics basics
- **Statistics**: science of collecting, organizing, analysing and interpreting data.
- **Descriptive**: summarise the data in hand — central tendency (mean, median, mode), dispersion (range, variance, SD, IQR), shape (skewness, kurtosis), distributions (Bernoulli, Uniform, Binomial, Normal, Exponential, Poisson).
- **Inferential**: draw conclusions about a *population* from a *sample* — t-test, Z-test, Chi-square, ANOVA, hypothesis tests, p-value, significance level.
- **Population (N)** = everything of interest; **sample (n)** = subset. Parameters (μ, σ) describe populations; statistics (x̄, s) describe samples.
- **Scales of measurement**: Nominal (labels, no order) → Ordinal (order, unequal gaps) → Interval (equal gaps, no true zero, e.g. °C) → Ratio (true zero, e.g. price, height).
- Data types: Qualitative (nominal/ordinal) vs Quantitative (discrete = counts, continuous = any value).
- z-score: z = (x − μ)/σ — answers "how many SDs from the mean" (e.g. 140 cm in the cricket-camp sample).

## 2. Covariance and correlation (Lab 6 – Part B)
**Covariance** measures how two variables vary together:
cov(X,Y) = Σ(xᵢ − x̄)(yᵢ − ȳ) / (n − 1)
- > 0: move together; < 0: move opposite; ≈ 0: no linear relation.
- Magnitude depends on units, so it can't be compared across variable pairs.

**Pearson correlation** standardises covariance: r = cov(X,Y) / (sₓ·s_y), −1 ≤ r ≤ 1.
- Measures *linear* association. Sensitive to outliers. r² = share of variance in Y explained linearly by X.
- Rough strength guide (|r|): <0.2 very weak, 0.2–0.4 weak, 0.4–0.6 moderate, 0.6–0.8 strong, >0.8 very strong.

**Spearman rank correlation** (ρ): Pearson computed on ranks. Detects any *monotonic* relation, robust to outliers and non-normal data; works for ordinal data.

Correlation ≠ causation.

## 3. Hypothesis testing for correlation (Lab 6 – Part C)
- H₀: ρ = 0 (no correlation) vs H₁: ρ ≠ 0 (two-tailed).
- Pearson test statistic: t = r·√(n−2)/√(1−r²), df = n − 2.
- Decision: if p < α (usually 0.05) reject H₀ → statistically significant correlation. Significance ≠ practical importance; always report r and its CI (Fisher z: z = arctanh(r), SE = 1/√(n−3)).
- Assumptions — Pearson: linear relation, roughly bivariate normal, no extreme outliers. Spearman: monotonic relation, ordinal or continuous.

## 4. Hypothesis-testing framework
1. State H₀ and H₁. 2. Choose α. 3. Pick the test. 4. Compute statistic and p-value. 5. Decide. 6. Interpret in context.
Type I error (α) = reject a true H₀; Type II error (β) = fail to reject a false H₀; power = 1 − β.

| Situation | Test |
|---|---|
| Mean vs known value, σ known, large n | Z-test |
| Mean vs known value, σ unknown | One-sample t-test |
| Two groups' means | Independent t-test (paired t-test for before/after) |
| ≥ 3 groups' means | One-way ANOVA |
| Two categorical variables | Chi-square test of independence |

## 5. Chi-square test of independence (Practical 6)
χ² = Σ (O − E)² / E, with E = (row total × column total)/grand total, df = (r−1)(c−1).
H₀: the variables are independent. Assumes counts (not percentages), independent observations, expected counts ≥ 5. Effect size: Cramér's V = √(χ²/(n·(k−1))).

## 6. One-way ANOVA (Practical 6)
Compares means of k groups: F = MS_between / MS_within = [SSB/(k−1)] / [SSW/(N−k)].
H₀: μ₁ = μ₂ = … = μ_k; H₁: at least one mean differs. Assumptions: independence, normal residuals, equal variances (Levene). A significant F says *some* group differs; use Tukey HSD to find which. Non-parametric alternative: Kruskal-Wallis. Effect size: η² = SSB/SST.

## 7. Sampling, CLT, standard error, bootstrap
- **Sampling distribution**: distribution of a statistic (e.g. x̄) over repeated samples.
- **Central Limit Theorem**: for independent samples of size n from any population with mean μ and finite variance σ², x̄ → Normal(μ, σ²/n) as n grows. Skewed populations need larger n.
- **Standard error** SE = σ/√n (estimated by s/√n). Quadrupling n halves the SE.
- **Confidence interval**: x̄ ± t*·SE. "95%" means 95% of intervals built this way cover the true μ (coverage probability — Exercise 5).
- **Bootstrap**: resample the *sample* with replacement many times, compute the statistic each time; the spread approximates the sampling distribution without distributional assumptions.
- **Mean vs median as estimators**: mean is unbiased for μ and has lower variance for symmetric light-tailed data; median is robust to outliers and targets the population median.

## 8. Regression metrics used in the project
- **R²** = 1 − SS_res/SS_tot (share of variance explained; can be negative on test data if the model is worse than predicting the mean).
- **Adjusted R²** = 1 − (1−R²)(n−1)/(n−p−1) penalises useless predictors.
- **MAE** (average absolute error), **MSE**, **RMSE** (same units as target), **MAPE** (% error).
- Compare Train vs Test R² for overfitting; use cross-validated R² for model selection.
- **Ridge** (L2) shrinks coefficients; **Lasso** (L1) shrinks and can zero out features; both need scaled inputs. Trees/Forests capture non-linear effects and interactions without scaling.
