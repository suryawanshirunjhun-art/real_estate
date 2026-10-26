"""
Page 5: Theory, Mathematical Formulations & Viva Defense Guide
"""
import streamlit as st
from utils import apply_custom_styles

st.set_page_config(page_title="Viva Defense & Theory Guide - Real Estate AI", page_icon="📚", layout="wide")
apply_custom_styles()

st.title("📚 Viva Voce & Theory Reference Guide")
st.markdown("""
Quick-reference knowledge base containing mathematical definitions, evaluation metric formulations,
algorithm comparisons, and answers to the top 10 most anticipated presentation and viva questions.
""")

tab1, tab2, tab3 = st.tabs([
    "📐 Mathematical Formulations",
    "🎯 Top 10 Viva Questions & Answers",
    "🌐 Web Scraping & Data Engineering"
])

# ---------------------------------------------------------------------------
# TAB 1: FORMULAS
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Key Mathematical Equations")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### Regression Performance Metrics")
        st.markdown(r"""
        - **Coefficient of Determination ($R^2$):**
          $$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2} = 1 - \frac{\mathrm{SS}_{\mathrm{res}}}{\mathrm{SS}_{\mathrm{tot}}}$$
        - **Adjusted $R^2$ (Penalizes superfluous features):**
          $$R^2_{\mathrm{adj}} = 1 - \left[\frac{(1 - R^2)(n - 1)}{n - p - 1}\right]$$
        - **Root Mean Squared Error (RMSE):**
          $$\mathrm{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2}$$
        - **Mean Absolute Error (MAE):**
          $$\mathrm{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|$$
        - **Mean Absolute Percentage Error (MAPE):**
          $$\mathrm{MAPE} = \frac{100\%}{n} \sum_{i=1}^n \left|\frac{y_i - \hat{y}_i}{y_i}\right|$$
        """)
        
    with c2:
        st.markdown("#### Regularization & Shrinkage")
        st.markdown(r"""
        - **Ridge Regression ($L_2$ Regularization):**
          $$\min_{\mathbf{w}} \left\{ \sum_{i=1}^n (y_i - \mathbf{w}^T \mathbf{x}_i)^2 + \alpha \sum_{j=1}^p w_j^2 \right\}$$
          Shrinks coefficients smoothly toward zero; solves multicollinearity without eliminating features.
        
        - **Lasso Regression ($L_1$ Regularization):**
          $$\min_{\mathbf{w}} \left\{ \sum_{i=1}^n (y_i - \mathbf{w}^T \mathbf{x}_i)^2 + \alpha \sum_{j=1}^p |w_j| \right\}$$
          Forces less informative feature coefficients exactly to zero; performs embedded feature selection.
        """)

# ---------------------------------------------------------------------------
# TAB 2: TOP 10 VIVA QUESTIONS
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Top 10 Viva Voce Questions & Model Answers")
    
    with st.expander("Q1: Why did Random Forest outperform Linear, Ridge, and Lasso Regression?"):
        st.markdown("""
        **Answer:** Real estate pricing involves heavy **non-linear feature interactions**. For example, the effect of `area_sqft` on `price` depends dramatically on the `city` (₹16k/sqft in Mumbai vs ₹4k/sqft in Raipur) and `property_type` (Villas have higher multipliers).
        Linear models model each feature additively, whereas Decision Trees and Random Forests split recursively on feature combinations, capturing spatial-structural interactions naturally without needing manual interaction terms.
        """)

    with st.expander("Q2: Why was model selection based on Cross-Validated R² instead of Test R²?"):
        st.markdown("""
        **Answer:** Selecting a model based on the test set score creates **data leakage** (the test set becomes part of the training/selection feedback loop).
        By using 5-Fold Cross-Validation strictly within the training split (`CV R2`), the held-out Test set remains completely unseen and unbiased for true generalizability verification.
        """)

    with st.expander("Q3: What is the mathematical difference between Ridge (L2) and Lasso (L1)?"):
        st.markdown(r"""
        **Answer:**
        - **Ridge ($L_2$ penalty):** Penalizes the sum of squared weights ($\alpha \sum w_j^2$). The derivative is proportional to $w_j$, shrinking weights toward zero but never reaching exact zero.
        - **Lasso ($L_1$ penalty):** Penalizes the sum of absolute weights ($\alpha \sum |w_j|$). The derivative is a constant sign function ($\pm \alpha$), driving uninformative weights strictly to zero, effectively acting as an automatic feature selector.
        """)

    with st.expander("Q4: Why do we report Adjusted R² alongside standard R²?"):
        st.markdown(r"""
        **Answer:** Standard $R^2$ never decreases when new predictor variables are added, even if the variables are pure random noise. Adjusted $R^2$ incorporates a penalty term based on the number of predictors ($p$) relative to sample size ($n$). If a new variable doesn't improve the model more than expected by chance, Adjusted $R^2$ decreases.
        """)

    with st.expander("Q5: What is the distinction between Covariance and Pearson Correlation?"):
        st.markdown(r"""
        **Answer:**
        - **Covariance:** $\mathrm{Cov}(X, Y) = \frac{\sum (x - \bar{x})(y - \bar{y})}{n - 1}$. It retains the product of the units of $X$ and $Y$ (e.g., $\text{sq.ft} \times ₹$), making its magnitude uninterpretable across different feature pairs.
        - **Pearson Correlation:** $r = \frac{\mathrm{Cov}(X, Y)}{s_X s_Y}$. By dividing by the product of standard deviations, it becomes a dimensionless standardized quantity bounded between $[-1, +1]$.
        """)

    with st.expander("Q6: When would you use Spearman rank correlation over Pearson?"):
        st.markdown(r"""
        **Answer:** Pearson correlation assumes continuous, bivariate-normal data and only detects linear relationships; it is highly vulnerable to outliers.
        Spearman rank correlation calculates Pearson's $r$ on the *ranked* values, making it robust against outliers and capable of detecting any monotonic relationship (even if curved or non-linear).
        """)

    with st.expander("Q7: How does Random Forest prevent overfitting compared to a single Decision Tree?"):
        st.markdown(r"""
        **Answer:** A single deep decision tree has low bias but high variance (memorizes training noise). Random Forest uses **Bagging (Bootstrap Aggregation)** and **Random Feature Subspace Selection**:
        1. It trains $B=100$ trees on bootstrap samples with replacement.
        2. At each split, only a random subset of $m \approx \sqrt{p}$ features is considered, decorrelating the trees.
        3. Averaging the predictions of 100 decorrelated trees reduces variance by a factor of $\approx B$ while preserving low bias.
        """)

    with st.expander("Q8: What are the key assumptions of Multiple Linear Regression?"):
        st.markdown(r"""
        **Answer:**
        1. **Linearity:** Linear relationship between independent predictors and target.
        2. **Homoscedasticity:** Constant variance of residuals across all predicted values.
        3. **Independence:** Residuals are uncorrelated (no autocorrelation).
        4. **Normality of Residuals:** Errors are normally distributed with zero mean.
        5. **No Multicollinearity:** Predictors are not collinear (low Variance Inflation Factor).
        """)

    with st.expander("Q9: What is the Central Limit Theorem and why is it important in ML?"):
        st.markdown(r"""
        **Answer:** The CLT states that the sampling distribution of the sample mean approaches a Normal distribution with variance $\sigma^2 / n$ as sample size $n$ increases, regardless of the underlying population distribution.
        It allows data scientists to construct valid confidence intervals and perform hypothesis tests on real-world datasets even when raw features are heavily skewed.
        """)

    with st.expander("Q10: Why did we scale features before Ridge/Lasso, but not for Random Forest?"):
        st.markdown(r"""
        **Answer:** Regularized regression penalties ($\alpha \sum w_j^2$ or $\alpha \sum |w_j|$) penalize large weights equally. If features have different scales (e.g. area in thousands vs bedrooms from 1-6), the weights for unscaled features will naturally have wildly different orders of magnitude, causing the regularizer to unfairly penalize small-unit features.
        Decision trees and Random Forests evaluate threshold splits monotonically along individual features one at a time ($x_j \le \theta$), so monotonic scale transformations have zero effect on split decisions.
        """)

# ---------------------------------------------------------------------------
# TAB 3: WEB SCRAPING MODULE
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Data Acquisition Pipeline: Web Scraping Modules")
    st.markdown("""
    The system supports automated data ingestion built using `requests`, `BeautifulSoup4`, and `lxml`.
    
    - **Assignment 1:** Scraping global population and demographic indicators from Worldometers.
    - **Assignment 2:** Scraping e-commerce pricing indices and structural catalogs.
    - **Assignment 3:** Parsing tabular web sources with automated HTML cleaning and error recovery.
    - **Assignment 4 & 5:** Multi-page pagination crawlers with rate limiting and polite request headers.
    """)
    st.code("""
# Example Web Scraping Ingestion Architecture (scraping_assignments.py)
import requests
from bs4 import BeautifulSoup
import pandas as pd

HEADERS = {"User-Agent": "Mozilla/5.0 (Data Science Research Scraper)"}

def fetch_market_listings(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    
    records = []
    for card in soup.select("div.property-card"):
        price = card.select_one(".price").get_text(strip=True)
        area = card.select_one(".area").get_text(strip=True)
        records.append({"price": price, "area": area})
    return pd.DataFrame(records)
    """, language="python")
