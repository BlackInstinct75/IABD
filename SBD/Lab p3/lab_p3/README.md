# UD1 · Tarea guiada — EDA + Calidad + Parquet + DuckDB (ventas)

## Reproducir desde los datos de partida
```bash
conda env create -f environment.yml      # o: conda env update -f environment.yml --prune
conda activate sbd-lab
pip install matplotlib                   # sólo para las figuras (no está en environment.yml)
python gen_sales.py                      # opcional: regenera data/sales_raw.csv (semilla fija)
python EDA_sales.py                      # todo el análisis, limpieza, export y benchmark
duckdb -c ".read duckdb_queries.sql"     # consultas de validación (o ejecutar el .sql desde Python)
```
Probado con Python 3.12, pandas, pyarrow y DuckDB `EDA_sales.py` es determinista salvo los tiempos del benchmark, que varían de una máquina a otra.

## Entregables
| Fichero | Contenido |
|---|---|
| `EDA_sales.py` | Perfilado, métricas antes/después, tratamientos, gráficos, export Parquet y benchmarks |
| `data_curated/parquet/anio=2024/mes=M/` | Dataset curado, Parquet particionado por año/mes, compresión zstd |
| `data_curated/quarantine/rows_removed.csv` | Filas eliminadas (1 017) con el motivo, para trazabilidad |
| `duckdb_queries.sql` | 7 consultas de validación reproducibles |
| `quality_metrics.md` / `.csv` | Matriz de métricas antes/después con interpretación |
| `quality_report.json` | Métricas en formato máquina-legible y log de tratamientos |
| `benchmark.csv`, `partition_benchmark.csv` | CSV vs Parquet; layouts y compresión |
| `figures/` | 5 gráficos del EDA |
| `UD1_Informe_Calidad.md` | Mini-informe con decisiones calidad ↔ coste |

## Esquema curado
`fecha DATE, tienda_id, sku, canal (tienda|web|app), unidades SMALLINT, precio DOUBLE, importe DOUBLE` + flags `flag_unidades_neg`, `flag_unidades_cero`, `flag_precio_imputado`, `flag_importe_recalculado`, `flag_importe_inconsistente`, `flag_precio_outlier` + particiones `anio`, `mes`.

## Resumen de decisiones
- **Limpiar:** coma decimal en `precio`, normalizar `canal`, imputar `precio` con la mediana del SKU, recalcular `importe` ausente.
- **Etiquetar (sin borrar):** unidades negativas y cero, importes inconsistentes, outliers de precio, valores imputados/recalculados.
- **Eliminar (cuarentena):** 161 fechas 2099 y 856 duplicados exactos.

## RGPD
El dataset no contiene datos personales (tienda, SKU, importes), así que no hace falta seudonimizar. No se usan credenciales, por lo que no hay `.env.example`.

## Nota sobre los scripts de la plantilla
`eda_quality.py` (de la plantilla) se mantiene como referencia pero `EDA_sales.py` corrige varios problemas: el mapeo de canal ya no deja `W` sin tratar, la unicidad no mezcla una clave que no es única con duplicados reales, la regla de fecha no depende de «hoy», y las métricas «antes» miden el dato crudo sin arreglarlo antes.
