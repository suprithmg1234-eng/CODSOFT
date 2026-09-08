# Task 1 — Data Cleaning & Preprocessing

## Objective

- Import a dataset using Python and inspect its structure.
- Identify missing values, duplicate records, and inconsistent data entries.
- Clean the dataset by handling null values, removing duplicates, and correcting data types.
- Prepare the data for further analysis using Pandas.
- **Bonus:** Save the cleaned dataset as a new CSV file.

## Dataset

`dataset/raw_customer_sales.csv` — a synthetic e-commerce customer sales
export (635 rows, 12 columns) deliberately generated with realistic data
quality problems:

- Missing values in `Age`, `Gender`, `City`, `Quantity`, `Rating`, `SignupChannel`
- Inconsistent categorical labels (`Male` / `male` / `M`, `bangalore` / `Bengaluru`, `COD` / `Cash on Delivery`)
- Extra whitespace in text fields (`"Mumbai "`, `"UPI "`)
- Mixed date formats in `OrderDate` (`YYYY-MM-DD`, `DD/MM/YYYY`, `DD-MM-YYYY`)
- An invalid rating value (`6`, outside the valid 1–5 scale)
- 35 duplicate rows (exact duplicates and re-cased duplicate records)

## Approach

1. **Inspect** — load with `pandas.read_csv`, check `.shape`, `.dtypes`, and column list.
2. **Identify issues** — `.isnull().sum()` for missing values, `.duplicated()` for duplicate rows, `.unique()` on categorical columns to spot inconsistent labels.
3. **Clean**
   - Standardize text casing/whitespace (`.str.strip()`, `.str.title()`)
   - Map inconsistent category labels to a single canonical value
   - Parse mixed date formats into a proper `datetime` column
   - Replace invalid `Rating` values (outside 1–5) with `NaN`, then impute
   - Impute missing values with sensible defaults (median for numeric, "Unknown" for categorical)
   - Drop exact duplicate rows and duplicate transactions
   - Correct final data types (`int`, `float`, `datetime`, `str`)
   - Add a derived `TotalAmount` column (`Price × Quantity`) for downstream analysis
4. **Save** — export the cleaned data to `dataset/cleaned_customer_sales.csv`.

## How to Run

```bash
pip install -r ../requirements.txt
python task1_data_cleaning.py
```

## Outputs

- `dataset/cleaned_customer_sales.csv` — the cleaned dataset (600 rows, 13 columns, zero missing values, zero duplicates)
- `outputs/cleaning_report.txt` — a full log of every issue found and every cleaning step applied, generated automatically by the script

## Result Summary

| Metric | Before | After |
|---|---|---|
| Rows | 635 | 600 |
| Missing values (total) | 506 | 0 |
| Duplicate rows | 35 | 0 |
| Inconsistent category labels | Yes (Gender, City, PaymentMode) | Standardized |
| `OrderDate` dtype | mixed-format string | `datetime64` |
