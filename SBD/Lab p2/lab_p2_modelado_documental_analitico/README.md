# Mini-práctica P2 — Modelado documental vs analítico (JSON ↔ Parquet + DuckDB)

**Objetivo:** comparar cómo resolver las mismas preguntas con (a) un modelo documental y (b) un modelo analítico en Parquet consultado con DuckDB.

Antes de ejecutar, lee la [guía de modelado de datos](../../../01-teoria/02-almacenamiento-y-nosql/UD1_Modelado_de_Datos.md) y decide: entidad, claves y campos a calcular. Después sigue el laboratorio.

## 0) Requisitos
pip install pandas pyarrow duckdb

## 1) Generar datos
python genera_datos_p2.py

## 2) Ejecutar consultas en DuckDB
duckdb -c ".read p2_duckdb.sql"

## 3) (Opcional) MongoDB (Docker)
docker run -d --name mongo -p 27017:27017 mongo:6
docker exec -i mongo mongoimport --db sbd --collection orders --type json --file /dev/stdin < data/orders.ndjson
docker exec -it mongo mongosh
use sbd
db.orders.createIndex({customer_id:1, ts:1})
db.orders.aggregate([
  {$unwind:"$items"},
  {$group:{_id:"$items.sku", margen:{$sum:{$multiply:[{$subtract:["$items.price","$items.cost"]},"$items.qty"]}}}},
  {$sort:{margen:-1}}, {$limit:5}
])
