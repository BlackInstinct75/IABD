-- =====================================================================
-- UD1 · P2 · Modelado documental y consulta analítica (DuckDB)
-- Ejecución (desde la carpeta del laboratorio):
--     duckdb -c ".read p2_duckdb.sql"
-- Entrada : data/orders_flat.csv  (una fila = una LÍNEA de pedido)
-- Salida  : tabla orders_flat en memoria + data/orders_flat.parquet
-- Datos sintéticos: sirven para validar la lógica, no como benchmark.
-- =====================================================================

-- 0. Carga con tipos explícitos --------------------------------------
-- Se fijan los tipos para no depender de la autodetección y se usa
-- DECIMAL para importes (evita errores de coma flotante).
CREATE OR REPLACE TABLE orders_flat AS
SELECT
    CAST(order_id    AS BIGINT)        AS order_id,
    CAST(customer_id AS INTEGER)       AS customer_id,
    CAST(fecha       AS DATE)          AS fecha,
    CAST(canal       AS VARCHAR)       AS canal,
    CAST(sku         AS VARCHAR)       AS sku,
    CAST(qty         AS INTEGER)       AS qty,
    CAST(price       AS DECIMAL(10,2)) AS price,   -- precio HISTÓRICO de la compra
    CAST(cost        AS DECIMAL(10,2)) AS cost
FROM read_csv('data/orders_flat.csv', AUTO_DETECT = TRUE);

-- 1. Comprobación de granularidad ------------------------------------
-- lineas = filas del CSV; pedidos = order_id distintos.
-- Un pedido con N productos ocupa N filas, por eso COUNT(*) != pedidos.
SELECT COUNT(*)                  AS lineas,
       COUNT(DISTINCT order_id)  AS pedidos
FROM orders_flat;

-- 2. Reglas de calidad (solo informan; NO borran ni modifican datos) --
-- Cada fila devuelta es una línea que incumple la regla indicada.
SELECT 'qty_no_positiva' AS regla, COUNT(*) AS incumplimientos
FROM orders_flat WHERE qty IS NULL OR qty <= 0
UNION ALL
SELECT 'precio_o_coste_negativo', COUNT(*)
FROM orders_flat WHERE price IS NULL OR cost IS NULL OR price < 0 OR cost < 0
UNION ALL
SELECT 'coste_mayor_que_precio (margen negativo)', COUNT(*)
FROM orders_flat WHERE cost > price
UNION ALL
SELECT 'canal_fuera_de_catalogo', COUNT(*)
FROM orders_flat WHERE canal NOT IN ('tienda', 'web', 'app')
UNION ALL
SELECT 'cabecera_inconsistente (pedido con >1 cliente/fecha/canal)', COUNT(*)
FROM (
    SELECT order_id
    FROM orders_flat
    GROUP BY order_id
    HAVING COUNT(DISTINCT customer_id) > 1
        OR COUNT(DISTINCT fecha)       > 1
        OR COUNT(DISTINCT canal)       > 1
)
UNION ALL
-- Limitación de P2: sin line_number, (order_id, sku) NO es clave de línea.
SELECT 'sku_repetido_en_mismo_pedido (informativa)', COUNT(*)
FROM (
    SELECT order_id, sku
    FROM orders_flat
    GROUP BY order_id, sku
    HAVING COUNT(*) > 1
);

-- 3. Ventas por canal y mes ------------------------------------------
-- Importe de línea = qty * price (precio histórico, no de catálogo).
SELECT canal,
       strftime(fecha, '%Y-%m')   AS ym,
       ROUND(SUM(qty * price), 2) AS venta
FROM orders_flat
GROUP BY 1, 2
ORDER BY 2, 3 DESC;

-- 4. Margen por producto (SKU) ---------------------------------------
-- margen = (price - cost) * qty; se añade el % sobre venta para comparar
-- productos de distinto volumen. NULLIF evita dividir entre cero.
SELECT sku,
       SUM(qty)                                          AS unidades,
       ROUND(SUM(qty * price), 2)                        AS venta,
       ROUND(SUM((price - cost) * qty), 2)               AS margen_total,
       ROUND(100 * SUM((price - cost) * qty)
                 / NULLIF(SUM(qty * price), 0), 1)       AS margen_pct
FROM orders_flat
GROUP BY sku
ORDER BY margen_total DESC;

-- Top 5 por margen (formato del enunciado)
SELECT sku, ROUND(SUM((price - cost) * qty), 2) AS margen_total
FROM orders_flat
GROUP BY 1
ORDER BY margen_total DESC
LIMIT 5;

-- 5. Evolución temporal de pedidos -----------------------------------
-- Pedidos = COUNT(DISTINCT order_id), NO COUNT(*) (que cuenta líneas).
SELECT strftime(fecha, '%Y-%m')              AS ym,
       COUNT(DISTINCT order_id)              AS pedidos,
       COUNT(*)                              AS lineas,
       ROUND(SUM(qty * price), 2)            AS venta,
       -- variación de pedidos respecto al mes anterior
       COUNT(DISTINCT order_id)
         - LAG(COUNT(DISTINCT order_id)) OVER (ORDER BY strftime(fecha, '%Y-%m'))
                                             AS var_pedidos_mes_anterior
FROM orders_flat
GROUP BY 1
ORDER BY 1;

-- 6. Consulta adicional: ticket medio y tamaño de pedido por canal ---
-- Justificación: ventas por canal (apartado 3) no distingue si un canal
-- vende más por tener MÁS pedidos o pedidos MÁS GRANDES. El ticket medio
-- ayuda a decidir (p. ej.) si conviene fomentar venta cruzada en un canal.
-- Hay que agregar primero por pedido y luego por canal; promediar líneas
-- directamente daría el importe medio de línea, no el de pedido.
WITH pedido AS (
    SELECT order_id,
           ANY_VALUE(canal)           AS canal,
           SUM(qty * price)           AS importe,
           SUM(qty)                   AS unidades,
           COUNT(*)                   AS lineas
    FROM orders_flat
    GROUP BY order_id
)
SELECT canal,
       COUNT(*)                       AS pedidos,
       ROUND(AVG(importe), 2)         AS ticket_medio,
       ROUND(AVG(unidades), 2)        AS unidades_por_pedido,
       ROUND(AVG(lineas), 2)          AS lineas_por_pedido
FROM pedido
GROUP BY canal
ORDER BY ticket_medio DESC;

-- 7. Exportación a Parquet (formato analítico columnar) --------------
-- Se conservan solo las columnas que usan las consultas analíticas y
-- se comprime con ZSTD. Es un fichero regenerable: no se entrega.
COPY (
    SELECT order_id, customer_id, fecha, canal, sku, qty, price, cost
    FROM orders_flat
) TO 'data/orders_flat.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);

-- Verificación: el Parquet debe tener las mismas filas que la tabla.
SELECT COUNT(*) AS filas_parquet
FROM read_parquet('data/orders_flat.parquet');
