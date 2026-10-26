"""
EstatePulse AI — Market Analytics & Pricing Dynamics
"""
import os
import streamlit as st
import pandas as pd
from utils import load_dataset, format_inr, apply_custom_styles, render_dataframe, render_image

st.set_page_config(page_title="Market Analytics | EstatePulse AI", page_icon="📊", layout="wide")
apply_custom_styles()

st.title("📊 Real Estate Market Analytics & Asset Dynamics")
st.markdown("""
Macro and micro-level exploratory analysis across 5 major urban housing markets, 
evaluating square footage rates, geographic variance, structural characteristics, and asset depreciation trends.
""")

df = load_dataset()
img_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")

# Institutional KPI metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Monitored Asset Pool", f"{len(df):,} Properties")
m2.metric("Median Asset Valuation", format_inr(df['price'].median()))
m3.metric("Average Carpet Area", f"{df['area_sqft'].mean():,.0f} sq.ft")
m4.metric("Market Average Rate", f"₹ {df['price'].sum() / df['area_sqft'].sum():,.0f} / sq.ft")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "🏙️ Regional Pricing Breakdown",
    "📐 Asset Characteristics & Distributions",
    "🔗 Feature Correlation & Capital Drivers",
    "📉 Bivariate Market Elasticity"
])

# ---------------------------------------------------------------------------
# TAB 1: Regional & Asset Breakdown
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Regional Pricing Disparities & Typology Benchmarks")
    st.caption("Distributional spreads of property values across metropolitan corridors and asset classifications.")
    
    cat_dim = st.radio(
        "Segment Market By:",
        ["city", "property_type", "furnishing"],
        horizontal=True,
        format_func=lambda x: {"city": "Metro Market", "property_type": "Asset Typology", "furnishing": "Interior Specification"}[x]
    )
    
    cat_img = os.path.join(img_dir, f"box_{cat_dim}_vs_price.png")
    col_plot, col_stats = st.columns([3, 2])
    
    with col_plot:
        if os.path.exists(cat_img):
            render_image(cat_img, caption=f"Valuation Distribution by {cat_dim.replace('_', ' ').title()}")
    
    with col_stats:
        st.markdown(f"#### Valuation Summary ({cat_dim.replace('_', ' ').title()})")
        agg = df.groupby(cat_dim)["price"].agg(["count", "mean", "median", "std"]).reset_index()
        agg.columns = [cat_dim.replace('_', ' ').title(), "Volume", "Average Price", "Median Price", "Std Deviation"]
        agg["Average Price"] = agg["Average Price"].apply(format_inr)
        agg["Median Price"] = agg["Median Price"].apply(format_inr)
        agg["Std Deviation"] = agg["Std Deviation"].apply(format_inr)
        render_dataframe(agg)
        
        st.markdown("""
        <div class="market-callout">
        <strong>Strategic Takeaway:</strong>
        Tier-1 metropolitan nodes (Mumbai, Bengaluru) demonstrate substantial price-per-square-foot premiums driven by land constraints, while regional growth corridors (Pune, Nagpur, Raipur) offer favorable yield profiles for institutional capital.
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 2: Asset Characteristics & Distributions
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Asset Size, Age & Volatility Profiles")
    st.caption("Density profiles and dispersion bounds across key physical variables.")
    
    feat_sel = st.selectbox(
        "Select Asset Attribute:",
        ["price", "area_sqft", "bedrooms", "bathrooms", "age_years", "distance_to_center_km"],
        format_func=lambda x: x.replace("_", " ").title()
    )
    
    feat_img = os.path.join(img_dir, f"dist_box_{feat_sel}.png")
    c_left, c_right = st.columns([3, 2])
    
    with c_left:
        if os.path.exists(feat_img):
            render_image(feat_img, caption=f"Empirical Spread & Quartile Bounds for {feat_sel.replace('_', ' ').title()}")
    
    with c_right:
        st.markdown(f"#### Metric Profiling: `{feat_sel}`")
        s = df[feat_sel].describe()
        stats_df = pd.DataFrame({
            "Quartile / Statistic": ["Total Records", "Mean", "Std Deviation", "Minimum", "25th Percentile", "Median (50th)", "75th Percentile", "Maximum", "Interquartile Range"],
            "Value": [
                f"{s['count']:.0f}",
                f"{s['mean']:,.2f}",
                f"{s['std']:,.2f}",
                f"{s['min']:,.2f}",
                f"{s['25%']:,.2f}",
                f"{s['50%']:,.2f}",
                f"{s['75%']:,.2f}",
                f"{s['max']:,.2f}",
                f"{s['75%'] - s['25%']:,.2f}"
            ]
        })
        render_dataframe(stats_df)

# ---------------------------------------------------------------------------
# TAB 3: Correlation & Capital Drivers
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Multivariate Correlation & Capital Drivers")
    st.markdown("""
    Correlation analysis evaluates the strength and directional dependency between structural asset characteristics, 
    spatial location coefficients, and final market valuations.
    """)
    
    corr_img = os.path.join(img_dir, "correlation_heatmap.png")
    if os.path.exists(corr_img):
        render_image(corr_img, caption="Correlation Matrix across One-Hot Encoded Features and Spatial Indicators")
        
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.markdown("#### Key Positive Drivers")
        st.markdown("""
        - **Carpet Area (sq.ft)**: $r = +0.51$ — Primary linear determinant of baseline property valuation.
        - **Mumbai Metro Market**: $r = +0.68$ — Substantial regional capital premium.
        - **Bedrooms / Unit Capacity**: $r = +0.36$ — Expands potential household footprint.
        """)
    with c_m2:
        st.markdown("#### Discounting Factors")
        st.markdown("""
        - **Raipur & Nagpur Baselines**: $r = -0.41, -0.36$ — Moderate tier-2 pricing baseline.
        - **Distance from CBD**: $r = -0.04$ — Gradual spatial discount with suburban transit radius.
        - **Structural Age**: $r = -0.01$ — Measured physical depreciation schedule.
        """)

# ---------------------------------------------------------------------------
# TAB 4: Bivariate Market Elasticity
# ---------------------------------------------------------------------------
with tab4:
    st.subheader("Bivariate Value Elasticity")
    scatter_target = st.selectbox(
        "Evaluate Price Elasticity Against:",
        ["area_sqft", "distance_to_center_km", "age_years", "bedrooms", "bathrooms"],
        format_func=lambda x: f"Price vs {x.replace('_', ' ').title()}"
    )
    
    scat_img = os.path.join(img_dir, f"scatter_{scatter_target}_vs_price.png")
    if os.path.exists(scat_img):
        render_image(scat_img, caption=f"Price Elasticity Trend: {scatter_target.replace('_', ' ').title()}")
