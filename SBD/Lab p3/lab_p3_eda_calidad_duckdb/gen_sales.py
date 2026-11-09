# -*- coding: utf-8 -*-
import random, csv
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

random.seed(7)
np.random.seed(7)

def main():
    root = Path(__file__).resolve().parent
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)
    n_days = 90
    base_date = datetime(2024, 6, 1)
    dates = [base_date + timedelta(days=i) for i in range(n_days)]
    stores = [f"S{str(i).zfill(3)}" for i in range(1, 21)]
    skus = [f"SKU{str(i).zfill(5)}" for i in range(1, 401)]
    channels = ["tienda", "web", "app"]

    rows = []
    for d in dates:
        n_orders = random.randint(800, 1100)
        for _ in range(n_orders):
            store = random.choice(stores)
            sku = random.choice(skus)
            ch = random.choices(channels, weights=[0.45,0.4,0.15])[0]
            if random.random() < 0.03:
                ch = random.choice(["WEB","Web","online"," wEb ","W"])
            qty = max(0, int(abs(np.random.normal(2.2, 1.2))))
            if random.random() < 0.01:
                qty *= -1
            price = max(0.5, float(np.random.gamma(3, 6)))
            price_str = f"{price:.2f}"
            if random.random() < 0.02:
                price_str = ""
            elif random.random() < 0.02:
                price_str = price_str.replace(".", ",")
            amount = ""
            if price_str != "" and qty >= 0:
                p = float(price_str.replace(",", "."))
                amt = p * qty
                if random.random() < 0.03:
                    import random as r
                    amt *= r.uniform(0.97, 1.03)
                amount = f"{amt:.2f}"
            d_str = d.strftime("%Y-%m-%d")
            if random.random() < 0.002:
                d_str = "2099-01-01"
            rows.append([d_str, store, sku, ch, qty, price_str, amount])

    dups_idx = random.sample(range(len(rows)), k=int(0.01*len(rows)))
    for idx in dups_idx:
        rows.append(rows[idx])

    raw_csv = data_dir / "sales_raw.csv"
    with open(raw_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["fecha","tienda_id","sku","canal","unidades","precio","importe"])
        writer.writerows(rows)
    print("OK: data/sales_raw.csv generado")

if __name__ == "__main__":
    main()
