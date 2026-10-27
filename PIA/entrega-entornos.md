# Registro — Taller de entornos de Python

**Nombre:** Francisco Javier Porta Borge
**Fecha:** 27/10/2026
**Equipo:** Windows 11 · PowerShell

## Estado global

| Bloque | Estado (completo / en curso / no iniciado) |
|---|---|
| venv + pip | completado |
| uv | completo |
| conda | completo |
| Pixi | completo |

## 1. venv + pip

| Evidencia | Valor |
|---|---|
| ¿Instalado o ya estaba? / versión | Python ya estaba instalado. `py --version`: Python 3.12.2; `python --version`: Python 3.12.2. Dentro de `.venv`, pip 26.2.2. |
| Comando de creación y activación | `py -m venv .venv` y `.\.venv\Scripts\Activate.ps1` |
| Ruta de Python (`sys.executable`) | `C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\01-venv\.venv\Scripts\python.exe` |
| Salida inicial | `pandas: 3.1.0`; `Total: 60`; `Por grupo: {'A': 30, 'B': 30}`; `PRUEBA OK`. |
| Cambio realizado | Se cambió el importe de 30 a 40. Resultado: `Total: 70`; `Por grupo: {'A': 30, 'B': 40}`; `PRUEBA OK`. |
| `requirements.txt` | `pandas>=2.2,<3` |


## 2. uv

| Evidencia | Valor |
|---|---|
| ¿Instalado o ya estaba? / versión | Ya estaba instalado: `uv 0.13.6 (329bf9448 2026-10-26 x86_64-pc-windows-msvc)`. |
| Comando de creación del proyecto | Proyecto con `pyproject.toml` (`requires-python = ">=3.12"` y `pandas>=2.2,<3`); ejecución con `uv run python analisis.py`. |
| Ruta de Python | `C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\02-uv\.venv\Scripts\python.exe` |
| Salida de la prueba | `pandas: 2.3.3`; `Total: 60`; `Por grupo: {'A': 30, 'B': 30}`; `PRUEBA OK`. |
| Dependencia añadida (`rich`) | `uv add rich`; se comprobó con `uv run python -c "from rich import print; print('[green]uv listo[/green]')"`, que mostró `uv listo`. Tras `uv sync --locked`, el análisis volvió a terminar con `PRUEBA OK`. |
| Archivos del manifiesto | `pyproject.toml` y `uv.lock`. |
| Comando para reconstruir desde el lock | `uv sync --locked` |


## 3. conda

| Evidencia | Valor |
|---|---|
| ¿Instalado o ya estaba? / versión | Miniconda ya estaba instalado en `C:\Users\ia\miniconda3`; `conda 26.9.4`. |
| Comando de creación del entorno | El entorno `pia-taller-conda` ya existía y se actualizó con `conda env update -n pia-taller-conda -f environment.yml --prune`. El YAML define Python 3.12, `pandas>=2.2,<3` y el canal `conda-forge`. |
| Ruta de Python (prefijo de `pia-taller-conda`) | `C:\Users\ia\miniconda3\envs\pia-taller-conda\python.exe` |
| Salida de la prueba | `pandas: 2.3.3`; `Total: 60`; `Por grupo: {'A': 30, 'B': 30}`; `PRUEBA OK`. |
| Cambio en el YAML (`rich`) y exportación | Se añadió `rich` a `environment.yml`, se actualizó el entorno con `conda env update ... --prune` y la prueba de importación mostró `conda listo`. Se generó `environment-exportado.yml` con `conda env export -n pia-taller-conda --from-history > environment-exportado.yml`. |
| Solver usado | `libmamba` |


## 4. Pixi

| Evidencia | Valor |
|---|---|
| ¿Instalado o ya estaba? / versión | `pixi 0.80.0`. |
| Comando de creación del proyecto | `pixi init .` y `pixi add "python=3.12" "pandas>=2.2,<3"`. |
| Ruta de Python (en `.pixi/envs/default`) | `C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi\.pixi\envs\default\python.exe` |
| Salida de la prueba | `pandas: 2.3.3`; `Total: 60`; `Por grupo: {'A': 30, 'B': 30}`; `PRUEBA OK`. |
| Tarea `analizar` creada | Sí: `pixi task add analizar "python analisis.py"`. `pixi run analizar` ejecutó el análisis y terminó con `PRUEBA OK`. |
| Comando que instala desde el lock | `pixi install --locked` |

Se añadió `rich` con `pixi add rich` (rango registrado: `>=15.0.0,<16`) y se comprobó la importación, que mostró `Pixi listo`. El manifiesto final `pixi.toml` contiene la tarea `analizar` y las dependencias `python = "3.12.*"`, `pandas = ">=2.2,<3"` y `rich = ">=15.0.0,<16"`.

## 5. Comparación

| Opción | Ventaja | Inconveniente | Cuándo la elegiría |
|---|---|---|---|
| venv + pip | Viene con Python y no exige instalar otro gestor; el aislamiento se comprueba con `sys.executable`. | Con Python 3.15, la instalación de pandas 2.3.3 intentó compilar desde el código fuente y falló; requiere activar el entorno manualmente y `requirements.txt` con rangos no fija versiones. | Para un script pequeño en un equipo que ya tiene Python. |
| uv | `uv run` crea y utiliza el entorno del proyecto; `pyproject.toml` y `uv.lock` permiten reconstruir dependencias. | Está centrado en paquetes Python de PyPI y no cubre paquetes nativos como conda. | Para un proyecto solo Python con dependencias y lock compartible. |
| conda | Entorno con nombre reutilizable y gestión de Python y paquetes nativos desde `conda-forge`. | Hay que activar el entorno manualmente; los rangos del YAML no garantizan las mismas versiones finales y puede haber confusión entre varios entornos. | Para experimentación con Python y paquetes nativos. |
| Pixi | `pixi run` no necesita activación manual; el lock fija versiones y las tareas quedan en `pixi.toml`. | Requiere aprender otra herramienta y el entorno local ocupa espacio dentro de `.pixi/`. | Para proyectos del módulo que necesitan entornos, dependencias y tareas reproducibles. |

## 6. Decisiones (una elección + razón)

1. **Script pequeño en un equipo con Python:** venv + pip, porque no obliga a instalar otro gestor.
2. **Proyecto solo Python con lock:** uv, porque `pyproject.toml` y `uv.lock` permiten reconstruir el entorno con `uv sync --locked`.
3. **Entorno de experimentación con paquetes nativos:** conda, porque gestiona paquetes nativos de `conda-forge` en un entorno con nombre.
4. **Proyecto del módulo reproducible:** Pixi, porque reúne dependencias, lock y tareas en un manifiesto.


## Archivos de código y dependencias que se adjuntan

- **01-venv:** `analisis.py` final y `requirements.txt`.
- **02-uv:** `analisis.py`, `pyproject.toml` y `uv.lock`.
- **03-conda:** `analisis.py`, `environment.yml` y `environment-exportado.yml`.
- **04-pixi:** `analisis.py`, `pixi.toml` y `pixi.lock`.

No adjuntar las carpetas `.venv/`, `.pixi/` ni la instalación de conda. El registro no contiene el código completo de los manifiestos de conda, así que deben adjuntarse los archivos originales.

