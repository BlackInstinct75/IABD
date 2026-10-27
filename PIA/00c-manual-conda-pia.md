# Manual práctico de conda para PIA

Este manual se introduce en **UD2** y queda como referencia para las unidades posteriores. El [mapa de entornos de Python](00a-entornos-python.md) explica cuándo elegir cada herramienta; aquí aprenderás a trabajar con conda sin instalar las dependencias del proyecto en `base` ni crear un entorno por cada prueba.

**Pixi sigue siendo la herramienta principal del módulo.** Conda es una alternativa para experimentar con entornos nombrados y paquetes Python y nativos. Si una actividad indica una ruta concreta, sigue esa ruta. La [guía de proyecto de UD2](10a-guia-proyecto-python-pixi.md) concreta las dependencias de tratamiento de datos.

**Primera sesión:** realiza el [taller práctico](../03-practicas/00-entornos-hazlo-tu.md): instalar o comprobar Miniforge/conda, preparar un entorno mínimo desde YAML, ejecutar un análisis, añadir una dependencia y volver a probar. Este manual sirve como consulta durante ese trabajo y para ampliarlo después.

## 1. Qué es cada cosa

| Nombre | Significado |
|---|---|
| **conda** | Gestor de paquetes y entornos; también instala versiones de Python y bibliotecas nativas. |
| **Miniforge** | Instalador mínimo del ecosistema conda, preconfigurado para conda-forge. |
| **Miniconda / Anaconda Distribution** | Otras distribuciones que incluyen conda; no necesitas instalarlas si ya tienes una distribución funcional. |
| **conda-forge** | Canal comunitario de paquetes, no un gestor de entornos. |
| **libmamba** | Motor de resolución usado por defecto desde conda 23.10; una configuración previa puede seleccionar otro. |
| **mamba / micromamba** | Interfaces alternativas del ecosistema; no hace falta instalarlas para seguir este manual. |

Un entorno contiene su propio Python y sus paquetes. **Activarlo** modifica el entorno de la terminal para usar esos ejecutables; no modifica los paquetes de otros entornos. El aislamiento de dependencias no impide que tu programa lea o modifique archivos del equipo.

## 2. Instalación y primera comprobación

Si `conda --version` ya funciona, no reinstales. Si no tienes conda, una opción sencilla es [Miniforge](https://github.com/conda-forge/miniforge#install): descarga el instalador de tu sistema y arquitectura (Windows, Linux o macOS; Intel/AMD o ARM según el equipo) y sigue sus instrucciones.

- **Windows:** abre Miniforge Prompt. Si prefieres PowerShell, ejecuta `conda init powershell` desde una terminal donde conda funcione y vuelve a abrir PowerShell.
- **Linux/macOS:** sigue la inicialización de la shell que propone el instalador y abre una terminal nueva. Para Bash, si fuera necesario, usa `conda init bash` desde una terminal donde conda funcione.
- No encadenes una activación de `venv`, una shell de Pixi y una activación de conda. Empieza desde una terminal limpia.

Comprueba:

```bash
conda --version
conda info
conda env list
conda config --show solver
```

`base` contiene el gestor: **no es el entorno de las prácticas**. Instalar NumPy, pandas o Jupyter en `base` por comodidad mezcla el mantenimiento del gestor con las dependencias del proyecto.

## 3. Crear el entorno de UD2

Desde la carpeta de trabajo del proyecto, crea el entorno **una sola vez**, si no existe:

```bash
conda create -n pia-ud2 --override-channels -c conda-forge --strict-channel-priority python=3.12 "numpy>=2,<3" "pandas>=2.2,<3" "matplotlib>=3.8,<4" jupyterlab ipykernel
conda activate pia-ud2
python --version
python -c "import sys; print(sys.executable)"
python -c "import numpy, pandas, matplotlib; print(numpy.__version__, pandas.__version__, matplotlib.__version__)"
conda list
```

Las comillas evitan que la shell interprete los símbolos `<` y `>`. `--override-channels` limita esta operación a conda-forge; la prioridad estricta resulta especialmente relevante cuando hay varios canales. Estos argumentos no cambian la configuración global de otros proyectos.

La ruta de `sys.executable` debe pertenecer a `pia-ud2`. Si el nombre ya aparece en `conda env list`, actívalo y comprueba sus paquetes antes de crear nada.

También puedes ejecutar sin activar una shell:

```bash
conda run -n pia-ud2 python -c "import sys, pandas; print(sys.executable); print(pandas.__version__)"
```

## 4. Guardar una especificación del proyecto

Para repetir la instalación, guarda este archivo como `pia-ud2.yml` en la carpeta del proyecto:

```yaml
name: pia-ud2
channels:
  - conda-forge
  - nodefaults
dependencies:
  - python=3.12
  - numpy>=2,<3
  - pandas>=2.2,<3
  - matplotlib>=3.8,<4
  - jupyterlab
  - ipykernel
```

`nodefaults` evita añadir los canales predeterminados al crear el entorno desde este archivo. No es un canal del que descargar paquetes.

En otro equipo donde el entorno aún no exista:

```bash
conda env create -f pia-ud2.yml
conda activate pia-ud2
```

**No ejecutes las dos rutas de creación sobre el mismo entorno.** Puedes crearlo con el comando del apartado anterior o con el YAML; después trabajas con él y lo actualizas.

## 5. Actualizar sin multiplicar entornos

Si una práctica añade una dependencia compatible, modifica `pia-ud2.yml` y aplica:

```bash
conda env update -n pia-ud2 -f pia-ud2.yml --prune
```

`--prune` elimina dependencias que dejan de ser necesarias según la especificación. Revisa la propuesta antes de confirmarla. No es una orden para crear `pia-ud2-v2`, ni garantiza limpiar instalaciones hechas con pip.

Para añadir una dependencia de forma interactiva, por ejemplo Seaborn cuando se trabaje en clase:

```bash
conda install -n pia-ud2 --override-channels -c conda-forge --strict-channel-priority seaborn
```

Después actualiza la especificación: si no anotas el cambio, otro equipo no podrá repetirlo. Evita una actualización masiva de todos los paquetes justo antes de una entrega.

**Cuándo separar:** si un proyecto exige versiones incompatibles, necesita otro entorno. Por ejemplo, PyCaret 3.3 requiere versiones de NumPy/pandas distintas de las de UD2; no rebajes `pia-ud2` para hacerlo funcionar. La unidad de ML indicará su entorno específico.

## 6. Exportar: especificación no significa lockfile

Para obtener las dependencias solicitadas explícitamente:

```bash
conda env export -n pia-ud2 --from-history > pia-ud2.yml
```

Este comando **sobrescribe el archivo de destino**. Exporta a otro nombre si quieres comparar con una especificación escrita a mano. Revisa el YAML antes de compartirlo: elimina un eventual `prefix` local y comprueba nombre, canales y restricciones. Las dependencias instaladas con pip deben documentarse aparte; `--from-history` no es un inventario completo de ellas.

| Archivo | Qué conserva | Límite |
|---|---|---|
| YAML escrito a mano o exportado con `--from-history` | Dependencias directas y restricciones | Al resolver otro día pueden cambiar las versiones finales. |
| `conda env export -n pia-ud2` | Paquetes instalados y versiones resueltas | Puede incluir detalles específicos de una plataforma. |
| Lockfile de conda-lock | Resolución para las plataformas seleccionadas | Requiere generar y validar el lock; se profundizará cuando haga falta. |

Para UD2 basta con comprender y conservar la especificación. No confundas `environment.yml` con un lockfile ni copies los directorios locales de entornos al repositorio.

## 7. Jupyter y VS Code

Desde la raíz del módulo, con `pia-ud2` activo:

```bash
jupyter lab
```

En VS Code selecciona el intérprete de `pia-ud2` para scripts y el **kernel de ese entorno** para notebooks. El intérprete del editor y el kernel de un notebook pueden ser diferentes.

Si Jupyter no lo ofrece, registra el kernel desde el entorno:

```bash
conda run -n pia-ud2 python -m ipykernel install --user --name pia-ud2 --display-name "Python (PIA UD2)"
```

Esto registra un kernel para tu usuario; no instala las bibliotecas del proyecto en el Python del sistema. En la primera celda del notebook comprueba:

```python
import sys
import pandas as pd

print(sys.executable)
print(pd.__version__)
```

Abre `02-tratamiento-datos/02-ejemplos/03_pandas_eda_visualizacion.ipynb` para comprobar NumPy, pandas y Matplotlib con datos de la unidad.

## 8. Si necesitas pip

Busca primero el paquete en conda-forge. Si una dependencia solo está en PyPI, instala pip en el entorno y úsalo explícitamente:

```bash
conda install -n pia-ud2 --override-channels -c conda-forge pip
conda run -n pia-ud2 python -m pip --version
```

Después usa `conda run -n pia-ud2 python -m pip install nombre-del-paquete` con el nombre y la versión indicados por la actividad. Es un patrón, no un paquete que debas instalar ahora. Instala primero las dependencias conda y después las de pip; conserva estas últimas en una sección `pip:` del YAML cuando sean necesarias. Si conda cambia después dependencias que pip también gestiona, puede ser preferible recrear el entorno desde una especificación revisada.

No uses `sudo pip`, `pip install --user` ni un `pip` cuyo intérprete desconozcas para añadir paquetes a la práctica.

## 9. Terminar y resolver problemas

```bash
conda deactivate
conda env list
```

| Problema | Qué comprobar |
|---|---|
| `conda` no se reconoce | Terminal adecuada, inicialización de la shell y apertura de una terminal nueva. |
| `conda activate` pide inicializar | Usa `conda init` para la shell correspondiente y vuelve a abrirla. |
| El paquete está instalado, pero falla el import | `sys.executable` y kernel de Jupyter; prueba `conda run -n pia-ud2 ...`. |
| No se resuelven las versiones | Nombre del paquete, plataforma, canales y restricciones; conserva el mensaje del solver. |
| Solver distinto del esperado | Consulta `conda config --show solver`; conda moderno usa libmamba por defecto, pero una configuración anterior puede cambiarlo. |
| Entorno muy pesado | Revisa dependencias directas; el `environment.yml` raíz del curso no es el entorno mínimo de UD2. |

Solo para un entorno que ya no necesites, después de guardar su especificación y desactivarlo:

```bash
conda env remove -n nombre-del-entorno
```

No elimines `base`. Si registraste un kernel de un entorno eliminado, puedes retirar esa entrada con `jupyter kernelspec uninstall nombre-del-kernel` desde una instalación de Jupyter que funcione.

## 10. Chuleta de cierre

1. Comprueba el entorno antes de instalar o ejecutar.
2. Reutiliza un entorno mientras sus dependencias sean compatibles.
3. Versiona el YAML; no versiones los prefijos locales.
4. Una exportación portable no fija exactamente todos los paquetes.
5. En las unidades posteriores retomaremos locks, GPU o despliegue cuando sean necesarios.

## Referencias

- [Gestión de entornos — documentación oficial de conda](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html).
- [Prioridad de canales — documentación oficial de conda](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-channels.html).
- [Miniforge: instalación por plataforma](https://github.com/conda-forge/miniforge#install).
- [Manual de Pixi](00b-manual-pixi-pia.md) y [guía de proyecto de UD2](10a-guia-proyecto-python-pixi.md).
