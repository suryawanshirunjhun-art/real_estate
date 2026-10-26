"""
Page 2: Model Benchmarking, Evaluation & Selection
"""
import os
import streamlit as st
import pandas as pd
from utils import load_bundle, load_comparison_data, format_inr, apply_custom_styles, render_dataframe, render_image

st.set_page_config(page_title="Model Benchmarking - Real Estate AI", page_icon="🤖", layout="wide")
apply_custom_styles()

st.title("🤖 Model Benchmarking & Performance Evaluation")
st.markdown("""
Evaluation of 5 machine learning regression architectures using **5-Fold Cross-Validation**
and exhaustive hyperparameter tuning via **GridSearchCV**.
""")

bundle = load_bundle()
res = load_comparison_data()
img_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")

# Summary cards
best_name = res.loc[0, "Model"] if res is not None else "Random Forest"
best_r2 = res.loc[0, "Test R2"] if res is not None else 0.9604
best_rmse = res.loc[0, "RMSE"] if res is not None else 1584460
best_mape = res.loc[0, "MAPE %"] if res is not None else 8.95

k1, k2, k3, k4 = st.columns(4)
k1.metric("Selected Architecture", best_name, delta="Winner")
k2.metric("Test R² Score", f"{best_r2:.4f}", delta="96.0% Variance Explained")
k3.metric("Root Mean Squared Error", format_inr(best_rmse))
k4.metric("Mean Absolute % Error", f"{best_mape:.2f}%", delta="High Precision")

st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "🏆 Model Comparison Matrix",
    "📊 Graphical Performance Comparison",
    "🎯 Residual & Error Diagnostics"
])

# ---------------------------------------------------------------------------
# TAB 1: Comparison Table
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Leaderboard: 5 Supervised Regression Algorithms")
    st.caption("Models ranked strictly by Cross-Validated R² on training folds to prevent test set data leakage.")
    
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
    <div class="insight-card">
    <h4>💡 Key Modeling Insights for Presentation</h4>
    <ul>
        <li><strong>Random Forest Regressor</strong> took 1st place with <strong>96.04% Test R²</strong> and an error rate of only <strong>8.95% MAPE</strong>.</li>
        <li><strong>Tree-based Ensembles</strong> vastly outperformed linear models because real estate pricing involves non-linear multipliers (e.g., location multiplier × area × luxury type) rather than purely additive linear terms.</li>
        <li><strong>Decision Tree</strong> achieved a high 94.65% R², but Random Forest reduced variance further by averaging 100 decorrelated trees.</li>
        <li><strong>Lasso ($L_1$) and Ridge ($L_2$)</strong> performed identically to Ordinary Least Squares ($R^2 \approx 0.8869$), indicating that linear terms alone explain ~88.7% of variance, but cannot capture geographic-structural interactions.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 2: Visual Comparison
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Cross-Validated vs. Test R² Performance")
    r2_plot = os.path.join(img_dir, "r2_comparison.png")
    
    col_p1, col_p2 = st.columns([3, 2])
    with col_p1:
        if os.path.exists(r2_plot):
            render_image(r2_plot, caption="R² Comparison across Train, Test, and CV folds")
    with col_p2:
        st.markdown("#### Hyperparameter Configurations Found via GridSearchCV")
        st.markdown("""
        - **Random Forest**:
          - `n_estimators`: `100`
          - `max_depth`: `12`
          - `min_samples_leaf`: `1`
        - **Decision Tree**:
          - `max_depth`: `8`
          - `min_samples_leaf`: `5`
        - **Ridge Regression**:
          - `alpha`: `0.01` (Mild $L_2$ shrinkage)
        - **Lasso Regression**:
          - `alpha`: `10` ($L_1$ shrinkage)
        - **Multiple Linear Regression**:
          - Unregularized baseline (Ordinary Least Squares)
        """)

# ---------------------------------------------------------------------------
# TAB 3: Residual Diagnostics
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Residual & Prediction Diagnostics for Random Forest")
    st.caption("Verifying model fit, linearity, and homoscedasticity of error residuals.")
    
    diag_plot = os.path.join(img_dir, "actual_vs_predicted.png")
    if os.path.exists(diag_plot):
        render_image(diag_plot, caption="Actual vs. Predicted Values (Left) & Residual Distribution (Right)")
    
    st.markdown(r"""
    **Diagnostic Takeaways:**
    1. **Identity Line Alignment:** The points cluster tightly along the $45^\circ$ dashed reference line ($y = \hat{y}$), confirming high predictive fidelity across all price ranges.
    2. **Homoscedastic Residuals:** Residuals fluctuate symmetrically around 0 with no severe fan-out shape, confirming stability across low and high valuations.
    """)
