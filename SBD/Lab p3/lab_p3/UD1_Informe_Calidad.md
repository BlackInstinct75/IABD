# Mini-informe de calidad — Dataset de ventas (UD1)

**Dataset:** `sales_raw.csv` · 86 536 filas × 7 columnas · 2024-06-01 → 2024-08-29 · 20 tiendas, 400 SKU, 3 canales.

## 1. ¿Se puede usar para BI con confianza?
**Apto con reservas.** Tras el tratamiento, las 9 reglas de calidad cumplen su umbral (matriz en `quality_metrics.md`). Las reservas son tres: (a) hay 703 líneas con unidades negativas cuyo importe no se ha podido determinar, (b) 689 importes (0,8 %) no cuadran con unidades × precio y se han etiquetado, no corregido, y (c) el 15 % de las líneas tiene 0 unidades, algo que debería aclararse con el origen.

## 2. Hallazgos del EDA
- **Canal:** 8 variantes de escritura para 3 valores (`Web`, `WEB`, ` wEb `, `W`, `online`…); afectaban al 3 % de las filas y habrían partido las ventas web en varias categorías en cualquier informe.
- **Precio:** 2 de cada 100 filas con precio vacío y otras 2 con coma decimal, que un lector estricto trata como no numérico (96,0 % de completitud real). La distribución es asimétrica (mediana 16,1 €, máximo 124,3 €) y los 2 277 outliers por IQR (> 42,6 €) son la cola normal de esa distribución, no errores.
- **Fechas:** 161 filas con `2099-01-01`; con ellas, un máximo de fecha y cualquier «último día disponible» saldrían mal.
- **Duplicados:** 856 filas idénticas (1 %), que inflarían ventas.
- **Unidades:** 719 negativas y 13 210 ceros (15,3 %).
- **Clave:** `(fecha, tienda, sku)` no es única por diseño (varias líneas el mismo día), por lo que no sirve para deduplicar.

Los gráficos están en `figures/` (canal antes/después, precio, unidades, serie diaria, desvío del importe).

## 3. Decisiones y su justificación
| Acción | Qué | Por qué |
|---|---|---|
| **Limpiar** | Coma decimal → punto; canal normalizado | Cambio sin pérdida de información |
| **Imputar** | 1 720 precios con la mediana del SKU (flag) | Evitar perder 2 % de filas; el precio por SKU es estable. Riesgo: el importe de esas filas es derivado, no observado |
| **Recalcular** | 1 702 importes ausentes = unidades × precio, sólo si unidades ≥ 0 | Con unidades negativas no sabemos si es devolución |
| **Etiquetar** | Negativos, ceros, outliers, importes inconsistentes | No hay evidencia para borrar; el analista decide con el flag |
| **Eliminar** | 161 fechas 2099 + 856 duplicados exactos (1 017 filas, 1,2 %) | La fecha real es irrecuperable; el duplicado exacto no aporta información. Todo queda en `quarantine/rows_removed.csv` |

**Calidad ↔ coste:** se eliminó sólo el 1,2 % de los datos y el resto se conserva con trazabilidad. El precio de esa prudencia es que el dataset sigue teniendo filas «dudosas» marcadas: la consulta V5 de `duckdb_queries.sql` muestra cómo excluirlas para el BI.

## 4. Formato y rendimiento (CSV vs Parquet)
| Fuente | Tamaño | Q1 agregado | Q2 top-10 SKU | Q3 filtro mes |
|---|---:|---:|---:|---:|
| CSV crudo (7 col.) | 3 778 KB | 35 ms | 35 ms | 32 ms |
| CSV curado (15 col.) | 5 217 KB | 74 ms | 72 ms | 70 ms |
| **Parquet curado, anio/mes, zstd** | **654 KB** | **3,5 ms** | **4,4 ms** | **1,6 ms** |

El Parquet pesa unas 6 veces menos que el CSV crudo (8 veces menos que el curado, que tiene más columnas) y sus consultas son unas 10-40 veces más rápidas (mediana de 7 ejecuciones, DuckDB; los tiempos varían según la máquina, el orden de magnitud no).

**Particionado y compresión (`partition_benchmark.csv`):** zstd ocupa ~10-28 % menos que snappy en todos los layouts. En cambio, **el particionado no mejora el rendimiento con este volumen**: un único fichero (559 KB) es igual de rápido o más que `anio/mes` (654 KB, 3 ficheros) y `anio/mes/canal` (9 ficheros) es más lento y más grande. Se ha elegido **`anio/mes` + zstd** porque es el patrón que escala (las cargas semanales se añaden como nueva partición y DuckDB poda por mes) y su coste a este tamaño es de unos milisegundos y ~100 KB; con tres meses y 85 k filas un único fichero sería igualmente válido. Particionar también por `canal` genera ficheros muy pequeños y no compensa.

## 5. Limitaciones
- Puntualidad no evaluable: es un snapshot de 2024 (último dato 2024-08-29).
- El benchmark es con datos pequeños; la ventaja de la poda de particiones sólo se vería con mucho más volumen.
- La imputación de precio asume que el SKU mantiene precio; no se ha podido verificar con una fuente externa.
- No hay datos personales, por lo que no se aplica seudonimización.
