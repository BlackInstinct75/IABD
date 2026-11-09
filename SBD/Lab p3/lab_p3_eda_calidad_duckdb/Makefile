install:
	python -m pip install -r requirements.txt

data:
	python gen_sales.py

run:
	python eda_quality.py

check:
	duckdb -c ".read duckdb_checks.sql"
