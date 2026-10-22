# InsurRisk Analytics: Motor de Tarificación Dinámica y Puntuación de Riesgo

## 1. Introducción y Objetivo del Proyecto

El sector asegurador tradicional suele utilizar modelos de tarificación estáticos y genéricos que no siempre reflejan de forma precisa el riesgo real asociado a un conductor y a su vehículo. **InsurRisk Analytics** es un prototipo de sistema basado en Big Data y analítica de datos diseñado para evaluar de forma multidimensional el perfil de riesgo antes de emitir una póliza de seguro.

El objetivo principal es procesar variables del conductor (como la edad y la experiencia al volante) y del vehículo (como el modelo, año de matriculación y visibilidad/color) para calcular un **Score de Riesgo Dinámico** que determine de manera justa y automatizada la prima del seguro.

---

## 2. Variables Analizadas y Fuentes de Datos

El sistema procesa dos bloques principales de información para alimentar el motor de reglas:

* **Perfil del Conductor:**
* *Edad:* Factor estadístico de experiencia y madurez al volante (excluyendo el género por cumplimiento normativo y ético).
* *Antigüedad del permiso de conducir:* Indicador clave de solidez y destreza en la conducción.


* **Características del Vehículo:**
* *Modelo y gama:* Tasas de siniestralidad histórica asociadas a modelos específicos según datos oficiales.
* *Antigüedad del vehículo:* Presencia o ausencia de sistemas avanzados de asistencia a la conducción (ADAS).
* *Color / Visibilidad:* Factor analítico complementario relacionado con la visibilidad nocturna y tasas de incidente asociadas.



---

## 3. Modelo de Puntuación de Riesgo (Sistema de Pesos)

Para calcular el riesgo de manera transparente y escalable, el sistema implementa una **matriz de pesos ponderados**. Cada condición suma o resta puntos (*weights*) al balance global de riesgo ($S$):

| Categoría | Factor / Condición | Puntuación ($w$) | Justificación Técnica |
| --- | --- | --- | --- |
| **Conductor** | Edad: 18 - 24 años | **+3** | Mayor índice de siniestralidad juvenil / Inexperiencia |
|  | Edad: 25 - 65 años | **-1** | Franja de estabilidad en la conducción |
|  | Experiencia carné: < 3 años | **+2** | Conductor novel |
|  | Experiencia carné: > 10 años | **-2** | Conductor experimentado |
| **Vehículo** | Antigüedad: > 15 años | **+2** | Menor presencia de sistemas de seguridad activa (ADAS) |
|  | Antigüedad: 0 - 3 años | **+1** | Vehículo nuevo (menor riesgo mecánico, mayor coste de reparación) |
|  | Modelo de alta siniestralidad | **+2** | Basado en estadísticas públicas de accidentalidad |
|  | Color / Visibilidad (ej. Tonos oscuros) | **+1** | Menor visibilidad en condiciones nocturnas |

---

## 4. Lógica de Tarificación (Cálculo de la Cuota)

Una vez evaluados todos los parámetros, el sistema obtiene un **Puntaje Total de Riesgo ($S$)**. La cuota final se calcula mediante una función lineal parametrizada:

$$\text{Cuota Final} = \text{Cuota Base} + (S \times \text{Factor Multiplicador})$$

### Ejemplo Práctico de Simulación:

* **Perfil de Entrada:** Conductor de 20 años, con 2 años de carné, conduciendo un Dacia Sandero azul de 2023.
* **Desglose de Puntos:**
* Base inicial: `0`
* Edad (20 años): `+3`
* Experiencia (<3 años): `+2`
* Modelo (Dacia Sandero): `+2`
* Año vehículo (2023): `+1`
* Color (Azul): `+1`
* **Puntuación Total ($S$): `9 puntos**`


* **Cálculo Económico:** Si la cuota base es de **150 $** y cada punto equivale a **20 $**:

$$\text{Cuota} = 150 + (9 \times 20) = 330 \$ \text{ / año}$$



---

## 5. Arquitectura Técnica Propuesta

El proyecto se estructura bajo una arquitectura moderna orientada a microservicios y procesamiento de datos:

1. **Capa de Ingesta:** Endpoints y formularios web optimizados para la recodificación rápida de los datos del cliente y del vehículo.
2. **Capa de Procesamiento (Motor de Reglas):** Microservicio backend (ej. Node.js / Python) encargado de consultar la tabla de pesos en base de datos y ejecutar el algoritmo de puntuación en milisegundos.
3. **Capa de Almacenamiento:** Base de datos relacional (PostgreSQL) para la gestión transaccional de pólizas, clientes y la matriz de pesos dinámicos (permitiendo reajustes actuariales sin alterar el código fuente).
4. **Capa de Presentación:** Interfaz de usuario intuitiva que muestra el desglose del presupuesto y los factores determinantes del precio de forma transparente.

---

## 6. Cumplimiento Normativo y Privacidad

* **Exclusión de Sesgos Demográficos:** El sistema elimina por completo el uso del género como variable de tarificación, cumpliendo estrictamente con la normativa europea aplicable al sector asegurador.
* **Privacidad de Datos (RGPD):** Tratamiento seguro de los datos personales de los usuarios bajo estricta confidencialidad, utilizando únicamente fuentes estadísticas agregadas para el cálculo de probabilidades.

---

## 7. Conclusiones y Futuros Desarrollos

InsurRisk Analytics demuestra cómo la analítica de datos aplicada puede transformar un proceso complejo en una experiencia ágil, automatizada y justa tanto para la compañía como para el asegurado.

Como líneas de evolución futura se contempla:

* Integración de datos telemáticos en tiempo real (*Pay-How-You-Drive* mediante dispositivos móviles u OBD).
* Implementación de modelos de Machine Learning predictivo para reajustar automáticamente los pesos de la matriz basándose en el histórico real de siniestros de la compañía.