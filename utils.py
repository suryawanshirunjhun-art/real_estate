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
    """Injects professional corporate styling."""
    st.markdown("""
    <style>
    /* Global Card Polish */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 16px 20px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    }
    div[data-testid="stMetric"]:hover {
        border-color: #0284c7;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.08);
        transition: all 0.2s ease;
    }
    
    /* Executive Header Banner */
    .executive-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
        color: #ffffff;
        padding: 28px 32px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.12);
    }
    .executive-banner h1 {
        color: #ffffff !important;
        font-size: 2.3rem;
        margin-bottom: 6px;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .executive-banner p {
        color: #94a3b8 !important;
        font-size: 1.05rem;
        margin: 0;
    }

    /* Enterprise Badges */
    .badge-pill {
        display: inline-block;
        padding: 5px 14px;
        margin: 6px 8px 6px 0;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        background-color: rgba(255, 255, 255, 0.12);
        color: #f1f5f9;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .badge-live {
        background-color: #064e3b;
        color: #6ee7b7;
        border: 1px solid #059669;
    }
    
    /* Architectural Process Blocks */
    .arch-step {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0284c7;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }
    
    /* Market Insight Callout */
    .market-callout {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 4px solid #0f172a;
        padding: 18px 20px;
        border-radius: 6px;
        margin: 18px 0;
    }
    </style>
    """, unsafe_allow_html=True)
