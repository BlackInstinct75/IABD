"""Utilidades compartidas: conexión DuckDB y ejecución de plantillas SQL."""
import pathlib
import duckdb

BASE = pathlib.Path(__file__).resolve().parents[1]      # modelo_fisico/
DATA = BASE / "data"
SQL = BASE / "sql"
OUT = BASE / "out"


def connect():
    return duckdb.connect(":memory:")


def render(name, **params):
    text = (SQL / name).read_text(encoding="utf-8")
    for k, v in params.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


def run_sql_file(con, name, **params):
    """Ejecuta todas las sentencias del fichero; devuelve el resultado de la última."""
    return con.execute(render(name, **params))


def csv_literal(*paths):
    """Literal SQL para read_csv: 'ruta' o ['ruta1','ruta2']."""
    items = ["'" + pathlib.Path(p).as_posix() + "'" for p in paths]
    return items[0] if len(items) == 1 else "[" + ",".join(items) + "]"


def load_and_validate(con, *reservas_csv):
    """Carga staging y devuelve la lista de violaciones [(regla, reservation_id)]."""
    run_sql_file(con, "01_staging.sql", RESERVAS_CSV=csv_literal(*reservas_csv), DATA=DATA.as_posix())
    return run_sql_file(con, "02_validacion.sql").fetchall()


def split_queries(text):
    """Separa 05_consultas.sql en [(id, titulo, sql)] usando los marcadores '-- @Qn'."""
    out = []
    for block in text.split("-- @")[1:]:
        head, _, body = block.partition("\n")
        qid, _, title = head.partition(" ")
        out.append((qid, title.strip(), body.strip().rstrip(";")))
    return out
