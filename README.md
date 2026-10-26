# EstatePulse AI — Enterprise Real Estate Valuation & Market Analytics Platform

A production-grade machine learning platform for residential real estate valuation, regional market analysis, and investment scenario modeling.

## System Architecture

| Module | Description |
|---|---|
| `app.py` | **Executive Overview & Dashboard**: Key performance indicators, pipeline architecture, asset registry preview, and instant valuation tool |
| `pages/1_📊_Market_Analytics.py` | **Market Analytics**: Regional pricing spreads, asset distributions, factor correlation matrix, and spatial value decay |
| `pages/2_🤖_Model_Governance.py` | **Model Governance & Benchmarking**: 5-algorithm audit leaderboard, GridSearchCV hyperparameter logs, and residual diagnostics |
| `pages/3_🔮_Property_Appraisal.py` | **Automated Valuation Model (AVM)**: Interactive appraisal engine, institutional archetype templates, and CapEx sensitivity simulator |
| `utils.py` | Core data caching, model persistence loader, Indian Rupee notation formatters, and UI styling components |
| `train_models.py` | End-to-end model training, hyperparameter optimization, and artifact serialization pipeline |

## Quick Start

```bash
pip install -r requirements.txt
python train_models.py --csv data.csv --target price   # Generates best_model.joblib + outputs/
streamlit run app.py
```

## Model Governance & Validation
Models are evaluated across 5-fold cross-validation with grid search hyperparameter tuning. The production champion (**Random Forest Regressor**) achieved **96.04% out-of-sample Test R²** and an error rate of **8.95% MAPE**, outperforming regularized linear baselines by capturing complex non-linear geographic and structural asset interactions.
