"""
CodSoft Data Analytics Internship - Task 3
Data Visualization Dashboard

Dataset: Cleaned Customer Sales Data (output of Task 1)

Steps performed:
1. Create meaningful visualizations using Matplotlib and Seaborn.
2. Build bar charts, line charts, pie charts, histograms, and scatter plots.
3. Customize charts with titles, labels, legends, and color schemes.
4. Combine key charts into a single dashboard-style image.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_PATH = "dataset/cleaned_customer_sales.csv"
OUT_DIR = "outputs"

os.makedirs(OUT_DIR, exist_ok=True)
sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110

PALETTE = "viridis"


def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["OrderDate"])
    df["OrderMonth"] = df["OrderDate"].dt.to_period("M").astype(str)

    # ------------------------------------------------------------------
    # 1. Bar chart — Revenue by product category
    # ------------------------------------------------------------------
    revenue_by_category = df.groupby("ProductCategory")["TotalAmount"].sum().sort_values(ascending=False)
    plt.figure(figsize=(9, 5.5))
    sns.barplot(x=revenue_by_category.index, y=revenue_by_category.values,
                hue=revenue_by_category.index, palette=PALETTE, legend=False)
    plt.title("Total Revenue by Product Category", fontsize=14, fontweight="bold")
    plt.xlabel("Product Category")
    plt.ylabel("Total Revenue (INR)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "01_bar_revenue_by_category.png"))
    plt.close()

    # ------------------------------------------------------------------
    # 2. Line chart — Monthly revenue trend
    # ------------------------------------------------------------------
    monthly_revenue = df.groupby("OrderMonth")["TotalAmount"].sum().sort_index()
    plt.figure(figsize=(10, 5.5))
    plt.plot(monthly_revenue.index, monthly_revenue.values, marker="o",
             color="#2c7fb8", linewidth=2, label="Monthly Revenue")
    plt.title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue (INR)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "02_line_monthly_revenue.png"))
    plt.close()

    # ------------------------------------------------------------------
    # 3. Pie chart — Share of orders by payment mode
    # ------------------------------------------------------------------
    payment_counts = df["PaymentMode"].value_counts()
    plt.figure(figsize=(7.5, 7.5))
    colors = sns.color_palette(PALETTE, len(payment_counts))
    plt.pie(payment_counts.values, labels=payment_counts.index, autopct="%1.1f%%",
            colors=colors, startangle=90, wedgeprops={"edgecolor": "white"})
    plt.title("Share of Orders by Payment Mode", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "03_pie_payment_mode_share.png"))
    plt.close()

    # ------------------------------------------------------------------
    # 4. Histogram — Distribution of order values
    # ------------------------------------------------------------------
    plt.figure(figsize=(9, 5.5))
    sns.histplot(df["TotalAmount"], bins=25, kde=True, color="#e6550d")
    plt.title("Distribution of Order Values", fontsize=14, fontweight="bold")
    plt.xlabel("Order Value (INR)")
    plt.ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "04_histogram_order_values.png"))
    plt.close()

    # ------------------------------------------------------------------
    # 5. Scatter plot — Price vs Quantity, colored by category
    # ------------------------------------------------------------------
    plt.figure(figsize=(9, 6))
    sns.scatterplot(data=df, x="Price", y="TotalAmount", hue="ProductCategory",
                     palette=PALETTE, alpha=0.7, s=60)
    plt.title("Unit Price vs Total Order Amount", fontsize=14, fontweight="bold")
    plt.xlabel("Unit Price (INR)")
    plt.ylabel("Total Order Amount (INR)")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="Category", fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "05_scatter_price_vs_total.png"))
    plt.close()

    # ------------------------------------------------------------------
    # 6. Combined dashboard — 2x3 grid summarizing the key charts
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(2, 3, figsize=(20, 11))
    fig.suptitle("Customer Sales — Data Visualization Dashboard", fontsize=18, fontweight="bold")

    # Bar
    sns.barplot(x=revenue_by_category.index, y=revenue_by_category.values,
                hue=revenue_by_category.index, palette=PALETTE, legend=False, ax=axes[0, 0])
    axes[0, 0].set_title("Revenue by Category")
    axes[0, 0].tick_params(axis="x", rotation=30)
    axes[0, 0].set_xlabel("")

    # Line
    axes[0, 1].plot(monthly_revenue.index, monthly_revenue.values, marker="o", color="#2c7fb8")
    axes[0, 1].set_title("Monthly Revenue Trend")
    axes[0, 1].tick_params(axis="x", rotation=45)

    # Pie
    axes[0, 2].pie(payment_counts.values, labels=payment_counts.index, autopct="%1.0f%%",
                   colors=sns.color_palette(PALETTE, len(payment_counts)), startangle=90)
    axes[0, 2].set_title("Payment Mode Share")

    # Histogram
    sns.histplot(df["TotalAmount"], bins=25, kde=True, color="#e6550d", ax=axes[1, 0])
    axes[1, 0].set_title("Order Value Distribution")

    # Scatter
    sns.scatterplot(data=df, x="Price", y="TotalAmount", hue="ProductCategory",
                     palette=PALETTE, alpha=0.7, s=40, ax=axes[1, 1], legend=False)
    axes[1, 1].set_title("Price vs Total Amount")

    # City-wise average rating (bonus chart)
    city_rating = df.groupby("City")["Rating"].mean().sort_values(ascending=False)
    sns.barplot(x=city_rating.values, y=city_rating.index,
                hue=city_rating.index, palette="mako", legend=False, ax=axes[1, 2])
    axes[1, 2].set_title("Average Rating by City")
    axes[1, 2].set_xlabel("Average Rating")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(OUT_DIR, "00_full_dashboard.png"), dpi=130)
    plt.close()

    print("All charts and the combined dashboard have been saved to the outputs/ folder.")


if __name__ == "__main__":
    main()
