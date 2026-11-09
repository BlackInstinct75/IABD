"""Mide Q5-Q8 sobre out/parquet (prototipo) y out/scale (ampliación).

Uso: python benchmark.py   (ejecuta antes run_all.py y generar_ampliacion.py)
Mediana de 5 ejecuciones por consulta tras 1 de calentamiento. Conexión nueva por dataset.
"""
import statistics, time, platform, duckdb
from common import OUT, connect, render, run_sql_file, split_queries

queries = split_queries(render("05_consultas.sql"))
print(f"DuckDB {duckdb.__version__} | Python {platform.python_version()} | hilos={connect().execute('SELECT current_setting(\'threads\')').fetchone()[0]}")
print(f"{'dataset':<10}{'consulta':<8}{'filas_resultado':>16}{'mediana_ms':>12}")
for name in ["parquet", "scale"]:
    d = OUT / name
    if not d.exists():
        print(f"(omitido {name}: no existe {d})"); continue
    con = connect()
    run_sql_file(con, "04_vistas.sql", PQ=d.as_posix())
    n = con.execute("SELECT count(*) FROM fact_reserva").fetchone()[0]
    for qid, _, sql in queries:
        con.execute(sql).fetchall()
        ts = []
        for _ in range(5):
            t0 = time.perf_counter(); rows = con.execute(sql).fetchall(); ts.append((time.perf_counter() - t0) * 1000)
        print(f"{name+f' ({n:,})':<10}{qid:<8}{len(rows):>16}{statistics.median(ts):>12.1f}")
