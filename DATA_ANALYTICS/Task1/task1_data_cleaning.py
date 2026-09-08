"""
CodSoft Data Analytics Internship - Task 1
Data Cleaning & Preprocessing

Dataset: Customer Sales Data (synthetic, mimics a real e-commerce export)

Steps performed:
1. Import the dataset and inspect its structure.
2. Identify missing values, duplicate records, and inconsistent data entries.
3. Clean the dataset by handling nulls, removing duplicates, and correcting data types.
4. Prepare the data for further analysis using Pandas.
5. Bonus: Save the cleaned dataset as a new CSV file.
"""

import pandas as pd
import numpy as np
import os

RAW_PATH = "dataset/raw_customer_sales.csv"
CLEAN_PATH = "dataset/cleaned_customer_sales.csv"
REPORT_PATH = "outputs/cleaning_report.txt"

os.makedirs("outputs", exist_ok=True)


def log(lines, msg):
    print(msg)
    lines.append(str(msg))


def main():
    report_lines = []

    # ------------------------------------------------------------------
    # 1. Import dataset and inspect structure
    # ------------------------------------------------------------------
    df = pd.read_csv(RAW_PATH)

    log(report_lines, "=" * 70)
    log(report_lines, "STEP 1: INITIAL DATA INSPECTION")
    log(report_lines, "=" * 70)
    log(report_lines, f"Shape (rows, columns): {df.shape}")
    log(report_lines, f"Columns: {list(df.columns)}")
    log(report_lines, "\nData types before cleaning:")
    log(report_lines, df.dtypes.to_string())

    # ------------------------------------------------------------------
    # 2. Identify missing values, duplicates, inconsistent entries
    # ------------------------------------------------------------------
    log(report_lines, "\n" + "=" * 70)
    log(report_lines, "STEP 2: IDENTIFYING DATA QUALITY ISSUES")
    log(report_lines, "=" * 70)

    missing_counts = df.isnull().sum()
    log(report_lines, "\nMissing values per column:")
    log(report_lines, missing_counts.to_string())

    full_dupes = df.duplicated().sum()
    id_dupes = df.duplicated(subset=["CustomerID"]).sum()
    log(report_lines, f"\nFully duplicated rows: {full_dupes}")
    log(report_lines, f"Duplicated CustomerID rows (post first occurrence): {id_dupes}")

    log(report_lines, "\nInconsistent categorical entries found:")
    log(report_lines, f"  Gender unique values: {sorted(df['Gender'].dropna().unique().tolist())}")
    log(report_lines, f"  City unique values: {sorted(df['City'].dropna().unique().tolist())}")
    log(report_lines, f"  PaymentMode unique values: {sorted(df['PaymentMode'].dropna().unique().tolist())}")
    log(report_lines, f"  Rating unique values: {sorted(df['Rating'].dropna().unique().tolist())}")
    log(report_lines, f"  OrderDate sample formats: {df['OrderDate'].sample(5, random_state=1).tolist()}")

    # ------------------------------------------------------------------
    # 3. Clean the dataset
    # ------------------------------------------------------------------
    log(report_lines, "\n" + "=" * 70)
    log(report_lines, "STEP 3: CLEANING THE DATASET")
    log(report_lines, "=" * 70)

    clean = df.copy()

    # 3a. Standardize text fields (strip whitespace, fix casing)
    clean["CustomerName"] = clean["CustomerName"].str.strip().str.title()
    clean["City"] = clean["City"].str.strip().str.title()
    clean["PaymentMode"] = clean["PaymentMode"].str.strip().str.title()

    # 3b. Standardize Gender values into Male/Female
    gender_map = {
        "M": "Male", "male": "Male", "Male": "Male",
        "F": "Female", "female": "Female", "Female": "Female"
    }
    clean["Gender"] = clean["Gender"].map(gender_map)

    # 3c. Standardize PaymentMode label variants
    payment_map = {
        "Cod": "Cash On Delivery",
        "Cash On Delivery": "Cash On Delivery",
        "Upi": "UPI",
    }
    clean["PaymentMode"] = clean["PaymentMode"].replace(payment_map)

    # 3d. Parse OrderDate with mixed formats into a single datetime type
    clean["OrderDate"] = pd.to_datetime(clean["OrderDate"], format="mixed", dayfirst=True, errors="coerce")

    # 3e. Fix invalid Rating values (only 1-5 is valid); anything else -> NaN
    clean.loc[~clean["Rating"].isin([1, 2, 3, 4, 5]), "Rating"] = np.nan

    # 3f. Handle missing values
    #   - Age: fill with median age
    #   - Gender/City/SignupChannel: fill with "Unknown"
    #   - Quantity: fill with 1 (most common order quantity)
    #   - Rating: fill with median rating
    clean["Age"] = clean["Age"].fillna(clean["Age"].median())
    clean["Gender"] = clean["Gender"].fillna("Unknown")
    clean["City"] = clean["City"].fillna("Unknown")
    clean["SignupChannel"] = clean["SignupChannel"].fillna("Unknown")
    clean["Quantity"] = clean["Quantity"].fillna(1)
    clean["Rating"] = clean["Rating"].fillna(clean["Rating"].median())

    # Rows where OrderDate could not be parsed are dropped (critical field)
    before_date_drop = len(clean)
    clean = clean.dropna(subset=["OrderDate"])
    log(report_lines, f"\nRows dropped due to unparseable OrderDate: {before_date_drop - len(clean)}")

    # 3g. Remove duplicate rows (exact duplicates and duplicate CustomerID+OrderDate+Price combos)
    before = len(clean)
    clean = clean.drop_duplicates()
    log(report_lines, f"Exact duplicate rows removed: {before - len(clean)}")

    before = len(clean)
    clean = clean.drop_duplicates(subset=["CustomerID", "OrderDate", "Price", "ProductCategory"])
    log(report_lines, f"Duplicate transactions (same customer/date/price/category) removed: {before - len(clean)}")

    # 3h. Correct data types
    clean["Age"] = clean["Age"].astype(int)
    clean["Quantity"] = clean["Quantity"].astype(int)
    clean["Rating"] = clean["Rating"].astype(int)
    clean["Price"] = clean["Price"].round(2).astype(float)
    clean["CustomerID"] = clean["CustomerID"].astype(str)

    # 3i. Derived column useful for later analysis
    clean["TotalAmount"] = (clean["Price"] * clean["Quantity"]).round(2)

    # 3j. Reset index
    clean = clean.reset_index(drop=True)

    log(report_lines, "\nData types after cleaning:")
    log(report_lines, clean.dtypes.to_string())

    # ------------------------------------------------------------------
    # 4. Final inspection
    # ------------------------------------------------------------------
    log(report_lines, "\n" + "=" * 70)
    log(report_lines, "STEP 4: FINAL CLEANED DATA SUMMARY")
    log(report_lines, "=" * 70)
    log(report_lines, f"Original shape: {df.shape}")
    log(report_lines, f"Cleaned shape:  {clean.shape}")
    log(report_lines, f"Remaining missing values:\n{clean.isnull().sum().to_string()}")
    log(report_lines, f"Remaining duplicate rows: {clean.duplicated().sum()}")

    # ------------------------------------------------------------------
    # 5. Bonus: Save cleaned dataset
    # ------------------------------------------------------------------
    clean.to_csv(CLEAN_PATH, index=False)
    log(report_lines, f"\nCleaned dataset saved to: {CLEAN_PATH}")

    with open(REPORT_PATH, "w") as f:
        f.write("\n".join(report_lines))
    print(f"\nCleaning report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
