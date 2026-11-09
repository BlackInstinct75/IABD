-- Capa staging: todo como texto para poder VALIDAR antes de convertir tipos.
CREATE OR REPLACE TABLE stg_reservas AS SELECT * FROM read_csv({{RESERVAS_CSV}}, header=true, all_varchar=true);
CREATE OR REPLACE TABLE stg_miembros AS SELECT * FROM read_csv('{{DATA}}/miembros_fuente.csv', header=true, all_varchar=true);
CREATE OR REPLACE TABLE stg_espacios AS SELECT * FROM read_csv('{{DATA}}/espacios_fuente.csv', header=true, all_varchar=true);
CREATE OR REPLACE TABLE stg_servicios AS SELECT * FROM read_csv('{{DATA}}/catalogo_servicios.csv', header=true, all_varchar=true);

-- Reservas con tipos "seguros": try_cast devuelve NULL si el valor es inválido.
CREATE OR REPLACE VIEW v_res AS
SELECT *,
  try_cast(start_at   AS TIMESTAMP)       AS s,
  try_cast(end_at     AS TIMESTAMP)       AS e,
  try_cast(created_at AS TIMESTAMP)       AS c,
  try_cast(seats      AS INTEGER)         AS seats_n,
  try_cast(base_amount  AS DECIMAL(10,2)) AS base_n,
  try_cast(total_amount AS DECIMAL(10,2)) AS total_n
FROM stg_reservas;

-- Desanidado de service_items ("codigo=cantidad;codigo=cantidad") a una fila por ítem.
CREATE OR REPLACE VIEW v_items AS
SELECT r.reservation_id,
       trim(t.it)                                          AS item,
       split_part(trim(t.it), '=', 1)                      AS code,
       len(string_split(trim(t.it), '='))                  AS parts,
       try_cast(split_part(trim(t.it), '=', 2) AS INTEGER) AS qty
FROM stg_reservas r, UNNEST(string_split(r.service_items, ';')) AS t(it)
WHERE coalesce(trim(r.service_items), '') <> '';
