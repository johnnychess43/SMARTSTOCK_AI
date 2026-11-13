"""Create exploratory summaries and charts from prepared SmartStock AI data."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    source = root / "data" / "processed" / "cleaned_sales.csv"
    reports = root / "reports"
    figures = reports / "figures"
    figures.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        raise FileNotFoundError(
            f"Prepared dataset not found at {source}. "
            "Run: python src/prepare_data.py"
        )

    data = pd.read_csv(source, parse_dates=["date"])
    sns.set_theme(style="whitegrid")

    # Product-level performance summary.
    product_summary = (
        data.groupby(["product", "category"], as_index=False)
        .agg(
            total_units_sold=("units_sold", "sum"),
            average_daily_sales=("units_sold", "mean"),
            average_stock=("stock_available", "mean"),
            average_price_kes=("unit_price_kes", "mean"),
            stockout_days=("units_sold", lambda values: 0),
        )
    )
    # A stockout proxy: stock available was fully sold on that date.
    stockout_days = (
        data.assign(stockout=data["units_sold"] >= data["stock_available"])
        .groupby("product")["stockout"].sum()
    )
    product_summary["stockout_days"] = product_summary["product"].map(stockout_days)
    product_summary.to_csv(reports / "product_summary.csv", index=False)

    daily = data.groupby("date", as_index=False)["units_sold"].sum()
    daily.to_csv(reports / "daily_sales_summary.csv", index=False)

    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_summary = (
        data.groupby("day_of_week", as_index=False)["units_sold"]
        .mean()
        .rename(columns={"units_sold": "average_units_sold"})
    )
    weekday_summary["day_name"] = weekday_summary["day_of_week"].map(
        dict(enumerate(weekday_names))
    )
    weekday_summary.to_csv(reports / "weekday_summary.csv", index=False)

    occasion_summary = (
        data.groupby(["is_weekend", "is_payday_period"], as_index=False)
        .agg(
            average_units_sold=("units_sold", "mean"),
            records=("units_sold", "size"),
        )
    )
    occasion_summary.to_csv(reports / "weekend_payday_summary.csv", index=False)

    # Chart 1: total units sold by product.
    plt.figure(figsize=(10, 6))
    ordered = product_summary.sort_values("total_units_sold", ascending=False)
    sns.barplot(data=ordered, x="total_units_sold", y="product")
    plt.title("Total Units Sold by Product (Simulated Data)")
    plt.xlabel("Units sold")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(figures / "sales_by_product.png", dpi=160)
    plt.close()

    # Chart 2: daily total sales over time with a 7-day rolling average.
    daily["date"] = pd.to_datetime(daily["date"])
    daily["rolling_7_day"] = daily["units_sold"].rolling(7, min_periods=1).mean()
    plt.figure(figsize=(12, 5))
    plt.plot(daily["date"], daily["units_sold"], alpha=0.35, label="Daily sales")
    plt.plot(daily["date"], daily["rolling_7_day"], label="7-day average")
    plt.title("Daily Supermarket Units Sold (Simulated Data)")
    plt.xlabel("Date")
    plt.ylabel("Units sold")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures / "daily_sales_trend.png", dpi=160)
    plt.close()

    # Chart 3: average units sold by weekday.
    plt.figure(figsize=(9, 5))
    sns.barplot(data=weekday_summary, x="day_name", y="average_units_sold")
    plt.title("Average Sales by Day of Week (Simulated Data)")
    plt.xlabel("Day")
    plt.ylabel("Average units sold")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(figures / "sales_by_weekday.png", dpi=160)
    plt.close()

    # Chart 4: weekend and payday comparison.
    comparison = (
        data.assign(
            period=data.apply(
                lambda row: "Weekend + payday" if row["is_weekend"] and row["is_payday_period"]
                else "Weekend" if row["is_weekend"]
                else "Payday" if row["is_payday_period"]
                else "Regular day",
                axis=1,
            )
        )
        .groupby("period", as_index=False)["units_sold"]
        .mean()
        .rename(columns={"units_sold": "average_units_sold"})
    )
    comparison.to_csv(reports / "sales_period_comparison.csv", index=False)
    plt.figure(figsize=(9, 5))
    sns.barplot(data=comparison, x="period", y="average_units_sold")
    plt.title("Average Sales by Weekend and Payday Period (Simulated Data)")
    plt.xlabel("Period")
    plt.ylabel("Average units sold")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(figures / "weekend_payday_comparison.png", dpi=160)
    plt.close()

    print("Exploratory analysis completed.")
    print(f"Summary tables: {reports}")
    print(f"Charts: {figures}")
    print("Interpret all findings as patterns in simulated academic data.")


if __name__ == "__main__":
    main()
