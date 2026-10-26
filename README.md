# Real Estate Price & Market Analysis – Regression Project

Forecasts property price (or, with `--target units_demanded`, units demanded per store per month)
using Multiple Linear, Ridge, Lasso, Decision Tree and Random Forest regression.

## Files & Architecture
| File / Directory | Purpose |
|---|---|
| `app.py` | **Master Presentation Deck & Executive Overview** (KPI cards, architecture flow, dataset preview, instant valuation) |
| `pages/1_📊_Exploratory_Data_Analysis.py` | **EDA Dashboard**: distributions, city/type boxplots, correlation heatmap, covariance, scatter trends |
| `pages/2_🤖_Model_Benchmarking.py` | **ML Studio**: 5-model comparison leaderboard, GridSearchCV hyperparams, residual diagnostics |
| `pages/3_🔮_Interactive_Predictor.py` | **Live Predictor & What-If Simulator**: 5 city presets, sliders, confidence ranges (±1 RMSE), sensitivity testing |
| `pages/4_📐_Statistical_Inference.py` | **Statistical Labs**: Lab 6B/6C (Corr t-test), Practical 6 (ANOVA/Chi-square), CLT & Bootstrap CIs |
| `pages/5_📚_Theory_&_Viva_Guide.py` | **Viva Defense Guide**: KaTeX math formulas, L1 vs L2, top 10 viva questions & model answers |
| `utils.py` | Shared caching, data loaders, INR currency formatters, and custom presentation CSS styles |
| `train_models.py` | Steps 1-13: load, EDA, preprocessing, correlation, covariance, split, 5 models, **R² / Adj R² / MAE / MSE / RMSE / MAPE / CV R²**, selection, joblib save |
| `stats_labs.py` | Lab 6 (B, C), Practical 6, CLT / bootstrap exercises |
| `scraping_assignments.py` | Web scraping assignments 1-5 |
| `THEORY.md` | Theory notes for the labs |

## Run
```bash
pip install -r requirements.txt
python train_models.py --csv your_data.csv --target price   # creates best_model.joblib + outputs/
streamlit run app.py
```
If `your_data.csv` is absent, a synthetic real-estate dataset is used so the code still runs.

## Model selection
Models are tuned with 5-fold GridSearchCV (scoring = R²). The best model is chosen by
**cross-validated R²** (not test R²) so the test set stays unbiased; test R², Adj R², MAE, RMSE, MAPE
are reported for the chosen model. Results: `outputs/model_comparison.csv`.

## GitHub integration (step 15)
```bash
git init
printf "__pycache__/\n*.pyc\n.venv/\n" > .gitignore
git add .
git commit -m "Real estate regression project"
git branch -M main
git remote add origin https://github.com/<your-username>/real-estate-price-analysis.git
git push -u origin main
```
Create the empty repo on github.com first. Large `best_model.joblib` files (>100 MB) need Git LFS.
To deploy the app free: Streamlit Community Cloud -> connect the repo -> main file `app.py`.
