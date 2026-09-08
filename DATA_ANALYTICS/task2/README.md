# Task 2 — Exploratory Data Analysis (EDA)

## Objective

- Load a dataset and examine its features using descriptive statistics.
- Identify trends, distributions, and relationships between variables.
- Detect outliers and unusual patterns within the data.
- Use summary statistics to answer key business questions.
- **Bonus:** Create a short report highlighting the findings.

## Dataset

`dataset/cleaned_customer_sales.csv` — the cleaned dataset produced in
[Task 1](../Task1_Data_Cleaning_Preprocessing), containing 600 customer
orders across 14 columns (customer info, product category, price,
quantity, order date, payment mode, rating, and derived `TotalAmount`).

## Approach

1. **Descriptive statistics** — `.describe()` on numeric and categorical columns.
2. **Trends & distributions**
   - Monthly revenue trend (line chart)
   - Customer age distribution (histogram + KDE)
   - Revenue by product category (bar chart)
   - Price vs. rating relationship (scatter plot)
   - Correlation heatmap across numeric fields
3. **Outlier detection** — IQR (interquartile range) method applied to `Price` and `TotalAmount`, visualized with a boxplot.
4. **Business questions answered** — top city by revenue, best-selling category, most common payment mode, best revenue month, average order value.

## How to Run

```bash
pip install -r ../requirements.txt
python task2_eda.py
```

## Outputs (`outputs/`)

| File | Description |
|---|---|
| `monthly_revenue_trend.png` | Revenue trend across months |
| `age_distribution.png` | Distribution of customer ages |
| `revenue_by_category.png` | Total revenue per product category |
| `price_vs_rating.png` | Relationship between price and customer rating |
| `correlation_heatmap.png` | Correlation matrix of numeric features |
| `price_boxplot_outliers.png` | Boxplot used for outlier detection on price |
| `eda_findings_report.md` | Auto-generated summary of key findings |

## Key Findings

- **Average order value:** ₹19,560.88
- **Top-performing city by revenue:** Delhi (₹19,56,529.15)
- **Best-selling product category by revenue:** Grocery
- **Most used payment mode:** Cash on Delivery
- **Best revenue month:** July 2025
- **Outliers detected:** 31 unusually high/low order values (IQR method on `TotalAmount`); no price-level outliers
- **Correlation:** Price and TotalAmount are strongly correlated (0.71), as expected since amount is derived from price × quantity. Age shows essentially no correlation with rating (0.02), suggesting customer satisfaction is not age-dependent in this dataset.

See `outputs/eda_findings_report.md` for the full auto-generated report.
