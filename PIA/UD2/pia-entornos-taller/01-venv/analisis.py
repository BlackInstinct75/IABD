import sys

import pandas as pd

datos = pd.DataFrame({
    "grupo": ["A", "A", "B"],
    "importe": [10, 20, 40],
})
total = int(datos["importe"].sum())
resumen = datos.groupby("grupo")["importe"].sum().to_dict()

print("Python:", sys.executable)
print("pandas:", pd.__version__)
print("Total:", total)
print("Por grupo:", resumen)
assert total == 70, "Revisa los datos o el resultado esperado"
print("PRUEBA OK")