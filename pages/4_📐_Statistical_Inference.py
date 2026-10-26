"""
Page 4: Applied Statistical Inference, Hypothesis Testing & Sampling Theory
"""
import os
import streamlit as st
from utils import apply_custom_styles

st.set_page_config(page_title="Statistical Inference - Real Estate AI", page_icon="📐", layout="wide")
apply_custom_styles()

st.title("📐 Statistical Inference & Academic Lab Experiments")
st.markdown("""
Empirical verification of statistical theories supporting the predictive models:
**Lab 6B/6C (Covariance, Correlation & Hypothesis Testing)**, **Practical 6 (ANOVA & Chi-Square)**,
and **Sampling Distributions, Central Limit Theorem (CLT) & Bootstrap Confidence Intervals**.
""")

stats_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs_stats")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔗 Lab 6: Correlation & Hypothesis Testing",
    "📊 Practical 6: Chi-Square & ANOVA",
    "🎲 Central Limit Theorem (CLT)",
    "🔁 Bootstrapping & Resampling CIs"
])

# ---------------------------------------------------------------------------
# TAB 1: LAB 6 (B & C)
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Lab 6 (B & C): Covariance, Pearson vs. Spearman, and Hypothesis Testing")
    st.markdown(r"""
    - **Covariance:** $\mathrm{Cov}(X,Y) = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{n-1}$. Measures directional co-movement; dependent on variable units.
    - **Pearson Correlation ($r$):** Standardized covariance in $[-1, 1]$ measuring purely *linear* association.
    - **Spearman Rank Correlation ($\rho$):** Pearson applied on ranks; robust to extreme outliers and evaluates any *monotonic* relation.
    """)
    
    corr_img = os.path.join(stats_dir, "lab6b_corr.png")
    c1, c2 = st.columns([3, 2])
    with c1:
        if os.path.exists(corr_img):
            st.image(corr_img, caption="Lab 6B: Correlation Scatter Plots and Fitted Regression Lines", use_container_width=True)
    with c2:
        st.markdown("#### Hypothesis Testing on Pearson $r$ (Lab 6C)")
        st.markdown(r"""
        - **Null Hypothesis ($H_0$):** $\rho = 0$ (No correlation in population)
        - **Alternative Hypothesis ($H_1$):** $\rho \neq 0$ (Statistically significant correlation)
        - **Test Statistic:**
          $$t = \frac{r \sqrt{n-2}}{\sqrt{1 - r^2}}, \quad \text{with } df = n-2$$
        - **Fisher's $z$-Transformation:**
          $$z' = \frac{1}{2} \ln\left(\frac{1+r}{1-r}\right) = \operatorname{arctanh}(r), \quad \mathrm{SE} = \frac{1}{\sqrt{n-3}}$$
        - **Decision Rule:** Since $p < 0.001 \ll 0.05$, reject $H_0$. Strong evidence that property size and location significantly correlate with valuation.
        """)

# ---------------------------------------------------------------------------
# TAB 2: PRACTICAL 6 (CHI-SQUARE & ANOVA)
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Practical 6: Categorical Association & Variance Decomposition")
    
    prac_img = os.path.join(stats_dir, "practical6_plots.png")
    p1, p2 = st.columns([3, 2])
    with p1:
        if os.path.exists(prac_img):
            st.image(prac_img, caption="Practical 6: ANOVA Group Comparisons and Contingency Distributions", use_container_width=True)
    with p2:
        st.markdown(r"#### 1. Chi-Square Test of Independence ($\chi^2$)")
        st.markdown(r"""
        $$\chi^2 = \sum \frac{(O - E)^2}{E}, \quad df = (r-1)(c-1)$$
        - Tests whether categorical dimensions (e.g., City vs. Furnishing type) are statistically independent.
        - Effect size computed via **Cramér's $V$**:
          $$V = \sqrt{\frac{\chi^2}{n \cdot \min(r-1, c-1)}}$$
        
        #### 2. One-Way ANOVA ($F$-Test)
        - Compares price variations between multiple city tiers:
          $$F = \frac{\mathrm{MS}_{\mathrm{between}}}{\mathrm{MS}_{\mathrm{within}}} = \frac{\mathrm{SSB}/(k-1)}{\mathrm{SSW}/(N-k)}$$
        - **Result:** $F \gg F_{\mathrm{crit}}$, confirming statistically significant price divergence across Tier-1 and Tier-2 metropolitan zones.
        """)

# ---------------------------------------------------------------------------
# TAB 3: CENTRAL LIMIT THEOREM (CLT)
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Central Limit Theorem (CLT) & Sample Size Dynamics")
    st.markdown(r"""
    **The Theorem:** For independent random samples of size $n$ drawn from ANY population with mean $\mu$ and finite variance $\sigma^2$,
    the sampling distribution of the sample mean approaches normality as $n \to \infty$:
    $$\bar{X}_n \sim \mathcal{N}\left(\mu, \frac{\sigma^2}{n}\right)$$
    """)
    
    n_choice = st.select_slider("Select Sample Size (n):", options=[10, 30, 100], value=30)
    
    clt_col1, clt_col2 = st.columns(2)
    with clt_col1:
        pop_img = os.path.join(stats_dir, "ex3_population.png")
        if os.path.exists(pop_img):
            st.image(pop_img, caption="Underlying Population Distribution (Highly Skewed / Exponential)", use_container_width=True)
    with clt_col2:
        samp_img = os.path.join(stats_dir, f"ex3_sampling_n{n_choice}.png")
        if os.path.exists(samp_img):
            st.image(samp_img, caption=f"Sampling Distribution of Mean at n = {n_choice}", use_container_width=True)
    
    st.markdown(fr"""
    **Takeaway at $n={n_choice}$:**
    - Notice that even when the underlying population is heavily skewed, the distribution of sample averages becomes smooth, symmetric, and bell-shaped.
    - Standard error shrinks at rate $1/\sqrt{{n}}$: $\mathrm{{SE}} = \sigma / \sqrt{{{n_choice}}}$.
    """)

# ---------------------------------------------------------------------------
# TAB 4: BOOTSTRAPPING
# ---------------------------------------------------------------------------
with tab4:
    st.subheader("Non-Parametric Bootstrap Resampling")
    st.markdown(r"""
    Bootstrapping creates $B = 1,000+$ surrogate datasets by resampling observations **with replacement** from the original sample.
    This provides empirical confidence intervals without relying on strict parametric normality assumptions.
    """)
    
    boot_img = os.path.join(stats_dir, "ex2_bootstrap.png")
    b1, b2 = st.columns([3, 2])
    with b1:
        if os.path.exists(boot_img):
            st.image(boot_img, caption="Bootstrap Sampling Distribution & 95% Confidence Bounds", use_container_width=True)
    with b2:
        st.markdown("#### Mean vs. Median as Estimators")
        st.markdown("""
        - **Sample Mean ($\bar{x}$):** Minimum variance unbiased estimator for symmetric light-tailed data; sensitive to extreme price outliers.
        - **Sample Median:** Highly robust against luxury mega-mansion outliers; superior measure of central tendency in skewed real estate markets.
        - The bootstrap enables empirical computation of standard errors and 95% CIs for both estimators directly.
        """)
