"""
EstatePulse AI — Automated Valuation Model (AVM) & Investment Simulator
"""
import streamlit as st
import pandas as pd
from utils import load_bundle, format_inr, apply_custom_styles, render_button

st.set_page_config(page_title="Property Appraisal AVM | EstatePulse AI", page_icon="🔮", layout="wide")
apply_custom_styles()

st.title("🔮 Automated Valuation Model (AVM) & Investment Simulator")
st.markdown("""
Real-time property appraisal engine powered by the production **Random Forest Ensemble**.
Appraise residential assets across major urban submarkets, test institutional scenario templates, or model CapEx sensitivity.
""")

bundle = load_bundle()
if not bundle:
    st.error("Model bundle `best_model.joblib` not found. Please verify backend pipeline execution.")
    st.stop()

model, meta = bundle["model"], bundle["meta"]
target = meta["target"]
rmse = meta["metrics"]["RMSE"]

# ---------------------------------------------------------------------------
# INSTITUTIONAL SCENARIO PRESETS
# ---------------------------------------------------------------------------
st.subheader("📋 Market Archetype Presets")
preset_cols = st.columns(5)

PRESETS = {
    "🏙️ Metro Prime Villa": {
        "city": "Mumbai", "property_type": "Villa", "furnishing": "Furnished",
        "area_sqft": 2800, "bedrooms": 4, "bathrooms": 5, "age_years": 2, "distance_to_center_km": 3.0
    },
    "🌆 IT Corridor Flat": {
        "city": "Pune", "property_type": "Apartment", "furnishing": "Semi-Furnished",
        "area_sqft": 1350, "bedrooms": 3, "bathrooms": 2, "age_years": 4, "distance_to_center_km": 7.5
    },
    "🏢 Tech Hub High-Rise": {
        "city": "Bengaluru", "property_type": "Apartment", "furnishing": "Furnished",
        "area_sqft": 1500, "bedrooms": 3, "bathrooms": 3, "age_years": 1, "distance_to_center_km": 4.5
    },
    "🏡 Sub-Metro Estate": {
        "city": "Nagpur", "property_type": "Independent House", "furnishing": "Furnished",
        "area_sqft": 1600, "bedrooms": 3, "bathrooms": 3, "age_years": 8, "distance_to_center_km": 5.0
    },
    "🌾 Growth Corridor Unit": {
        "city": "Raipur", "property_type": "Apartment", "furnishing": "Unfurnished",
        "area_sqft": 850, "bedrooms": 2, "bathrooms": 1, "age_years": 10, "distance_to_center_km": 12.0
    }
}

if "current_preset" not in st.session_state:
    st.session_state["current_preset"] = "🏙️ Metro Prime Villa"

for idx, (p_name, p_data) in enumerate(PRESETS.items()):
    if render_button(p_name, container=preset_cols[idx]):
        st.session_state["current_preset"] = p_name
        for k, v in p_data.items():
            st.session_state[f"input_{k}"] = v

active_preset = PRESETS.get(st.session_state["current_preset"], PRESETS["🏙️ Metro Prime Villa"])

st.markdown("---")

# ---------------------------------------------------------------------------
# ASSET SPECIFICATION FORM
# ---------------------------------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📍 Geographic & Structural Specifications")
    city_val = st.selectbox(
        "Metropolitan Market",
        meta["cat_options"]["city"],
        index=meta["cat_options"]["city"].index(st.session_state.get("input_city", active_preset["city"]))
    )
    ptype_val = st.selectbox(
        "Asset Typology",
        meta["cat_options"]["property_type"],
        index=meta["cat_options"]["property_type"].index(st.session_state.get("input_property_type", active_preset["property_type"]))
    )
    furn_val = st.selectbox(
        "Interior Fitout Specification",
        meta["cat_options"]["furnishing"],
        index=meta["cat_options"]["furnishing"].index(st.session_state.get("input_furnishing", active_preset["furnishing"]))
    )
    area_min, area_max, _ = meta["num_ranges"]["area_sqft"]
    area_val = st.slider(
        "Carpet / Usable Area (sq.ft)",
        int(area_min), int(area_max),
        int(st.session_state.get("input_area_sqft", active_preset["area_sqft"])),
        step=50
    )

with col_right:
    st.markdown("### 📐 Physical Layout & Asset Age")
    bhk_min, bhk_max, _ = meta["num_ranges"]["bedrooms"]
    bhk_val = st.number_input(
        "Bedrooms (BHK)",
        int(bhk_min), int(bhk_max),
        int(st.session_state.get("input_bedrooms", active_preset["bedrooms"]))
    )
    bath_min, bath_max, _ = meta["num_ranges"]["bathrooms"]
    bath_val = st.number_input(
        "Bathrooms",
        int(bath_min), int(bath_max),
        int(st.session_state.get("input_bathrooms", active_preset["bathrooms"]))
    )
    age_min, age_max, _ = meta["num_ranges"]["age_years"]
    age_val = st.slider(
        "Building Age (Years since completion)",
        int(age_min), int(age_max),
        int(st.session_state.get("input_age_years", active_preset["age_years"]))
    )
    dist_min, dist_max, _ = meta["num_ranges"]["distance_to_center_km"]
    dist_val = st.slider(
        "Distance to Central Business District (km)",
        float(dist_min), float(dist_max),
        float(st.session_state.get("input_distance_to_center_km", active_preset["distance_to_center_km"])),
        step=0.5
    )

# Model inference
row_dict = {
    "city": city_val,
    "property_type": ptype_val,
    "furnishing": furn_val,
    "area_sqft": area_val,
    "bedrooms": bhk_val,
    "bathrooms": bath_val,
    "age_years": age_val,
    "distance_to_center_km": dist_val
}

input_df = pd.DataFrame([row_dict])[meta["num_features"] + meta["cat_features"]]
pred_price = float(model.predict(input_df)[0])
lower_bound = max(pred_price - rmse, 0)
upper_bound = pred_price + rmse
rate_per_sqft = pred_price / area_val if area_val > 0 else 0

st.markdown("---")

# ---------------------------------------------------------------------------
# APPRAISAL RESULT CARD
# ---------------------------------------------------------------------------
res_c1, res_c2, res_c3 = st.columns([2, 1, 1])

with res_c1:
    st.markdown("### 🏷️ Estimated Fair Market Valuation")
    st.markdown(f"<h1 style='color: #0284c7; font-size: 3.2rem; margin: 0; font-weight: 800;'>{format_inr(pred_price)}</h1>", unsafe_allow_html=True)
    st.caption(f"Exact Base Valuation: ₹ {pred_price:,.0f}")

with res_c2:
    st.metric("Valuation Confidence Band (±1 RMSE)", f"{format_inr(lower_bound)} - {format_inr(upper_bound)}")
    st.caption("Standard 68% statistical confidence interval")

with res_c3:
    st.metric("Implied Rate / sq.ft", f"₹ {rate_per_sqft:,.0f} / sqft")
    st.caption(f"Computed on {area_val} sq.ft area")

# ---------------------------------------------------------------------------
# SCENARIO & CAPEX SIMULATOR
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("🧪 Capital Expenditure & Value-Add Simulator")
st.caption("Model the financial impact of asset enhancements, renovations, and location adjustments in real time.")

w_col1, w_col2, w_col3 = st.columns(3)

# Capex: +200 sqft
df_area_up = input_df.copy()
df_area_up["area_sqft"] += 200
pred_area_up = float(model.predict(df_area_up)[0])
diff_area = pred_area_up - pred_price
w_col1.metric("Floorplate Expansion (+200 sq.ft)", format_inr(pred_area_up), delta=f"+{format_inr(diff_area)}")

# Capex: Furnishing upgrade
df_furn = input_df.copy()
df_furn["furnishing"] = "Furnished" if furn_val != "Furnished" else "Unfurnished"
pred_furn = float(model.predict(df_furn)[0])
diff_furn = pred_furn - pred_price
target_label = "Fitout: Upgrade to Fully Furnished" if furn_val != "Furnished" else "Fitout: Model as Unfurnished"
w_col2.metric(target_label, format_inr(pred_furn), delta=f"{format_inr(diff_furn)}")

# Capex: Proximity upgrade
df_closer = input_df.copy()
df_closer["distance_to_center_km"] = max(df_closer["distance_to_center_km"].values[0] - 3.0, 0.5)
pred_closer = float(model.predict(df_closer)[0])
diff_closer = pred_closer - pred_price
w_col3.metric("Transit / Core Proximity (3 km closer)", format_inr(pred_closer), delta=f"+{format_inr(diff_closer)}")
