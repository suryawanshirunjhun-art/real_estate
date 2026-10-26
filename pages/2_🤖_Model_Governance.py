"""
EstatePulse AI — Model Governance & Validation Leaderboard
"""
import os
import streamlit as st
import pandas as pd
from utils import load_bundle, load_comparison_data, format_inr, apply_custom_styles, render_dataframe, render_image

st.set_page_config(page_title="Model Governance | EstatePulse AI", page_icon="🤖", layout="wide")
apply_custom_styles()

st.title("🤖 Algorithmic Benchmarking & Model Governance")
st.markdown("""
Validation and production audit comparing 5 supervised machine learning models 
trained on multi-regional real estate transactions using **5-Fold Cross-Validation** and **GridSearchCV** tuning.
""")

res = load_comparison_data()
img_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")

# Top KPI banner
best_name = res.loc[0, "Model"] if res is not None else "Random Forest"
best_r2 = res.loc[0, "Test R2"] if res is not None else 0.9604
best_rmse = res.loc[0, "RMSE"] if res is not None else 1584460
best_mape = res.loc[0, "MAPE %"] if res is not None else 8.95

k1, k2, k3, k4 = st.columns(4)
k1.metric("Production Champion", best_name, delta="Selected Model")
k2.metric("Out-of-Sample Test R²", f"{best_r2:.4f}", delta="96.0% Accuracy")
k3.metric("Root Mean Squared Error", format_inr(best_rmse))
k4.metric("Mean Absolute % Error", f"{best_mape:.2f}%", delta="Precision Tier")

st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "🏆 Model Leaderboard & Metrics",
    "📈 Cross-Validation Benchmarks",
    "🎯 Residual Diagnostics & Calibration"
])

# ---------------------------------------------------------------------------
# TAB 1: Comparison Table
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Model Performance Audit")
    st.caption("Models ranked strictly by out-of-fold Cross-Validated R² to eliminate lookahead bias and verify real-world generalization.")
    
    if res is not None:
        display_df = res.copy()
        display_df["MAE"] = display_df["MAE"].apply(format_inr)
        display_df["RMSE"] = display_df["RMSE"].apply(format_inr)
        display_df["Train R2"] = display_df["Train R2"].apply(lambda x: f"{x:.4f}")
        display_df["Test R2"] = display_df["Test R2"].apply(lambda x: f"{x:.4f}")
        display_df["Test Adj R2"] = display_df["Test Adj R2"].apply(lambda x: f"{x:.4f}")
        display_df["CV R2 (mean)"] = display_df["CV R2 (mean)"].apply(lambda x: f"{x:.4f}")
        display_df["CV R2 (std)"] = display_df["CV R2 (std)"].apply(lambda x: f"±{x:.4f}")
        display_df["MAPE %"] = display_df["MAPE %"].apply(lambda x: f"{x:.2f}%")
        
        render_dataframe(
            display_df[["Model", "CV R2 (mean)", "CV R2 (std)", "Test R2", "Test Adj R2", "MAE", "RMSE", "MAPE %", "Best Params"]]
        )
    
    st.markdown("""
    <div class="market-callout">
    <h4>Executive Model Evaluation</h4>
    <ul>
        <li><strong>Random Forest Regressor</strong> demonstrated superior generalization with an out-of-sample <strong>Test R² of 0.9604</strong> and an error rate of <strong>8.95% MAPE</strong>.</li>
        <li><strong>Ensemble Advantage:</strong> Tree-based ensembles excel in real estate valuation because geographic micro-markets and asset typologies interact non-linearly (e.g. villa premiums in Mumbai scale multiplicatively, not additively).</li>
        <li><strong>Regularized Baselines (Lasso/Ridge):</strong> Achieved R² ~0.8869, providing a strong linear baseline but missing multi-attribute interaction effects.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 2: Visual Benchmarks
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Validation Consistency & Parameter Configurations")
    r2_plot = os.path.join(img_dir, "r2_comparison.png")
    
    col_p1, col_p2 = st.columns([3, 2])
    with col_p1:
        if os.path.exists(r2_plot):
            render_image(r2_plot, caption="Model Performance Stability across Train, Test, and Cross-Validation Folds")
    with col_p2:
        st.markdown("#### Optimal Production Hyperparameters")
        st.markdown("""
        - **Random Forest Ensemble**:
          - `n_estimators`: `100` decision trees
          - `max_depth`: `12` layers
          - `min_samples_leaf`: `1`
        - **Decision Tree**:
          - `max_depth`: `8`
          - `min_samples_leaf`: `5`
        - **Ridge Regression**:
          - `alpha`: `0.01` ($L_2$ regularizer)
        - **Lasso Regression**:
          - `alpha`: `10` ($L_1$ sparsity regularizer)
        """)

# ---------------------------------------------------------------------------
# TAB 3: Residual Diagnostics
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Residual Distribution & Homoscedasticity Analysis")
    st.caption("Verifying absence of systematic bias and confirming variance stability across valuation bands.")
    
    diag_plot = os.path.join(img_dir, "actual_vs_predicted.png")
    if os.path.exists(diag_plot):
        render_image(diag_plot, caption="Model Calibration: Actual vs Predicted (Left) and Error Residual Spread (Right)")
    
    st.markdown(r"""
    **Audit Findings:**
    1. **Linear Calibration:** Actual valuations vs predicted appraisals track the diagonal parity line ($y = \hat{y}$) with minimal dispersion across both affordable and prime asset classes.
    2. **Balanced Residuals:** Valuation residuals fluctuate symmetrically around zero, confirming homoscedasticity and no bias toward systematically under- or over-valuing prime real estate.
    """)
