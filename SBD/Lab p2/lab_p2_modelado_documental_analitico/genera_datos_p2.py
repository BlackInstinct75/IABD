# -*- coding: utf-8 -*-
import pandas as pd, numpy as np, json, random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(13)
Path("data").mkdir(exist_ok=True)

skus = [f"SKU{str(i).zfill(4)}" for i in range(100)]
canales = ["tienda","web","app"]

base = datetime(2024, 6, 1)
fechas = [base + timedelta(days=i) for i in range(60)]

orders_ndjson = []
rows_flat = []

order_id = 1
for d in fechas:
    for _ in range(random.randint(120, 180)):
        canal = random.choice(canales)
        customer = random.randint(1, 3000)
        n_items = random.randint(1, 4)
        items = []
        for _ in range(n_items):
            sku = random.choice(skus)
            qty = max(1, int(abs(np.random.normal(2, 1))))
            price = round(max(1.5, float(np.random.gamma(3, 5))), 2)
            cost  = round(price * random.uniform(0.5, 0.8), 2)
            items.append({"sku": sku, "qty": qty, "price": price, "cost": cost})
            rows_flat.append({
                "order_id": order_id, "customer_id": customer, "fecha": d.date().isoformat(),
                "canal": canal, "sku": sku, "qty": qty, "price": price, "cost": cost
            })
        orders_ndjson.append({
            "order_id": order_id, "customer_id": customer,
            "ts": d.isoformat()+"T12:00:00", "canal": canal, "items": items
        })
        order_id += 1

with open("data/orders.ndjson", "w", encoding="utf-8") as f:
    for doc in orders_ndjson:
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

import pandas as pd
df = pd.DataFrame(rows_flat)
df.to_csv("data/orders_flat.csv", index=False)
print("Listo: data/orders.ndjson y data/orders_flat.csv")
