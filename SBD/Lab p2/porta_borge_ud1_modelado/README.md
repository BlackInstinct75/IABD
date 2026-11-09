# UD1 · Modelado documental y analítico (JSON ↔ Parquet + DuckDB)

**Autor:** Francisco Javier Porta Borge

## Contenido de la entrega

- `respuestas.md`: decisiones de modelado, ejemplo de JSON, comparación documental/analítico.
- `p2_duckdb.sql`: carga, exportación a Parquet y consultas.
- `README.md`: este archivo.

No se incluyen datos generados, Parquet ni entornos virtuales (se regeneran con el material de partida).

## Cómo reproducirlo

Con el material de partida (`lab_p2_modelado_documental_analitico.zip`) descomprimido en una carpeta, y `p2_duckdb.sql` de esta entrega copiado encima del original:

```bash
pip install -r requirements.txt
python genera_datos_p2.py
duckdb -c ".read p2_duckdb.sql"
```

Sin la CLI de DuckDB, desde Python:

```python
import duckdb
con = duckdb.connect()
sql = open("p2_duckdb.sql", encoding="utf-8").read()
for stmt in [s.strip() for s in sql.split(";\n") if s.strip()]:
    res = con.execute(stmt)
    try:
        print(res.fetchall()[:10])
    except Exception:
        pass
```

Ejecutar siempre desde la carpeta que contiene `data/`. `INSTALL parquet` necesita conexión la primera vez; en versiones recientes de DuckDB el soporte Parquet ya viene incluido.

## Nota sobre reproducibilidad

El generador original fija `random.seed(13)` pero **no** la semilla de NumPy, por lo que `qty`, `price` y `cost` varían entre ejecuciones. Para obtener las cifras citadas en `respuestas.md`, cambiar localmente la línea inicial por:

```python
random.seed(13); np.random.seed(13)
```

Sin ese cambio, el número de pedidos y las estructuras serán similares, pero los importes y el ranking de productos pueden diferir.

## Versiones usadas

Python 3, `pandas`, `pyarrow`, `duckdb` (probado con DuckDB 2.0.0).
