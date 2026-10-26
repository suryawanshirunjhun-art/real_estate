"""
Shared utilities, helpers, styling and data loaders for EstatePulse AI.
"""
import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

RANDOM_STATE = 42


@st.cache_resource
def load_bundle():
    """Loads the trained model and metadata bundle."""
    model_path = os.path.join(os.path.dirname(__file__), "best_model.joblib")
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None


@st.cache_data
def load_comparison_data():
    """Loads model benchmark results from outputs/model_comparison.csv."""
    csv_path = os.path.join(os.path.dirname(__file__), "outputs", "model_comparison.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None


@st.cache_data
def load_dataset(csv_path="data.csv"):
    """Loads the real or synthetic dataset."""
    full_path = os.path.join(os.path.dirname(__file__), csv_path)
    if os.path.exists(full_path):
        return pd.read_csv(full_path)
    
    # Synthetic dataset generator fallback matching train_models.py
    rng = np.random.default_rng(RANDOM_STATE)
    n = 1500
    city = rng.choice(["Nagpur", "Pune", "Mumbai", "Bengaluru", "Raipur"], n)
    ptype = rng.choice(["Apartment", "Villa", "Independent House"], n, p=[0.6, 0.15, 0.25])
    furnishing = rng.choice(["Unfurnished", "Semi-Furnished", "Furnished"], n)
    area = rng.normal(1200, 400, n).clip(300, 4000)
    bhk = np.clip((area / 450).round() + rng.integers(-1, 2, n), 1, 6)
    bath = np.clip(bhk + rng.integers(-1, 2, n), 1, 6)
    age = rng.integers(0, 30, n)
    dist = rng.uniform(0.5, 25, n)
    city_mult = pd.Series({
        "Nagpur": 4500, "Pune": 8000, "Mumbai": 16000,
        "Bengaluru": 9500, "Raipur": 4000
    })[city].values
    type_mult = pd.Series({"Apartment": 1.0, "Villa": 1.5, "Independent House": 1.2})[ptype].values
    furn_add = pd.Series({"Unfurnished": 0, "Semi-Furnished": 150000, "Furnished": 300000})[furnishing].values
    price = (area * city_mult * type_mult - age * 8000 - dist * 20000 + furn_add
             + bath * 50000 + rng.normal(0, 400000, n))
    
    df = pd.DataFrame(dict(
        city=city,
        property_type=ptype,
        furnishing=furnishing,
        area_sqft=area.round(0).astype(int),
        bedrooms=bhk.astype(int),
        bathrooms=bath.astype(int),
        age_years=age.astype(int),
        distance_to_center_km=dist.round(1),
        price=price.round(0).astype(int)
    ))
    return df


def format_inr(value):
    """Formats a number in Indian Lakhs/Crores notation."""
    if value is None or np.isnan(value):
        return "N/A"
    abs_val = abs(value)
    if abs_val >= 1e7:
        formatted = f"₹ {value / 1e7:.2f} Cr"
    elif abs_val >= 1e5:
        formatted = f"₹ {value / 1e5:.2f} L"
    else:
        formatted = f"₹ {value:,.0f}"
    return formatted


def render_dataframe(df, hide_index=True, **kwargs):
    """Renders dataframe with modern width stretch compatibility."""
    try:
        return st.dataframe(df, width="stretch", hide_index=hide_index, **kwargs)
    except (TypeError, ValueError):
        return st.dataframe(df, use_container_width=True, hide_index=hide_index, **kwargs)


def render_image(image, caption=None, **kwargs):
    """Renders image with modern width stretch compatibility."""
    try:
        return st.image(image, caption=caption, width="stretch", **kwargs)
    except (TypeError, ValueError):
        return st.image(image, caption=caption, use_container_width=True, **kwargs)


def render_button(label, container=None, **kwargs):
    """Renders button full-width without deprecation warnings."""
    target = container if container is not None else st
    try:
        return target.button(label, width="stretch", **kwargs)
    except (TypeError, ValueError):
        return target.button(label, use_container_width=True, **kwargs)


def apply_custom_styles():
    """Injects professional corporate styling compatible with both Light and Dark mode."""
    st.markdown("""
    <style>
    /* Metric Cards: Auto-adapt to Light / Dark Theme without washing out text */
    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        padding: 16px 20px !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #0284c7 !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.12) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stMetric"] label {
        color: inherit !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: inherit !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        color: inherit !important;
    }
    
    /* Executive Header Banner */
    .executive-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%) !important;
        color: #ffffff !important;
        padding: 28px 32px !important;
        border-radius: 12px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.18) !important;
    }
    .executive-banner h1 {
        color: #ffffff !important;
        font-size: 2.3rem !important;
        margin-bottom: 6px !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }
    .executive-banner p {
        color: #cbd5e1 !important;
        font-size: 1.05rem !important;
        margin: 0 !important;
    }

    /* Enterprise Badges */
    .badge-pill {
        display: inline-block !important;
        padding: 5px 14px !important;
        margin: 6px 8px 6px 0 !important;
        border-radius: 6px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        background-color: rgba(255, 255, 255, 0.14) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
    }
    .badge-live {
        background-color: #064e3b !important;
        color: #6ee7b7 !important;
        border: 1px solid #059669 !important;
    }
    
    /* Architectural Process Blocks: Dark & Light theme compatible */
    .arch-step {
        background-color: rgba(128, 128, 128, 0.08) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-left: 4px solid #0284c7 !important;
        padding: 14px 18px !important;
        border-radius: 6px !important;
        margin-bottom: 12px !important;
        color: inherit !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    }
    .arch-step strong {
        color: #0284c7 !important;
    }
    
    /* Market Insight Callout: Dark & Light theme compatible */
    .market-callout {
        background-color: rgba(2, 132, 199, 0.08) !important;
        border: 1px solid rgba(2, 132, 199, 0.25) !important;
        border-left: 4px solid #0284c7 !important;
        padding: 18px 20px !important;
        border-radius: 6px !important;
        margin: 18px 0 !important;
        color: inherit !important;
    }
    .market-callout h4, .market-callout strong {
        color: #0284c7 !important;
    }
    </style>
    """, unsafe_allow_html=True)
