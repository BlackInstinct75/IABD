# Mini-práctica P3 — EDA y Calidad con DuckDB (UD1 · Parte 4)

**Objetivo.** Practicar un flujo completo de **EDA + calidad**: lectura con problemas reales (decimales, nulos, duplicados, dominios inconsistentes), **decidir** (eliminar/limpiar/etiquetar), **publicar en Parquet particionado**, y **verificar** con SQL en **DuckDB**.  
**Alternativa “legado”**: si prefieres, puedes hacer la versión antigua con **MongoDB + `sales.json`** (ver al final).

## 0) Requisitos
```bash
pip install pandas pyarrow duckdb
```
*(Opcional para checks con CLI)* Instala el **CLI** de DuckDB (ver `README_instalacion_duckdb.md` del lab P2).

## 1) Datos
Ya tienes un `data/sales_raw.csv` con **errores intencionados** (canales inconsistentes, decimales con coma, nulos, unidades negativas, fechas 2099, duplicados).  
Si quieres regenerarlo:
```bash
python gen_sales.py
```

## 2) Ejecutar la limpieza y publicar Parquet
```bash
python eda_quality.py
```
Esto genera:
- `data/curated/anio=YYYY/mes=MM/...parquet` (particionado)
- `quality_report.json` (métricas antes/después + tamaños)
- `duckdb_checks.sql` (carga el dataset y reusa `duckdb_checks_template.sql`)

## 3) Verificar con DuckDB
**Con CLI:**
```bash
duckdb -c ".read duckdb_checks.sql"
```
**Con Python (si no tienes CLI):**
```bash
python - << 'PY'
import duckdb, pathlib
sql = pathlib.Path("duckdb_checks.sql").read_text(encoding="utf-8")
con = duckdb.connect()
con.execute(sql)
print("Checks ejecutados.")
PY
```

## 4) Informe de calidad (entregable)
Rellena la plantilla `UD1_Informe_Calidad_template.md` con:
- Tabla **antes → después** por regla (usa `quality_report.json` y, si quieres, `quality_metrics_template.csv`).
- Decisiones **eliminar/limpiar/etiquetar** + ejemplos.
- Impacto **CSV vs Parquet** (tamaño y tiempos de 2–3 consultas si mides con DuckDB).

## 5) Rúbrica rápida (/10)
- (3) Limpieza y tipado correctos (decisiones justificadas).
- (3) Publicación en **Parquet** particionado (estructura y compresión).
- (2) Verificaciones DuckDB OK y comentadas.
- (2) Informe claro con métricas y conclusiones coste/calidad.

## 6) Opción “legado” (MongoDB + `sales.json`)
Si quieres repetir la práctica antigua:
1. Convierte `data/sales_raw.csv` a NDJSON (una línea por documento) con un `items` anidado si lo deseas.  
2. Importa a MongoDB (Docker):
   ```bash
   docker run -d --name mongo -p 27017:27017 mongo:6
   docker exec -i mongo mongoimport --db sbd --collection sales --type json --file /dev/stdin < data/sales.ndjson
   docker exec -it mongo mongosh
   ```
3. En `mongosh`, crea índices y agrega por canal/mes y consistencia de `importe` (~precio*unidades).  
4. Compara esfuerzo y latencia con la ruta **Parquet + DuckDB** y saca conclusiones.
