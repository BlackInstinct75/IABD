# Actividad cooperativa: EDA de Titanic con tres motores

## El reto

¿Qué variables aparecen asociadas con la supervivencia en el Titanic? Vais a
investigarlo con el mismo CSV y las mismas preguntas usando **Polars**, **DuckDB**
o **cuDF**. Después compartiréis lo aprendido y presentaréis una conclusión
respaldada por datos.

La actividad es de **análisis exploratorio**: describimos asociaciones observadas
en este conjunto de datos; no demostramos causas ni entrenamos modelos.

## Organización y tiempo

Duración: **una sesión de 3 h** o **trabajo de 2 h y exposiciones en la siguiente**. No se adelantan las exposiciones recortando el tiempo de probar el motor.

1. **Equipo experto:** cada persona trabaja solo con el motor que le
   corresponda. No hay que completar los otros dos notebooks.
2. **Grupo mixto:** se reúne una persona experta en Polars, otra en
   DuckDB y otra en cuDF. Cada cual enseña su flujo, resultados y limitaciones.
3. **Preparar y presentar:** el grupo mixto organiza una exposición
   al resto de la clase. Hablan los tres representantes.

Los grupos mixtos pueden tener **3–4 integrantes** para ajustar el reparto. Debe
haber al menos una persona de cada motor; la cuarta actúa como coexperta de uno
de ellos y también explica su aportación.

| Minutos de una sesión de 3 h | Trabajo |
|---|---|
| 0–10 | Reparto de motores, pregunta y contrato de resultados |
| 10–60 | Trabajo experto: núcleo común y pregunta propia |
| 60–70 | Descanso |
| 70–100 | Grupos mixtos: contrastar evidencias y resolver discrepancias |
| 100–120 | Preparar informe y presentación |
| 120–170 | Exposiciones: hasta siete grupos, 5 min + 2 min de preguntas cada uno |
| 170–180 | Síntesis y entrega |

Si la sesión es de **2 h**, el último tramo se dedica a preparar/guardar la
entrega; las exposiciones pasan a la siguiente. Si hay más de siete grupos,
el profesor repartirá las exposiciones entre sesiones.

| Equipo experto | Recurso | Entorno |
|---|---|---|
| Polars | [Notebook Titanic con Polars](eda_titanic_polars.ipynb) | Python local; Polars |
| DuckDB | [Notebook Titanic con DuckDB](eda_titanic_duckdb.ipynb) | Python local; SQL |
| cuDF | [Notebook Titanic con cuDF](eda_titanic_cudf_colab.ipynb) | Google Colab con GPU NVIDIA si está disponible |

El profesor proporciona por Moodle un paquete autónomo con esta consigna, los tres
notebooks, el CSV original y `requirements-titanic-multimotor.txt`. Extraed todos
los archivos en la misma carpeta. Los notebooks locales ya están preparados para
cargar `titanic.csv` situado junto a ellos. En Colab, subid el mismo CSV original
cuando lo solicite el notebook.

## Preparar el entorno local (CPU, recomendado en Windows)

No necesitáis clonar GitHub ni descargar el repositorio completo. Los archivos
`pixi.toml` y `pixi.lock` de la raíz son herramientas docentes y no son requisitos
para el alumnado. Con Python **3.12** instalado, abrid PowerShell en la carpeta
que contiene los archivos de Moodle y ejecutad:

```bash
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip
python -m pip install -r requirements-titanic-multimotor.txt
jupyter lab
```

Si PowerShell bloquea la activación, usad el activador de `cmd`:

```bash
.venv\Scripts\activate.bat
```

En macOS/Linux, abrid una terminal en esa misma carpeta y ejecutad el equivalente:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install --upgrade pip
python -m pip install -r requirements-titanic-multimotor.txt
jupyter lab
```

DuckDB se usa principalmente con SQL; su conversión a pandas mediante `.df()`
está disponible en el notebook.

## Preparar cuDF en Google Colab

El equipo de cuDF debe abrir Colab, elegir **File > Upload notebook** y subir
`eda_titanic_cudf_colab.ipynb`. Después elegid **Runtime > Change runtime type**,
seleccionad **GPU** y ejecutad el preflight del notebook. Cuando lo solicite,
subid también el CSV original. Si cuDF aparece **LISTO**, no instaléis nada. Si
hay GPU detectada pero aparece **ERROR DE INSTALACIÓN**, seguid la celda del
notebook y su instalador oficial. Sin GPU, marcad **NO EJECUCIÓN DE CUDF** y no
intentéis instalar RAPIDS en local.

## Análisis común

Todos los equipos deben producir resultados comparables:

1. Cargar el CSV original y comprobar forma, columnas, tipos y valores ausentes.
2. Calcular supervivientes, total y tasa para `Sex` y para `Pclass`.
3. Repetir el cálculo para cada combinación de `Pclass × Sex`.
4. Comparar `Age < 18` con `Age >= 18`. En este cálculo se excluyen las filas
   cuya edad falta; indicad los denominadores.
5. Escribir un hallazgo respaldado por cifras y una limitación del análisis.

### Contrato de las tablas

Los tres motores deben devolver las mismas claves de agrupación y, a continuación,
**exactamente estas tres columnas**:

| Columna | Significado |
|---|---|
| `total` | Número de pasajeros **de ese grupo** |
| `supervivientes` | Suma de `Survived` en ese grupo |
| `tasa` | `supervivientes / total`, entre 0 y 1 |

No se usan `n` ni un `total` global repetido en las filas. Ejemplo: mujeres =
`total=314`, `supervivientes=233`, `tasa=233/314`. La tasa de menores de edad usa
113 como denominador; 714 es el total de edades conocidas, no el denominador de
cada tramo. Los tres cuadernos incluyen también una tabla global de comprobación.

### Reglas para que la comparación sea justa

- Usad el CSV **sin limpiar, imputar ni eliminar filas**. Solo se excluyen edades
  ausentes al calcular los dos tramos de edad.
- En cada grupo, `total` es el número de pasajeros y `supervivientes` es la suma
  de `Survived`; `tasa = supervivientes / total`. Mostrad siempre las tres
  cantidades, no solo el porcentaje.
- Ordenad `Sex` como `female`, `male`; `Pclass` como 1, 2, 3; y el cruce por
  clase ascendente y luego sexo `female`, `male`.
- Usad las mismas claves: `Sex`, `Pclass` y `grupo_edad`. En edad, las etiquetas
  son `<18`, `>=18`, en ese orden. Contrastad también la huella SHA-256 del CSV
  que imprime cada cuaderno: comparar archivos distintos no sería la misma tarea.
- Los recuentos deben coincidir exactamente. Las tasas pueden diferir como
  máximo `0.000001` por redondeo.
- No comparéis ni presentéis tiempos de ejecución: se usan entornos y equipos
  distintos.
- DuckDB se trabaja principalmente escribiendo SQL; no intentéis convertirlo en
  una API de DataFrame para que parezca igual a las otras herramientas.

## Pregunta propia del equipo experto

Además del núcleo común, **cada equipo experto formula y programa una pregunta
adicional**. No basta ejecutar las celdas resueltas ni volver a describir una tabla
ya incluida. Ejemplos de punto de partida:

- ¿Cómo cambia la supervivencia entre quienes viajan sin familiares registrados
  (`SibSp + Parch = 0`) y quienes tienen alguno?
- Dentro de tercera clase, ¿cambia la asociación observada al considerar solo
  pasajeros con edad conocida?
- ¿Qué comparación aporta el puerto de embarque? ¿Qué hacéis con los dos nulos?

Podéis elegir otra pregunta. Debe quedar en el cuaderno: **pregunta, filtro y
agrupación, denominador, código del motor, resultado y limitación**. El CSV
original no se modifica ni se imputan valores. Una tabla derivada o un filtro
explícito para responder a la pregunta no es una limpieza del original.

En el grupo mixto, distinguid **paridad del núcleo común** y **preguntas propias**:
si cada experto preguntó algo diferente, sus resultados extra no tienen por qué
coincidir. Si no se pudo ejecutar cuDF, su pregunta se entrega formulada y con el
código preparado, marcada como **PENDIENTE DE EJECUCIÓN**, sin inventar cifras.

## Si Colab no asigna una GPU

No dediquéis la sesión a instalar RAPIDS en los ordenadores del aula. Si Colab no
da una GPU compatible, anotadlo en el cuaderno y en el informe como **NO
EJECUCIÓN DE CUDF**. Si falla la instalación o la carga, conservad el estado de
error y su mensaje. Podéis explicar el código y usar la tabla de referencia
incluida en el notebook para participar en la puesta en común. No sustituyáis
cuDF por pandas ni presentéis esos resultados como una ejecución propia.

La detección del entorno, la carga del CSV y todas las operaciones cuDF están
condicionadas a un estado válido. Un import de cuDF por sí solo **no** acredita
una GPU utilizable. Limitad las incidencias de instalación a unos 10 minutos y
documentadlas para no perder toda la actividad.

## Puesta en común y presentación

**5 minutos de exposición y 2 de preguntas por grupo mixto**, con un máximo de
cinco diapositivas. Repartid la intervención entre todos los integrantes. Orden:
pregunta/datos → evidencia común → preguntas propias → herramientas y límites →
conclusión y siguiente pregunta para ML.

En el grupo mixto, cada representante debe explicar:

- cómo cargó y consultó los mismos datos;
- un resultado y su evidencia (numerador, denominador y tasa);
- una limitación o dificultad de su motor/entorno;
- en qué situación elegiría esa herramienta.

Presentad una conclusión común, no una competición de bibliotecas. El reto
amistoso puede reconocer el **hallazgo mejor respaldado**, la **explicación más
clara** o la **comparación más razonada**. **No se puntúan la rapidez ni los
tiempos de ejecución y no se declara un motor ganador.**

### Informe del grupo mixto

Copiad esta plantilla en el documento de presentación:

```text
Integrantes y motor experto de cada persona:

1. Pregunta que investigamos:
2. Resultado común que observamos (con numerador/denominador/tasa):
3. ¿Qué comparación nos pareció más informativa? ¿Por qué?
4. ¿Qué limitación impide interpretar esto como causalidad?
5. Polars: ¿qué aporta y qué dificultad encontramos?
6. DuckDB: ¿qué aporta el enfoque SQL y qué dificultad encontramos?
7. cuDF: ¿se ejecutó realmente con GPU? ¿Qué aporta y qué limitación hubo?
8. ¿Qué herramienta elegiríamos para este análisis y por qué?
9. ¿Qué pregunta o hipótesis retomaríamos al empezar ML?
10. Aportación individual de cada representante a la presentación:
```

## Entregas y seguimiento

Hay una entrega **por equipo experto** y otra **por grupo mixto**; no hay que
entregar los tres notebooks por estudiante. Una persona designada sube cada ZIP,
incluyendo la aportación de cada integrante. Archivos, nombres, plantilla y listas
de control en [entrega-comparativa-motores-titanic.md](entrega-comparativa-motores-titanic.md).

El seguimiento valora evidencias, explicación, interpretación y participación,
sin añadir porcentajes ni una carrera de velocidad. Una incidencia de GPU se
documenta: no se penaliza como si fuera un error de razonamiento.

## Continuidad con aprendizaje automático

Este EDA puede servir como punto de partida para una actividad posterior, pero
**aquí no se entrena ningún modelo**. Al empezar ML, `Survived` será la variable
objetivo `y`, nunca una columna de entrada `X`; la separación de entrenamiento y
prueba deberá preceder al ajuste de transformaciones para evitar fuga de datos.

## Preparación docente

- Entorno local: `pixi run --environment ud2 jupyter lab`.
- La guía antigua de cuDF del repositorio no se debe usar para instalar RAPIDS;
  el notebook de Colab enlaza la documentación oficial actual.
- Comprobaciones de referencia para docentes: 891 filas y 12 columnas; 177
  edades ausentes, 687 cabinas y 2 puertos de embarque. Global: 342/891.
  Mujeres: 233/314; hombres: 109/577. Por clase: 1, 136/216; 2, 87/184;
  3, 119/491. Cruce: Pclass 1 mujer 91/94 y hombre 45/122; Pclass 2 mujer
  70/76 y hombre 17/108; Pclass 3 mujer 72/144 y hombre 47/347. Edad menor
  de 18: 61/113; edad 18 o más: 229/601.
