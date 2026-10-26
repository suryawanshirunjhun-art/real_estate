"""
Shared utilities, helpers, styling and data loaders for the Streamlit presentation.
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


def apply_custom_styles():
    """Injects high-end presentation styling."""
    st.markdown("""
    <style>
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 14px 18px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    div[data-testid="stMetric"]:hover {
        border-color: #4361ee;
        transform: translateY(-2px);
        transition: all 0.2s ease-in-out;
    }
    
    /* Presentation Banner */
    .present-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 24px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);
    }
    .present-banner h1 {
        color: white !important;
        font-size: 2.2rem;
        margin-bottom: 6px;
        font-weight: 700;
    }
    .present-banner p {
        color: #e0e7ff !important;
        font-size: 1.05rem;
        margin: 0;
    }

    /* Badge Pills */
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        margin: 4px 6px 4px 0;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        background-color: #e0e7ff;
        color: #1e40af;
        border: 1px solid #bfdbfe;
    }
    .badge-success {
        background-color: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
    }
    
    /* Flowchart / Step Card */
    .pipeline-step {
        background: white;
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Callout Card */
    .insight-card {
        background-color: #f0fdf4;
        border-left: 5px solid #22c55e;
        padding: 16px;
        border-radius: 0 10px 10px 0;
        margin: 16px 0;
    }
    </style>
    """, unsafe_allow_html=True)
