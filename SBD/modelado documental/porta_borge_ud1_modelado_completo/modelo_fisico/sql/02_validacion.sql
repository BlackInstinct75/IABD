-- Devuelve una fila (regla, reservation_id) por cada violación detectada.
-- Resultado vacío = datos válidos.
WITH
svc AS (   -- importe de servicios SOLO con ítems bien formados y existentes
  SELECT i.reservation_id,
         sum(i.qty * try_cast(s.unit_price AS DECIMAL(10,2))) AS amt
  FROM v_items i JOIN stg_servicios s ON s.service_code = i.code
  WHERE i.parts = 2 AND i.qty > 0
  GROUP BY 1),
ovl AS (   -- pares solapados en el mismo espacio, ignorando canceladas
  SELECT a.reservation_id AS a_id, b.reservation_id AS b_id
  FROM v_res a JOIN v_res b
    ON a.space_id = b.space_id AND a.reservation_id < b.reservation_id
   AND a.status <> 'cancelled' AND b.status <> 'cancelled'
   AND a.s < b.e AND b.s < a.e)
SELECT rule, reservation_id FROM (
  SELECT 'V01_id_unico' AS rule, reservation_id FROM stg_reservas
    GROUP BY reservation_id HAVING count(*) > 1 OR reservation_id IS NULL
  UNION ALL SELECT 'V02_fecha_importe_invalido', reservation_id FROM v_res
    WHERE s IS NULL OR e IS NULL OR c IS NULL OR base_n IS NULL OR total_n IS NULL
  UNION ALL SELECT 'V03_inicio_antes_de_fin', reservation_id FROM v_res WHERE s >= e
  UNION ALL SELECT 'V04_estado_en_dominio', reservation_id FROM v_res
    WHERE status IS NULL OR status NOT IN ('pending','confirmed','completed','cancelled')
  UNION ALL SELECT 'V05_miembro_existe', reservation_id FROM v_res
    WHERE member_id NOT IN (SELECT member_id FROM stg_miembros)
  UNION ALL SELECT 'V06_espacio_existe', reservation_id FROM v_res
    WHERE space_id NOT IN (SELECT space_id FROM stg_espacios)
  UNION ALL SELECT 'V07_servicio_existe_y_formato', reservation_id FROM v_items
    WHERE parts <> 2 OR code NOT IN (SELECT service_code FROM stg_servicios)
  UNION ALL SELECT 'V08_cantidad_positiva', reservation_id FROM v_items
    WHERE parts = 2 AND (qty IS NULL OR qty <= 0)
  UNION ALL SELECT 'V09_sin_solapamiento', a_id FROM ovl
  UNION ALL SELECT 'V09_sin_solapamiento', b_id FROM ovl
  UNION ALL SELECT 'V10_importe_coherente', r.reservation_id FROM v_res r
    LEFT JOIN svc USING (reservation_id)
    WHERE r.base_n IS NOT NULL AND r.total_n IS NOT NULL
      AND abs(r.total_n - (r.base_n + coalesce(svc.amt, 0))) > 0.005
  UNION ALL SELECT 'V11_plazas_dentro_de_capacidad', r.reservation_id FROM v_res r
    JOIN stg_espacios e USING (space_id)
    WHERE r.seats_n IS NULL OR r.seats_n < 1 OR r.seats_n > try_cast(e.capacity AS INTEGER)
  UNION ALL SELECT 'V12_redundancia_coherente', r.reservation_id FROM v_res r
    JOIN stg_espacios e USING (space_id)
    WHERE r.location_id <> e.location_id OR r.location_city <> e.location_city
       OR r.space_type <> e.space_type
  UNION ALL SELECT 'V12_redundancia_coherente', r.reservation_id FROM v_res r
    JOIN stg_miembros m USING (member_id) WHERE r.member_segment <> m.member_segment
  UNION ALL SELECT 'V13_creada_antes_del_inicio', reservation_id FROM v_res WHERE c > s
  UNION ALL SELECT 'V14_canal_en_dominio', reservation_id FROM v_res
    WHERE channel IS NULL OR channel NOT IN ('web','app','partner','phone')
  UNION ALL SELECT 'V15_servicio_no_repetido_en_reserva', reservation_id FROM v_items
    WHERE parts = 2 GROUP BY reservation_id, code HAVING count(*) > 1
) ORDER BY rule, reservation_id;
