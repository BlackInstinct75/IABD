install:
	python -m pip install -r requirements.txt

data:
	python genera_datos_p2.py

duckdb:
	duckdb -c ".read p2_duckdb.sql"
