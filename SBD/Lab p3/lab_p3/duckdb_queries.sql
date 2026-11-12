-- duckdb_queries.sql — Consultas de validación sobre el Parquet curado
-- Reproducir (desde la raíz del proyecto, tras ejecutar `python EDA_sales.py`):
--   duckdb -c ".read duckdb_queries.sql"
--   (o con Python: duckdb.connect().execute(open('duckdb_queries.sql').read()))

CREATE OR REPLACE VIEW sales_curated AS
SELECT * FROM read_parquet('data_curated/parquet/**/*.parquet', hive_partitioning = true);

-- V1) Reglas de calidad sobre el dataset curado (debe cumplir umbrales)
SELECT
  ROUND(100.0 * AVG((precio IS NOT NULL)::INT), 2)                              AS pct_precio_no_nulo,
  ROUND(100.0 * AVG((canal IN ('tienda','web','app'))::INT), 2)                 AS pct_canal_valido,
  ROUND(100.0 * AVG((unidades >= 0)::INT), 2)                                   AS pct_unidades_ge0,
  ROUND(100.0 * AVG((precio > 0)::INT), 2)                                      AS pct_precio_gt0,
  ROUND(100.0 * AVG((fecha BETWEEN DATE '2024-01-01' AND DATE '2025-12-31')::INT), 2) AS pct_fecha_rango
FROM sales_curated;

-- V2) Unicidad: duplicados exactos restantes (esperado: 0)
SELECT COUNT(*) AS filas_duplicadas_exactas FROM (
  SELECT fecha, tienda_id, sku, canal, unidades, precio, importe, COUNT(*) c
  FROM sales_curated GROUP BY ALL HAVING COUNT(*) > 1
);

-- V3) Consistencia importe ≈ unidades*precio (±2%) y filas etiquetadas
SELECT
  COUNT(*) FILTER (WHERE importe IS NOT NULL)                                      AS filas_con_importe,
  COUNT(*) FILTER (WHERE importe IS NOT NULL
                   AND ABS(importe - unidades*precio) <= GREATEST(0.02*ABS(unidades*precio), 0.01)) AS consistentes,
  SUM(flag_importe_inconsistente)                                                  AS etiquetadas_inconsistentes
FROM sales_curated;

-- V4) Resumen de etiquetas de calidad (trazabilidad de decisiones)
SELECT SUM(flag_precio_imputado)       AS precio_imputado,
       SUM(flag_importe_recalculado)   AS importe_recalculado,
       SUM(flag_unidades_neg)          AS unidades_negativas,
       SUM(flag_unidades_cero)         AS unidades_cero,
       SUM(flag_precio_outlier)        AS precio_outlier_iqr
FROM sales_curated;

-- V5) Consulta de negocio (BI semanal): ventas por mes y canal, excluyendo filas dudosas
SELECT mes, canal, COUNT(*) AS lineas, ROUND(SUM(importe), 2) AS importe_total
FROM sales_curated
WHERE flag_unidades_neg = 0 AND flag_importe_inconsistente = 0
GROUP BY mes, canal ORDER BY mes, canal;

-- V6) Puntualidad: rango de fechas disponible
SELECT MIN(fecha) AS min_fecha, MAX(fecha) AS max_fecha, COUNT(DISTINCT fecha) AS dias FROM sales_curated;

-- V7) Poda de particiones: el plan sólo debe leer mes=7
EXPLAIN SELECT SUM(importe) FROM sales_curated WHERE anio = 2024 AND mes = 7;
