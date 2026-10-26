# RAMDEOBABA UNIVERSITY, NAGPUR
## DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING
### B.Tech. CSE (Artificial Intelligence and Data Science) (AIDS)
**SEMESTER V — SI LAB PROJECT REPORT**

---

# Real Estate Price Prediction and Market Valuation Analysis Using Machine Learning

**Submitted by:**
- **Student Name:** Runjhun Suryawanshi
- **Roll No.:** 18
- **Enrollment No.:** [Insert Enrollment Number Here]
- **Academic Year:** 2026–27

---

## 1. PROJECT OBJECTIVE
The primary objective of this project is to develop an automated, end-to-end Machine Learning regression and market analysis system (**EstatePulse AI**) to forecast residential real estate prices based on structural, spatial, and geographic attributes.

**Key Objectives:**
- Load, inspect, and perform exploratory data analysis (EDA) on multi-metro residential housing transaction data.
- Design an automated data preprocessing pipeline handling missing value imputation, duplicate removal, categorical encoding, and feature scaling.
- Train and tune 5 distinct regression architectures: Multiple Linear Regression, Ridge Regression ($L_2$), Lasso Regression ($L_1$), Decision Tree Regressor, and Random Forest Regressor.
- Evaluate model performance across statistical metrics including $R^2$, Adjusted $R^2$, Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), Mean Absolute Percentage Error (MAPE), and 5-Fold Cross-Validation $R^2$.
- Select the optimal model using cross-validation to prevent data leakage and ensure generalizability.
- Deploy an interactive multi-page Graphical User Interface (GUI) using Streamlit for real-time property valuation and "What-If" CapEx sensitivity simulation.

---

## 2. INTRODUCTION
Real estate valuation has traditionally relied on subjective manual appraisals, physical broker surveys, or rigid linear metrics (e.g., fixed price-per-square-foot rates). These traditional methodologies frequently fail because property pricing involves complex non-linear interactions between physical features (carpet area, bedrooms), structural condition (building age, interior finish), and spatial factors (city-level economic baselines, transit distance to central business districts).

Machine learning offers a rigorous, data-driven alternative by modeling these non-linear feature interactions simultaneously. This project provides a production-grade Automated Valuation Model (AVM) capable of sub-second property appraisal and market scenario modeling.

### 2.1 Problem Statement
To accurately estimate the fair market valuation of residential properties given multi-dimensional physical and geographic inputs, minimizing forecasting error (RMSE and MAPE) and mitigating overfitting through rigorous cross-validation.

### 2.2 Scope of the Project
- **Included Functions:** Multi-metro dataset ingestion, statistical profiling, distribution and correlation analysis, automated cleaning and One-Hot encoding, 5-fold cross-validation grid search, residual diagnostics, and an interactive Streamlit GUI with preset archetypes and live sensitivity testing.
- **Limitations:** Model valuations assume standard economic market conditions; extreme localized macro-economic anomalies or subjective architectural prestige are outside the numerical feature space.

---

## 3. PROJECT METHODOLOGY

### 3.1 Dataset Loading and Exploration
- **Dataset Name / Source:** Indian Metro Residential Housing Dataset (compiled from housing transaction benchmarks across major Indian urban corridors).
- **Dimensions:** 1,515 observations, 9 features (8 independent predictors + 1 continuous target).
- **Target Variable:** `price` (Continuous numerical, in Indian Rupees, ranging from ₹15 Lakhs to ₹7.5+ Crores).
- **Input Features & Data Types:**
  - `area_sqft` (float/int): Carpet / living area (300 to 4,000 sq.ft)
  - `bedrooms` (int): Number of bedrooms (1 to 6 BHK)
  - `bathrooms` (int): Number of bathrooms (1 to 6)
  - `age_years` (int): Property age (0 to 30 years)
  - `distance_to_center_km` (float): Distance to Central Business District (0.5 to 25 km)
  - `city` (object): Metropolitan market (`Mumbai`, `Bengaluru`, `Pune`, `Nagpur`, `Raipur`)
  - `property_type` (object): Asset typology (`Apartment`, `Independent House`, `Villa`)
  - `furnishing` (object): Interior fitout (`Unfurnished`, `Semi-Furnished`, `Furnished`)

### 3.2 Data Preprocessing
- **Handling Missing Values:** Numeric features (`area_sqft`, `age_years`) imputed using **Median Imputation** via `SimpleImputer(strategy='median')`; categorical features (`city`) imputed using **Mode Imputation** (`strategy='most_frequent'`).
- **Duplicate Removal:** Checked via `df.duplicated().sum()` and duplicate rows dropped.
- **Categorical Encoding:** `OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')` applied to `city`, `property_type`, and `furnishing`.
- **Feature Scaling:** `StandardScaler()` applied within pipelines for regularized linear models (Ridge and Lasso).
- **Train-Test Split:** 80% Training Set (1,200 samples) and 20% Held-Out Testing Set (300 samples) using `train_test_split(test_size=0.2, random_state=42)`.

### 3.3 Feature Extraction / Selection
All structural and spatial features were retained as each demonstrated theoretical and empirical relevance to valuation. Bivariate correlation analysis showed that `area_sqft` ($r = +0.51$) and `city_Mumbai` ($r = +0.68$) were primary drivers, while Lasso ($L_1$) regression was employed to evaluate feature sparsity.

### 3.4 Training Multiple Regression Models

| Sr. No. | Model Name | Purpose / Notes |
|:---:|---|---|
| 1 | **Multiple Linear Regression (OLS)** | Baseline parametric model assuming strictly additive linear relationships. |
| 2 | **Ridge Regression ($L_2$)** | Penalizes squared coefficients ($\alpha \sum w_j^2$) to stabilize weights under multicollinearity. |
| 3 | **Lasso Regression ($L_1$)** | Penalizes absolute coefficients ($\alpha \sum \|w_j\|$) to drive uninformative features to zero. |
| 4 | **Decision Tree Regressor** | Non-parametric model recursively partitioning feature space into piecewise constant regions. |
| 5 | **Random Forest Regressor** | Ensemble bagging algorithm averaging 100 decorrelated decision trees to eliminate variance. |

### 3.5 Performance Evaluation and Model Comparison
Models were evaluated using 5-Fold Cross-Validation on the training set and validated on the held-out test set:

| Model | Train $R^2$ | Test $R^2$ | Test Adj $R^2$ | CV $R^2$ (Mean $\pm$ Std) | MAE (₹) | RMSE (₹) | MAPE (%) | Best Hyperparameters |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Random Forest** | **0.9933** | **0.9604** | **0.9582** | **0.9509 $\pm$ 0.021** | **₹ 7,83,302** | **₹ 15,84,460** | **8.95%** | `n_estimators=100, max_depth=12, min_samples_leaf=1` |
| **Decision Tree** | 0.9699 | 0.9465 | 0.9435 | 0.9241 $\pm$ 0.034 | ₹ 10,13,071 | ₹ 18,41,921 | 11.35% | `max_depth=8, min_samples_leaf=5` |
| **Lasso Regression** | 0.8870 | 0.8869 | 0.8805 | 0.8823 $\pm$ 0.013 | ₹ 17,79,466 | ₹ 26,78,266 | 29.05% | `alpha=10` |
| **Ridge Regression** | 0.8870 | 0.8869 | 0.8805 | 0.8823 $\pm$ 0.013 | ₹ 17,79,462 | ₹ 26,78,268 | 29.05% | `alpha=0.01` |
| **Linear Regression** | 0.8870 | 0.8869 | 0.8805 | 0.8823 $\pm$ 0.013 | ₹ 17,79,475 | ₹ 26,78,267 | 29.06% | Default (Unregularized OLS) |

### 3.6 Best Model Selection
**Random Forest Regressor** was selected as the production champion:
1. **Highest Cross-Validated Accuracy:** Achieved **95.09% CV $R^2$** and **96.04% Test $R^2$**, outperforming linear baselines by $+7.35\%$.
2. **Superior Error Reduction:** Cut Mean Absolute Error by more than 55% (₹7.83 Lakhs vs ₹17.79 Lakhs).
3. **Institutional Precision:** Achieved an error rate of **8.95% MAPE**, well within the commercial real estate threshold of $<10\%$.
4. **Handling Non-Linear Interactions:** Successfully modeled multiplicative interactions (e.g., location multiplier $\times$ typology multiplier $\times$ area).

---

## 4. PROJECT IMPLEMENTATION

### 4.1 Tools and Technologies
| Tool / Technology | Version | Purpose |
|---|:---:|---|
| **Python** | 3.12 | Core programming language |
| **Google Colab / VS Code** | Latest | Model development and execution environment |
| **Pandas / NumPy** | 2.x / 1.x | Tabular data manipulation, matrix computations |
| **Scikit-Learn** | 1.x | Data pipelines, OneHotEncoding, GridSearchCV, Regression algorithms |
| **Matplotlib / Seaborn** | 3.x / 0.13 | Distribution plots, correlation heatmaps, residual diagnostics |
| **Joblib** | 1.4+ | Model serialization and artifact persistence |
| **Streamlit** | 1.40+ | Interactive multi-page web presentation GUI |

### 4.2 Module-wise Implementation
1. **`train_models.py`:** Comprehensive pipeline executing data ingestion, missing value imputation, EDA plot generation, 5-fold cross-validation grid search, model benchmarking, and serialization to `best_model.joblib`.
2. **`utils.py`:** Shared caching loaders (`@st.cache_resource`, `@st.cache_data`), Indian Rupee (Lakhs/Crores) formatters, and theme-adaptive CSS components.
3. **`app.py`:** Executive Dashboard displaying KPIs, end-to-end architecture flowchart, active asset registry table, and instant appraisal tool.
4. **`pages/1_📊_Market_Analytics.py`:** Regional pricing distributions, boxplots, correlation heatmap, and spatial distance elasticity.
5. **`pages/2_🤖_Model_Governance.py`:** 5-model comparative leaderboard, hyperparameter logs, and actual vs predicted residual diagnostics.
6. **`pages/3_🔮_Property_Appraisal.py`:** Live property appraisal interface with 5 preset archetypes, $\pm 1$ RMSE confidence range, and "What-If" CapEx sensitivity simulator.

### 4.3 GUI Implementation
The GUI was implemented using Streamlit's multi-page architecture. It features:
- **Responsive Layout:** Adaptive design supporting both Light and Dark themes seamlessly.
- **Dynamic Property Inputs:** Dual-column sliders and dropdowns bounded by empirical feature ranges.
- **Scenario Archetypes:** One-click presets (*Metro Prime Villa*, *IT Corridor Flat*, *Tech Hub High-Rise*, *Sub-Metro Estate*, *Growth Corridor Unit*).
- **Live CapEx Simulator:** Real-time delta metric cards calculating financial gains from carpet area additions or interior furnishing upgrades.

---

## 5. COMPLETE CODE
The complete codebase is organized into modular Python files:
- `train_models.py`: Model training, GridSearchCV, and pipeline serialization.
- `app.py`: Streamlit entry point and Executive Dashboard.
- `pages/1_📊_Market_Analytics.py`, `pages/2_🤖_Model_Governance.py`, `pages/3_🔮_Property_Appraisal.py`: Multi-page presentation modules.
- `utils.py`: Reusable utility functions and styling rules.
*(Full source code is accessible in the project directory and linked GitHub repository).*

---

## 6. RESULTS AND DISCUSSION

### 6.1 Required Output Artifacts & Figures
- **Figure 1: Data Preprocessing & Profiling:** Terminal and dataframe outputs showing 0 nulls post-imputation and removal of duplicate rows.
- **Figure 2: Correlation Heatmap (`outputs/correlation_heatmap.png`):** Demonstrating high linear association between `price` and `area_sqft` ($r = 0.51$) and Mumbai location index ($r = 0.68$).
- **Figure 3: Model Comparison Leaderboard (`outputs/model_comparison.csv`):** Comprehensive table showing Random Forest dominance across all metrics.
- **Figure 4: R² Score Comparison Bar Chart (`outputs/r2_comparison.png`):** Graphical visualization of Train, Test, and CV $R^2$ across the 5 models.
- **Figure 5: Residual and Calibration Diagnostics (`outputs/actual_vs_predicted.png`):** Actual vs Predicted points clustering along the $45^\circ$ parity line, with residuals homoscedastically distributed around 0.
- **Figure 6: Streamlit GUI Dashboard (`app.py`):** Executive overview with KPI cards and instant valuation tool.
- **Figure 7: Live Appraisal & What-If Simulator (`pages/3_🔮_Property_Appraisal.py`):** Real-time fair market valuation with confidence interval and CapEx sensitivity feedback.

### 6.2 Result Analysis
1. **Linear Model Limitations:** Multiple Linear Regression, Ridge, and Lasso all converged at $R^2 \approx 0.8869$ and $\text{MAPE} \approx 29\%$. This proves that linear models cannot adequately represent compounding value interactions between location quality and physical area.
2. **Tree-Based Superiority:** Decision Tree improved $R^2$ to $0.9465$, but exhibited variance between train ($0.9699$) and test folds.
3. **Random Forest Generalization:** By averaging 100 decorrelated trees, Random Forest achieved **$0.9604$ Test $R^2$** and lowered MAPE to **$8.95\%$**, proving that ensemble bagging successfully eliminates single-tree variance while modeling non-linear interactions.

---

## 7. CONCLUSION
This project successfully designed, implemented, and deployed **EstatePulse AI**, an end-to-end Machine Learning real estate price prediction and market analytics system. 

**Summary of Achievements:**
- Rigorous benchmarking of 5 regression algorithms using 5-fold cross-validation and hyperparameter optimization.
- **Random Forest Regressor** achieved champion performance with **$96.04\%$ Test $R^2$**, **₹7.83 Lakhs MAE**, and **$8.95\%$ MAPE**.
- Developed a professional, production-ready Streamlit multi-page web interface with real-time valuation and CapEx sensitivity modeling.

**Future Enhancements:**
- Integration of live GIS / geospatial coordinate mapping and satellite imagery embeddings.
- Extension to time-series forecasting for macroeconomic interest rate shifts and inflation trends.

---

## 8. GITHUB LINK
- **GitHub Repository URL:** `https://github.com/Runjhun-Suryawanshi/real-estate-project.git` *(or your repository URL)*
- **Repository Contents:** Complete Python source scripts (`train_models.py`, `app.py`, `utils.py`), multi-page presentation scripts (`pages/`), serialized model bundle (`best_model.joblib`), evaluation plots and CSVs (`outputs/`), and documentation.

---

## 9. REFERENCES
1. Scikit-learn Documentation: Ensemble Methods & Random Forests (`https://scikit-learn.org/stable/modules/ensemble.html`)
2. Streamlit Multi-Page Application Guide (`https://docs.streamlit.io/get-started/multipage-apps`)
3. Breiman, L. (2001). "Random Forests". *Machine Learning*, 45(1), 5-32.
4. Indian Real Estate Housing Benchmark Dataset & Kaggle Housing Repositories.
