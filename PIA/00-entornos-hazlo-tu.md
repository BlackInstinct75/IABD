# Taller «hazlo tú» — Instalar, configurar y probar entornos de Python

**Primero lo hacemos; después comparamos.** Trabajaremos, por este orden, con **venv + pip → uv → conda → Pixi**. En cada bloque instalarás o comprobarás la herramienta, prepararás un entorno, ejecutarás el mismo análisis y harás una modificación. No basta con mirar una demostración o explicar qué haría un comando.

**Entrega:** un registro `registro-entornos.md` o PDF en Moodle. **Valoración binaria:** hecho / no hecho, como evidencia de seguimiento; no es una prueba de aciertos. Entrega lo realizado al acabar la sesión y completa después lo que falte. No marques un bloque como terminado si solo has descargado el instalador.

Puedes resolver incidencias con tu pareja, pero cada estudiante ejecuta los pasos en su equipo y conserva su registro. Si una restricción del equipo lo impide, realiza el bloque en el equipo de la pareja por turnos y anota qué queda pendiente en el tuyo.

## 0. Preparar la mesa de trabajo

### Carpetas y terminal

1. Crea una carpeta **fuera del repositorio del curso**, por ejemplo `pia-entornos-taller`, y ábrela en VS Code.
2. Dentro, crea `01-venv`, `02-uv`, `03-conda` y `04-pixi`. Cada bloque tiene su carpeta para que sus manifiestos y entornos no se mezclen.
3. Abre una terminal en la carpeta del bloque indicado. Para cambiar de herramienta, desactiva el entorno anterior y abre una terminal nueva. En la terminal de conda usa `conda deactivate` si aparece un entorno activo que no corresponde.
4. Los comandos de instalación se ejecutan **solo si la herramienta falta**. Si ya funciona, registra su versión y pasa a configurar el ejemplo; no reinstales por rutina.

### Un mismo ejemplo para comparar

Crea `analisis.py` en `01-venv` con este contenido. Después copia **la versión inicial** del archivo a las otras tres carpetas usando el explorador de VS Code:

```python
import sys

import pandas as pd

datos = pd.DataFrame({
    "grupo": ["A", "A", "B"],
    "importe": [10, 20, 30],
})
total = int(datos["importe"].sum())
resumen = datos.groupby("grupo")["importe"].sum().to_dict()

print("Python:", sys.executable)
print("pandas:", pd.__version__)
print("Total:", total)
print("Por grupo:", resumen)
assert total == 60, "Revisa los datos o el resultado esperado"
print("PRUEBA OK")
```

**Resultado inicial esperado en los cuatro entornos:** `Total: 60`, `Por grupo: {'A': 30, 'B': 30}` y `PRUEBA OK`. La ruta de Python debe corresponder al entorno de ese bloque; las versiones concretas de pandas pueden variar dentro de las restricciones indicadas.

### Registro desde el primer bloque

Crea `registro-entornos.md`. Para **cada herramienta**, anota:

| Evidencia | Qué guardar |
|---|---|
| Instalar / comprobar | Sistema operativo, comando de instalación o «ya instalada» y versión. |
| Configurar | Comandos de creación del entorno y dependencias. |
| Ejecutar y probar | Comando de ejecución, ruta de Python y salida con `PRUEBA OK`. |
| Modificar | Cambio solicitado, comando repetido y resultado obtenido. |
| Repetir | Archivo de dependencias o manifiesto y comando para instalar desde él. |
| Incidencia, si la hay | Error exacto, intento de solución y estado final. |

## 1. venv + pip: el punto de partida

**Dónde:** terminal en `01-venv`. Aquí `venv` crea el aislamiento y `pip` instala paquetes dentro de él.

### 1.1. Instalar o comprobar Python, venv y pip

**Windows (PowerShell):**

```powershell
py --version
py -m venv --help
```

Si `py` no existe, prueba `python --version`. Si no tienes Python, instala Python 3.12 desde [python.org](https://www.python.org/downloads/), incluyendo pip y el lanzador de Python, y abre una terminal nueva. Si en tu equipo solo funciona `python`, sustituye `py` por `python` en el comando de creación siguiente.

**Linux/macOS:**

```bash
python3 --version
python3 -m venv --help
```

Si falta Python en macOS, usa el instalador de [python.org](https://www.python.org/downloads/macos/). En Ubuntu/Debian, si falta el módulo `venv`, instala el paquete del sistema que corresponda a tu Python; para el Python predeterminado:

```bash
sudo apt install python3-venv
```

Si tampoco existe `python3`, el profesor ayudará con la instalación apropiada para esa distribución. El permiso de administración es para instalar un componente del sistema, **no para instalar pandas con `sudo pip`**.

### 1.2. Crear y activar

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, usa una terminal **CMD** en esa misma carpeta y ejecuta `.venv\Scripts\activate.bat`. También puedes trabajar sin activar usando `.\.venv\Scripts\python.exe` en lugar de `python` en los comandos del bloque.

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 1.3. Instalar dependencias, ejecutar y probar

Crea `requirements.txt` en el editor con una línea:

```text
pandas>=2.2,<3
```

Con el entorno activo:

```bash
python -m pip --version
python -m pip install -r requirements.txt
python analisis.py
```

**Punto de control:** pip y Python apuntan a `.venv`, el total es 60 y aparece `PRUEBA OK`.

### 1.4. Haz un cambio y repite

En este `analisis.py`, cambia el último importe de **30 a 40** y la comprobación a `assert total == 70, "Revisa los datos o el resultado esperado"`. Ejecuta otra vez:

```bash
python analisis.py
```

Debes obtener total **70**, grupo B **40** y `PRUEBA OK`. Guarda las dos salidas en tu registro. `python -m pip install -r requirements.txt` permite instalar de nuevo las dependencias declaradas; este archivo con rangos **no fija una resolución exacta**.

Termina con `deactivate` si activaste el entorno. Fuera de él **no suponemos que pandas vaya a fallar**: puede estar instalado en otro Python. La prueba de aislamiento es la ruta de `sys.executable`, no provocar un import fallido.

## 2. uv: proyecto Python con manifiesto y lock

**Dónde:** terminal nueva en `02-uv`, con la versión inicial de `analisis.py`.

### 2.1. Instalar y dejar el comando disponible

Prueba `uv --version`. Si falta, ejecuta **solo el comando de tu sistema**:

**Linux/macOS:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Abre una terminal nueva en `02-uv` y comprueba `uv --version`. La configuración inicial consiste en que el ejecutable esté disponible en el `PATH`; sigue el mensaje del instalador si no aparece. [Instalación oficial de uv](https://docs.astral.sh/uv/getting-started/installation/).

### 2.2. Crear el proyecto y añadir pandas

```bash
uv init --bare --python 3.12
uv add "pandas>=2.2,<3"
uv run python analisis.py
```

uv puede descargar Python 3.12 si hace falta. No necesitas activar `.venv` ni instalar pip manualmente: `uv run` usa el entorno del proyecto.

**Punto de control:** total 60, `PRUEBA OK`, Python dentro de `02-uv/.venv` y archivos `pyproject.toml` y `uv.lock`. Abre el manifiesto y localiza pandas en las dependencias; no hace falta leer todo el lock.

### 2.3. Añadir una dependencia y comprobar el cambio

```bash
uv add rich
uv run python -c "from rich import print; print('[green]uv listo[/green]')"
uv sync --locked
uv run python analisis.py
```

Comprueba que `rich` aparece en `pyproject.toml` y que el análisis sigue pasando. Anota qué cambió en el manifiesto y en el lock. Para reconstruir el entorno con esos archivos, el comando es `uv sync --locked`; no se comparte `.venv/`.

## 3. conda: entorno nombrado y especificación YAML

**Dónde:** carpeta `03-conda`, con la versión inicial de `analisis.py`.

### 3.1. Instalar y configurar conda

Prueba `conda --version`. Si ya funciona en Miniconda, Anaconda o Miniforge, utiliza esa instalación. Si falta, instala **Miniforge**:

**Windows:**

1. Abre la [página oficial de Miniforge](https://github.com/conda-forge/miniforge#download) y descarga el instalador de Windows correspondiente a tu equipo.
2. Ejecuta el instalador para tu usuario y completa el asistente.
3. Abre **Miniforge Prompt** desde Inicio. En esa terminal, cambia a `03-conda` (puedes usar `cd /d "ruta-completa\03-conda"`).
4. Comprueba `conda --version`. Si prefieres PowerShell, ejecuta `conda init powershell` desde una terminal donde conda funcione y abre de nuevo PowerShell.

**Linux/macOS:**

Descarga el instalador para la arquitectura del equipo. Ejecuta **solo el bloque de tu sistema**, desde una carpeta donde quieras guardar el instalador:

**Linux:**

```bash
curl -fsSLo Miniforge3.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-$(uname -m).sh"
```

**macOS:**

```bash
curl -fsSLo Miniforge3.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-$(uname -m).sh"
```

Después, en esa misma carpeta:

```bash
bash Miniforge3.sh
```

Completa el asistente y acepta inicializar conda para tu shell. Abre una terminal nueva en `03-conda`. Si no aceptaste la inicialización, ejecuta el `conda init` correspondiente a tu shell desde la instalación, como explica el [manual de conda](../01-teoria/00c-manual-conda-pia.md). Si tu arquitectura no tiene instalador disponible, consulta la tabla oficial con el profesor.

En ambos sistemas:

```bash
conda --version
conda env list
conda config --show solver
```

Miniforge usa conda-forge. Conda moderno usa libmamba como solver por defecto; **no tienes que instalar mamba además**. Ver y anotar la configuración es parte del bloque.

### 3.2. Crear la especificación e instalar el entorno

Crea `environment.yml` en `03-conda`:

```yaml
name: pia-taller-conda
channels:
  - conda-forge
  - nodefaults
dependencies:
  - python=3.12
  - pandas>=2.2,<3
```

```bash
conda env create -f environment.yml
conda activate pia-taller-conda
python analisis.py
```

Si `pia-taller-conda` ya existe por un intento anterior, actualízalo con `conda env update -n pia-taller-conda -f environment.yml --prune` en lugar de crear otro con otro nombre.

**Punto de control:** total 60, `PRUEBA OK`, Python dentro del prefijo de `pia-taller-conda` y entorno visible en `conda env list`. El entorno nombrado no tiene por qué estar dentro de `03-conda`.

### 3.3. Actualizar el mismo entorno y probar

Añade `- rich` a la lista `dependencies` del YAML, con la misma sangría que pandas, y ejecuta:

```bash
conda env update -n pia-taller-conda -f environment.yml --prune
python -c "from rich import print; print('[green]conda listo[/green]')"
python analisis.py
conda env export -n pia-taller-conda --from-history > environment-exportado.yml
conda deactivate
```

Abre la exportación y localiza Python, pandas y rich. La exportación va a **otro archivo** para conservar la especificación original. Un YAML con rangos no garantiza las mismas versiones finales al resolver otro día.

## 4. Pixi: proyecto con paquetes conda, lock y tareas

**Dónde:** terminal nueva en `04-pixi`, con la versión inicial de `analisis.py`. Creas un proyecto pequeño propio; no resuelvas todos los entornos del repositorio del curso para este taller.

### 4.1. Instalar y dejar el comando disponible

Prueba `pixi --version`. Si falta:

**Linux/macOS:**

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

Abre una terminal nueva en `04-pixi` y comprueba:

```bash
pixi --version
```

Si no aparece, sigue el ajuste de `PATH` indicado por el instalador. [Instalación oficial de Pixi](https://pixi.sh/latest/installation/).

### 4.2. Crear, configurar y ejecutar

```bash
pixi init .
pixi add "python=3.12" "pandas>=2.2,<3"
pixi run python analisis.py
```

Abre `pixi.toml` y localiza el canal y las dependencias. Comprueba que existe `pixi.lock` y que Python está en `.pixi/envs/default`.

**Punto de control:** total 60, `PRUEBA OK`, manifiesto y lock presentes. `pixi run` prepara y usa el entorno sin una activación manual.

### 4.3. Crear una tarea y añadir una dependencia

```bash
pixi task add analizar "python analisis.py"
pixi run analizar
pixi add rich
pixi run python -c "from rich import print; print('[green]Pixi listo[/green]')"
pixi install --locked
pixi run analizar
```

Localiza `analizar` y `rich` en el manifiesto. Anota qué comando instala desde el lock y cuál ejecuta tu tarea. Se comparten `pixi.toml`, `pixi.lock` y el código; **no** `.pixi/`.

## 5. Ahora sí: comparar lo que has probado

Completa esta tabla con **una ventaja, un inconveniente y un uso razonable de cada opción**, basándote en la experiencia del taller:

| Opción | Ventaja observada | Inconveniente observado | Cuándo la elegiría |
|---|---|---|---|
| venv + pip | | | |
| uv | | | |
| conda | | | |
| Pixi | | | |

No compares velocidades como si fueran un benchmark: unas descargas pueden aprovechar caché y otras no. Compara pasos, aislamiento, archivos de proyecto, paquetes nativos y posibilidad de repetir el trabajo.

Resuelve con una herramienta y una razón:

1. Script pequeño en un equipo que ya tiene Python, sin instalar otro gestor.
2. Proyecto solo Python con dependencias y lock para compartir.
3. Entorno nombrado de experimentación con Python y paquetes nativos.
4. Proyecto del módulo con entornos y tareas reproducibles.

Puede haber más de una respuesta defendible. Después de escribir la tuya, consulta el [mapa de herramientas](../01-teoria/00a-entornos-python.md) para contrastarla.

**Qué retomaremos después:** Poetry para empaquetar/publicar, pipx para utilidades y Docker para despliegue. Se sitúan brevemente al cerrar; no son nuevas instalaciones obligatorias de este taller. Mamba/micromamba son alternativas del ecosistema conda, no un quinto entorno que tengas que preparar hoy.

## 6. Entrega y continuación

- Adjunta `registro-entornos.md` o PDF con las evidencias y la comparación.
- Incluye el código final y los archivos de dependencias de los bloques realizados, como archivos adjuntos o bloques de texto identificados por carpeta. No adjuntes los directorios `.venv/` o `.pixi/`, ni la instalación de conda.
- Indica por separado los bloques **completos**, **en curso** y **no iniciados**. La evidencia mínima de un bloque completo es su prueba ejecutada y su modificación comprobada.
- Si no caben todas las instalaciones en las dos horas, guarda el punto exacto y continúa en la siguiente sesión o en casa. No se sustituye una práctica pendiente por una explicación oral.

### Ampliación cuando los cuatro bloques estén completos

En **uno de los proyectos**, añade Matplotlib con su gestor, ejecuta una gráfica y guarda `resumen.png`. Escribe en el registro qué comando has utilizado. Puedes tomar como referencia el notebook `02-tratamiento-datos/02-ejemplos/03_pandas_eda_visualizacion.ipynb` del módulo. No ejecutes `pixi run --environment ud2` en el repositorio del curso: ese entorno aún no está declarado; el proyecto pequeño de este taller sí se puede ampliar directamente.

## Referencias de consulta

- [Mapa de entornos de Python](../01-teoria/00a-entornos-python.md).
- [Manual de Pixi](../01-teoria/00b-manual-pixi-pia.md).
- [Manual de conda](../01-teoria/00c-manual-conda-pia.md).
- [Guía de proyecto de UD2](../01-teoria/10a-guia-proyecto-python-pixi.md).
- [Proyectos con uv](https://docs.astral.sh/uv/guides/projects/).
