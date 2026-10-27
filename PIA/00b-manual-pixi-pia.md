# Manual práctico de Pixi para PIA

Este manual introduce **Pixi** desde cero en **UD2** y se retoma en las unidades posteriores conforme hagan falta más entornos. Se apoya en el [mapa de herramientas de Python](00a-entornos-python.md); para la alternativa tradicional, consulta el [manual de conda](00c-manual-conda-pia.md).

El repositorio ya incluye `pixi.toml` y `pixi.lock`. Los ejemplos de diseño no equivalen a una migración completa: hay que comprobar las dependencias de cada actividad antes de sustituir `environment.yml`. Para empezar con datos tabulares, sigue la [guía de proyecto de UD2](10a-guia-proyecto-python-pixi.md); los apartados de ML y GPU se consultarán cuando se utilicen.

**Primera sesión:** sigue el [taller práctico](../03-practicas/00-entornos-hazlo-tu.md), que instala Pixi y crea un proyecto pequeño con un ejemplo comprobable. Después usa este manual para ampliar; no hace falta resolver todos los entornos del curso para aprender el flujo básico.

## Ruta rápida

1. Instala Pixi y comprueba la versión.
2. Crea o abre el proyecto que contiene `pixi.toml`.
3. Instala el entorno `default`; los demás se preparan al ejecutarlos.
4. Ejecuta los comandos del curso con `pixi run` o entra en una shell Pixi.

```bash
pixi --version
pixi install
# Este comando instala/prepara el entorno ud3 si todavía no existe
pixi run --environment ud3 python --version
```

## ¿Qué problema resuelve?

Conda y Mamba resuelven bien paquetes Python y nativos, pero la composición de un entorno base con extras por unidad suele requerir varios ficheros o clones manuales. `uv` es rápido y excelente para proyectos Python, aunque trabaja principalmente con un entorno virtual y paquetes Python.

Pixi combina canales Conda y PyPI, fija versiones en un lockfile y permite definir **features** reutilizables y **environments** que las combinan. No hay herencia física perfecta: cada entorno tiene su prefijo, aunque Pixi comparte resolución y caché.

| Necesidad | Opción más adecuada |
|---|---|
| Python puro y un `.venv` | `uv` |
| Paquetes nativos, Conda y CPU/GPU aisladas | Pixi |
| Entorno Conda tradicional | Conda/Mamba |

## Instalación segura

Consulta siempre la [instalación oficial de Pixi](https://pixi.sh/latest/installation/). En Linux o macOS, el instalador oficial puede ejecutarse así:

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

Después, abre un terminal nuevo y verifica:

```bash
pixi --version
pixi info
```

En Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

Abre una terminal nueva y comprueba `pixi --version`. Como alternativa, la [guía oficial](https://pixi.sh/latest/installation/) documenta la instalación con WinGet. Usa un solo método; no reinstales si ya funciona.

## Conceptos esenciales

- **`pixi.toml`**: manifiesto del proyecto: canales, dependencias, tareas, features y entornos.
- **`pixi.lock`**: versiones exactas resueltas. Debe versionarse para reproducibilidad.
- **Feature**: conjunto nombrado de dependencias, por ejemplo `ud3` o `gpu`.
- **Environment**: combinación de features que se instala y ejecuta como un entorno independiente.
- **Feature `base`**: dependencias comunes del curso. Cada entorno la incluye de forma explícita cuando la necesita; así se pueden aislar herramientas incompatibles.
- **`.pixi/`**: prefijos y metadatos locales de los entornos. No se versiona; la caché de paquetes suele estar fuera del proyecto.

Referencia: [manifesto y conceptos de Pixi](https://pixi.prefix.dev/latest/reference/pixi_manifest/).

## Comandos esenciales

```bash
# Crear un proyecto nuevo
pixi init pia-piloto
cd pia-piloto

# Añadir dependencias comunes a la feature default
pixi add python=3.12 numpy pandas jupyterlab

# Añadir dependencias a una feature
pixi add --feature ud3 scikit-learn xgboost

# Crear un entorno que combine features
pixi project environment add ud3 --feature default --feature ud3

# Resolver e instalar
pixi install

# Ejecutar sin activar una shell
pixi run python --version
pixi run --environment ud3 python -c "import sklearn; print(sklearn.__version__)"

# Entrar temporalmente en una shell
pixi shell --environment ud3

# Consultar paquetes y dependencias
pixi list --environment ud3
pixi tree --environment ud3

# Actualizar versiones permitidas por pixi.toml
pixi update
```

Las opciones exactas pueden cambiar entre versiones; si un comando no coincide, consulta `pixi <comando> --help` y la [referencia de CLI](https://pixi.prefix.dev/latest/reference/cli/pixi/).

## Diseño piloto para PIA

La siguiente estructura es un **diseño de prueba**, no una migración terminada:

```toml
[workspace]
name = "pia"
channels = ["conda-forge"]
platforms = ["linux-64", "win-64", "osx-64", "osx-arm64"]

[feature.base.dependencies]
python = "3.12.*"
numpy = "*"
pandas = "*"
jupyterlab = "*"

[feature.ud3.dependencies]
scikit-learn = "*"
xgboost = "*"

[feature.ud4.dependencies]
pytorch = "*"
torchvision = "*"

[feature.gpu.dependencies]
# La selección concreta de CUDA debe validarse por plataforma y hardware.

[environments]
default = ["base"]
ud3 = ["base", "ud3"]
ud3-pycaret = ["ud3-pycaret"]
ud3-flaml = ["base", "ud3", "ud3-flaml"]
ud4 = ["base", "ud4"]
ud4-gpu = ["base", "ud4", "gpu"]
```

La sintaxis y las dependencias concretas deben validarse con el prototipo real. En particular, no se debe añadir CUDA al entorno común: muchos equipos del alumnado solo disponen de CPU y una variante GPU puede exigir controladores compatibles. Consulta la guía oficial de [entornos múltiples y features](https://pixi.prefix.dev/latest/workspace/multi_environment/).

## Seleccionar un entorno

Desde la raíz del proyecto:

```bash
pixi run --environment default jupyter lab
pixi run --environment ud3 python practica.py
pixi run --environment ud4 python entrenamiento.py
pixi run --environment ud4-gpu python entrenamiento_gpu.py
```

También puedes entrar en una shell (`pixi shell --environment ud3`) y trabajar normalmente. Sal de ella con `exit`. Para evitar errores, indica siempre el entorno en instrucciones escritas para el alumnado.

## PyCaret (UD3, P2)

PyCaret 3.3 declara compatibilidad con NumPy `>=1.21,<1.27`, mientras que la base del curso usa NumPy 2. Para P2 se fija la serie 1.26, ya validada con el lockfile, en un entorno autónomo con Python 3.11; no compone `default` ni `ud3`:

```bash
pixi install --environment ud3-pycaret
pixi run --environment ud3-pycaret python -c "import pycaret; print(pycaret.__version__)"
pixi run --environment ud3-pycaret jupyter lab
```

Usa `ud3-pycaret` únicamente para P2. Para el resto del modelado clásico, usa `ud3`; no añadas GPU a esta práctica.

## FLAML (UD3, alternativa experimental)

[FLAML](https://microsoft.github.io/FLAML/) queda disponible como alternativa ligera de AutoML para evaluar durante el curso. **No sustituye PyCaret ni es requisito de P2**. Comparte la base de UD3 (Python 3.12 y NumPy 2), por lo que no necesita el aislamiento de compatibilidad de PyCaret.

```bash
pixi install --environment ud3-flaml
pixi run --environment ud3-flaml python 03-machine-learning/02-ejemplos/flaml/flaml_holdout_sintetico.py
```

El ejemplo reserva el 20 % de datos sintéticos antes de la búsqueda, limita el tiempo y usa F1. Sus métricas solo son una comprobación técnica: no se interpretan ni se entregan. Consulta su [README](../../03-machine-learning/02-ejemplos/flaml/README.md) para el patrón completo.

## VS Code y Jupyter

1. Ejecuta `pixi install` desde la carpeta del proyecto.
2. En VS Code, selecciona como intérprete el Python del entorno Pixi correspondiente; la extensión Python permite elegir intérpretes detectados en `.pixi/envs/`.
3. Para notebooks, inicia Jupyter con `pixi run --environment ud3 jupyter lab`.
4. Si el kernel no aparece, instala o registra `ipykernel` en esa feature y reinicia VS Code/Jupyter.

No abras notebooks desde otro Python del sistema: es una causa frecuente de importaciones inconsistentes.

## CPU, GPU y CUDA

- El entorno `default` debe funcionar en CPU.
- GPU es una variante opcional, no un requisito general.
- CUDA necesita versión compatible de controlador, sistema operativo y paquete.
- Hay que probar cada combinación antes de publicarla y documentar cómo volver al entorno CPU.
- Nunca incluyas claves, tokens ni datos personales en `pixi.toml` o notebooks.

## Problemas frecuentes

| Problema | Comprobación o solución |
|---|---|
| `pixi: command not found` | Abre un terminal nuevo y revisa el `PATH`; vuelve a ejecutar `pixi --version`. |
| El paquete no se resuelve | Comprueba nombre/canal, plataforma y versión; prueba primero sin restricciones demasiado estrechas. |
| Importación desde el Python equivocado | Usa `pixi run --environment ...` y selecciona el intérprete Pixi en VS Code. |
| El kernel no aparece | Instala `ipykernel` en el entorno y reinicia Jupyter/VS Code. |
| Fallo de GPU | Comprueba `nvidia-smi`, controlador, plataforma y compatibilidad CUDA; usa CPU como diagnóstico. |
| Lockfile desactualizado | Ejecuta `pixi update` de forma deliberada y revisa el diff de `pixi.lock`. |

## Buenas prácticas de repositorio

- Versiona `pixi.toml` y `pixi.lock`.
- Añade `.pixi/` al `.gitignore`; nunca versiones los prefijos locales.
- Revisa los cambios de actualización masiva del lockfile antes de confirmarlos.
- Mantén features pequeñas y con nombres estables (`ud3`, `ud4`, `gpu`).
- Documenta la versión de Pixi y las plataformas probadas.
- Conserva `environment.yml` hasta cerrar la migración y verificar dependencias reales.

## Flujo recomendado

1. Instalar Pixi una sola vez.
2. Clonar o actualizar el repositorio.
3. Ejecutar `pixi install`.
4. Usar el entorno indicado en la tarea (`pixi run --environment ud3 ...`).
5. Comunicar el comando y el error completo si algo falla; no borrar `.pixi/` sin conservar el mensaje de error.

Si una actividad no indica un entorno Pixi, sigue su enunciado o consulta al
profesorado antes de instalar dependencias adicionales.
