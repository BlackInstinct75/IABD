---
name: informe-cumplimiento
description: Redacta un informe de cumplimiento del DB-SUA para un elemento concreto de un proyecto (una rampa, una escalera, una barandilla...). Úsala cuando el usuario pida un informe, una ficha o una comprobación por escrito que tenga que guardarse.
---

# Informe de cumplimiento del DB-SUA

## Pasos

1. Identifica el elemento y sus datos (medidas, uso del edificio, si forma parte de un itinerario accesible). Si falta algún dato imprescindible, pregúntalo antes de seguir.
2. Busca en el documento todas las exigencias que se aplican a ese elemento con `buscar_normativa`. Haz varias búsquedas si hace falta.
3. Haz los cálculos con las herramientas disponibles, nunca de cabeza.
4. Escribe el informe en `/informes/` con un nombre descriptivo en minúsculas y con guiones, por ejemplo `/informes/rampa-acceso-principal.md`.
5. Responde al usuario con un resumen de dos o tres líneas y la ruta del informe.

## Estructura del informe

```markdown
# Informe de cumplimiento: <elemento>

## Datos del elemento
<tabla con los datos que ha dado el usuario>

## Comprobaciones
| Exigencia | Valor exigido | Valor del proyecto | Cumple | Referencia |
|---|---|---|---|---|

## Conclusión
<cumple / no cumple y qué habría que cambiar>

> Informe generado automáticamente. Debe revisarlo un técnico competente antes de usarlo.
```

La columna «Referencia» indica el apartado y la página del DB-SUA.