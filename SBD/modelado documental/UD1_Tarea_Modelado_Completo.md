# UD1 · Tarea: diseño completo de un modelo de datos

> **RA/CE relacionados:** RA1.f (seleccionar e integrar sistemas), RA3.b
> (tecnologías eficientes para extraer valor) y, si se elige la ruta documental,
> RA4.a (escenarios y tipologías de datos no estructurados).

## 1. Problema

La empresa **NexoWork** gestiona una red de espacios de trabajo en Madrid,
Sevilla y Lisboa. Sus datos proceden de una exportación inicial de reservas,
pero todavía no existe un modelo de datos justificado.

La dirección necesita una solución que pueda responder a necesidades diferentes:

- registrar, modificar y cancelar reservas sin perder consistencia;
- mostrar a una persona su reserva completa con servicios adicionales;
- analizar ocupación, ingresos y cancelaciones por ciudad, espacio y mes;
- incorporar nuevos servicios y nuevas sedes sin rediseñar todo el sistema;
- conservar únicamente identificadores ficticios y no publicar datos personales.

Tu trabajo no consiste en elegir una tecnología conocida y adaptar los datos a
ella. Consiste en **diseñar el modelo a partir de los requisitos**, comparar
alternativas y justificar qué gestor o combinación de formato y motor resuelve
mejor el perfil de carga que elijas.

Esta actividad es independiente de la P2 de pedidos. No reutilices su modelo ni
la demo docente de reservas hoteleras como solución.

## 2. Material de partida

En `data/` encontrarás una pequeña exportación de reservas y sus ficheros
maestros:

- `reservas_fuente.csv`: una fila por reserva recibida desde la aplicación.
- `miembros_fuente.csv`: identificadores y segmentos ficticios de los miembros.
- `espacios_fuente.csv`: espacios reservables, sede, tipo y capacidad.
- `catalogo_servicios.csv`: código, descripción y precio unitario de cada
  servicio adicional.

La exportación es una **fuente**, no el modelo final. El campo `service_items`
usa el formato `codigo=cantidad;codigo=cantidad`; una cadena vacía significa que
no hay servicios. Las cantidades son enteros positivos y los códigos deben
existir en `catalogo_servicios.csv`. Debes decidir cómo representar esta
información en tu modelo.

Datos de partida:

- 18 reservas ficticias, pequeñas y suficientes para prototipar.
- 3 ciudades, 9 espacios, varios tipos de espacio y 4 canales de reserva.
- Estados `pending`, `confirmed`, `completed` y `cancelled`.
- Identificadores artificiales; no hay nombres, correos ni teléfonos reales.

## 3. Perfiles de carga: elige uno como principal

Todos los equipos trabajan sobre el mismo caso y deben describir brevemente los
tres perfiles. Después elegirán **uno** como objetivo principal de su prototipo.

### Perfil A · Operacional/transaccional

La prioridad es registrar reservas, evitar solapamientos, modificar estados y
mantener referencias válidas entre miembros, espacios y servicios.

Se espera consistencia inmediata, actualizaciones frecuentes y operaciones
concurrentes. Una base relacional como PostgreSQL suele ser una opción natural.

### Perfil B · Documental/de servicio

La prioridad es recuperar rápidamente una reserva completa para una API: datos
de la reserva, espacio, servicios, importes y estado en una única respuesta.

Se acepta un modelo documental como MongoDB, siempre que justifiques qué datos se
anidan, cuáles se referencian y cómo evitarás inconsistencias al actualizar.

### Perfil C · Analítico

La prioridad es calcular ocupación, ingresos y cancelaciones sobre el histórico,
leyendo muchas filas y agregando pocas columnas.

DuckDB + Parquet es una opción adecuada para un prototipo local OLAP. Debes
explicar por qué no lo estás utilizando como sistema transaccional principal.

## 4. Consultas y operaciones candidatas

Analiza todas y selecciona al menos **tres prioritarias** para tu perfil. Debes
implementar o demostrar las tres que selecciones.

1. ¿Qué reservas futuras y confirmadas tiene un miembro?
2. ¿Existe solapamiento de reservas en el mismo `space_id` y horario?
3. ¿Qué reservas incluyen un servicio determinado y en qué cantidad?
4. ¿Cómo recuperar una reserva completa para mostrarla en una aplicación?
5. ¿Qué ciudad tiene más horas reservadas por mes? Define si medirás horas de
   reserva o horas-plaza (`duración × seats`).
6. ¿Qué ingresos genera cada ciudad y tipo de espacio?
7. ¿Cuál es la tasa de cancelación por canal y mes? Usa como denominador todas
   las reservas creadas en ese periodo, salvo que justifiques otra definición.
8. ¿Qué servicios adicionales se solicitan más?

Para cada consulta prioritaria indica:

- usuario o proceso que la necesita;
- frecuencia aproximada;
- tiempo de respuesta esperado, aunque sea cualitativo;
- datos que debe leer o modificar;
- por qué influye en la elección del modelo.

## 5. Trabajo a realizar

### Fase 1 · Requisitos y objetivo

1. Resume el problema de NexoWork en 5–10 líneas.
2. Describe los tres perfiles de carga.
3. Elige uno como principal y justifica la elección con las consultas
   prioritarias.
4. Anota volumen actual, crecimiento esperado, frecuencia de lecturas y
   escrituras, concurrencia, evolución del esquema y nivel de consistencia.

### Fase 2 · Modelo conceptual

Identifica entidades, eventos y relaciones. Incluye un diagrama con, al menos:

- miembros;
- espacios o sedes;
- reservas;
- servicios;
- elementos de reserva o consumos de servicio.

Indica cardinalidades, por ejemplo `miembro 1:N reserva` y
`reserva N:M servicio` mediante una entidad o estructura intermedia.

El diagrama puede estar en Mermaid, draw.io, PlantUML o una imagen exportada.
Si utilizas Mermaid, entrega también una explicación textual para que el modelo
pueda revisarse sin renderizarlo.

### Fase 3 · Granularidad, claves y reglas

Completa una tabla como esta para cada tabla, documento o archivo del modelo:

| Elemento | ¿Qué representa exactamente? | Clave | Relaciones | Reglas |
|---|---|---|---|---|
| Reserva | Una reserva solicitada por un miembro | `reservation_id` | miembro, espacio | inicio < fin |

Debes justificar:

- clave primaria o identificador documental;
- claves foráneas o referencias;
- unicidad y posibles claves compuestas;
- granularidad de cada registro;
- representación de servicios y cantidades;
- campos originales frente a campos derivados.

### Fase 4 · Normalización, duplicación y anidamiento

Elabora una tabla de decisiones:

| Dato o relación | Decisión | Motivo | Riesgo | Cómo se mantiene la consistencia |
|---|---|---|---|---|
| Servicios de una reserva | Anidar / separar / referenciar | … | … | … |

No se busca una única respuesta correcta. Se evalúa que la decisión sea
coherente con el perfil elegido y que reconozca sus costes.

### Fase 5 · Comparación y elección tecnológica

Compara como mínimo **tres alternativas**, incluyendo las dos que no vas a
implementar. Como referencia puedes usar:

| Ruta | Ventaja principal | Riesgo o límite que debes valorar |
|---|---|---|
| PostgreSQL u otro SQL relacional | Integridad, joins y transacciones | Administración y esquema explícito |
| MongoDB u otro documental | Agregados y esquema flexible | Duplicación y relaciones complejas |
| DuckDB + Parquet | Analítica local y lectura columnar | No es el sistema OLTP principal |

Tu decisión debe incluir:

- gestor, formato y versión;
- modelo físico elegido;
- dos alternativas descartadas y el motivo;
- coste de operación y recursos necesarios;
- cómo evolucionaría el esquema;
- qué ocurriría si el volumen o la concurrencia se multiplicaran.

No es obligatorio instalar los tres gestores. La herramienta elegida debe poder
probarse localmente, con Docker o mediante una evidencia reproducible equivalente.
Otra tecnología es válida si explicas la elección y entregas las mismas pruebas.

### Fase 6 · Prototipo mínimo

Implementa sólo la ruta principal elegida:

- **SQL relacional:** DDL, restricciones, carga de una muestra y consultas
  reproducibles. PostgreSQL es recomendable para el perfil operacional; SQLite o
  DuckDB pueden usarse como prototipo si declaras sus límites.
- **MongoDB/documental:** NDJSON o script de carga, índices, una consulta de
  reserva completa y dos agregaciones. Usa Docker si necesitas el servidor.
- **DuckDB/analítico:** transformación desde los CSV de partida, salida Parquet,
  tres consultas agregadas y explicación de la granularidad.

El prototipo debe contener datos suficientes para demostrar las decisiones, pero
no necesitas construir una aplicación web.

El dataset de partida es pequeño y sirve para demostrar el modelo, no para
extraer conclusiones de rendimiento. Si eliges la ruta analítica y afirmas algo
sobre escalabilidad, crea una ampliación reproducible de los datos o limita
explícitamente la conclusión al prototipo.

### Fase 7 · Calidad y validación

Define y comprueba al menos estas reglas:

- identificadores únicos;
- reservas con inicio anterior al fin;
- estado dentro del dominio permitido;
- miembro, espacio y servicio existentes en sus ficheros maestros;
- cantidades positivas;
- ausencia de reservas solapadas cuando el perfil lo requiera;
- coherencia entre `base_amount`, servicios y `total_amount`. La fuente no
  contiene impuestos: si los añades, define la fórmula y documenta la decisión.

Incluye un caso límite o registro inválido creado por ti y demuestra que la regla
lo detecta o explica cómo lo trataría el sistema.

## 6. Entrega

Entrega un único archivo:

```text
apellido1_apellido2_ud1_modelado_completo.zip
```

Con esta estructura mínima:

```text
README.md
decision_record.md
modelo_conceptual.mmd   # o imagen/documento equivalente
modelo_logico.md
modelo_fisico/          # SQL, JSON, consultas o scripts según la ruta
validacion.md
```

El `README.md` debe indicar:

- nombres de los integrantes;
- perfil principal y tecnología elegida;
- versiones y requisitos;
- comandos exactos de ejecución;
- orden de ejecución;
- resultados esperados o archivos generados;
- limitaciones conocidas.

No incluy entornos virtuales, imágenes Docker, bases de datos completas ni
credenciales. Los datos de partida son ficticios y no deben sustituirse por PII
real.

## 7. Rúbrica (/10)

| Criterio | Puntos |
|---|---:|
| Objetivo, perfiles de carga y consultas prioritarias | 1,5 |
| Entidades, relaciones, claves y granularidad | 2 |
| Normalización/anidamiento y modelo físico | 1,5 |
| Calidad, casos límite y consistencia | 1,5 |
| Prototipo y consultas/operaciones reproducibles | 2 |
| Comparación tecnológica, validación y README | 1,5 |

### Mínimos para considerar la tarea superada

- El modelo declara la granularidad y las claves.
- La tecnología elegida está relacionada con un perfil de carga real.
- Existe al menos un prototipo o validación ejecutable/reproducible.
- Se comprueban reglas de calidad y un caso límite.
- Las alternativas descartadas y las limitaciones están documentadas.

La elección de MongoDB, PostgreSQL, DuckDB u otra tecnología **no da puntos por sí sola**. Se evalúa la calidad del razonamiento y de las evidencias.

## 8. Autoría y defensa

La actividad puede realizarse en pareja. Ambos integrantes entregan el mismo ZIP
e indican sus nombres en el `README.md`, pero deben poder explicar cualquier
decisión, consulta y resultado. El profesorado podrá solicitar una modificación
individual o una defensa breve.

## 9. Relación con otras actividades

- La [guía de modelado de datos](../../01-teoria/02-almacenamiento-y-nosql/UD1_Modelado_de_Datos.md)
  explica los conceptos y pasos utilizados aquí.
- La [P2 de pedidos](../modelado-documental-analitico/UD1_02_Tarea_Modelado_Documental_y_Analitico.md)
  es una práctica posterior de comparación documental y analítica con decisiones
  más guiadas.
- La demo de [reservas hoteleras](../modelado-documental-analitico/demo_p2_reservas_hotel/README.md)
  es material docente, no una solución para entregar.
