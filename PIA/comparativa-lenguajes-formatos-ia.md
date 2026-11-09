# Actividad de aula — Comparativa de lenguajes y formatos para IA

**Tiempo orientativo:** 35 minutos en clase, tras la introducción breve a R.

**Producto que entregarás:** una tabla comparativa, una decisión técnica breve y un ejemplo de marcado explicado. Puedes usar este documento como plantilla. Consulta en Moodle el plazo y el lugar de entrega.

## Propósito

Esta actividad trabaja la selección razonada de tecnologías y los criterios **RA1.b, RA1.c, RA1.d, RA1.e y RA1.f**. Al final tienes la relación entre cada criterio y lo que debes mostrar.

La idea no es aprender todos los lenguajes en profundidad, sino justificar cuándo tiene sentido usar cada uno en una aplicación de inteligencia artificial y qué papel cumplen los formatos de intercambio, configuración, documentación y marcado.

## Situación de partida

Un equipo debe diseñar una aplicación que analice un dataset sintético de empleados (edad, salario, experiencia, horas y satisfacción), prepare un modelo y permita consultar resultados desde una interfaz web o una API. También deberá conservar la configuración y documentar cómo repetir el análisis.

No tienes que programar la aplicación ni entrenar un modelo. Debes proponer tecnologías adecuadas y justificar sus funciones. Puedes consultar los apuntes y fuentes fiables; no es necesario dominar todos los lenguajes para comparar sus usos.

Debe decidir qué tecnologías usar para:

1. explorar y preparar datos;
2. entrenar o evaluar modelos;
3. integrar el resultado en una aplicación o API;
4. documentar, configurar e intercambiar información;
5. justificar por qué descarta alternativas.

## Lenguajes y formatos mínimos a comparar

| Tecnología | Rol típico en IA | Qué debe valorar el alumnado |
|---|---|---|
| Python | Lenguaje principal para IA, datos, ML, deep learning y APIs. | Bibliotecas, comunidad, productividad, integración y rendimiento suficiente. |
| R | Análisis estadístico, visualización, informes reproducibles y entornos donde ya se usa R. | Lo observado con vectores y `data.frame`; posibilidades estadísticas y comparación con Python. No necesitas usar paquetes nuevos. |
| Java | Integración empresarial, sistemas robustos, plataformas corporativas. | Ecosistema, rendimiento, mantenimiento y presencia en empresas. |
| JavaScript / NodeJS | Interfaces web, integración ligera, APIs y aplicaciones interactivas. | Relación con frontend/backend, despliegue y consumo de servicios IA. |
| JSON | Intercambio de datos, APIs, configuración y respuestas de modelos. | Estructura, legibilidad, interoperabilidad y limitaciones. |
| YAML | Configuración de pipelines, despliegues y herramientas MLOps. | Claridad, anidamiento, riesgos de ambigüedad y uso en herramientas. |
| Markdown | Documentación técnica, notebooks, informes y repositorios. | Comunicación, reproducibilidad y trazabilidad del trabajo. |
| XML / HTML | Marcado, documentos estructurados, web y datos legacy. | Etiquetas, estructura, interoperabilidad y casos donde aún aparece. |

Python, R, Java y JavaScript son lenguajes de programación. JSON es un formato de intercambio; YAML, uno habitual de configuración; Markdown se usa para documentación. XML y HTML son lenguajes de marcado con finalidades diferentes. No los presentes como alternativas intercambiables para entrenar un modelo.

## Entrega del alumnado

La entrega debe ser breve: una tabla comparativa, una conclusión técnica y la explicación de un fragmento de marcado. Incluye nombre, fecha y fuentes consultadas.

Esta actividad se rige por las [normas comunes de entrega y uso de IA](https://ies-rafael-alberti.github.io/programacion-inteligencia-artificial/normas-entregas-y-uso-de-ia/).

### 1. Tabla comparativa

Completar una tabla con estas columnas:

| Tecnología | Caso de uso en IA | Ventaja principal | Limitación principal | ¿La usarías en el proyecto? | Justificación |
|---|---|---|---|---|---|
| Python |  |  |  | Sí/No |  |
| R |  |  |  | Sí/No |  |
| Java |  |  |  | Sí/No |  |
| JavaScript/NodeJS |  |  |  | Sí/No |  |
| JSON |  |  |  | Sí/No |  |
| YAML |  |  |  | Sí/No |  |
| Markdown |  |  |  | Sí/No |  |
| XML/HTML |  |  |  | Sí/No |  |

Puedes elegir varias tecnologías, cada una para una función distinta. En la fila XML/HTML distingue al menos sus dos usos: XML para datos/documentos estructurados y HTML para presentar una página web.

### 2. Decisión final

Responder en 10–15 líneas:

- qué lenguaje usarías como base del proyecto y por qué;
- qué formato usarías para intercambiar datos por API;
- qué formato usarías para configuración;
- qué formato usarías para documentar el proyecto;
- qué alternativa descartas y por qué.

### 3. Reconocer el marcado

Observa estos fragmentos:

```xml
<empleado id="E01">
  <salario moneda="EUR">2500</salario>
</empleado>
```

```html
<h1>Resumen de empleados</h1>
<p>Salario medio: 2500 EUR</p>
```

En 3–5 líneas, identifica las etiquetas, un atributo y su valor en el XML. Explica qué información representan y por qué el fragmento HTML se orienta a presentar contenido, aunque ambos usen etiquetas.

### 4. Archivo y comprobación de entrega

- Entrega un único archivo `Apellidos_Nombre_comparativa_lenguajes_formatos` en PDF o Markdown, según lo que indique Moodle.
- Incluye al menos dos fuentes consultadas (título y enlace), además de los apuntes si los utilizas.
- Añade una breve declaración de uso de IA: herramienta, para qué la usaste y cómo comprobaste lo obtenido, o «No he utilizado IA». Sigue las normas comunes enlazadas arriba.
- Antes de enviar, comprueba que las ocho filas tienen contenido y que tus elecciones encajan con el caso de empleados. No basta con copiar una definición de cada tecnología.

## Criterios de evaluación

| Criterio | Peso | Evidencia esperada |
|---|---:|---|
| Comparación de lenguajes según aplicación | 25% | Diferencia Python, R, Java y JavaScript/NodeJS con casos de uso realistas. |
| Idoneidad para IA | 25% | Justifica bibliotecas, rendimiento, soporte, integración y ecosistema. |
| Formatos y lenguajes de marcado | 25% | Explica JSON, YAML, Markdown y XML/HTML con su función en IA; identifica etiquetas y atributos del ejemplo. |
| Decisión técnica razonada | 25% | Elige y descarta alternativas con argumentos, no por preferencias personales. |

## Relación RA/CE

| RA/CE | Evidencia |
|---|---|
| RA1.b | Valora características de lenguajes según el tipo de aplicación. |
| RA1.c | Determina el lenguaje más apropiado para la aplicación. |
| RA1.d | Valora características de lenguajes para desarrollo de IA. |
| RA1.e | Determina el lenguaje más apropiado para una aplicación de IA. |
| RA1.f | Caracteriza lenguajes de marcado y la información de sus etiquetas. |
