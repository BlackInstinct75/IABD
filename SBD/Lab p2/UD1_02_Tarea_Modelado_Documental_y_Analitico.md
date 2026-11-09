# UD1 · Tarea: modelado documental y consulta analítica

> **RA/CE:** RA4.a (escenarios y tipologías de datos no estructurados) y
> contraste con RA1.b (extracción de información).

## Objetivo

Comparar un modelo documental basado en JSON con una representación analítica
consultable con DuckDB. No se evalúa instalar MongoDB ni memorizar comandos:
se evalúa reconocer la estructura de los datos, justificar el modelo elegido y
obtener respuestas reproducibles.

Antes del laboratorio, lee la [guía de modelado de datos](../../01-teoria/02-almacenamiento-y-nosql/UD1_Modelado_de_Datos.md):
explica qué es modelar, el modelo documental frente al analítico y cómo elegir
según cómo vas a leer.

## Material de partida

Descarga en Moodle `lab_p2_modelado_documental_analitico.zip`. Incluye el
generador de datos, consultas iniciales, `README.md`, `requirements.txt` y un
`Makefile` opcional. Ejecuta:

```bash
pip install -r requirements.txt
python genera_datos_p2.py
duckdb -c ".read p2_duckdb.sql"
```

Si no tienes la CLI de DuckDB, puedes ejecutar el SQL desde Python o un notebook.
MongoDB es una ampliación opcional: no es requisito para esta entrega.

## Trabajo a realizar

Antes de ejecutar, decide el modelado paso a paso (apóyate en la guía):

1. **Identifica la entidad.** Un pedido es la unidad lógica; sus líneas son
   subelementos.
2. **Elige la clave.** `order_id` identifica cada pedido; al aplanar se repite en
   cada fila para relacionar las líneas del mismo pedido.
3. **Decide campos a conservar y a calcular.** `importe` y `margen` se calculan;
   decide si conviene guardarlos para que las consultas sean rápidas.
4. **Elige el modelo de salida.** Analítico plano y Parquet para consultas
   agregadas; documental JSON si se va a recuperar el pedido completo.
5. **Justifica y documenta** cada decisión antes de escribir SQL.

Después:

1. Genera y revisa los datos. Comprueba que la entidad, las claves y los campos
   calculados coinciden con lo que decidiste.
2. Incluye en `respuestas.md` un ejemplo abreviado de un documento JSON y explica
   dos ventajas y una limitación del modelado documental para este caso.
3. Completa o adapta `p2_duckdb.sql` para responder, como mínimo, a estas
   preguntas: margen por producto, evolución temporal de pedidos y una consulta
   adicional justificada por ti.
4. Explica qué datos conservarías en un formato analítico como Parquet y por qué
   DuckDB permite explorarlos sin desplegar un servidor.
5. Documenta cómo reproducir tu resultado en un `README.md` breve.

## Entrega en Moodle

Entregar un único archivo `apellido1_apellido2_ud1_modelado.zip` que contenga:

```text
respuestas.md
p2_duckdb.sql
README.md
```

No incluir entornos virtuales, dependencias instaladas, bases de datos generadas
ni archivos grandes que puedan volver a generarse con el material de partida.

## Rúbrica (/10)

| Criterio | Puntos |
|---|---:|
| Identifica correctamente estructura, tipologías y campos del documento JSON | 2 |
| Justifica el uso y límites del modelo documental | 2 |
| Consultas DuckDB correctas, legibles y reproducibles | 3 |
| Compara razonadamente JSON/documental y Parquet/analítico | 2 |
| README y entrega ordenados | 1 |

## Autoría y trabajo en pareja

La actividad se realiza en pareja. Ambos integrantes entregan el mismo ZIP e
indican los dos nombres en el `README.md`, pero deben poder explicar cualquier
consulta, decisión de modelado y comparación. El profesorado podrá solicitar una
modificación o comprobación individual.
