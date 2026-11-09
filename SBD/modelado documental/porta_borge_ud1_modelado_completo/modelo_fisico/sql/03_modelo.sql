-- Construcción del modelo dimensional (esquema en estrella) y salida a Parquet.
-- Precondición: los datos han pasado 02_validacion.sql.

CREATE OR REPLACE TABLE dim_miembro AS
SELECT member_id, member_segment FROM stg_miembros;

CREATE OR REPLACE TABLE dim_espacio AS
SELECT space_id, location_id, location_city, space_type, CAST(capacity AS INTEGER) AS capacity
FROM stg_espacios;

CREATE OR REPLACE TABLE dim_servicio AS
SELECT service_code, description, CAST(unit_price AS DECIMAL(10,2)) AS unit_price
FROM stg_servicios;

-- Grano: una fila por (reserva, servicio). Sustituye a la cadena service_items.
CREATE OR REPLACE TABLE fact_reserva_servicio AS
SELECT i.reservation_id, i.code AS service_code, i.qty AS quantity,
       d.unit_price,                                   -- precio congelado en el momento de la reserva
       CAST(i.qty * d.unit_price AS DECIMAL(10,2)) AS line_amount
FROM v_items i JOIN dim_servicio d ON d.service_code = i.code;

-- Grano: una fila por reserva.
CREATE OR REPLACE TABLE fact_reserva AS
SELECT r.reservation_id, r.member_id, r.space_id,
       r.s AS start_at, r.e AS end_at, r.c AS created_at,
       CAST(date_trunc('month', r.s) AS DATE) AS start_month,
       CAST(date_trunc('month', r.c) AS DATE) AS created_month,
       r.seats_n AS seats, r.status, r.channel,
       date_diff('minute', r.s, r.e) / 60.0                 AS duration_hours,  -- derivado
       date_diff('minute', r.s, r.e) / 60.0 * r.seats_n     AS seat_hours,      -- derivado
       r.base_n  AS base_amount,                                                -- original
       CAST(coalesce(sv.amt, 0) AS DECIMAL(10,2)) AS services_amount,          -- derivado
       r.total_n AS total_amount                                                -- original
FROM v_res r
LEFT JOIN (SELECT reservation_id, sum(line_amount) AS amt
           FROM fact_reserva_servicio GROUP BY 1) sv USING (reservation_id);

COPY dim_miembro  TO '{{PQ}}/dim_miembro.parquet'  (FORMAT parquet, COMPRESSION zstd);
COPY dim_espacio  TO '{{PQ}}/dim_espacio.parquet'  (FORMAT parquet, COMPRESSION zstd);
COPY dim_servicio TO '{{PQ}}/dim_servicio.parquet' (FORMAT parquet, COMPRESSION zstd);
COPY (SELECT * FROM fact_reserva ORDER BY start_at)
  TO '{{PQ}}/fact_reserva.parquet' (FORMAT parquet, COMPRESSION zstd);
COPY (SELECT * FROM fact_reserva_servicio ORDER BY reservation_id)
  TO '{{PQ}}/fact_reserva_servicio.parquet' (FORMAT parquet, COMPRESSION zstd);
