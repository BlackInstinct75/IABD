# Decision record — NexoWork · UD1

**Decisión:** el prototipo se construye para el **Perfil C (analítico)** con **DuckDB 2.0.0 + Parquet (zstd)**, modelado como esquema en estrella.
**Estado:** aceptada · **Fecha:** 9-nov-2026

---

## Fase 1 · Requisitos y objetivo

### 1.1 Problema (resumen)
NexoWork gestiona espacios de trabajo en Madrid, Sevilla y Lisboa (9 espacios: salas de reuniones, puestos flexibles y salas de formación). Dispone de una exportación inicial de 18 reservas con estados `pending/confirmed/completed/cancelled`, 4 canales de reserva y servicios adicionales codificados en una cadena. No existe un modelo de datos justificado. La dirección necesita registrar y modificar reservas sin perder consistencia, mostrar una reserva completa, analizar ocupación/ingresos/cancelaciones por ciudad, espacio y mes, y admitir nuevos servicios y sedes sin rediseñar. Los datos son ficticios: solo se conservan identificadores artificiales.

### 1.2 Los tres perfiles de carga

| Perfil | Prioridad | Patrón de acceso | Encaje natural |
|---|---|---|---|
| **A · Operacional** | Registrar reservas, evitar solapamientos, cambiar estados | Muchas escrituras pequeñas, concurrentes, consistencia inmediata, lecturas por clave | SQL relacional (PostgreSQL) |
| **B · Documental / servicio** | Devolver una reserva completa a una API en una sola lectura | Lectura por id de un agregado (reserva + espacio + servicios), esquema flexible | Documental (MongoDB) |
| **C · Analítico** | Ocupación, ingresos, cancelaciones sobre el histórico | Pocas consultas, leen muchas filas y pocas columnas, escritura por lotes | Columnar (DuckDB + Parquet) |

### 1.3 Perfil elegido: C — y por qué no es el único que NexoWork necesita
Se elige **C** porque 4 de las 8 consultas candidatas (Q5–Q8) son agregaciones sobre histórico y, además, es el perfil cuyo prototipo puede **demostrarse de forma totalmente reproducible** con una dependencia (`pip install duckdb`), sin servidor ni Docker, y sobre el que se puede hacer la ampliación de datos que exige el enunciado.

Dicho con honestidad: **el negocio real necesita también el perfil A** (registrar y cancelar sin solapes es lo primero que pide la dirección). La arquitectura razonable es *OLTP relacional en producción → carga por lotes → capa analítica en Parquet*. Este trabajo diseña y valida **la capa analítica**; **no** pretende sustituir al sistema transaccional (ver §5.3).

### 1.4 Análisis de las 8 consultas candidatas

| # | Consulta | Perfil al que empuja | ¿Prioritaria? |
|---|---|---|---|
| 1 | Reservas futuras confirmadas de un miembro | A/B (lectura puntual por miembro) | No |
| 2 | ¿Solapamiento en `space_id` y horario? | A (prevención transaccional); en C solo se **audita** (V09) | No (se cubre como regla de calidad) |
| 3 | Reservas con un servicio y su cantidad | A/C (con la tabla puente es un filtro) | No (queda resuelta por `fact_reserva_servicio`) |
| 4 | Reserva completa para una app | B | No |
| **5** | **Horas reservadas por ciudad y mes** | **C** | **Sí** |
| **6** | **Ingresos por ciudad y tipo de espacio** | **C** | **Sí** |
| **7** | **Tasa de cancelación por canal y mes** | **C** | **Sí** |
| **8** | **Servicios adicionales más solicitados** | **C** | **Sí** |

### 1.5 Consultas prioritarias (implementadas en `modelo_fisico/sql/05_consultas.sql`)

> Las frecuencias y tiempos son **estimaciones de diseño**, no datos medidos de NexoWork (el enunciado no los facilita).

| | Q5 Horas por ciudad/mes | Q6 Ingresos ciudad × tipo | Q7 Cancelación canal × mes | Q8 Servicios top |
|---|---|---|---|---|
| **Usuario/proceso** | Dirección de operaciones | Finanzas / dirección | Marketing y canales (partners) | Producto / compras |
| **Frecuencia** | Semanal / cierre de mes | Mensual | Semanal | Mensual |
| **Tiempo esperado** | Segundos (informe interactivo) | Segundos | Segundos | Segundos |
| **Lee** | `start_at`, `end_at`, `seats`, `status`, `space_id` + ciudad | `status`, importes, `space_id` + ciudad/tipo | `created_at`, `status`, `channel` | líneas de servicio + `status` |
| **Modifica** | Nada | Nada | Nada | Nada |
| **Por qué condiciona el modelo** | Lectura de 3-4 columnas sobre todo el histórico → almacenamiento columnar; exige definir la métrica (**horas-reserva** vs **horas-plaza**) | Necesita `base` y `servicios` por separado → importe de servicios derivado | Denominador = reservas **creadas** en el mes → el eje temporal es `created_month`, no el mes de uso | Exige servicios **desanidados** (una fila por reserva × servicio) |

**Definiciones adoptadas**
- *Horas reservadas (Q5):* se reportan **ambas** métricas; excluye `cancelled`; el mes es el de **inicio** de la reserva. Una reserva que cruza de mes se imputa íntegra al mes de inicio (en la muestra no hay ninguna).
- *Ingresos (Q6):* `total_amount` de reservas `confirmed` + `completed`; excluye `pending` (sin confirmar) y `cancelled`; sin impuestos.
- *Tasa de cancelación (Q7):* `canceladas / todas las reservas creadas` en el mes de **creación**. La fuente no trae `cancelled_at`, por lo que no se puede imputar la cancelación al mes en que ocurrió.
- *Servicio solicitado (Q8):* unidades en reservas no canceladas (se muestra también el total con canceladas).

### 1.6 Perfil de carga esperado

| Dimensión | Actual | Supuesto de crecimiento (**hipótesis de trabajo**) |
|---|---|---|
| Volumen | 18 reservas, 17 líneas de servicio | ~100–300 reservas/día en la red → 40–110 k reservas/año. La ampliación de prueba (2 M) equivale a >15 años a ese ritmo: es un colchón, no una previsión |
| Lecturas / escrituras | Lecturas: unas pocas consultas al día/semana. Escrituras: **una carga por lotes** (diaria o por cierre) | Igual; el sistema transaccional absorbe las escrituras de verdad |
| Concurrencia | 1 proceso de carga + pocos analistas (<10) | Lectura concurrente de ficheros Parquet de solo lectura |
| Evolución del esquema | Nuevos servicios y sedes | Aditiva: filas nuevas en dimensiones; columnas nuevas en hechos |
| Consistencia | **Eventual** (instantánea desde el origen); la carga es todo-o-nada e idempotente (`CREATE OR REPLACE`) | — |

---

## Fase 5 · Comparación y elección tecnológica

### 5.1 Comparación de alternativas frente al Perfil C

| Criterio | PostgreSQL | MongoDB | **DuckDB + Parquet** |
|---|---|---|---|
| Almacenamiento | Filas (heap) | Documentos BSON | **Columnas comprimidas** |
| Agregar pocas columnas sobre muchas filas (Q5–Q8) | Correcto con índices/particiones; lee filas completas | Pipeline de agregación válido, pero menos eficiente en analítica pesada | **Muy eficiente por diseño** |
| Integridad (PK/FK/CHECK, transacciones) | **Excelente** | Débil entre colecciones; validación de esquema opcional | **Ninguna en Parquet**: se hace en el pipeline |
| Escrituras concurrentes | **Excelente** | Buena | **No es su objetivo** (un escritor) |
| Reserva completa en una lectura (Q4) | Joins | **Excelente** (agregado) | No optimizado para lectura puntual |
| Coste de operación | Servidor, backups, tuning, usuarios | Servidor/cluster | **Ninguno**: un paquete y ficheros |
| Evolución del esquema | `ALTER TABLE` / migraciones | Flexible, pero sin contrato | Columnas aditivas; `union_by_name` |
| Reproducible en el aula | Docker o instalación | Docker | **`pip install duckdb`** |

### 5.2 Decisión

| Aspecto | Elección |
|---|---|
| Gestor | **DuckDB 2.0.0** (embebido, en proceso) |
| Formato | **Parquet** con compresión **zstd** (escrito por DuckDB 2.0.0) |
| Modelo físico | Estrella: `fact_reserva` (16 columnas), `fact_reserva_servicio`, `dim_miembro`, `dim_espacio`, `dim_servicio`. Hechos ordenados por `start_at` |
| Lenguaje y entorno | SQL de DuckDB + Python 3.12.3 (solo como orquestador) |

**Alternativas descartadas**
1. **PostgreSQL como sistema principal de este perfil.** Descartado *para la capa analítica*, no en general: sería la elección correcta del Perfil A y sigue siendo la fuente lógica del dato. Motivo: añade administración de un servidor para un patrón de uso (pocas lecturas por lotes) que no lo necesita, y almacena filas completas cuando las consultas leen 3–4 columnas.
2. **MongoDB.** Descartado porque su fortaleza (agregado anidado, esquema flexible) resuelve Q4, que aquí no es prioritaria. Las consultas elegidas cruzan entidades (reserva × espacio × servicio) y MongoDB obligaría a duplicar ciudad/tipo o a usar `$lookup`, con el riesgo de inconsistencias que el enunciado pide evitar.

### 5.3 Por qué DuckDB + Parquet **no** se usa como sistema transaccional
- **Parquet es inmutable:** modificar un estado (`pending → confirmed`) implica reescribir ficheros, no actualizar una fila.
- **Sin restricciones en el motor:** no hay PK, FK ni `CHECK` sobre ficheros Parquet; la unicidad y las referencias son una convención que hay que vigilar fuera.
- **Un solo escritor:** DuckDB admite lecturas concurrentes, pero no es un servidor multiusuario con control de concurrencia para muchas escrituras simultáneas.
- **Los solapamientos no se pueden *impedir*, solo *detectar* a posteriori** (V09). Impedirlos exige una restricción transaccional; en PostgreSQL se haría con una restricción de exclusión sobre un rango de tiempo por `space_id`.

### 5.4 Coste de operación y recursos
- **Sin servidor, sin licencias, sin credenciales.** Dependencia única: `duckdb==2.0.0`.
- **Recursos medidos** (contenedor de pruebas: 1 CPU, ~4 GB RAM): la ampliación de **2 M reservas + 2,7 M líneas** ocupa **≈ 39 MB** en Parquet (32,4 + 6,9 MB) y se genera y consulta sin problema en esa máquina.
- Operación: reejecutar `run_all.py` tras cada exportación; el pipeline se detiene si hay datos inválidos.

### 5.5 Evolución del esquema
| Cambio | Cómo se absorbe |
|---|---|
| Nuevo servicio | Una fila en `dim_servicio` (y en el catálogo fuente). **Sin cambios en el esquema** gracias a la tabla puente |
| Nueva sede / espacios | Filas nuevas en `dim_espacio`. Sin DDL |
| Nuevo atributo de reserva (p. ej. `cancelled_at`) | Columna nueva en `fact_reserva`; los ficheros antiguos se leen con `read_parquet(…, union_by_name = true)` (valor `NULL` en el histórico) |
| La sede gana atributos | Extraer `dim_sede` y sustituir las 2 columnas aplanadas por `location_id`: cambio aditivo |
| Impuestos | Columna derivada `tax_amount` con fórmula documentada por país |

### 5.6 ¿Y si el volumen o la concurrencia se multiplicaran?
- **Volumen ×10–×100:** particionar los hechos por mes (`start_month=YYYY-MM/`) para podar lecturas, y cargar de forma incremental en vez de reconstruir todo. Mi evidencia llega a **2 M filas en una máquina de 1 hilo**; más allá no se ha medido y no afirmo nada.
- **Concurrencia de lectura:** los ficheros Parquet de solo lectura admiten muchos lectores independientes.
- **Concurrencia de escritura / uso operativo en tiempo real:** es el límite. Habría que mantener un OLTP (PostgreSQL) delante y tratar este modelo como réplica analítica. Si el volumen analítico superara lo que cabe en una máquina, habría que migrar a un almacén analítico distribuido o gestionado; **no** lo he probado.
