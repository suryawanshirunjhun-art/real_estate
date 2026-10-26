"""
Page 3: Live Real Estate Price Predictor & What-If Simulator
"""
import streamlit as st
import pandas as pd
from utils import load_bundle, format_inr, apply_custom_styles

st.set_page_config(page_title="Price Predictor - Real Estate AI", page_icon="🔮", layout="wide")
apply_custom_styles()

st.title("🔮 Interactive Real Estate Valuation Engine")
st.markdown("""
Real-time property appraisal powered by the optimized **Random Forest Regressor** (`best_model.joblib`).
Test realistic market configurations, explore preset scenarios, or run sensitivity what-if simulations.
""")

bundle = load_bundle()
if not bundle:
    st.error("Model bundle `best_model.joblib` not found. Please run `python train_models.py` first.")
    st.stop()

model, meta = bundle["model"], bundle["meta"]
target = meta["target"]
rmse = meta["metrics"]["RMSE"]

# ---------------------------------------------------------------------------
# PRESET SELECTOR FOR PRESENTATION
# ---------------------------------------------------------------------------
st.subheader("⚡ Quick Presentation Demo Presets")
preset_cols = st.columns(5)

PRESETS = {
    "🏙️ Mumbai Luxury Villa": {
        "city": "Mumbai", "property_type": "Villa", "furnishing": "Furnished",
        "area_sqft": 2800, "bedrooms": 4, "bathrooms": 5, "age_years": 2, "distance_to_center_km": 3.0
    },
    "🌆 Pune Techie Flat": {
        "city": "Pune", "property_type": "Apartment", "furnishing": "Semi-Furnished",
        "area_sqft": 1350, "bedrooms": 3, "bathrooms": 2, "age_years": 4, "distance_to_center_km": 7.5
    },
    "🏡 Nagpur Family House": {
        "city": "Nagpur", "property_type": "Independent House", "furnishing": "Furnished",
        "area_sqft": 1600, "bedrooms": 3, "bathrooms": 3, "age_years": 8, "distance_to_center_km": 5.0
    },
    "🏢 Bengaluru Modern Condo": {
        "city": "Bengaluru", "property_type": "Apartment", "furnishing": "Furnished",
        "area_sqft": 1500, "bedrooms": 3, "bathrooms": 3, "age_years": 1, "distance_to_center_km": 4.5
    },
    "🌾 Raipur Starter Home": {
        "city": "Raipur", "property_type": "Apartment", "furnishing": "Unfurnished",
        "area_sqft": 850, "bedrooms": 2, "bathrooms": 1, "age_years": 10, "distance_to_center_km": 12.0
    }
}

# Session state initialization for form inputs
if "current_preset" not in st.session_state:
    st.session_state["current_preset"] = "🏙️ Mumbai Luxury Villa"

for idx, (p_name, p_data) in enumerate(PRESETS.items()):
    if preset_cols[idx].button(p_name, use_container_width=True):
        st.session_state["current_preset"] = p_name
        for k, v in p_data.items():
            st.session_state[f"input_{k}"] = v

# Load initial values
active_preset = PRESETS.get(st.session_state["current_preset"], PRESETS["🏙️ Mumbai Luxury Villa"])

st.markdown("---")

# ---------------------------------------------------------------------------
# PROPERTY INPUT FORM
# ---------------------------------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📍 Location & Structural Attributes")
    city_val = st.selectbox(
        "City / Market",
        meta["cat_options"]["city"],
        index=meta["cat_options"]["city"].index(st.session_state.get("input_city", active_preset["city"]))
    )
    ptype_val = st.selectbox(
        "Property Type",
        meta["cat_options"]["property_type"],
        index=meta["cat_options"]["property_type"].index(st.session_state.get("input_property_type", active_preset["property_type"]))
    )
    furn_val = st.selectbox(
        "Furnishing Status",
        meta["cat_options"]["furnishing"],
        index=meta["cat_options"]["furnishing"].index(st.session_state.get("input_furnishing", active_preset["furnishing"]))
    )
    area_min, area_max, _ = meta["num_ranges"]["area_sqft"]
    area_val = st.slider(
        "Carpet / Built-up Area (sq.ft)",
        int(area_min), int(area_max),
        int(st.session_state.get("input_area_sqft", active_preset["area_sqft"])),
        step=50
    )

with col_right:
    st.markdown("### 📐 Layout & Physical Condition")
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
        "Property Age (Years)",
        int(age_min), int(age_max),
        int(st.session_state.get("input_age_years", active_preset["age_years"]))
    )
    dist_min, dist_max, _ = meta["num_ranges"]["distance_to_center_km"]
    dist_val = st.slider(
        "Distance to City Center (km)",
        float(dist_min), float(dist_max),
        float(st.session_state.get("input_distance_to_center_km", active_preset["distance_to_center_km"])),
        step=0.5
    )

# Prepare inference payload
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
# VALUATION RESULT CARD
# ---------------------------------------------------------------------------
res_c1, res_c2, res_c3 = st.columns([2, 1, 1])

with res_c1:
    st.markdown("### 🏷️ Estimated Market Valuation")
    st.markdown(f"<h1 style='color: #1e3a8a; font-size: 3.2rem; margin: 0;'>{format_inr(pred_price)}</h1>", unsafe_allow_html=True)
    st.caption(f"Exact Value: ₹ {pred_price:,.0f}")

with res_c2:
    st.metric("Expected Range (±1 RMSE)", f"{format_inr(lower_bound)} - {format_inr(upper_bound)}")
    st.caption("68% confidence prediction interval")

with res_c3:
    st.metric("Estimated Price / sq.ft", f"₹ {rate_per_sqft:,.0f} / sqft")
    st.caption(f"Based on {area_val} sq.ft area")

# ---------------------------------------------------------------------------
# WHAT-IF SENSITIVITY SIMULATOR
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("🧪 Live 'What-If' Scenario Analysis")
st.caption("Understand how alterations to property characteristics immediately affect the valuation.")

w_col1, w_col2, w_col3 = st.columns(3)

# What if area +200 sqft
df_area_up = input_df.copy()
df_area_up["area_sqft"] += 200
pred_area_up = float(model.predict(df_area_up)[0])
diff_area = pred_area_up - pred_price
w_col1.metric("Add +200 sq.ft Space", format_inr(pred_area_up), delta=f"+{format_inr(diff_area)}")

# What if furnished
df_furn = input_df.copy()
df_furn["furnishing"] = "Furnished" if furn_val != "Furnished" else "Unfurnished"
pred_furn = float(model.predict(df_furn)[0])
diff_furn = pred_furn - pred_price
target_label = "Switch to Furnished" if furn_val != "Furnished" else "Switch to Unfurnished"
w_col2.metric(target_label, format_inr(pred_furn), delta=f"{format_inr(diff_furn)}")

# What if moved 3km closer
df_closer = input_df.copy()
df_closer["distance_to_center_km"] = max(df_closer["distance_to_center_km"].values[0] - 3.0, 0.5)
pred_closer = float(model.predict(df_closer)[0])
diff_closer = pred_closer - pred_price
w_col3.metric("Move 3 km Closer to Center", format_inr(pred_closer), delta=f"+{format_inr(diff_closer)}")
