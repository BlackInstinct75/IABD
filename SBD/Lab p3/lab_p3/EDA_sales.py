# -*- coding: utf-8 -*-
"""
UD1 · Tarea guiada — EDA + Calidad + Parquet + DuckDB (dataset: ventas)

Reproducir:   python EDA_sales.py
Entrada:      data/sales_raw.csv   (regenerable con gen_sales.py, semilla fija)
Salidas:      data_curated/parquet/anio=YYYY/mes=MM/*.parquet
              data_curated/quarantine/rows_removed.csv
              figures/*.png
              quality_metrics.csv / quality_metrics.md / quality_report.json
              benchmark.csv / partition_benchmark.csv
"""
import json, time, shutil, statistics
from pathlib import Path

import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
RAW = BASE / "data" / "sales_raw.csv"
CUR = BASE / "data_curated"
PARQ = CUR / "parquet"
QUAR = CUR / "quarantine"
FIG = BASE / "figures"
BENCH_TMP = BASE / "data" / "_bench_tmp"
for p in (CUR, QUAR, FIG):
    p.mkdir(parents=True, exist_ok=True)

CANALES = {"tienda", "web", "app"}
CANAL_MAP = {"web": "web", "tienda": "tienda", "app": "app", "online": "web", "w": "web"}
TOL = 0.02                 # tolerancia de consistencia importe ≈ unidades*precio
FECHA_MAX = pd.Timestamp("2025-12-31")   # fecha máxima razonable para el negocio
FECHA_MIN = pd.Timestamp("2024-01-01")
KEY_COLS = ["fecha", "tienda_id", "sku", "canal", "unidades", "precio", "importe"]


# ----------------------------------------------------------------------------
# 1) Lectura "estricta" (ANTES): todo como texto, tipado sin arreglar nada
# ----------------------------------------------------------------------------
def read_raw_strict() -> pd.DataFrame:
    df = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    out = pd.DataFrame(index=df.index)
    out["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="coerce")
    out["tienda_id"] = df["tienda_id"]
    out["sku"] = df["sku"]
    out["canal"] = df["canal"]                                   # sin normalizar
    out["unidades"] = pd.to_numeric(df["unidades"], errors="coerce")
    out["precio"] = pd.to_numeric(df["precio"], errors="coerce")   # "12,5" -> NaN (tipado roto)
    out["importe"] = pd.to_numeric(df["importe"], errors="coerce")
    out["_precio_txt"] = df["precio"]
    return out


# ----------------------------------------------------------------------------
# 2) Métricas de calidad (misma función para ANTES y DESPUÉS)
# ----------------------------------------------------------------------------
def quality_rules(df: pd.DataFrame) -> dict:
    n = len(df)
    r = {}
    r["R1_completitud_precio"] = df["precio"].notna().mean()
    r["R2_completitud_unidades"] = df["unidades"].notna().mean()
    r["R3_completitud_importe"] = df["importe"].notna().mean()
    # R4: unicidad = filas que NO son copia exacta de otra anterior
    r["R4_unicidad_fila_completa"] = 1 - df.duplicated(subset=KEY_COLS).mean()
    # R5/R6/R7/R8: validez
    r["R5_validez_canal"] = df["canal"].isin(CANALES).mean()
    r["R6_validez_unidades_ge0"] = (df["unidades"] >= 0).mean()
    r["R7_validez_precio_gt0"] = (df["precio"] > 0).mean()
    r["R8_validez_fecha_rango"] = pd.to_datetime(df["fecha"]).between(FECHA_MIN, FECHA_MAX).mean()
    # R9: consistencia entre columnas, sobre filas con los 3 campos informados
    t = df.dropna(subset=["unidades", "precio", "importe"])
    esperado = t["unidades"] * t["precio"]
    ok = (t["importe"] - esperado).abs() <= np.maximum(TOL * esperado.abs(), 0.01)
    r["R9_consistencia_importe"] = ok.mean()
    r["_n_R9"] = len(t)
    r["_n"] = n
    return {k: float(v) for k, v in r.items()}


RULES = {
    "R1_completitud_precio": ("Completitud", "precio no nulo", "precio", 0.99),
    "R2_completitud_unidades": ("Completitud", "unidades no nulo", "unidades", 0.99),
    "R3_completitud_importe": ("Completitud", "importe no nulo", "importe", 0.99),
    "R4_unicidad_fila_completa": ("Unicidad", "sin filas duplicadas exactas", "todas", 1.00),
    "R5_validez_canal": ("Validez", "canal ∈ {tienda,web,app}", "canal", 1.00),
    "R6_validez_unidades_ge0": ("Validez", "unidades >= 0", "unidades", 0.99),
    "R7_validez_precio_gt0": ("Validez", "precio > 0", "precio", 0.99),
    "R8_validez_fecha_rango": ("Validez", "fecha en [2024-01-01, 2025-12-31]", "fecha", 1.00),
    "R9_consistencia_importe": ("Consistencia", "importe ≈ unidades*precio (±2%)", "importe,unidades,precio", 0.98),
}


# ----------------------------------------------------------------------------
# 3) Tratamientos: limpiar / etiquetar / eliminar (solo lo irrecuperable)
# ----------------------------------------------------------------------------
def treat(raw_strict: pd.DataFrame):
    df = raw_strict.copy()
    log = {}

    # --- LIMPIAR: tipado de decimales con coma en precio ("12,5" -> 12.5)
    comma = df["_precio_txt"].str.contains(",", regex=False)
    df["precio"] = pd.to_numeric(df["_precio_txt"].str.replace(",", ".", regex=False), errors="coerce")
    log["precio_coma_recuperados"] = int(comma.sum())

    # --- LIMPIAR: canal (trim + minúsculas + mapeo de sinónimos)
    canal_in = df["canal"]
    df["canal"] = canal_in.str.strip().str.lower().map(CANAL_MAP)
    log["canal_normalizados"] = int((canal_in != df["canal"]).sum())
    log["canal_sin_mapeo"] = int(df["canal"].isna().sum())

    # --- ETIQUETAR: señales que NO se borran
    df["flag_unidades_neg"] = (df["unidades"] < 0).astype(int)    # posibles devoluciones
    df["flag_unidades_cero"] = (df["unidades"] == 0).astype(int)  # venta de 0 uds (sospechoso)
    df["flag_precio_imputado"] = df["precio"].isna().astype(int)

    # --- LIMPIAR (imputar): precio faltante = mediana del SKU (fallback: mediana global)
    med_sku = df.groupby("sku")["precio"].transform("median")
    df["precio"] = df["precio"].fillna(med_sku).fillna(df["precio"].median())
    log["precio_imputados"] = int(df["flag_precio_imputado"].sum())

    # --- LIMPIAR: importe faltante = unidades*precio, SOLO si unidades >= 0
    #     (con unidades negativas no sabemos si es devolución -> se deja nulo y flag)
    falta = df["importe"].isna() & (df["unidades"] >= 0)
    df["flag_importe_recalculado"] = falta.astype(int)
    df.loc[falta, "importe"] = (df["unidades"] * df["precio"]).round(2)
    log["importe_recalculados"] = int(falta.sum())

    # --- ETIQUETAR: importe inconsistente (se conserva el valor original)
    esperado = df["unidades"] * df["precio"]
    desvio = (df["importe"] - esperado).abs()
    df["flag_importe_inconsistente"] = (
        df["importe"].notna() & (desvio > np.maximum(TOL * esperado.abs(), 0.01))
    ).astype(int)
    log["importe_inconsistente_etiquetados"] = int(df["flag_importe_inconsistente"].sum())

    # --- ETIQUETAR: outliers de precio por IQR (se investigan, NO se borran)
    q1, q3 = df["precio"].quantile([0.25, 0.75])
    hi = q3 + 1.5 * (q3 - q1)
    df["flag_precio_outlier"] = (df["precio"] > hi).astype(int)
    log["precio_outlier_umbral_iqr"] = round(float(hi), 2)
    log["precio_outliers_etiquetados"] = int(df["flag_precio_outlier"].sum())

    # --- ELIMINAR (cuarentena): fecha fuera de rango (2099) -> irrecuperable
    mala_fecha = ~df["fecha"].between(FECHA_MIN, FECHA_MAX)
    quarantine = df[mala_fecha].copy()
    quarantine["motivo"] = "fecha fuera de rango / no parseable"
    df = df[~mala_fecha]
    log["filas_eliminadas_fecha"] = int(mala_fecha.sum())

    # --- ELIMINAR: duplicados exactos (se conserva la primera aparición)
    dup = df.duplicated(subset=KEY_COLS, keep="first")
    q2 = df[dup].copy()
    q2["motivo"] = "duplicado exacto"
    quarantine = pd.concat([quarantine, q2])
    df = df[~dup]
    log["filas_eliminadas_duplicado"] = int(dup.sum())

    df = df.drop(columns=["_precio_txt"]).reset_index(drop=True)
    quarantine = quarantine.drop(columns=["_precio_txt"])
    df["anio"] = df["fecha"].dt.year.astype("int16")
    df["mes"] = df["fecha"].dt.month.astype("int8")
    df["fecha"] = df["fecha"].dt.date
    df["unidades"] = df["unidades"].astype("int16")
    df["precio"] = df["precio"].round(2)
    return df, quarantine, log


# ----------------------------------------------------------------------------
# 4) Visualizaciones (4) con insight en el título
# ----------------------------------------------------------------------------
def make_figures(raw, cur):
    plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False})

    # F1 canal antes/después
    raw_c = raw["canal"].value_counts()
    cur_c = cur["canal"].value_counts()
    cats = list(raw_c.index)
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
    ax[0].barh(cats, raw_c.values, color="#c0504d"); ax[0].set_title("ANTES: 8 variantes de canal (valores crudos)")
    ax[0].invert_yaxis()
    ax[1].barh(cur_c.index, cur_c.values, color="#4a7ebb"); ax[1].set_title("DESPUÉS: 3 canales válidos")
    ax[1].invert_yaxis()
    fig.tight_layout(); fig.savefig(FIG / "f1_canal_antes_despues.png"); plt.close(fig)

    # F2 distribución de precio + outliers
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
    ax[0].hist(cur["precio"], bins=60, color="#4a7ebb")
    ax[0].axvline(cur.loc[cur.flag_precio_outlier == 1, "precio"].min(), color="red", ls="--", label="umbral IQR")
    ax[0].set_title("Precio: asimétrico a la derecha (gamma)"); ax[0].set_xlabel("€"); ax[0].legend()
    ax[1].boxplot(cur["precio"], orientation="horizontal", showfliers=True, flierprops={"markersize": 2})
    ax[1].set_title("Boxplot precio: cola larga, sin valores imposibles")
    fig.tight_layout(); fig.savefig(FIG / "f2_precio_distribucion.png"); plt.close(fig)

    # F3 unidades
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    vc = raw["unidades"].value_counts().sort_index()
    ax.bar(vc.index.astype(int), vc.values, color=["#c0504d" if i <= 0 else "#4a7ebb" for i in vc.index])
    ax.set_title("Unidades (crudo): negativos (<0) y 15% de ceros"); ax.set_xlabel("unidades")
    fig.tight_layout(); fig.savefig(FIG / "f3_unidades.png"); plt.close(fig)

    # F4 serie diaria
    d = cur.groupby("fecha").size()
    fig, ax = plt.subplots(figsize=(11, 3.4))
    ax.plot(pd.to_datetime(d.index), d.values, color="#4a7ebb")
    ax.set_ylim(0, d.max() * 1.15)
    ax.set_title("Filas por día (curado): serie estable ≈800-1100, sin huecos")
    fig.tight_layout(); fig.savefig(FIG / "f4_serie_diaria.png"); plt.close(fig)

    # F5 consistencia
    t = cur.dropna(subset=["importe"])
    dev = ((t["importe"] - t["unidades"] * t["precio"]) / (t["unidades"] * t["precio"]).replace(0, np.nan)).dropna()
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.hist(dev.clip(-0.06, 0.06), bins=80, color="#4a7ebb")
    ax.axvline(-TOL, color="red", ls="--"); ax.axvline(TOL, color="red", ls="--")
    ax.set_title("Desvío relativo importe vs unidades·precio (tolerancia ±2%)")
    fig.tight_layout(); fig.savefig(FIG / "f5_consistencia_importe.png"); plt.close(fig)


# ----------------------------------------------------------------------------
# 5) Export Parquet + benchmark de layout/compresión + CSV vs Parquet
# ----------------------------------------------------------------------------
def dir_size(p: Path) -> int:
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())


def timeit(con, sql, reps=7):
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter(); con.execute(sql).fetchall(); ts.append(time.perf_counter() - t0)
    return statistics.median(ts) * 1000  # ms


def export_and_bench(cur: pd.DataFrame):
    if BENCH_TMP.exists():
        shutil.rmtree(BENCH_TMP)
    BENCH_TMP.mkdir(parents=True)
    con = duckdb.connect()
    con.register("cur", cur)

    # --- layouts candidatos
    layouts = {}
    for comp in ("snappy", "zstd"):
        for name, part in (("sin_particion", None), ("anio_mes", "anio, mes"), ("anio_mes_canal", "anio, mes, canal")):
            out = BENCH_TMP / f"{name}_{comp}"
            if part:
                con.execute(f"COPY cur TO '{out}' (FORMAT PARQUET, COMPRESSION {comp}, PARTITION_BY ({part}))")
                glob = f"{out}/**/*.parquet"
            else:
                out.mkdir()
                con.execute(f"COPY cur TO '{out}/data.parquet' (FORMAT PARQUET, COMPRESSION {comp})")
                glob = f"{out}/*.parquet"
            layouts[f"{name}|{comp}"] = (out, glob)

    q_mes = "SELECT canal, SUM(importe) FROM {src} WHERE mes = 7 GROUP BY 1"
    q_all = "SELECT canal, SUM(importe) s, AVG(precio) FROM {src} GROUP BY 1 ORDER BY s DESC"
    rows = []
    for key, (out, glob) in layouts.items():
        name, comp = key.split("|")
        src = f"read_parquet('{glob}', hive_partitioning=true)"
        files = len(list(out.rglob("*.parquet")))
        rows.append({"layout": name, "compresion": comp, "ficheros": files,
                     "tamano_KB": round(dir_size(out) / 1024, 1),
                     "q_mes_ms": round(timeit(con, q_mes.format(src=src)), 2),
                     "q_agregado_ms": round(timeit(con, q_all.format(src=src)), 2)})
    part_bench = pd.DataFrame(rows)
    part_bench.to_csv(BASE / "partition_benchmark.csv", index=False)

    # --- layout elegido -> data_curated/parquet
    if PARQ.exists():
        shutil.rmtree(PARQ)
    con.execute(f"COPY cur TO '{PARQ}' (FORMAT PARQUET, COMPRESSION zstd, PARTITION_BY (anio, mes))")

    # --- CSV vs Parquet (mismo contenido curado, + CSV crudo)
    csv_cur = BENCH_TMP / "curado.csv"
    con.execute(f"COPY cur TO '{csv_cur}' (HEADER, DELIMITER ',')")
    srcs = {
        "CSV crudo (sales_raw.csv)": (f"read_csv('{RAW}', header=true, all_varchar=true)", RAW.stat().st_size),
        "CSV curado": (f"read_csv('{csv_cur}', header=true)", csv_cur.stat().st_size),
        "Parquet curado (anio/mes, zstd)": (f"read_parquet('{PARQ}/**/*.parquet', hive_partitioning=true)", dir_size(PARQ)),
    }
    qs = {
        "Q1 agregado por canal": "SELECT canal, SUM(CAST(importe AS DOUBLE)) FROM {src} GROUP BY 1",
        "Q2 top-10 SKU por importe": "SELECT sku, SUM(CAST(importe AS DOUBLE)) s FROM {src} GROUP BY 1 ORDER BY s DESC LIMIT 10",
        "Q3 filtro mes=7 (poda)": "SELECT COUNT(*) FROM {src} WHERE CAST(fecha AS DATE) >= DATE '2024-07-01' AND CAST(fecha AS DATE) < DATE '2024-08-01'",
    }
    brows = []
    for sname, (src, size) in srcs.items():
        row = {"fuente": sname, "tamano_KB": round(size / 1024, 1)}
        for qn, q in qs.items():
            row[qn + " (ms)"] = round(timeit(con, q.format(src=src)), 2)
        brows.append(row)
    bench = pd.DataFrame(brows)
    bench.to_csv(BASE / "benchmark.csv", index=False)
    shutil.rmtree(BENCH_TMP)
    return part_bench, bench


# ----------------------------------------------------------------------------
def main():
    raw = read_raw_strict()
    before = quality_rules(raw)
    cur, quarantine, log = treat(raw)
    after = quality_rules(cur)

    # EDA numérico (tabla por columna, sobre curado)
    prof = []
    for c in ["unidades", "precio", "importe"]:
        s = cur[c]; q1, q3 = s.quantile([.25, .75]); iqr = q3 - q1
        prof.append({"columna": c, "completitud_%": round(100 * s.notna().mean(), 2), "distintos": int(s.nunique()),
                     "min": s.min(), "p25": q1, "mediana": s.median(), "p75": q3, "max": s.max(),
                     "outliers_IQR": int(((s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)).sum())})
    pd.DataFrame(prof).round(2).to_csv(BASE / "eda_profile_columns.csv", index=False)

    make_figures(raw, cur)
    quarantine.to_csv(QUAR / "rows_removed.csv", index=False)
    part_bench, bench = export_and_bench(cur)

    # Matriz de métricas
    mrows = []
    for rid, (dim, desc, cols, thr) in RULES.items():
        b, a = before[rid], after[rid]
        n_b = int(round((1 - b) * (before["_n_R9"] if rid.startswith("R9") else before["_n"])))
        n_a = int(round((1 - a) * (after["_n_R9"] if rid.startswith("R9") else after["_n"])))
        mrows.append({"rule_id": rid.split("_")[0], "dimension": dim, "description": desc, "columns": cols,
                      "threshold": thr, "before_ratio": round(b, 4), "after_ratio": round(a, 4),
                      "delta_pp": round(100 * (a - b), 2), "incidents_before": n_b, "incidents_after": n_a,
                      "cumple_despues": bool(a >= thr)})
    mm = pd.DataFrame(mrows)
    mm.to_csv(BASE / "quality_metrics.csv", index=False)

    report = {"dataset": "sales", "rows_before": len(raw), "rows_after": len(cur),
              "rows_quarantine": len(quarantine), "treatment_log": log,
              "metrics_before": before, "metrics_after": after,
              "timeliness": {"max_date": str(max(cur["fecha"])), "min_date": str(min(cur["fecha"]))},
              "sizes_kb": {r["fuente"]: r["tamano_KB"] for r in bench.to_dict("records")}}
    (BASE / "quality_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)
    print(mm.to_string(index=False)); print(); print(json.dumps(log, indent=2))
    print("\nfilas:", len(raw), "->", len(cur), "| cuarentena:", len(quarantine))
    print("\nEDA por columna:\n", pd.DataFrame(prof).round(2).to_string(index=False))
    print("\nBenchmark layouts:\n", part_bench.to_string(index=False))
    print("\nBenchmark CSV vs Parquet:\n", bench.to_string(index=False))


if __name__ == "__main__":
    main()
