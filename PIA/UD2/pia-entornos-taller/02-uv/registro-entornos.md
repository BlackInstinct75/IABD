02-uv

PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\02-uv> python .\analisis.py
Python: C:\Python315\python.exe
pandas: 3.1.0
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\02-uv> 

[[package]]
name = "pandas"
version = "2.3.3"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "numpy" },
    { name = "python-dateutil" },
    { name = "pytz" },
    { name = "tzdata" },
]


[project]
name = "02-uv"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pandas>=2.2,<3",
    "rich>=15.0.0",
]


PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\02-uv> uv run python analisis.py
Python: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\02-uv\.venv\Scripts\python.exe
pandas: 2.3.3
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\02-uv> PS 

[[package]]
name = "rich"
version = "15.0.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "markdown-it-py" },
    { name = "pygments" },
]

[project]
name = "02-uv"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pandas>=2.2,<3",
    "rich>=15.0.0",
]
