-- Las consultas leen EXCLUSIVAMENTE los ficheros Parquet.
CREATE OR REPLACE VIEW dim_miembro  AS SELECT * FROM read_parquet('{{PQ}}/dim_miembro.parquet');
CREATE OR REPLACE VIEW dim_espacio  AS SELECT * FROM read_parquet('{{PQ}}/dim_espacio.parquet');
CREATE OR REPLACE VIEW dim_servicio AS SELECT * FROM read_parquet('{{PQ}}/dim_servicio.parquet');
CREATE OR REPLACE VIEW fact_reserva AS SELECT * FROM read_parquet('{{PQ}}/fact_reserva.parquet');
CREATE OR REPLACE VIEW fact_reserva_servicio AS SELECT * FROM read_parquet('{{PQ}}/fact_reserva_servicio.parquet');
