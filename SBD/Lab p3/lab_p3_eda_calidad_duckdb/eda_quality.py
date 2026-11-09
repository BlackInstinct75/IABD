# -*- coding: utf-8 -*-

import pandas as pd, numpy as np, json, duckdb, os, math
from pathlib import Path
from datetime import datetime
from collections import OrderedDict

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
RAW = DATA / "sales_raw.csv"
CURATED_DIR = DATA / "curated"
CURATED_DIR.mkdir(exist_ok=True, parents=True)

def read_raw():
    df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    # strip spaces
    for col in ["fecha","tienda_id","sku","canal","precio","importe"]:
        df[col] = df[col].astype(str).str.strip()
    # tipos
    df["unidades"] = pd.to_numeric(df["unidades"], errors="coerce")
    # normaliza decimales de precio/importe
    df["precio"] = df["precio"].str.replace(",", ".", regex=False)
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
    df["importe"] = df["importe"].str.replace(",", ".", regex=False)
    df["importe"] = pd.to_numeric(df["importe"], errors="coerce")
    # fecha
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce").dt.date
    # canal normalizado
    canon = {"web":"web","tienda":"tienda","app":"app","web ":"web"," wEb ":"web","Web":"web","WEB":"web","online":"web","W":"web"}
    df["canal_norm"] = df["canal"].str.lower().str.strip().map(canon).fillna(df["canal"].str.lower().str.strip())
    return df

def compute_quality(df):
    total = len(df)
    def ratio(x): 
        return round(float(x)/total, 4) if total>0 else 0.0
    metrics = OrderedDict()

    # Completitud
    metrics["completeness"] = {
        "precio": {"value": ratio(df["precio"].notna().sum()), "threshold": 0.99},
        "unidades": {"value": ratio(df["unidades"].notna().sum()), "threshold": 0.99},
        "importe": {"value": ratio(df["importe"].notna().sum()), "threshold": 0.99},
    }
    # Unicidad de clave
    key = df[["fecha","tienda_id","sku"]].astype(str).agg("|".join, axis=1)
    dup = key.duplicated(keep=False).mean()
    metrics["uniqueness"] = {
        "fecha_tienda_sku": {"value": round(1.0 - float(dup), 4), "threshold": 1.0}
    }
    # Validez: canal in set y precio>0, unidades>=0, fecha razonable
    valid_canal = df["canal_norm"].isin(["tienda","web","app"]).mean()
    valid_precio = (df["precio"]>0).mean()
    valid_unidades = (df["unidades"]>=0).mean()
    valid_fecha = df["fecha"].notna().mean() * ((pd.to_datetime(df["fecha"], errors="coerce")<=pd.to_datetime("today")).mean())
    metrics["validity"] = {
        "canal_in_set": {"value": round(float(valid_canal),4), "threshold": 1.0},
        "precio_gt_0": {"value": round(float(valid_precio),4), "threshold": 0.99},
        "unidades_ge_0": {"value": round(float(valid_unidades),4), "threshold": 0.99},
    }
    # Consistencia importe ≈ unidades*precio (±2%)
    test = df.dropna(subset=["unidades","precio"])
    denom = (test["unidades"]*test["precio"]).abs() + 1e-9
    ok = ((df.loc[test.index, "importe"] - (test["unidades"]*test["precio"])).abs() <= 0.02*denom).mean()
    metrics["consistency"] = {
        "importe_eq_unidades_x_precio_tol2pct": {"value": round(float(ok),4), "threshold": 0.98}
    }
    # Puntualidad
    max_date = pd.to_datetime(df["fecha"], errors="coerce").max()
    lag_days = (pd.Timestamp.today().normalize() - max_date).days if pd.notna(max_date) else None
    metrics["timeliness"] = {"max_date": str(max_date.date() if pd.notna(max_date) else None), "lag_days": lag_days, "sla": "D+1 10:00"}

    return metrics

def clean_and_publish(df):
    # Decide: eliminar/limpiar/etiquetar
    # Eliminar: fechas muy futuras, unidades < 0 (pero etiquetar antes)
    df["flag_unidades_neg"] = (df["unidades"] < 0).fillna(False).astype(int)
    df["flag_precio_missing"] = df["precio"].isna().astype(int)
    df["flag_canal_invalido"] = (~df["canal_norm"].isin(["tienda","web","app"])).astype(int)

    # Limpiar: normalizar canal, imputar precio faltante con mediana por sku (si hay), si no global
    median_price_per_sku = df.groupby("sku")["precio"].median()
    df["precio"] = df.apply(lambda r: median_price_per_sku.get(r["sku"], np.nan) if pd.isna(r["precio"]) else r["precio"], axis=1)
    if df["precio"].isna().any():
        df["precio"] = df["precio"].fillna(df["precio"].median())
    # recomputar importe si falta
    df.loc[df["importe"].isna() & df["unidades"].notna() & df["precio"].notna(), "importe"] = df["unidades"]*df["precio"]

    # Normaliza canal
    df["canal"] = df["canal_norm"]

    # Etiquetar: importe inconsistente
    test = df.dropna(subset=["unidades","precio","importe"])
    denom = (test["unidades"]*test["precio"]).abs() + 1e-9
    bad = ((test["importe"] - (test["unidades"]*test["precio"])).abs() > 0.02*denom)
    df["flag_importe_inconsistente"] = 0
    df.loc[test.index[bad], "flag_importe_inconsistente"] = 1

    # Eliminar filas con fecha nula o en el futuro lejano
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df[df["fecha"].notna()]
    df = df[df["fecha"] <= pd.Timestamp.today().normalize()]

    # Deduplicar por clave manteniendo la primera
    df.sort_values(["fecha","tienda_id","sku"], inplace=True)
    df = df.drop_duplicates(subset=["fecha","tienda_id","sku","canal"], keep="first")

    # Tipos finales
    df["anio"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["fecha"] = df["fecha"].dt.date

    # Export a Parquet particionado
    import pyarrow as pa, pyarrow.parquet as pq
    table = pa.Table.from_pandas(df)
    pq.write_to_dataset(table, root_path=str(CURATED_DIR), partition_cols=["anio","mes"], compression="snappy")

    return df

def main():
    df = read_raw()
    metrics_before = compute_quality(df)
    df_clean = clean_and_publish(df.copy())
    metrics_after = compute_quality(df_clean)

    report = {
        "dataset":"sales",
        "version": datetime.now().strftime("%Y_%m_%d"),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "summary": {
            "rows_before": int(len(df)),
            "rows_after": int(len(df_clean)),
            "cols": int(df_clean.shape[1]),
            "file_sizes_bytes": {},
            "partitions": {}
        },
        "metrics": {
            "before": metrics_before,
            "after": metrics_after
        },
        "notes":"Este informe resume métricas clave y decisiones de limpieza básicas."
    }

    # Compute disk sizes
    csv_path = DATA / "sales_raw.csv"
    report["summary"]["file_sizes_bytes"]["csv"] = csv_path.stat().st_size if csv_path.exists() else None
    # Estimate parquet size by summing partition files
    pbytes = 0
    if CURATED_DIR.exists():
        for p in CURATED_DIR.rglob("*.parquet"):
            pbytes += p.stat().st_size
    report["summary"]["file_sizes_bytes"]["parquet"] = pbytes

    # partitions info
    parts = {}
    for p in CURATED_DIR.glob("anio=*"):
        anio = p.name.split("=")[1]
        months = sorted({q.name.split("=")[1] for q in p.glob("mes=*")})
        parts[anio] = months
    report["summary"]["partitions"] = parts

    # Save report JSON
    (BASE / "quality_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    # Create DuckDB checks SQL referencing the dataset through glob
    checks_sql = f\"\"\"-- Checks sobre dataset Parquet particionado
INSTALL parquet; LOAD parquet;
CREATE OR REPLACE VIEW sales_curated AS
SELECT * FROM read_parquet('{str(CURATED_DIR).replace("\\\\","/")}/anio=*/mes=*/*.parquet');

.read duckdb_checks_template.sql
\"\"\"
    (BASE / "duckdb_checks.sql").write_text(checks_sql, encoding="utf-8")

    print("Limpieza y publicación OK. quality_report.json generado.")

if __name__ == "__main__":
    main()
