"""
CodSoft Data Analytics Internship - Task 2
Exploratory Data Analysis (EDA)

Dataset: Cleaned Customer Sales Data (output of Task 1)

Steps performed:
1. Load the dataset and examine features using descriptive statistics.
2. Identify trends, distributions, and relationships between variables.
3. Detect outliers and unusual patterns.
4. Use summary statistics to answer key business questions.
5. Bonus: Generate a short findings report.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_PATH = "dataset/cleaned_customer_sales.csv"
OUT_DIR = "outputs"
REPORT_PATH = os.path.join(OUT_DIR, "eda_findings_report.md")

os.makedirs(OUT_DIR, exist_ok=True)
sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110


def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["OrderDate"])
    findings = []

    # ------------------------------------------------------------------
    # 1. Descriptive statistics
    # ------------------------------------------------------------------
    print("Shape:", df.shape)
    print("\nDescriptive statistics (numeric):")
    desc = df.describe()
    print(desc)

    print("\nDescriptive statistics (categorical):")
    cat_desc = df.describe(include="str")
    print(cat_desc)

    # ------------------------------------------------------------------
    # 2. Trends, distributions, relationships
    # ------------------------------------------------------------------

    # Monthly revenue trend
    df["OrderMonth"] = df["OrderDate"].dt.to_period("M").astype(str)
    monthly_revenue = df.groupby("OrderMonth")["TotalAmount"].sum().sort_index()

    plt.figure(figsize=(10, 5))
    monthly_revenue.plot(kind="line", marker="o", color="#1f77b4")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue (INR)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "monthly_revenue_trend.png"))
    plt.close()

    # Age distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df["Age"], bins=15, kde=True, color="#2ca02c")
    plt.title("Customer Age Distribution")
    plt.xlabel("Age")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "age_distribution.png"))
    plt.close()

    # Revenue by category
    revenue_by_category = df.groupby("ProductCategory")["TotalAmount"].sum().sort_values(ascending=False)
    plt.figure(figsize=(9, 5))
    sns.barplot(x=revenue_by_category.values, y=revenue_by_category.index,
                hue=revenue_by_category.index, palette="Blues_r", legend=False)
    plt.title("Total Revenue by Product Category")
    plt.xlabel("Total Revenue (INR)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "revenue_by_category.png"))
    plt.close()

    # Price vs Rating relationship
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="Price", y="Rating", hue="ProductCategory", alpha=0.6, legend=False)
    plt.title("Price vs Rating")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "price_vs_rating.png"))
    plt.close()

    # Correlation heatmap
    numeric_cols = ["Age", "Price", "Quantity", "Rating", "TotalAmount"]
    corr = df[numeric_cols].corr()
    plt.figure(figsize=(7, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "correlation_heatmap.png"))
    plt.close()

    # ------------------------------------------------------------------
    # 3. Outlier detection using IQR method
    # ------------------------------------------------------------------
    def iqr_outliers(series):
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        return series[(series < lower) | (series > upper)]

    price_outliers = iqr_outliers(df["Price"])
    total_outliers = iqr_outliers(df["TotalAmount"])

    plt.figure(figsize=(7, 5))
    sns.boxplot(y=df["Price"], color="#ff7f0e")
    plt.title("Price Distribution (Outlier Check)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "price_boxplot_outliers.png"))
    plt.close()

    # ------------------------------------------------------------------
    # 4. Key business questions
    # ------------------------------------------------------------------
    top_city = df.groupby("City")["TotalAmount"].sum().idxmax()
    top_city_revenue = df.groupby("City")["TotalAmount"].sum().max()
    top_category = revenue_by_category.idxmax()
    avg_order_value = df["TotalAmount"].mean()
    top_payment = df["PaymentMode"].value_counts().idxmax()
    best_month = monthly_revenue.idxmax()

    # ------------------------------------------------------------------
    # 5. Findings report
    # ------------------------------------------------------------------
    findings.append("# EDA Findings Report — Customer Sales Data\n")
    findings.append(f"- **Dataset size:** {df.shape[0]} rows x {df.shape[1]} columns\n")
    findings.append(f"- **Average order value:** INR {avg_order_value:,.2f}\n")
    findings.append(f"- **Top-performing city by revenue:** {top_city} (INR {top_city_revenue:,.2f})\n")
    findings.append(f"- **Best-selling product category by revenue:** {top_category}\n")
    findings.append(f"- **Most used payment mode:** {top_payment}\n")
    findings.append(f"- **Best revenue month:** {best_month}\n")
    findings.append(f"- **Price outliers detected (IQR method):** {len(price_outliers)} orders\n")
    findings.append(f"- **Total-amount outliers detected (IQR method):** {len(total_outliers)} orders\n")
    findings.append("\n## Correlation Highlights\n")
    findings.append(f"- Price vs TotalAmount correlation: {corr.loc['Price','TotalAmount']:.2f}\n")
    findings.append(f"- Age vs Rating correlation: {corr.loc['Age','Rating']:.2f}\n")
    findings.append("\n## Charts Generated\n")
    for chart in ["monthly_revenue_trend.png", "age_distribution.png", "revenue_by_category.png",
                  "price_vs_rating.png", "correlation_heatmap.png", "price_boxplot_outliers.png"]:
        findings.append(f"- outputs/{chart}\n")

    with open(REPORT_PATH, "w") as f:
        f.writelines(findings)

    print(f"\nEDA findings report saved to: {REPORT_PATH}")
    print("Charts saved in the outputs/ folder.")


if __name__ == "__main__":
    main()
