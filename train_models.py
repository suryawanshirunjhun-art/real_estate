"""
Real Estate Price & Market Analysis - full regression pipeline
================================================================
Covers: load -> inspect -> EDA -> preprocessing -> correlation -> covariance
        -> train/test split -> Linear / Ridge / Lasso / Decision Tree / Random Forest
        -> metrics (R2, Adj R2, MAE, MSE, RMSE, MAPE, CV R2) -> model selection
        -> save best model with joblib.

Usage:
    python train_models.py --csv data.csv --target price
If --csv is missing, a synthetic real-estate dataset is generated so the
script always runs (replace with your own CSV for the real project).
For the "units demanded per store per month" version, use --target units_demanded.
"""
import argparse
import os
import warnings

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

warnings.filterwarnings("ignore")
OUT = "outputs"
os.makedirs(OUT, exist_ok=True)
RANDOM_STATE = 42


# ----------------------------------------------------------------------------
# 0. Data (synthetic fallback)
# ----------------------------------------------------------------------------
def make_synthetic(n=1500, seed=RANDOM_STATE):
    rng = np.random.default_rng(seed)
    city = rng.choice(["Nagpur", "Pune", "Mumbai", "Bengaluru", "Raipur"], n)
    ptype = rng.choice(["Apartment", "Villa", "Independent House"], n, p=[.6, .15, .25])
    furnishing = rng.choice(["Unfurnished", "Semi-Furnished", "Furnished"], n)
    area = rng.normal(1200, 400, n).clip(300, 4000)
    bhk = np.clip((area / 450).round() + rng.integers(-1, 2, n), 1, 6)
    bath = np.clip(bhk + rng.integers(-1, 2, n), 1, 6)
    age = rng.integers(0, 30, n)
    dist = rng.uniform(0.5, 25, n)
    city_mult = pd.Series({"Nagpur": 4500, "Pune": 8000, "Mumbai": 16000,
                           "Bengaluru": 9500, "Raipur": 4000})[city].values
    type_mult = pd.Series({"Apartment": 1.0, "Villa": 1.5, "Independent House": 1.2})[ptype].values
    furn_add = pd.Series({"Unfurnished": 0, "Semi-Furnished": 150000, "Furnished": 300000})[furnishing].values
    price = (area * city_mult * type_mult - age * 8000 - dist * 20000 + furn_add
             + bath * 50000 + rng.normal(0, 400000, n))
    df = pd.DataFrame(dict(city=city, property_type=ptype, furnishing=furnishing,
                           area_sqft=area.round(0), bedrooms=bhk, bathrooms=bath,
                           age_years=age, distance_to_center_km=dist.round(1),
                           price=price.round(0)))
    # inject some dirt to demonstrate cleaning
    for c in ["area_sqft", "age_years"]:
        df.loc[rng.choice(n, 25, replace=False), c] = np.nan
    df.loc[rng.choice(n, 20, replace=False), "city"] = np.nan
    df = pd.concat([df, df.sample(15, random_state=1)], ignore_index=True)  # duplicates
    return df


def main(csv, target):
    # ------------------------------------------------------------------------
    # 1. Load + inspect
    # ------------------------------------------------------------------------
    if csv and os.path.exists(csv):
        df = pd.read_csv(csv)
    else:
        print(f"[info] '{csv}' not found -> using synthetic real-estate data (target='price')")
        df = make_synthetic()
        target = "price"
    print("\n===== 1. DATASET OVERVIEW =====")
    print("First 5 rows:\n", df.head())
    print("\nLast 5 rows:\n", df.tail())
    print("\nShape (rows, cols):", df.shape)
    print("\nColumns:", list(df.columns))
    print("\nData types:\n", df.dtypes)
    print("\nInfo:")
    df.info()
    print("\nMissing values:\n", df.isnull().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    print("\nDescribe:\n", df.describe().T)

    # ------------------------------------------------------------------------
    # 2. EDA
    # ------------------------------------------------------------------------
    print("\n===== 2. EDA =====")
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()
    print("Numerical:", num_cols)
    print("Categorical:", cat_cols)

    for c in num_cols:  # distribution + box plot
        fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
        sns.histplot(df[c].dropna(), kde=True, ax=ax[0])
        ax[0].set_title(f"Distribution of {c}")
        sns.boxplot(x=df[c], ax=ax[1])
        ax[1].set_title(f"Box plot of {c}")
        plt.tight_layout()
        plt.savefig(f"{OUT}/dist_box_{c}.png", dpi=110)
        plt.close()
    for c in [x for x in num_cols if x != target]:  # scatter vs target
        plt.figure(figsize=(5, 4))
        sns.scatterplot(x=df[c], y=df[target], alpha=.5)
        plt.title(f"{c} vs {target}")
        plt.tight_layout()
        plt.savefig(f"{OUT}/scatter_{c}_vs_{target}.png", dpi=110)
        plt.close()
    for c in cat_cols:  # categorical vs target
        plt.figure(figsize=(7, 4))
        sns.boxplot(x=df[c], y=df[target])
        plt.xticks(rotation=30)
        plt.title(f"{target} by {c}")
        plt.tight_layout()
        plt.savefig(f"{OUT}/box_{c}_vs_{target}.png", dpi=110)
        plt.close()

    # ------------------------------------------------------------------------
    # 3. Pre-processing
    # ------------------------------------------------------------------------
    print("\n===== 3. PRE-PROCESSING =====")
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"Removed {before - len(df)} duplicate rows")
    df = df.dropna(subset=[target])
    # (median / mode imputation is done inside the pipeline to avoid leakage)
    features = [c for c in df.columns if c != target]
    num_feats = [c for c in features if c in num_cols]
    cat_feats = [c for c in features if c in cat_cols]

    # Encoded copy only for correlation / covariance display
    df_enc = df.copy()
    df_enc[num_feats] = df_enc[num_feats].fillna(df_enc[num_feats].median())
    for c in cat_feats:
        df_enc[c] = df_enc[c].fillna(df_enc[c].mode()[0])
    df_enc = pd.get_dummies(df_enc, columns=cat_feats, drop_first=True, dtype=int)

    # ------------------------------------------------------------------------
    # 4 & 5. Correlation + Covariance
    # ------------------------------------------------------------------------
    print("\n===== 4. CORRELATION =====")
    corr = df_enc.corr()
    print(corr[target].sort_values(ascending=False))
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=len(corr) <= 15, fmt=".2f", cmap="coolwarm", center=0)
    plt.title("Correlation heatmap")
    plt.tight_layout()
    plt.savefig(f"{OUT}/correlation_heatmap.png", dpi=110)
    plt.close()

    print("\n===== 5. COVARIANCE =====")
    cov = df_enc.cov()
    print(cov[target].sort_values(ascending=False))
    cov.to_csv(f"{OUT}/covariance_matrix.csv")
    corr.to_csv(f"{OUT}/correlation_matrix.csv")

    # ------------------------------------------------------------------------
    # 6. Train-test split
    # ------------------------------------------------------------------------
    X, y = df[features], df[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE)
    print(f"\n===== 6. SPLIT ===== train={X_train.shape}, test={X_test.shape}")

    def prep(scale):
        num_steps = [("imp", SimpleImputer(strategy="median"))]
        if scale:
            num_steps.append(("sc", StandardScaler()))
        return ColumnTransformer([
            ("num", Pipeline(num_steps), num_feats),
            ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                              ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_feats),
        ])

    # ------------------------------------------------------------------------
    # 7-11. Models (with GridSearchCV for tunable ones)
    # ------------------------------------------------------------------------
    models = {
        "Multiple Linear Regression": (Pipeline([("p", prep(True)), ("m", LinearRegression())]), {}),
        "Ridge Regression": (Pipeline([("p", prep(True)), ("m", Ridge())]),
                             {"m__alpha": [0.01, 0.1, 1, 10, 100]}),
        "Lasso Regression": (Pipeline([("p", prep(True)), ("m", Lasso(max_iter=20000))]),
                             {"m__alpha": [0.001, 0.01, 0.1, 1, 10]}),
        "Decision Tree": (Pipeline([("p", prep(False)), ("m", DecisionTreeRegressor(random_state=RANDOM_STATE))]),
                          {"m__max_depth": [3, 5, 8, 12, None], "m__min_samples_leaf": [1, 5, 10]}),
        "Random Forest": (Pipeline([("p", prep(False)), ("m", RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1))]),
                          {"m__n_estimators": [100, 200], "m__max_depth": [8, 12, None],
                           "m__min_samples_leaf": [1, 3]}),
    }

    def adj_r2(r2, n, p):
        return 1 - (1 - r2) * (n - 1) / (n - p - 1)

    def mape(a, b):
        a, b = np.asarray(a), np.asarray(b)
        mask = a != 0
        return np.mean(np.abs((a[mask] - b[mask]) / a[mask])) * 100

    rows, fitted = [], {}
    n_feat_enc = None
    for name, (pipe, grid) in models.items():
        if grid:
            gs = GridSearchCV(pipe, grid, cv=5, scoring="r2", n_jobs=-1)
            gs.fit(X_train, y_train)
            best, params = gs.best_estimator_, gs.best_params_
        else:
            best, params = pipe.fit(X_train, y_train), {}
        n_feat_enc = best.named_steps["p"].transform(X_train.head(2)).shape[1]
        pred_tr, pred = best.predict(X_train), best.predict(X_test)
        r2_te = r2_score(y_test, pred)
        cv = cross_val_score(best, X_train, y_train, cv=5, scoring="r2")
        rows.append({
            "Model": name,
            "Train R2": r2_score(y_train, pred_tr),
            "Test R2": r2_te,
            "Test Adj R2": adj_r2(r2_te, len(y_test), n_feat_enc),
            "CV R2 (mean)": cv.mean(),
            "CV R2 (std)": cv.std(),
            "MAE": mean_absolute_error(y_test, pred),
            "MSE": mean_squared_error(y_test, pred),
            "RMSE": np.sqrt(mean_squared_error(y_test, pred)),
            "MAPE %": mape(y_test, pred),
            "Best Params": str(params),
        })
        fitted[name] = (best, pred)
        print(f"{name:28s} test R2={r2_te:.4f}  RMSE={rows[-1]['RMSE']:.2f}  {params}")

    # ------------------------------------------------------------------------
    # 12. Model selection
    # ------------------------------------------------------------------------
    res = pd.DataFrame(rows).sort_values("CV R2 (mean)", ascending=False).reset_index(drop=True)
    res.to_csv(f"{OUT}/model_comparison.csv", index=False)
    print("\n===== 12. MODEL COMPARISON =====")
    print(res.drop(columns="Best Params").round(4).to_string(index=False))
    # Select by cross-validated R2 (not test R2) to avoid selecting on the test set
    best_name = res.loc[0, "Model"]
    best_model = fitted[best_name][0]
    print(f"\nBEST MODEL: {best_name}  (test R2 = {res.loc[0, 'Test R2']:.4f})")

    ax = res.set_index("Model")[["Train R2", "Test R2", "CV R2 (mean)"]].plot.bar(figsize=(9, 4.5))
    ax.set_title("R² comparison"); ax.set_ylabel("R²"); plt.xticks(rotation=25, ha="right")
    plt.tight_layout(); plt.savefig(f"{OUT}/r2_comparison.png", dpi=110); plt.close()

    pred = fitted[best_name][1]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    ax[0].scatter(y_test, pred, alpha=.5)
    lim = [min(y_test.min(), pred.min()), max(y_test.max(), pred.max())]
    ax[0].plot(lim, lim, "r--"); ax[0].set_xlabel("Actual"); ax[0].set_ylabel("Predicted")
    ax[0].set_title(f"Actual vs Predicted - {best_name}")
    ax[1].scatter(pred, y_test - pred, alpha=.5); ax[1].axhline(0, color="r", ls="--")
    ax[1].set_xlabel("Predicted"); ax[1].set_ylabel("Residual"); ax[1].set_title("Residual plot")
    plt.tight_layout(); plt.savefig(f"{OUT}/actual_vs_predicted.png", dpi=110); plt.close()

    # ------------------------------------------------------------------------
    # 13. Save best model (+ metadata that the Streamlit app needs)
    # ------------------------------------------------------------------------
    meta = {
        "target": target,
        "num_features": num_feats,
        "cat_features": cat_feats,
        "num_ranges": {c: (float(df[c].min()), float(df[c].max()), float(df[c].median()))
                       for c in num_feats},
        "cat_options": {c: sorted(df[c].dropna().unique().tolist()) for c in cat_feats},
        "best_model_name": best_name,
        "metrics": res.loc[0].drop("Best Params").to_dict(),
        "comparison": res.drop(columns="Best Params").to_dict("records"),
    }
    joblib.dump({"model": best_model, "meta": meta}, "best_model.joblib")
    print("\nSaved -> best_model.joblib   |   plots/tables in ./outputs/")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="data.csv")
    ap.add_argument("--target", default="price")
    a = ap.parse_args()
    main(a.csv, a.target)
