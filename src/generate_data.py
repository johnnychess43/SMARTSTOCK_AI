"""Generate clearly labelled synthetic supermarket sales data for SmartStock AI."""

from pathlib import Path

import numpy as np
import pandas as pd


PRODUCTS = [
    {"product": "Milk 500ml", "category": "Dairy", "base_demand": 75, "price": 65, "shelf_life_days": 7},
    {"product": "Milk 1L", "category": "Dairy", "base_demand": 58, "price": 120, "shelf_life_days": 7},
    {"product": "Bread", "category": "Bakery", "base_demand": 90, "price": 70, "shelf_life_days": 4},
    {"product": "Bananas 1kg", "category": "Fruit", "base_demand": 42, "price": 110, "shelf_life_days": 5},
    {"product": "Tomatoes 1kg", "category": "Vegetables", "base_demand": 38, "price": 95, "shelf_life_days": 6},
    {"product": "Potatoes 1kg", "category": "Vegetables", "base_demand": 34, "price": 85, "shelf_life_days": 14},
    {"product": "Yoghurt 500ml", "category": "Dairy", "base_demand": 30, "price": 90, "shelf_life_days": 14},
    {"product": "Apples 1kg", "category": "Fruit", "base_demand": 24, "price": 220, "shelf_life_days": 14},
]


def generate_sales_data(seed: int = 42) -> pd.DataFrame:
    """Create daily product-level records from 2024 through 2025."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    rows = []

    for product in PRODUCTS:
        for date in dates:
            weekend = int(date.dayofweek >= 5)
            payday = int(date.day >= 25 or date.day <= 2)
            annual_factor = 1 + 0.08 * np.sin(2 * np.pi * date.dayofyear / 365.25)
            weekday_factor = 1.0 if weekend else 0.92
            payday_factor = 1.22 if payday else 1.0
            discount = float(rng.choice([0.0, 0.05, 0.10], p=[0.75, 0.15, 0.10]))
            discount_factor = 1 + discount * 1.5
            expected = (
                product["base_demand"]
                * annual_factor
                * (1.18 if weekend else weekday_factor)
                * payday_factor
                * discount_factor
            )
            latent_demand = max(0, int(round(rng.normal(expected, max(2, expected * 0.12)))))
            # Availability is simulated independently; units_sold can be censored by stock.
            stock_available = max(0, int(round(expected * rng.uniform(0.82, 1.35))))
            units_sold = min(latent_demand, stock_available)

            rows.append({
                "date": date.date().isoformat(),
                "product": product["product"],
                "category": product["category"],
                "unit_price_kes": product["price"],
                "discount": discount,
                "is_weekend": weekend,
                "is_payday_period": payday,
                "month": date.month,
                "day_of_week": date.dayofweek,
                "shelf_life_days": product["shelf_life_days"],
                "stock_available": stock_available,
                "units_sold": units_sold,
                "simulated_demand": latent_demand,
            })

    return pd.DataFrame(rows)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "data" / "raw" / "synthetic_sales.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = generate_sales_data()
    data.to_csv(output_path, index=False)

    print(f"Created {len(data):,} simulated records: {output_path}")
    print("Academic notice: this dataset is synthetic, not actual supermarket POS data.")


if __name__ == "__main__":
    main()
