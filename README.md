# SmartStock AI
## Supermarket Demand Forecasting and Inventory Planning

**Project type:** Academic data science project  
**Status:** Stage 2 — synthetic data generation, validation, and exploratory analysis

### 1. Problem statement
A supermarket may lose money when it orders too much fresh produce, dairy, and bakery stock that later expires. It may also lose sales when high-demand products such as milk and bread run out during weekends or end-of-month payday periods. SmartStock AI explores how historical sales patterns and machine learning can support better demand forecasts and replenishment decisions.

### 2. Project objectives
- Generate a reproducible, clearly labelled synthetic supermarket dataset.
- Explore demand patterns by product, weekday, weekend, and payday period.
- Prepare and analyse data for demand forecasting.
- Train and evaluate a regression model using a time-aware train/test split.
- Translate forecasts into explainable replenishment recommendations.
- Present results in a Streamlit dashboard.

### 3. Technology
Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Streamlit, Plotly, and Joblib.

### 4. Repository structure
```text
SMARTSTOCK_AI/
├── dashboard/          # Streamlit dashboard (later stage)
├── data/
│   ├── raw/             # Generated input data (CSV is not committed)
│   └── processed/       # Prepared data (generated locally)
├── models/              # Trained model artifacts (generated locally)
├── notebooks/           # Exploratory academic notebooks
├── reports/             # Quality reports, summaries, and charts
├── src/
│   ├── generate_data.py # Reproducible synthetic data generator
│   ├── prepare_data.py  # Validation and preparation pipeline
│   └── explore_data.py  # Exploratory summaries and charts
├── .gitignore
└── requirements.txt
```

### 5. Windows setup
Install Python 3.11 or newer and Git, then open PowerShell in the cloned repository:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python src/generate_data.py
```

The generator writes `data/raw/synthetic_sales.csv`. The dataset contains daily records for eight example products from 1 January 2024 to 31 December 2025. It includes product details, price, discounts, weekend/payday indicators, stock availability, units sold, and simulated demand. Run the Stage 2 pipeline in order:

```powershell
python src/prepare_data.py
python src/explore_data.py
```

The preparation script validates required fields, missing values, duplicate date/product records, numeric ranges, and stock/sales consistency. It writes `data/processed/cleaned_sales.csv` and `reports/data_quality_report.json`. The exploration script writes product, daily, weekday, and weekend/payday summary CSV files plus charts under `reports/figures/`.

### 6. Academic data notice
**All generated records are simulated.** They are intended for learning and demonstration, not represented as real supermarket point-of-sale records. Sales may be limited by simulated stock availability, so `simulated_demand` is retained separately from `units_sold` to make stockout censoring visible during analysis.

### 7. Roadmap
1. Repository foundation and synthetic data generation — completed.
2. Data validation, preparation, and exploratory analysis — implemented; run locally to generate outputs.
3. Feature engineering and demand forecasting.
4. Model evaluation using MAE, RMSE, and MAPE (with care around zero demand).
5. Inventory and replenishment recommendations.
6. Streamlit dashboard, testing, and academic documentation.

No model performance or business-impact improvement is claimed until it has been measured and evaluated.
