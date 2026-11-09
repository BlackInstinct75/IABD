# Entorno Conda sbd-lab (extensible)

## Crear/actualizar
```bash
conda env create -f environment.yml
# o
conda env update -f environment.yml --prune
```

## Activar
```bash
conda activate sbd-lab
```

## Probar
```bash
python -c "import duckdb, pandas, pyarrow, numpy; print('OK:', duckdb.__version__)"
```

## Lab P3
```bash
python eda_quality.py
duckdb -c ".read duckdb_checks.sql"   # si instalaste duckdb-cli
```

## Añadir paquetes (futuro)
```bash
conda install -n sbd-lab polars pyspark -c conda-forge
# o: editar environment.yml y actualizar con:
conda env update -f environment.yml --prune
```

## Kernel Jupyter (opcional)
```bash
python -m ipykernel install --user --name sbd-lab --display-name "Python (sbd-lab)"
```
