# UD1 · Tarea guiada: EDA + Calidad + Export a Parquet

> **RA/CE**: RA1.b (extraer información), RA1.g (criterios de calidad),
> RA3.b (tecnologías eficientes), RA4.f (visualizar resultados).

> **Problema:** Dirección necesita un dataset **fiable y eficiente** para BI semanal. Los datos actuales provocan **decisiones erróneas** y tiempos de consulta **lentos**.

El trabajo continúa lo visto en la guía de EDA/calidad: no se trata de “hacer
gráficos”, sino de justificar si el dataset puede usarse con confianza. Debes
mantener trazabilidad entre datos originales, decisiones de limpieza y dataset
curado.

## Objetivo
Entregar un **dataset curado** con **métricas de calidad** mejoradas, **Parquet particionado** y **consultas DuckDB** reproducibles.

Un dataset curado debe tener tipos correctos, reglas aplicadas, decisiones
documentadas y un formato adecuado para consulta. Si eliminas, imputas, corriges o
etiquetas datos, debe quedar claro qué ha cambiado y por qué.

## Pasos (orientativos)
1) **Perfilado inicial** y **métricas (ANTES)**.  
2) **Tratamientos** (limpiar/etiquetar; eliminar solo si procede).  
3) **Métricas (DESPUÉS)** + **Δ p.p.**  
4) **Visualizaciones** (3–5) con insight textual.  
5) **Export** a Parquet particionado (justifica particiones/compresión).  
6) **DuckDB**: 2–3 consultas de validación.  
7) **Benchmark** CSV vs Parquet (tiempo y tamaño).  
8) **Mini‑informe** (1–2 págs) con decisiones **calidad ↔ coste**.

Como mínimo, tus métricas deben cubrir completitud, duplicados/unicidad, validez
de dominios o rangos, y una regla de consistencia entre columnas. Si aparece un
valor extremo, no lo borres automáticamente: investígalo, decide y documenta.

## Entregables
- `EDA_<dataset>.ipynb`/`.py`  
- `/data_curated/parquet/` (particionado)  
- `duckdb_queries.sql`  
- `README.md` + **Matriz de métricas (CSV/MD)** + **Mini‑informe**

El `README.md` debe indicar cómo reproducir el análisis desde los datos de
partida. La matriz de métricas debe incluir valores antes/después y una frase de
interpretación por cada regla importante.

## Rúbrica (/10)
| Criterio | Puntos |
|---|---:|
| EDA completo, con perfilado, distribuciones, outliers y lectura de gráficos | 2 |
| Métricas de calidad antes/después, bien interpretadas | 2 |
| Limpieza, tipado, imputación/etiquetado y decisiones justificadas | 2 |
| Parquet, particionado, compresión y benchmark CSV vs Parquet | 2 |
| Consultas DuckDB reproducibles e informe claro sobre impacto calidad-coste | 2 |

## Nota sobre ética/RGPD
Si el dataset contiene **datos personales**, aplica **seudonimización** y evita publicar PII. Entrega `.env.example` si usas credenciales.
