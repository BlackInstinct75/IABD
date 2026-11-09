"""Pipeline completo: CSV -> validación -> modelo en estrella -> Parquet -> consultas.

Uso:  python modelo_fisico/scripts/run_all.py
Genera: modelo_fisico/out/parquet/*.parquet  y  modelo_fisico/out/resultados/Q*.csv
"""
import sys
from common import (DATA, OUT, connect, load_and_validate, run_sql_file, split_queries, render)


def main():
    pq = OUT / "parquet"
    res = OUT / "resultados"
    pq.mkdir(parents=True, exist_ok=True)
    res.mkdir(parents=True, exist_ok=True)

    # 1) Validación (se corta el pipeline si hay violaciones)
    con = connect()
    violaciones = load_and_validate(con, DATA / "reservas_fuente.csv")
    print(f"[1/4] Validación: {len(violaciones)} violaciones")
    if violaciones:
        for v in violaciones:
            print("   ", v)
        sys.exit("Pipeline detenido: corrige la fuente.")

    # 2) Modelo + Parquet
    run_sql_file(con, "03_modelo.sql", PQ=pq.as_posix())
    print(f"[2/4] Parquet escrito en {pq}")

    # 3) Conciliación contra la fuente
    n_src = con.execute("SELECT count(*) FROM stg_reservas").fetchone()[0]
    n_fact = con.execute("SELECT count(*) FROM fact_reserva").fetchone()[0]
    n_lin_src = con.execute("SELECT count(*) FROM v_items").fetchone()[0]
    n_lin = con.execute("SELECT count(*) FROM fact_reserva_servicio").fetchone()[0]
    tot_src = con.execute("SELECT sum(CAST(total_amount AS DECIMAL(12,2))) FROM stg_reservas").fetchone()[0]
    tot_fact = con.execute("SELECT sum(total_amount) FROM fact_reserva").fetchone()[0]
    tot_calc = con.execute("SELECT sum(base_amount + services_amount) FROM fact_reserva").fetchone()[0]
    assert n_src == n_fact, (n_src, n_fact)
    assert n_lin_src == n_lin, (n_lin_src, n_lin)
    assert tot_src == tot_fact == tot_calc, (tot_src, tot_fact, tot_calc)
    print(f"[3/4] Conciliación OK: {n_fact} reservas, {n_lin} líneas de servicio, total {tot_fact} EUR")
    con.close()

    # 4) Consultas sobre una conexión NUEVA: leen solo Parquet
    q = connect()
    run_sql_file(q, "04_vistas.sql", PQ=pq.as_posix())
    for qid, title, sql in split_queries(render("05_consultas.sql")):
        df = q.execute(sql)
        cols = [d[0] for d in df.description]
        rows = df.fetchall()
        out = res / f"{qid}.csv"
        with open(out, "w", encoding="utf-8") as f:
            f.write(",".join(cols) + "\n")
            for r in rows:
                f.write(",".join(str(x) for x in r) + "\n")
        print(f"\n== {qid}: {title}")
        print(" | ".join(cols))
        for r in rows:
            print(" | ".join(str(x) for x in r))
    print(f"\n[4/4] Resultados en {res}")


if __name__ == "__main__":
    main()
