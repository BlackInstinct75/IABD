# Matriz de métricas de calidad (antes → después)

Dataset `sales_raw.csv`: 86 536 filas → 85 519 curadas (1 017 en cuarentena). Generada por `EDA_sales.py` (ver también `quality_metrics.csv`).

| ID | Dimensión | Regla | Umbral | Antes | Después | Δ p.p. | Incid. antes → después | Interpretación |
|---|---|---|---:|---:|---:|---:|---:|---|
| R1 | Completitud | `precio` no nulo | ≥99 % | 96,00 % | 100,00 % | +4,00 | 3 459 → 0 | Antes incumplía: 1 720 precios vacíos y 1 739 con coma decimal que no se tipaban como número. Tras convertir comas e imputar con la mediana del SKU (flag `flag_precio_imputado`) se cumple. |
| R2 | Completitud | `unidades` no nulo | ≥99 % | 100,00 % | 100,00 % | 0,00 | 0 → 0 | Sin problema; no requiere tratamiento. |
| R3 | Completitud | `importe` no nulo | ≥99 % | 97,20 % | 99,18 % | +1,98 | 2 421 → 703 | Se recalcula `unidades*precio` cuando falta y `unidades>=0`. Quedan 703 nulos a propósito: son las filas con unidades negativas, donde no se sabe si el importe debe ser negativo (posible devolución). |
| R4 | Unicidad | sin filas duplicadas exactas | =100 % | 99,01 % | 100,00 % | +0,99 | 856 → 0 | Se elimina la copia exacta y se conserva la primera aparición. |
| R5 | Validez | `canal ∈ {tienda,web,app}` | =100 % | 97,00 % | 100,00 % | +3,00 | 2 596 → 0 | `Web`, `WEB`, ` wEb `, `W` y `online` se normalizan a `web`; todo queda mapeado, sin valores desconocidos. |
| R6 | Validez | `unidades >= 0` | ≥99 % | 99,17 % | 99,18 % | +0,01 | 719 → 703 | Cumplía ya el umbral. Los negativos **no se borran**: se etiquetan (`flag_unidades_neg`) porque pueden ser devoluciones. Sólo baja por los duplicados/fechas eliminados. |
| R7 | Validez | `precio > 0` | ≥99 % | 96,00 % | 100,00 % | +4,00 | 3 459 → 0 | Mismas filas que R1: nulo por vacío o por coma. No había precios ≤ 0 reales. |
| R8 | Validez | fecha en [2024-01-01, 2025-12-31] | =100 % | 99,81 % | 100,00 % | +0,19 | 161 → 0 | Las 161 filas con fecha `2099-01-01` no son recuperables (no se puede inferir la fecha real): se mueven a cuarentena. |
| R9 | Consistencia | `importe ≈ unidades*precio` (±2 %) | ≥98 % | 99,17 % | 99,19 % | +0,01 | 681 → 689 | Se cumple el umbral antes y después: el tratamiento **no mejora** esta regla porque las ~690 filas discrepantes no se corrigen, se etiquetan (`flag_importe_inconsistente`) para no decidir cuál de los dos valores es el correcto. |

**Otras observaciones (no son reglas de umbral):**
- **Puntualidad:** `max(fecha)` = 2024-08-29 (periodo 2024-06-01 → 2024-08-29, 90 días sin huecos). Es un snapshot histórico, así que el SLA D+1 no es evaluable; en producción habría que comprobarlo contra la fecha de carga.
- **Unidades = 0:** 13 050 filas (15,3 %) tienen 0 unidades e importe 0. No incumplen ninguna regla pero es mucho: se etiquetan (`flag_unidades_cero`) y habría que preguntar al origen si son líneas anuladas.
- **Outliers de precio (IQR > 42,64 €):** 2 277 filas (2,7 %), máximo 124,26 €. Forman la cola larga de una distribución asimétrica, sin valores imposibles: se etiquetan (`flag_precio_outlier`) y se conservan.
- **Clave `(fecha, tienda_id, sku)`:** no es una clave de negocio en estos datos (hay muchas filas distintas con la misma combinación, 5 687 repeticiones), por eso la unicidad se define sobre la fila completa.
