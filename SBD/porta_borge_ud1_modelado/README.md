# UD1 · Modelado documental y consulta analítica (P2)

**Integrante:** Francisco Javier Porta Borge

## Contenido del ZIP

- `respuestas.md`: modelo documental, comparación con Parquet, reglas de calidad y limitaciones.
- `p2_duckdb.sql`: carga, controles de calidad, consultas y exportación a Parquet.
- `README.md`: este archivo.

## Requisitos

- DuckDB (cliente de línea de comandos, versión reciente): https://duckdb.org
- Python 3 (solo para generar los datos)
- Carpeta `lab_p2_modelado_documental_analitico/` del material de partida

## Reproducción (orden de ejecución)

Trabajar sobre una **copia** de la carpeta del laboratorio:

```bash
cp -r lab_p2_modelado_documental_analitico lab_copia
cd lab_copia
python genera_datos_p2.py        # genera data/orders_flat.csv y data/orders.ndjson
cp ../p2_duckdb.sql .            # sustituye al SQL de partida por el entregado
duckdb -c ".read p2_duckdb.sql"
```

## Resultados esperados

Los datos pueden variar si se vuelve a ejecutar el generador. Lo que debe cumplirse:

1. `lineas` > `pedidos` (cada pedido tiene varias líneas); `pedidos` = nº de `order_id` distintos.
2. Controles de calidad: normalmente 0 incumplimientos (el generador es sintético). `sku_repetido_en_mismo_pedido` es informativo y puede ser > 0.
3. Ventas por canal y mes: una fila por combinación canal–mes.
4. Margen por SKU: ordenado de mayor a menor; el top 5 coincide con las primeras filas.
5. Evolución temporal: pedidos, líneas y venta por mes (el primer mes no tiene variación).
6. Ticket medio por canal: una fila por canal.
7. `filas_parquet` coincide con el número de líneas del CSV.

**Comprobación manual de la lógica** (ejemplo del enunciado): `SELECT 2*5.93 + 2*7.29;` → `26.44`; margen de las dos líneas: `5.10` y `3.48`.

## Notas

- La regla de `canal` asume los valores `tienda`, `web` y `app`. Si el generador usa otros, hay que ajustar esa lista en la sección 2 del SQL.
- El Parquet y las bases generadas **no se incluyen** en el ZIP: se regeneran con los comandos anteriores.
- Las pruebas solo validan la corrección de las consultas. No son un benchmark ni prometen rendimiento.
