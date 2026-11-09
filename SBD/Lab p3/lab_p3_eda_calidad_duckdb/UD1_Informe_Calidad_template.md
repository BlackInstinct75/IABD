# Informe de Calidad de Datos — UD1 (Plantilla)

**Proyecto:** _(rellenar)_  
**Módulo:** Sistemas de Big Data (SBD) · **Unidad:** UD1 · **Versión:** v_(YYYY_MM_DD)_  
**Autoría:** _(nombre)_ · **Fecha:** 2025-10-06

---

## 1. Resumen ejecutivo (½–1 página)
- **Objetivo del dataset:** _(qué decisión habilita)_  
- **Fuentes y periodo:** _(APIs/CSV, rango de fechas)_  
- **Principales hallazgos de calidad:** _(3–5 bullets en prosa)_  
- **Impacto en coste/tiempo:** _(CSV→Parquet, tiempos de lectura, tamaño)_  
- **Acciones tomadas:** _(eliminar/limpiar/etiquetar)_ y **riesgos residuales**.

---

## 2. Dataset y esquema esperado
- **Tabla/Conjunto:** `_(nombre)_`  
- **Tamaño bruto:** _N_ filas, _M_ columnas (antes); _N'_, _M_ (después)  
- **Esquema esperado (nombre:tipo:descripción):**
  - `fecha: DATE : fecha de la transacción`
  - `tienda_id: VARCHAR : identificador de tienda (normalizado)`
  - `sku: VARCHAR : código de producto normalizado`
  - `unidades: INTEGER : unidades vendidas`
  - `precio: DOUBLE : precio unitario`
  - `importe: DOUBLE : unidades*precio`  
  _(ajusta a tu caso)_

---

## 3. Metodología (EDA + reglas)
Describe brevemente cómo se han calculado las métricas:  
- EDA inicial (distribuciones, outliers, duplicados, tipos).  
- Reglas de **calidad**: completitud, unicidad, validez (dominio/rango/regex), consistencia entre columnas, puntualidad.  
- Umbrales pactados con negocio y tolerancias (p. ej., ±2% en `importe≈unidades*precio`).

---

## 4. Resultados de calidad (antes → después)
### 4.1 Tabla resumen de reglas
| ID | Dimensión | Regla (descripción corta) | Columnas | Umbral | Antes (%) | Después (%) | Δ p.p. | Incidencias | Decisión | Observaciones |
| -- | --------- | -------------------------- | -------- | ------ | --------: | ----------: | -----: | ----------: | ------- | ------------- |
| R1 | Completitud | `precio` no nulo | precio | ≥ 99.0% | 98.7 | 99.9 | +1.2 | 123 | Imputar mediana + flag | Separador decimal |
| R2 | Unicidad | clave `(fecha,tienda,sku)` | fecha,tienda,sku | = 100% | 99.2 | 100.0 | +0.8 | 89 | Dedup keep=first | Normaliza SKU |
| R3 | Validez | `canal ∈ {tienda,web,app}` | canal | = 100% | 95.1 | 100.0 | +4.9 | 430 | Limpiar mapeo | WEB/online→web |
| R4 | Consistencia | `importe≈unidades*precio` (±2%) | importe,unidades,precio | ≥ 98% | 92.4 | 99.1 | +6.7 | 512 | Tipado + redondeo | float/locale |
| R5 | Puntualidad | `max(fecha)` ~ D+1 (≤10:00) | fecha | SLA | — | OK | — | — | Ajuste job | — |

> _Amplía/ajusta filas según tu caso. “Incidencias” = nº de filas fuera de regla (antes o después, especifica)._

### 4.2 Métricas por columna (plantilla)
| Columna | Completitud (%) | Distintos | Min | P25 | Mediana | P75 | Max | Outliers (IQR) |
| ------ | ---------------: | --------: | ---:| ---:| ------: | ---:| ---:| -------------: |
| unidades | _ | _ | _ | _ | _ | _ | _ | _ |
| precio   | _ | _ | _ | _ | _ | _ | _ | _ |
| importe  | _ | _ | _ | _ | _ | _ | _ | _ |

---

## 5. Decisiones de tratamiento
- **Eliminar:** _(criterio + % filas afectadas + justificación)_  
- **Limpiar:** _(reglas aplicadas, mapeos, normalizaciones, corrección de tipos)_  
- **Etiquetar:** _(banderas creadas, uso esperado en análisis/modelos)_

Incluye ejemplos antes/después si ilustran un patrón (p. ej., `WEB, web, Online → web`).

---

## 6. Impacto en coste y rendimiento
- **Almacenamiento:** tamaño CSV vs Parquet (`snappy`/`zstd`), nº ficheros, particionado (`anio/mes[/día]`).  
- **Consulta:** tiempos de 2–3 queries típicas en DuckDB antes/después.  
- **Conclusión:** decisiones que se mantienen y mejoras pendientes.

---

## 7. Exportación y reproducibilidad
- Ruta de publicación: `data_lake/curated/v=YYYY_MM_DD/`  
- Formato: **Parquet**, **particionado** por `anio/mes` (y `canal` si aplica).  
- Artefactos adjuntos:
  - `quality_report.json` (métricas máquina-leyible).  
  - `duckdb_checks.sql` (consultas de verificación).  
  - `data_dictionary.md` (descripciones y dominios).

---

## 8. RGPD y gobierno (mínimo viable)
- **PII presente:** sí/no (qué campos, base jurídica).  
- **Técnicas aplicadas:** minimización, seudonimización, control de acceso (solo lectura).  
- **Retención:** _(plazo)_ · **Incidencias:** _(si las hubo)_.

---

## 9. Conclusiones y próximos pasos
- Estado de calidad: **Apto** / **Apto con reservas** / **No apto** (explica).  
- Próximos pasos: _(reglas adicionales, fuentes nuevas, automatización, alertas)_.

---

## Anexos
- Extractos de código (lectura/limpieza/exportación).  
- Gráficos de EDA (histogramas, boxplots, top-k, series).  
- Bitácora de cambios (quién, cuándo, qué).
