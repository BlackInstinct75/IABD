INSTALL parquet; LOAD parquet;
CREATE OR REPLACE TABLE orders_flat AS
SELECT *, qty*price AS importe, price - cost AS margen_u
FROM read_csv('data/orders_flat.csv', AUTO_DETECT=TRUE);
COPY (SELECT * FROM orders_flat) TO 'data/orders_flat.parquet' (FORMAT 'parquet');
SELECT canal, strftime(fecha, '%Y-%m') AS ym, ROUND(SUM(importe),2) AS venta
FROM orders_flat GROUP BY 1,2 ORDER BY 2,3 DESC;
SELECT sku, ROUND(SUM((price - cost)*qty),2) AS margen_total
FROM orders_flat GROUP BY 1 ORDER BY margen_total DESC LIMIT 5;
WITH pedidos AS (
  SELECT order_id, customer_id, MAX(fecha) AS fecha
  FROM orders_flat GROUP BY 1,2
)
SELECT customer_id, COUNT(*) AS n_pedidos
FROM pedidos
WHERE fecha >= DATE '2024-07-01'
GROUP BY 1 HAVING COUNT(*) > 5
ORDER BY n_pedidos DESC;
