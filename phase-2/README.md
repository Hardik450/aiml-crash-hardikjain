# 📦 Order Delay Intelligence: Predict, Explain, Recommend

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-ready-success)
![SHAP](https://img.shields.io/badge/SHAP-ready-success)
![Status](https://img.shields.io/badge/Phase%202%20Mini%20Project-Complete-brightgreen)

**Phase 2 Mini Project — CodeTrade.io AI/ML Internship**  
**Dataset:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle)

---

## Project Structure

```
phase2_project/
├── order_delay_notebook.ipynb   ← Full notebook: EDA, SQL, modeling, SHAP (Tasks 1-5)
├── REPORT.md                    ← Findings, model comparison, recommendations
├── README.md                    ← This file
├── cleaned_master.csv           ← Cleaned, feature-engineered dataset (output of Task 1)
├── data/
│   ├── olist_orders_dataset.csv
│   ├── olist_customers_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_products_dataset.csv
│   └── olist_order_payments_dataset.csv
└── charts/
    ├── eda1_delay_distribution.png
    ├── eda2_delay_by_state.png
    ├── eda3_monthly_trend.png
    ├── eda4_peak_season_delay.png
    ├── eda5_payment_delay.png
    ├── eda6_correlation_heatmap.png
    ├── task3_confusion_matrix_logreg.png
    ├── task4_roc_comparison.png
    └── task5_shap_summary.png
```

---

## ⚠️ A Note on XGBoost and SHAP

This notebook is written to use **real XGBoost and real SHAP** automatically if they are
installed in your environment:

```bash
pip install xgboost shap
```

If they are *not* installed, the notebook **automatically falls back** to:
- `sklearn.ensemble.GradientBoostingClassifier` in place of `XGBClassifier`
- Built-in `feature_importances_` in place of `shap.TreeExplainer`

This means the notebook always runs end-to-end without crashing, but **to fulfil the exact
assignment requirement (XGBoost + SHAP), install both packages before running.** The fallback
logic is visible in Cell 2 (imports) and clearly labelled wherever it activates.

---

## Setup & Running

```bash
git clone https://github.com/<your-username>/order-delay-intelligence.git
cd order-delay-intelligence

python -m venv .venv
source .venv/bin/activate         # macOS / Linux
.venv\Scripts\activate            # Windows

pip install pandas numpy matplotlib seaborn scikit-learn jupyter
pip install xgboost shap          # required for the real assignment-spec models

jupyter notebook order_delay_notebook.ipynb
```

---

## Task-by-Task Breakdown

| Task | What Was Done |
|---|---|
| **Task 1 — Data Audit, Cleaning, EDA** | Loaded 5 CSVs, audited nulls/duplicates/dtypes, engineered time-based features (weekday, month, hour, approval time, shipping time, promised days, peak season flag), created the `is_delayed` target, built 6 charts (distribution, comparison, time-trend, delay-behaviour, payment analysis, correlation heatmap), wrote 5 EDA insights |
| **Task 2 — SQL Practice** | Loaded cleaned data into SQLite, wrote 10 queries covering `SELECT`/`WHERE`/`GROUP BY`/`ORDER BY`/`JOIN`/aggregates/subquery, recreated the peak-season insight in SQL and verified an exact match against the pandas result |
| **Task 3 — Baseline Model** | Defined the binary target, built a `Pipeline` + `ColumnTransformer`, trained Logistic Regression, measured accuracy/precision/recall/F1/ROC-AUC/confusion matrix, explained why Recall + ROC-AUC matter most for this business problem |
| **Task 4 — Feature Engineering + XGBoost** | Reused the leak-safe pipeline, swapped in XGBoost (with fallback), compared against the baseline with a side-by-side metrics table and ROC curve overlay |
| **Task 5 — CV, Tuning, SHAP** | Ran 5-fold Stratified CV, tuned `max_depth`, `learning_rate`, and `n_estimators` via `GridSearchCV` (train-set only — no test-set leakage), compared baseline vs tuned model with CV mean/std, generated SHAP summary plot (or feature-importance fallback) and 3 individual prediction explanations |

---

## Key Results

- **Delay rate:** ~26% of delivered orders arrive after the promised date
- **Peak season effect:** Nov/Dec delay rate (~55%) is **2.7x** the regular-month rate (~20%)
- **Top geographic risk states:** AL, MA, SE — all 1.5–2.5x São Paulo's delay rate
- **Best model:** Tuned XGBoost/GradientBoosting — CV ROC-AUC ≈ 0.69, lowest variance across folds
- **Top predictive features:** `is_peak_season`, `customer_state`, `promised_days`, `total_freight`

---

## Business Recommendations (Summary)

1. Flag and prioritise Nov/Dec orders before the season starts
2. Set wider promised-delivery windows for AL, MA, SE
3. Trigger proactive "your order may be delayed" emails using the model's risk score
4. Pre-negotiate peak-season carrier capacity
5. Monitor high-freight orders as a secondary risk signal

Full details and rationale are in `REPORT.md`.

---

## Rules Followed

- ✅ Only Phase 1 + Phase 2 concepts used (pandas, NumPy, SQL, sklearn, XGBoost, CV, SHAP)
- ✅ No tuning on the test set — `GridSearchCV` runs exclusively on the training fold
- ✅ Feature and metric choices are explained with business reasoning throughout
- ✅ Notebook is organised into clearly labelled, sequential sections per task
