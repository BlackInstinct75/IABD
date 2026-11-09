-- @Q5 Horas reservadas por ciudad y mes (mes de INICIO; excluye canceladas)
-- Dos métricas: horas_reserva = duración; horas_plaza = duración x seats.
SELECT d.location_city AS ciudad, f.start_month AS mes,
       round(sum(f.duration_hours), 1) AS horas_reserva,
       round(sum(f.seat_hours), 1)     AS horas_plaza,
       count(*)                        AS reservas,
       rank() OVER (PARTITION BY f.start_month ORDER BY sum(f.duration_hours) DESC) AS rank_horas_reserva,
       rank() OVER (PARTITION BY f.start_month ORDER BY sum(f.seat_hours)     DESC) AS rank_horas_plaza
FROM fact_reserva f JOIN dim_espacio d USING (space_id)
WHERE f.status <> 'cancelled'
GROUP BY d.location_city, f.start_month
ORDER BY mes, rank_horas_reserva, ciudad;

-- @Q6 Ingresos por ciudad y tipo de espacio (solo confirmed + completed; sin impuestos)
SELECT d.location_city AS ciudad, d.space_type AS tipo_espacio,
       count(*)                AS reservas,
       sum(f.base_amount)      AS ingresos_espacio,
       sum(f.services_amount)  AS ingresos_servicios,
       sum(f.total_amount)     AS ingresos_totales
FROM fact_reserva f JOIN dim_espacio d USING (space_id)
WHERE f.status IN ('confirmed', 'completed')
GROUP BY 1, 2
ORDER BY ciudad, tipo_espacio;

-- @Q7 Tasa de cancelación por canal y mes de CREACIÓN (denominador: todas las reservas creadas)
SELECT f.created_month AS mes_creacion, f.channel AS canal,
       count(*)                                       AS reservas_creadas,
       count(*) FILTER (WHERE f.status = 'cancelled') AS canceladas,
       round(100.0 * count(*) FILTER (WHERE f.status = 'cancelled') / count(*), 1) AS tasa_cancelacion_pct
FROM fact_reserva f
GROUP BY 1, 2
ORDER BY 1, 2;

-- @Q8 Servicios adicionales más solicitados (unidades en reservas no canceladas)
SELECT ds.service_code AS servicio, ds.description AS descripcion,
       coalesce(sum(s.quantity)    FILTER (WHERE r.status <> 'cancelled'), 0) AS unidades,
       count(DISTINCT r.reservation_id) FILTER (WHERE r.status <> 'cancelled') AS reservas,
       coalesce(sum(s.line_amount) FILTER (WHERE r.status <> 'cancelled'), 0) AS importe,
       sum(s.quantity) AS unidades_incl_canceladas
FROM dim_servicio ds
LEFT JOIN fact_reserva_servicio s USING (service_code)
LEFT JOIN fact_reserva r USING (reservation_id)
GROUP BY 1, 2
ORDER BY unidades DESC, reservas DESC, servicio;
