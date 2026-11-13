"""Validate and prepare the generated SmartStock AI sales dataset."""

from pathlib import Path
import json

import pandas as pd


REQUIRED_COLUMNS = [
    "date", "product", "category", "unit_price_kes", "discount",
    "is_weekend", "is_payday_period", "month", "day_of_week",
    "shelf_life_days", "stock_available", "units_sold", "simulated_demand",
]
NUMERIC_COLUMNS = [
    "unit_price_kes", "discount", "is_weekend", "is_payday_period",
    "month", "day_of_week", "shelf_life_days", "stock_available",
    "units_sold", "simulated_demand",
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    source = root / "data" / "raw" / "synthetic_sales.csv"
    output_dir = root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "cleaned_sales.csv"
    report_path = root / "reports" / "data_quality_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        raise FileNotFoundError(
            f"Dataset not found at {source}. Run: python src/generate_data.py"
        )

    data = pd.read_csv(source)
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(data.columns))
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {missing_columns}")

    original_rows = len(data)
    missing_values = data[REQUIRED_COLUMNS].isna().sum().to_dict()
    duplicate_rows = int(data.duplicated(subset=["date", "product"]).sum())

    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    invalid_dates = int(data["date"].isna().sum())
    numeric_missing = {
        column: int(data[column].isna().sum()) for column in NUMERIC_COLUMNS
    }
    invalid_numeric_rows = int(data[NUMERIC_COLUMNS].isna().any(axis=1).sum())

    if duplicate_rows:
        raise ValueError(
            f"Found {duplicate_rows} duplicate date/product records. "
            "Resolve duplicates before modelling."
        )
    if invalid_dates or invalid_numeric_rows:
        raise ValueError(
            f"Invalid dates: {invalid_dates}; rows with missing/non-numeric "
            f"numeric fields: {invalid_numeric_rows}. Review the raw dataset."
        )

    checks = {
        "negative_units_sold": int((data["units_sold"] < 0).sum()),
        "negative_stock": int((data["stock_available"] < 0).sum()),
        "negative_simulated_demand": int((data["simulated_demand"] < 0).sum()),
        "sales_above_stock": int((data["units_sold"] > data["stock_available"]).sum()),
        "sales_above_simulated_demand": int(
            (data["units_sold"] > data["simulated_demand"]).sum()
        ),
        "invalid_discount": int(
            ((data["discount"] < 0) | (data["discount"] > 1)).sum()
        ),
        "invalid_month": int(((data["month"] < 1) | (data["month"] > 12)).sum()),
        "invalid_day_of_week": int(
            ((data["day_of_week"] < 0) | (data["day_of_week"] > 6)).sum()
        ),
    }
    failed_checks = {name: count for name, count in checks.items() if count > 0}
    if failed_checks:
        raise ValueError(f"Data validation failed: {failed_checks}")

    # The generator should produce complete records; do not silently delete data.
    data = data.sort_values(["date", "product"]).reset_index(drop=True)
    data["date"] = data["date"].dt.strftime("%Y-%m-%d")
    data.to_csv(output, index=False)

    report = {
        "dataset": "synthetic_sales.csv",
        "data_notice": "Simulated academic data; not real supermarket POS records.",
        "rows_before": original_rows,
        "rows_after": len(data),
        "columns": len(data.columns),
        "missing_values_before_conversion": missing_values,
        "numeric_missing_after_conversion": numeric_missing,
        "duplicate_date_product_records": duplicate_rows,
        "validation_checks": checks,
        "status": "passed",
        "prepared_file": str(output.relative_to(root)),
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Validation passed for {len(data):,} rows.")
    print(f"Prepared dataset: {output}")
    print(f"Quality report: {report_path}")
    print("No rows were silently removed.")


if __name__ == "__main__":
    main()
