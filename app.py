"""
🏠 Real Estate Valuation & Market Intelligence Platform
======================================================
Master Presentation Deck & Executive Summary Dashboard.
"""
import streamlit as st
import pandas as pd
from utils import (
    load_bundle,
    load_dataset,
    load_comparison_data,
    format_inr,
    apply_custom_styles,
    render_dataframe
)

# Page configuration
st.set_page_config(
    page_title="Executive Overview - Real Estate AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()

# Load resources
bundle = load_bundle()
res = load_comparison_data()
df = load_dataset()

# ---------------------------------------------------------------------------
# HERO PRESENTATION BANNER
# ---------------------------------------------------------------------------
st.markdown("""
<div class="present-banner">
    <h1>🏠 Real Estate Price Intelligence & Market Analysis</h1>
    <p>An End-to-End Applied Machine Learning System: Automated Preprocessing, 5-Fold Cross-Validation, Algorithm Benchmarking & Statistical Inference</p>
    <div style="margin-top: 14px;">
        <span class="badge-pill">Python 3.12</span>
        <span class="badge-pill">Scikit-Learn</span>
        <span class="badge-pill">Streamlit Multi-Page</span>
        <span class="badge-pill badge-success">🏆 Random Forest Winner (R² = 0.96)</span>
        <span class="badge-pill">5-Fold GridSearchCV</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SIDEBAR PRESENTATION GUIDE
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/real-estate.png", width=70)
    st.markdown("### 🧭 Presentation Navigation")
    st.info("""
    Use the **Pages menu above** to navigate through each phase of the presentation:
    - **1 📊 Exploratory Data Analysis (EDA)**
    - **2 🤖 Model Benchmarking**
    - **3 🔮 Interactive Predictor**
    - **4 📐 Statistical Inference & Labs**
    - **5 📚 Theory & Viva Guide**
    """)
    st.markdown("---")
    st.markdown("#### 👨‍🏫 Presenter Quick Info")
    st.caption("**Domain:** PropTech & Real Estate Econometrics")
    st.caption("**Primary Goal:** Forecast property valuation & analyze feature elasticity")
    st.caption("**Status:** Production Model Ready")

# ---------------------------------------------------------------------------
# EXECUTIVE KPI SUMMARY CARDS
# ---------------------------------------------------------------------------
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric("Selected Model", "Random Forest", "GridSearch Winner")
kpi2.metric("Test R² Score", "96.04%", "+7.3% vs Linear")
kpi3.metric("Cross-Val R²", "95.09%", "± 0.021 StDev")
kpi4.metric("Mean Abs Error (MAE)", "₹ 7.83 Lakhs", "Avg absolute error")
kpi5.metric("MAPE %", "8.95%", "High accuracy (<9%)")

st.markdown("---")

# ---------------------------------------------------------------------------
# TWO COLUMN LAYOUT: PIPELINE & DATASET
# ---------------------------------------------------------------------------
col_arch, col_data = st.columns([1, 1])

with col_arch:
    st.subheader("🛠️ End-to-End Machine Learning Pipeline")
    st.markdown("""
    <div class="pipeline-step">
        <strong>1. Raw Ingestion & Profiling:</strong> 1,500+ records across 5 metropolitan regions (Mumbai, Bengaluru, Pune, Nagpur, Raipur).
    </div>
    <div class="pipeline-step">
        <strong>2. Robust Preprocessing:</strong> Median imputation for numeric features, modal imputation for categories, and One-Hot Encoding via <code>ColumnTransformer</code>.
    </div>
    <div class="pipeline-step">
        <strong>3. Rigorous Cross-Validation:</strong> 80/20 train/test split. 5-Fold Stratified Cross-Validation on training split to eliminate data leakage.
    </div>
    <div class="pipeline-step">
        <strong>4. 5-Model Hyperparameter Tuning:</strong> Linear Regression, Ridge ($L_2$), Lasso ($L_1$), Decision Trees, and Random Forest evaluated with GridSearchCV.
    </div>
    <div class="pipeline-step">
        <strong>5. Model Selection & Persistence:</strong> Best model selected via <strong>CV R²</strong>; serialized using <code>joblib</code> with metadata.
    </div>
    <div class="pipeline-step">
        <strong>6. Interactive Deployment:</strong> Production Streamlit web application with real-time inference and sensitivity analysis.
    </div>
    """, unsafe_allow_html=True)

with col_data:
    st.subheader("📋 Dataset Overview & Structural Summary")
    st.caption(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} features | Target: `price`")
    render_dataframe(df.head(6))
    
    st.markdown("""
    **Core Feature Spectrum:**
    - **Continuous Numerical:** Living Area (`area_sqft`), Property Age (`age_years`), Distance to CBD (`distance_to_center_km`).
    - **Discrete Numerical:** Bedrooms (`bedrooms`), Bathrooms (`bathrooms`).
    - **Nominal Categorical:** Market City (`city`), Property Type (`property_type`), Furnishing Grade (`furnishing`).
    """)

st.markdown("---")

# ---------------------------------------------------------------------------
# PRESENTATION MODULES ROADMAP
# ---------------------------------------------------------------------------
st.subheader("🚀 Presentation Modules At A Glance")

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""
    #### 1️⃣ [EDA & Visualizations](1_📊_Exploratory_Data_Analysis)
    - Target price distribution & skewness
    - Inter-city boxplot pricing dynamics
    - Pearson correlation heatmap
    - Bivariate feature elasticity scatters
    """)

with m2:
    st.markdown("""
    #### 2️⃣ [Model Evaluation](2_🤖_Model_Benchmarking)
    - 5 Supervised models compared
    - Train R², Test R², Adj R², CV R²
    - Error metrics: MAE, MSE, RMSE, MAPE
    - Residual homoscedasticity diagnostics
    """)

with m3:
    st.markdown(r"""
    #### 3️⃣ [Live Price Predictor](3_🔮_Interactive_Predictor)
    - 5 Instant presentation demo presets
    - Real-time parameter sliders
    - Price confidence bounds ($\pm 1$ RMSE)
    - "What-If" Sensitivity Simulator
    """)

m4, m5, m6 = st.columns(3)

with m4:
    st.markdown("""
    #### 4️⃣ [Statistical Labs](4_📐_Statistical_Inference)
    - Lab 6B/6C: Covariance & Correlation test
    - Practical 6: Chi-Square & ANOVA tests
    - Central Limit Theorem (CLT) simulator
    - Bootstrap resampling confidence intervals
    """)

with m5:
    st.markdown("""
    #### 5️⃣ [Viva & Theory Prep](5_📚_Theory_&_Viva_Guide)
    - Complete mathematical formulation guide
    - $L_1$ (Lasso) vs $L_2$ (Ridge) shrinkage math
    - Top 10 viva defense questions & answers
    - Web scraping data pipelines overview
    """)

with m6:
    st.markdown("""
    #### 💾 Model Artifacts
    - Model binary: `best_model.joblib`
    - Benchmark table: `outputs/model_comparison.csv`
    - Visual plots: `outputs/*.png`
    - Academic lab results: `outputs_stats/*.png`
    """)

st.markdown("---")

# ---------------------------------------------------------------------------
# QUICK PREDICTION DEMO WIDGET (INLINE HOME DEMO)
# ---------------------------------------------------------------------------
st.subheader("⚡ Quick Prediction Snapshot (On Home Page)")
st.caption("Perform an instant prediction directly from the overview or visit the **Interactive Predictor** page for presets and what-if simulation.")

if bundle:
    model, meta = bundle["model"], bundle["meta"]
    quick_cols = st.columns(4)
    q_city = quick_cols[0].selectbox("City", meta["cat_options"]["city"], key="q_city")
    q_type = quick_cols[1].selectbox("Property Type", meta["cat_options"]["property_type"], key="q_type")
    q_area = quick_cols[2].number_input("Area (sq.ft)", 300, 4000, 1200, step=50, key="q_area")
    q_furn = quick_cols[3].selectbox("Furnishing", meta["cat_options"]["furnishing"], key="q_furn")
    
    # Defaults for other attributes
    sample_row = pd.DataFrame([{
        "city": q_city,
        "property_type": q_type,
        "furnishing": q_furn,
        "area_sqft": q_area,
        "bedrooms": 3,
        "bathrooms": 2,
        "age_years": 5,
        "distance_to_center_km": 6.0
    }])[meta["num_features"] + meta["cat_features"]]
    
    val = float(model.predict(sample_row)[0])
    st.success(f"Estimated Price: **{format_inr(val)}** (Exact: ₹ {val:,.0f})")
