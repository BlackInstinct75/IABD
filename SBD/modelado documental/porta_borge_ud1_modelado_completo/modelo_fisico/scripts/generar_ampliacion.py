"""Genera una ampliación SINTÉTICA y DETERMINISTA del modelo en Parquet.

Uso:  python generar_ampliacion.py [N_RESERVAS]     (por defecto 2_000_000)
Salida: modelo_fisico/out/scale/*.parquet  (mismo esquema que out/parquet)

Es solo para medir lectura/agregación. NO se garantiza ausencia de solapamientos
(regla V09), por lo que no sirve para validar reglas de negocio.
Determinismo: todo deriva de hash(i); sin random().
"""
import sys
from common import DATA, OUT, connect

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
out = OUT / "scale"
out.mkdir(parents=True, exist_ok=True)
con = connect()

con.execute(f"""
CREATE TABLE dim_espacio AS
SELECT e.space_id || '-' || lpad(k::VARCHAR, 2, '0')    AS space_id,
       e.location_id || '-' || lpad(k::VARCHAR, 2, '0') AS location_id,
       e.location_city, e.space_type, CAST(e.capacity AS INTEGER) AS capacity
FROM read_csv('{(DATA / "espacios_fuente.csv").as_posix()}', header=true) e
CROSS JOIN range(1, 11) t(k);

CREATE TABLE dim_servicio AS
SELECT service_code, description, CAST(unit_price AS DECIMAL(10,2)) AS unit_price,
       row_number() OVER (ORDER BY service_code) - 1 AS idx
FROM read_csv('{(DATA / "catalogo_servicios.csv").as_posix()}', header=true);

CREATE TABLE dim_miembro AS
SELECT 'M' || lpad(i::VARCHAR, 6, '0') AS member_id,
       (['freelancer','startup','enterprise','student'])[CAST(hash(i) % 4 + 1 AS BIGINT)] AS member_segment
FROM range(1, 50001) t(i);

CREATE TABLE sp AS
SELECT *, row_number() OVER (ORDER BY space_id) - 1 AS idx FROM dim_espacio;

CREATE TABLE r0 AS
WITH g AS (
  SELECT i, hash(i) h1, hash(i + 10000000) h2, hash(i + 20000000) h3, hash(i + 30000000) h4
  FROM range(1, {N} + 1) t(i)),
x AS (
  SELECT 'R' || lpad(i::VARCHAR, 9, '0') AS reservation_id,
         'M' || lpad((h1 % 50000 + 1)::VARCHAR, 6, '0') AS member_id,
         sp.space_id, sp.space_type, sp.capacity,
         TIMESTAMP '2024-01-01' + CAST(h3 % 26280 AS INTEGER) * INTERVAL 1 HOUR AS start_at,
         CAST(1 + h4 % 8 AS INTEGER) AS dur,
         CAST(1 + (h2 // 97) % sp.capacity AS INTEGER) AS seats,
         CASE WHEN (h4 // 11) % 100 < 7  THEN 'cancelled'
              WHEN (h4 // 11) % 100 < 12 THEN 'pending'
              WHEN (h4 // 11) % 100 < 62 THEN 'completed' ELSE 'confirmed' END AS status,
         (['web','app','partner','phone'])[CAST((h1 // 13) % 4 + 1 AS BIGINT)] AS channel,
         CAST(1 + (h3 // 7) % 60 AS INTEGER) AS days_before
  FROM g JOIN sp ON sp.idx = g.h2 % 90)
SELECT reservation_id, member_id, space_id,
       start_at, start_at + dur * INTERVAL 1 HOUR AS end_at,
       start_at - days_before * INTERVAL 1 DAY AS created_at,
       seats, status, channel, CAST(dur AS DOUBLE) AS duration_hours,
       CAST(dur AS DOUBLE) * seats AS seat_hours,
       CAST(dur * CASE space_type WHEN 'hot_desk' THEN 3.0 WHEN 'meeting_room' THEN 35.0 ELSE 45.0 END AS DECIMAL(10,2)) AS base_amount
FROM x;

CREATE TABLE fact_reserva_servicio AS
SELECT r.reservation_id, d.service_code,
       CAST(1 + hash(r.reservation_id, 'q', k) % 4 AS INTEGER) AS quantity,
       d.unit_price,
       CAST((1 + hash(r.reservation_id, 'q', k) % 4) * d.unit_price AS DECIMAL(10,2)) AS line_amount
FROM r0 r CROSS JOIN range(0, 3) t(k)
JOIN dim_servicio d ON d.idx = (hash(r.reservation_id) % 5 + k) % 5
WHERE hash(r.reservation_id, 'k', k) % 100 < 45;

CREATE TABLE fact_reserva AS
SELECT r.reservation_id, r.member_id, r.space_id, r.start_at, r.end_at, r.created_at,
       CAST(date_trunc('month', r.start_at) AS DATE)   AS start_month,
       CAST(date_trunc('month', r.created_at) AS DATE) AS created_month,
       r.seats, r.status, r.channel, r.duration_hours, r.seat_hours, r.base_amount,
       CAST(coalesce(s.amt, 0) AS DECIMAL(10,2)) AS services_amount,
       CAST(r.base_amount + coalesce(s.amt, 0) AS DECIMAL(10,2)) AS total_amount
FROM r0 r LEFT JOIN (SELECT reservation_id, sum(line_amount) amt
                     FROM fact_reserva_servicio GROUP BY 1) s USING (reservation_id);
""")

o = out.as_posix()
for t, order in [("dim_miembro", "member_id"), ("dim_espacio", "space_id"),
                 ("fact_reserva", "start_at"), ("fact_reserva_servicio", "reservation_id")]:
    con.execute(f"COPY (SELECT * FROM {t} ORDER BY {order}) TO '{o}/{t}.parquet' (FORMAT parquet, COMPRESSION zstd)")
con.execute(f"COPY (SELECT service_code, description, unit_price FROM dim_servicio) TO '{o}/dim_servicio.parquet' (FORMAT parquet, COMPRESSION zstd)")

n1 = con.execute("SELECT count(*) FROM fact_reserva").fetchone()[0]
n2 = con.execute("SELECT count(*) FROM fact_reserva_servicio").fetchone()[0]
print(f"fact_reserva={n1:,}  fact_reserva_servicio={n2:,}")
for f in sorted(out.glob("*.parquet")):
    print(f"  {f.name:<34}{f.stat().st_size/1e6:8.2f} MB")
