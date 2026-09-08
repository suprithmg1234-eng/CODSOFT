# Task 3 — Data Visualization Dashboard

## Objective

- Create meaningful visualizations using Matplotlib and Seaborn.
- Design bar charts, line charts, pie charts, histograms, and scatter plots.
- Customize charts with titles, labels, legends, and color schemes.
- Present insights through clear, easy-to-understand visualizations.
- **Bonus:** Combine the key charts into a single dashboard-style view.

## Dataset

`dataset/cleaned_customer_sales.csv` — the cleaned dataset produced in
[Task 1](../Task1_Data_Cleaning_Preprocessing).

## Approach

Six visualizations were built, each customized with titles, axis labels,
color palettes, and (where relevant) legends:

1. **Bar chart** — total revenue by product category
2. **Line chart** — monthly revenue trend across the year
3. **Pie chart** — share of orders by payment mode
4. **Histogram** — distribution of order values (with KDE overlay)
5. **Scatter plot** — unit price vs. total order amount, colored by category
6. **Combined dashboard** — all key charts (plus average rating by city) arranged in a single 2×3 grid image for an at-a-glance overview

## How to Run

```bash
pip install -r ../requirements.txt
python task3_visualization.py
```

## Outputs (`outputs/`)

| File | Chart Type |
|---|---|
| `00_full_dashboard.png` | Combined 2×3 dashboard |
| `01_bar_revenue_by_category.png` | Bar chart |
| `02_line_monthly_revenue.png` | Line chart |
| `03_pie_payment_mode_share.png` | Pie chart |
| `04_histogram_order_values.png` | Histogram |
| `05_scatter_price_vs_total.png` | Scatter plot |

## Insights Presented

- Grocery, Clothing, and Books lead in revenue among the 8 product categories.
- Revenue shows clear month-to-month volatility, with peaks in July and November.
- Cash on Delivery and UPI together account for roughly half of all orders.
- Order values are right-skewed — most orders are lower-value, with a long tail of high-value orders.
- Price and total order amount scale linearly within each category, as expected.

**Bonus (Power BI / Tableau):** the cleaned CSV in `dataset/` can be
plugged directly into Power BI or Tableau to build an interactive
version of this dashboard with filters by city, category, and date range.
