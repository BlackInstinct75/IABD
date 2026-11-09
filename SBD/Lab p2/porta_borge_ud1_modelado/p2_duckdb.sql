-- =====================================================================
-- P2 · Modelado documental vs analítico (JSON -> Parquet + DuckDB)
-- Ejecutar desde la carpeta que contiene data/:
--   duckdb -c ".read p2_duckdb.sql"
-- =====================================================================

-- 0) Preparación --------------------------------------------------------
INSTALL parquet; LOAD parquet;

-- Modelo analítico plano: una fila = una línea de pedido.
-- Clave de pedido: order_id (se repite en cada línea del mismo pedido).
-- Campos calculados guardados al aplanar: importe y margen.
CREATE OR REPLACE TABLE orders_flat AS
SELECT
  order_id, customer_id, fecha, canal, sku, qty, price, cost,
  qty * price                 AS importe,       -- ingreso de la línea
  (price - cost)              AS margen_u,      -- margen unitario
  qty * (price - cost)        AS margen         -- margen de la línea
FROM read_csv('data/orders_flat.csv', AUTO_DETECT = TRUE);

-- Exportación a Parquet (columnar, comprimido, tipado)
COPY (SELECT * FROM orders_flat)
TO 'data/orders_flat.parquet' (FORMAT 'parquet');

-- Comprobación de coherencia: líneas y pedidos distintos
SELECT COUNT(*) AS lineas, COUNT(DISTINCT order_id) AS pedidos FROM orders_flat;

-- Q0) Misma carga desde el modelo documental (NDJSON) ---------------------
-- DuckDB lee el JSON anidado y desanida la lista items con UNNEST.
-- `ts` se lee como texto porque el generador produce un formato inválido.
CREATE OR REPLACE TABLE orders_doc AS
SELECT order_id, customer_id, canal, items
FROM read_json('data/orders.ndjson', format = 'newline_delimited',
               columns = {order_id: 'BIGINT', customer_id: 'BIGINT',
                          ts: 'VARCHAR', canal: 'VARCHAR',
                          items: 'STRUCT(sku VARCHAR, qty INTEGER, price DOUBLE, cost DOUBLE)[]'});

-- Contraste: el margen total sale igual desde JSON que desde el plano
SELECT
  (SELECT ROUND(SUM(i.item.qty * (i.item.price - i.item.cost)), 2)
     FROM (SELECT UNNEST(items) AS item FROM orders_doc) i) AS margen_desde_json,
  (SELECT ROUND(SUM(margen), 2) FROM orders_flat)            AS margen_desde_plano;

-- Q1) Margen por producto (top 10) ----------------------------------------
SELECT sku,
       ROUND(SUM(margen), 2)                       AS margen_total,
       ROUND(100 * SUM(margen) / SUM(importe), 1)  AS margen_pct,
       SUM(qty)                                    AS unidades
FROM orders_flat
GROUP BY sku
ORDER BY margen_total DESC
LIMIT 10;

-- Q2) Evolución temporal de pedidos (por mes) ------------------------------
-- COUNT(DISTINCT order_id): cuenta pedidos, no líneas.
SELECT strftime(fecha, '%Y-%m')         AS ym,
       COUNT(DISTINCT order_id)         AS pedidos,
       ROUND(SUM(importe), 2)           AS venta,
       ROUND(SUM(importe) / COUNT(DISTINCT order_id), 2) AS ticket_medio
FROM orders_flat
GROUP BY ym
ORDER BY ym;

-- Q2b) Evolución semanal (ver tendencia con más detalle)
SELECT date_trunc('week', fecha) AS semana,
       COUNT(DISTINCT order_id)  AS pedidos
FROM orders_flat
GROUP BY semana
ORDER BY semana;

-- Q3) Consulta adicional: ticket medio y margen por canal ------------------
-- Justificación: el canal es la dimensión de negocio más clara del dataset.
-- Interesa saber si tienda, web o app difieren en ticket y rentabilidad.
-- Se agrega primero por pedido para no mezclar líneas con pedidos.
WITH pedidos AS (
  SELECT order_id, canal,
         SUM(importe) AS importe_pedido,
         SUM(margen)  AS margen_pedido
  FROM orders_flat
  GROUP BY order_id, canal
)
SELECT canal,
       COUNT(*)                                          AS pedidos,
       ROUND(AVG(importe_pedido), 2)                     AS ticket_medio,
       ROUND(SUM(margen_pedido), 2)                      AS margen_total,
       ROUND(100 * SUM(margen_pedido) / SUM(importe_pedido), 1) AS margen_pct
FROM pedidos
GROUP BY canal
ORDER BY ticket_medio DESC;

-- Q4) Clientes recurrentes (adaptación de la consulta de la plantilla) -----
-- Con ~3000 clientes y ~9000 pedidos la media es ~3 pedidos/cliente, así que
-- el filtro original (>5 pedidos desde julio) devolvería casi nada.
-- Se muestra la distribución completa y los clientes con 7 o más pedidos.
WITH pedidos AS (
  SELECT order_id, customer_id FROM orders_flat GROUP BY 1, 2
),
por_cliente AS (
  SELECT customer_id, COUNT(*) AS n_pedidos FROM pedidos GROUP BY 1
)
SELECT n_pedidos, COUNT(*) AS clientes
FROM por_cliente
GROUP BY n_pedidos
ORDER BY n_pedidos;

WITH pedidos AS (
  SELECT order_id, customer_id FROM orders_flat GROUP BY 1, 2
)
SELECT customer_id, COUNT(*) AS n_pedidos
FROM pedidos
GROUP BY customer_id
HAVING COUNT(*) >= 7
ORDER BY n_pedidos DESC, customer_id;
