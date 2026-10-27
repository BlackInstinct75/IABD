# Registro del taller de entornos de Python

**Sistema operativo:** Windows (PowerShell) · **Carpeta de trabajo:** `pia-entornos-taller`

## Estado de los bloques

| Bloque | Estado | Observaciones |
|---|---|---|
| 01 venv + pip | Prueba y modificación hechas; **incidencia abierta** | `pip install -r requirements.txt` falla en Python 3.15 y el entorno tiene pandas 3.1.0 (fuera del rango `<3`) |
| 02 uv | Completo | |
| 03 conda | Completo | Falta pegar el contenido de `environment.yml` y `environment-exportado.yml` |
| 04 pixi | Completo | |
| 05 comparación | Completo (borrador propio a revisar) | |

---

## 1. venv + pip (carpeta `01-venv`)

| Evidencia | Registro |
|---|---|
| Instalar / comprobar | Windows. Python ya instalado (no se reinstala): `py --version` → 3.15.0; `python --version` → 3.14.9. `py -m venv -help` muestra la ayuda de venv |
| Configurar | `.venv` creado con Python 3.15 (`py -m venv .venv`), activado con `.\.venv\Scripts\Activate.ps1`. `requirements.txt` creado con `Set-Content requirements.txt "pandas>=2.2,<3"`. `python -m pip --version` → pip 26.2.2 dentro de `.venv` (python 3.15) |
| Ejecutar y probar | `python analisis.py` con Python en `01-venv\.venv`; ver salidas abajo |
| Modificar | Importe 30 → 40 y `assert total == 70`; resultado: Total 70, grupo B 40, `PRUEBA OK` |
| Repetir | `python -m pip install -r requirements.txt` (**falla**, ver incidencia) |
| Incidencia | Ver abajo. Estado: **abierta** |

Comprobación de Python y venv:

```text
(base) PS ...\01-venv> py --version
Python 3.15.0
(base) PS ...\01-venv> python --version
Python 3.14.9
(base) PS ...\01-venv> py -m venv -help
usage: python.exe -m venv [-h] [--system-site-packages] [--symlinks | --copies] [--clear] [--upgrade]
                          [--without-pip] [--prompt PROMPT] [--upgrade-deps] [--without-scm-ignore-files]
                          ENV_DIR [ENV_DIR ...]
(... ayuda completa de venv)
```

Salida inicial (importes 10, 20, 30):

```text
(.venv) PS ...\01-venv> python analisis.py
Python: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\01-venv\.venv\Scripts\python.exe
pandas: 3.1.0
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
```

Tras la modificación (importes 10, 20, 40):

```text
(.venv) PS ...\01-venv> python analisis.py
Python: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\01-venv\.venv\Scripts\python.exe
pandas: 3.1.0
Total: 70
Por grupo: {'A': 30, 'B': 40}
PRUEBA OK
```

### Incidencia: `pip install -r requirements.txt` falla

```text
(.venv) PS ...\01-venv> python -m pip install -r requirements.txt
Collecting pandas<3,>=2.2 (from -r requirements.txt (line 1))
  Using cached pandas-2.3.3.tar.gz (4.5 MB)
  Preparing metadata (pyproject.toml) ... error
  error: subprocess-exited-with-error
  × Preparing metadata (pyproject.toml) did not run successfully.
  ...
      + meson setup ... --vsenv ...
      El sistema no puede encontrar el archivo especificado.
      UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe0 in position 104: invalid continuation byte
      ...
      AttributeError: 'NoneType' object has no attribute 'split'
      Activating VS 18.10.0
      Project name: pandas
      Project version: 2.3.3
      ..\meson.build:2:0: ERROR: Unhandled python exception
      This is a Meson bug and should be reported!
error: metadata-generation-failed
× Encountered error while generating package metadata.
╰─> pandas
note: This is an issue with the package mentioned above, not pip.
```

**Interpretación:** pip no encontró una versión ya compilada (wheel) de pandas 2.3.3 para Python 3.15. Por eso descargó el código fuente (`pandas-2.3.3.tar.gz`) e intentó compilarlo con Meson, y la compilación falló al detectar el compilador de C de Visual Studio. La salida de `python analisis.py` posterior sigue mostrando pandas 3.1.0, que ya estaba instalado en `.venv` y no cumple `pandas>=2.2,<3`.

**Intento de solución:** pendiente (ver notas de revisión). **Estado final:** abierta.

---

## 2. uv (carpeta `02-uv`)

| Evidencia | Registro |
|---|---|
| Instalar / comprobar | Ya instalado: `uv 0.13.6 (329bf9448 2026-10-26 x86_64-pc-windows-msvc)` |
| Configurar | Proyecto con `pyproject.toml` (Python `>=3.12`, `pandas>=2.2,<3`) y entorno `.venv` propio del proyecto |
| Ejecutar y probar | `uv run python analisis.py` con Python en `02-uv\.venv` y pandas 2.3.3 |
| Modificar | Dependencia `rich`: `uv add rich`, prueba con `rich`, `uv sync --locked` y análisis posterior |
| Repetir | `pyproject.toml` + `uv.lock`; reconstruir con `uv sync --locked` (no se comparte `.venv/`) |
| Incidencia | Escribí `un run python analisis.py` (falta la «u»): `un : El término 'un' no se reconoce como nombre de un cmdlet...` (`CommandNotFoundException`). Solución: repetir `uv run python analisis.py`. Estado: resuelta |

Comprobación del Python del sistema (fuera del entorno) y con uv:

```text
PS ...\02-uv> python .\analisis.py
Python: C:\Python315\python.exe
pandas: 3.1.0
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK

PS ...\02-uv> uv run python analisis.py
Python: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\02-uv\.venv\Scripts\python.exe
pandas: 2.3.3
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
```

Modificación con `rich`:

```text
(.venv) PS ...\02-uv> uv add rich
warning: `VIRTUAL_ENV=...\01-venv\.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
Resolved 11 packages in 1ms
Checked 10 packages in 0.83ms
(.venv) PS ...\02-uv> uv run python -c "from rich import print; print('[green]uv listo[/green]')"
warning: (el mismo aviso de VIRTUAL_ENV)
uv listo
(.venv) PS ...\02-uv> uv sync --locked
warning: (el mismo aviso de VIRTUAL_ENV)
Resolved 11 packages in 0.90ms
Checked 10 packages in 0.98ms
(.venv) PS ...\02-uv> uv run python analisis.py
warning: (el mismo aviso de VIRTUAL_ENV)
Python: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\02-uv\.venv\Scripts\python.exe
pandas: 2.3.3
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
```

El aviso aparece porque no abrí una terminal nueva y seguía activo el `.venv` de `01-venv`. uv lo ignora y usa el entorno de su proyecto, como indica la ruta de Python.

`pyproject.toml`:

```toml
[project]
name = "02-uv"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "pandas>=2.2,<3",
    "rich>=15.0.0",
]
```

Fragmentos de `uv.lock`:

```toml
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

[[package]]
name = "rich"
version = "15.0.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "markdown-it-py" },
    { name = "pygments" },
]
```

**Qué cambió al añadir rich:** en `pyproject.toml` apareció `rich>=15.0.0` dentro de `dependencies`; en `uv.lock` apareció el paquete `rich` 15.0.0 con sus dependencias `markdown-it-py` y `pygments`. En esta repetición `uv add rich` no modificó nada más (resolvió 11 paquetes y comprobó 10 ya instalados), porque `rich` ya estaba añadido. `uv sync --locked` confirmó que `uv.lock` coincide con `pyproject.toml`.

---

## 3. conda (carpeta `03-conda`)

| Evidencia | Registro |
|---|---|
| Instalar / comprobar | Ya instalado (Miniconda en `C:\Users\ia\miniconda3`): `conda 26.9.4`; solver: `libmamba` |
| Configurar | Entorno `pia-taller-conda` (Python 3.12 y pandas `>=2.2,<3`, canal conda-forge) definido en `environment.yml`; el entorno ya existía y se actualiza con `conda env update` |
| Ejecutar y probar | `python analisis.py` con Python en `C:\Users\ia\miniconda3\envs\pia-taller-conda\python.exe`, pandas 2.3.3 |
| Modificar | `rich` añadido al YAML y entorno actualizado con `conda env update ... --prune`; prueba de `rich` y análisis posterior correctos |
| Repetir | `environment.yml` (original) y `environment-exportado.yml` (exportación con `--from-history`) |

Entorno y prueba inicial:

```text
(pia-taller-conda) PS ...\03-conda> python analisis.py
Python: C:\Users\ia\miniconda3\envs\pia-taller-conda\python.exe
pandas: 2.3.3
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
(pia-taller-conda) PS ...\03-conda> conda env list

# conda environments:
#
# * -> active
# + -> frozen
                         C:\Users\ia\.anaconda-desktop\micromamba\envs\cuda
base                     C:\Users\ia\miniconda3
pia-taller-conda     *   C:\Users\ia\miniconda3\envs\pia-taller-conda
pia-ud2                  C:\Users\ia\miniconda3\envs\pia-ud2
                         C:\pinokio\bin\miniforge
                         C:\pinokio\bin\miniforge
```

Versión y solver:

```text
(base) PS ...\03-conda> conda --version
conda 26.9.4
(base) PS ...\03-conda> conda config --show solver
solver: libmamba
```

Actualización con `rich`, prueba y exportación:

```text
(.venv) PS ...\03-conda> conda activate pia-taller-conda
(.venv) (pia-taller-conda) PS ...\03-conda> conda env update -n pia-taller-conda -f environment.yml --prune
3 channel Terms of Service accepted
Channels:
 - conda-forge
Platform: win-64
Collecting package metadata (repodata.json): done
Solving environment: done
(... instrucciones de activación)
(.venv) (pia-taller-conda) PS ...\03-conda> python -c "from rich import print; print('[green]conda listo[/green]')"
conda listo
(.venv) (pia-taller-conda) PS ...\03-conda> python analisis.py
Python: C:\Users\ia\miniconda3\envs\pia-taller-conda\python.exe
pandas: 2.3.3
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
(.venv) (pia-taller-conda) PS ...\03-conda> conda env export -n pia-taller-conda --from-history > environment-exportado.yml
(.venv) (pia-taller-conda) PS ...\03-conda> conda deactivate
```

`environment.yml` (**PEGAR** aquí el resultado de `type environment.yml`):

```yaml

```

`environment-exportado.yml` (**PEGAR** aquí el resultado de `type environment-exportado.yml`):

```yaml

```

**Nota:** el YAML con rangos no garantiza las mismas versiones finales al resolver otro día. La exportación `--from-history` solo recoge lo pedido explícitamente.

---

## 4. Pixi (carpeta `04-pixi`)

| Evidencia | Registro |
|---|---|
| Instalar / comprobar | Windows, `pixi 0.80.0` |
| Configurar | `pixi init .` y `pixi add "python=3.12" "pandas>=2.2,<3"` |
| Ejecutar y probar | `pixi run python analisis.py`; Python en `.pixi\envs\default`, pandas 2.3.3 |
| Modificar | Tarea `analizar` y dependencia `rich` (`>=15.0.0,<16`); el análisis sigue pasando |
| Repetir | `pixi.toml` + `pixi.lock`; instalar desde el lock con `pixi install --locked` (no se comparte `.pixi/`) |

Instalación y configuración:

```text
(base) PS ...\04-pixi> pixi --version
pixi 0.80.0
(base) PS ...\04-pixi> pixi init .
Created ...\04-pixi\pixi.toml
(base) PS ...\04-pixi> pixi add "python=3.12" "pandas>=2.2,<3"
Added python=3.12
Added pandas>=2.2,<3
```

Primera ejecución:

```text
(base) PS ...\04-pixi> pixi run python analisis.py
Python: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi\.pixi\envs\default\python.exe
pandas: 2.3.3
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
```

Archivos del proyecto (`ls`): `.pixi`, `.gitattributes`, `.gitignore`, `analisis.py`, `pixi.lock`, `pixi.toml`. Python en `.pixi\envs\default\python.exe` (Python 3.12: `python312.dll`).

Tarea y dependencia nueva:

```text
(base) PS ...\04-pixi> pixi task add analizar "python analisis.py"
Added task `analizar`: python analisis.py
(base) PS ...\04-pixi> pixi run analizar
Pixi task (analizar): python analisis.py
Python: ...\04-pixi\.pixi\envs\default\python.exe
pandas: 2.3.3
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
(base) PS ...\04-pixi> pixi add rich
Added rich >=15.0.0,<16
(base) PS ...\04-pixi> pixi run python -c "from rich import print; print('[green]Pixi listo[/green]')"
Pixi listo
(base) PS ...\04-pixi> pixi run analizar
... PRUEBA OK
```

Instalación desde el lock y manifiesto final:

```text
(.venv) PS ...\04-pixi> pixi install --locked
The default environment has been installed.
(.venv) PS ...\04-pixi> type pixi.toml
```

```toml
[workspace]
authors = ["(autor)"]
channels = ["conda-forge"]
name = "04-pixi"
platforms = ["win-64"]
version = "0.1.0"

[tasks]
analizar = "python analisis.py"

[dependencies]
python = "3.12.*"
pandas = ">=2.2,<3"
rich = ">=15.0.0,<16"
```

Comandos clave: instalar desde el lock → `pixi install --locked`; ejecutar la tarea → `pixi run analizar`.

---

## 5. Comparación

| Opción | Ventaja observada | Inconveniente observado | Cuándo la elegiría |
|---|---|---|---|
| venv + pip | Viene con Python, sin instalar nada más; `sys.executable` confirma el aislamiento en `.venv`. | Usa la versión de Python que ya tengas: con Python 3.15, `pip install` intentó compilar pandas 2.3.3 desde el código fuente y falló. Hay que activar el entorno a mano y `requirements.txt` con rangos no fija versiones. | Script pequeño en un equipo que ya tiene Python. |
| uv | Un solo comando (`uv run`) crea y usa `.venv` con Python 3.12; `pyproject.toml` y `uv.lock` quedan separados y fijan pandas 2.3.3 exacto. | Solo gestiona paquetes de Python (PyPI); no cubre paquetes nativos como conda. | Proyecto solo Python con dependencias y lock para compartir. |
| conda | Entorno nombrado fuera de la carpeta, reutilizable desde cualquier proyecto; instala la versión de Python pedida y paquetes nativos de conda-forge. | Hay que activar el entorno a mano, y el YAML con rangos no garantiza las mismas versiones. Con varios entornos (`pia-ud2`, `cuda`...) es fácil confundirse de prefijo. | Entorno de experimentación con Python y paquetes nativos. |
| Pixi | `pixi run` no necesita activar; `pixi.lock` fija versiones y las tareas (`analizar`) dejan el comando guardado en `pixi.toml`. | Herramienta y manifiesto nuevos que aprender; el entorno vive en `.pixi/` dentro de cada proyecto y ocupa espacio. | Proyecto del módulo con entornos y tareas reproducibles. |

Casos (una herramienta y una razón):

1. **Script pequeño en un equipo que ya tiene Python:** venv + pip, porque no obliga a instalar otro gestor.
2. **Proyecto solo Python con dependencias y lock para compartir:** uv, porque `pyproject.toml` + `uv.lock` se comparten y se reconstruyen con `uv sync --locked`.
3. **Entorno nombrado de experimentación con Python y paquetes nativos:** conda, porque instala paquetes nativos de conda-forge en un entorno con nombre.
4. **Proyecto del módulo con entornos y tareas reproducibles:** Pixi, porque une paquetes conda, lock y tareas en un solo manifiesto.

---

## Notas de revisión

- **Terminales no nuevas:** en los bloques 02, 03 y 04 seguía activo el `.venv` de `01-venv` (el prompt muestra `(.venv)`). Las herramientas usaron igualmente su propio entorno, como demuestran las rutas de `sys.executable`. En el bloque 01 no ejecuté `deactivate` al terminar.
- **conda `(base)` activo** en parte del bloque 04, por el mismo motivo.
- **Python 3.15 del sistema** (`C:\Python315`) trae pandas 3.1.0; fuera del entorno es normal, y en 02-uv sirve como prueba de aislamiento.
