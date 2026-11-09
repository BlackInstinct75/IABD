# UD1 · Actividad: diseño de arquitectura Big Data con Medallion

## Objetivo

Diseñar una arquitectura Big Data razonada para un caso de uso realista, usando conceptos de batch, streaming, eventos, Lambda, Kappa, capas, lakehouse/Medallion y, si procede, data products.

No se evalúa que el diagrama sea bonito. Se evalúa que las decisiones tengan sentido.

## Agrupamiento

Actividad en **parejas**.

La arquitectura se discute mejor entre dos personas porque obliga a justificar decisiones y detectar contradicciones: qué entra en Bronze, qué se limpia en Silver, qué se publica en Gold y qué coste tiene mantener la solución. No se plantea como mini-proyecto porque su función es preparar la práctica técnica de UD2, no sustituirla.

## Relación curricular

- **RA1.c-d**: combinar fuentes y construir datasets complejos.
- **RA1.f-g**: seleccionar sistemas y valorar coste/calidad.
- **RA3.a-d**: extraer, almacenar, procesar y gestionar datos de forma eficiente y segura.
- **RA4.d-f**: procesar automáticamente estructuras de datos y visualizar resultados.

## Caso propuesto

Una zona turística quiere analizar actividad diaria para planificar recursos.

Fuentes disponibles:

- `ventas.csv`: ventas por comercio.
- `reservas_api.json`: reservas de alojamientos.
- `meteo.csv`: temperatura, lluvia y viento.
- `eventos_web.json`: búsquedas y clicks en una web turística.
- `catalogo_zonas.csv`: relación entre comercios, zonas y tipo de actividad.

El objetivo es crear un sistema que permita:

- consultar KPIs diarios,
- detectar datos de mala calidad,
- cruzar ventas, reservas y meteorología,
- preparar un dashboard técnico,
- justificar si hace falta batch o streaming.

## Entregable

Un documento Markdown con esta estructura:

```md
# Diseño de arquitectura Big Data

## 0. Miembros de la pareja

## 1. Caso de uso

## 2. Fuentes de datos

| Fuente | Tipo | Frecuencia | Problemas esperables |
| ------ | ---- | ---------- | -------------------- |

## 3. Arquitectura elegida

Indica si usarías batch, streaming, arquitectura orientada a eventos, Lambda, Kappa, Medallion o combinación. Si el caso tiene consumidores claros, indica también si algún Gold debería tratarse como data product.

## 4. Diseño Medallion

| Capa | Datos | Transformaciones | Calidad esperada | Formato |
| ---- | ----- | ---------------- | ---------------- | ------- |
| Bronze | | | | |
| Silver | | | | |
| Gold | | | | |

## 5. Tecnologías propuestas

| Parte | Herramienta | Motivo | Alternativa si falla |
| ----- | ----------- | ------ | -------------------- |

## 6. Calidad y trazabilidad

## 6.1 Responsabilidad del dato

¿Quién sería responsable de cada capa o dataset publicado? ¿Quién consumiría Gold?

## 7. Coste y viabilidad en aula

## 8. Diagrama simple

Puede ser texto, Mermaid o imagen.

## 9. Conclusión
```

## Restricciones

- No propongas una arquitectura cloud si no puedes justificar coste y acceso.
- No uses streaming si el caso puede resolverse bien en batch.
- No conviertas Gold en “todo el dataset”; Gold debe responder preguntas concretas.
- No pierdas el dato original: Bronze debe permitir reprocesar.

## Rúbrica

| Criterio                                                          | Peso |
| ----------------------------------------------------------------- | ---- |
| Identifica bien fuentes, tipos y frecuencia                       | 15%  |
| Justifica batch/streaming/eventos/Lambda/Kappa/Medallion          | 20%  |
| Diseña correctamente Bronze/Silver/Gold                           | 25%  |
| Incluye calidad, trazabilidad, errores y responsabilidad del dato | 15%  |
| Elige herramientas viables para aula                              | 15%  |
| Explica coste, limitaciones y alternativas                        | 10%  |

## Nivel excelente

Una entrega excelente no sólo dice “uso Medallion”. Explica por qué, qué entra en cada capa, qué calidad promete cada una, cómo se reprocesa, qué se publica en Gold y qué coste tiene mantenerlo.
