# Modelo lógico — NexoWork (Perfil C · analítico)

## 1. Modelo conceptual: explicación textual del diagrama

El diagrama está en `modelo_conceptual.mmd` (Mermaid). Se puede revisar sin renderizarlo con esta lectura:

| Relación | Cardinalidad | Lectura |
|---|---|---|
| MIEMBRO → RESERVA | 1:N | Un miembro hace cero o más reservas; cada reserva es de un único miembro. |
| SEDE → ESPACIO | 1:N | Una sede (Madrid, Sevilla, Lisboa) contiene uno o más espacios; cada espacio pertenece a una sede. |
| ESPACIO → RESERVA | 1:N | Un espacio recibe cero o más reservas; cada reserva es de un único espacio. |
| RESERVA → RESERVA_SERVICIO | 1:N | Una reserva incluye cero o más líneas de servicio. |
| SERVICIO → RESERVA_SERVICIO | 1:N | Un servicio aparece en cero o más líneas. |
| **RESERVA ↔ SERVICIO** | **N:M** | Se resuelve con la entidad intermedia RESERVA_SERVICIO (clave compuesta `reservation_id + service_code`, atributo propio `quantity`). |

- **Entidades:** miembro, sede, espacio, servicio. **Evento:** reserva (hecho que ocurre en el tiempo). **Evento dependiente:** línea de servicio consumida (RESERVA_SERVICIO).
- La **sede** es una entidad conceptual, pero en el modelo físico se aplana dentro de `dim_espacio` (ver §3 y decisión D6).

## 2. Resumen del esquema físico lógico (estrella)

```
                dim_miembro                 dim_servicio
                     │ 1                         │ 1
                     │ N                         │ N
dim_espacio 1──N  fact_reserva 1────────N fact_reserva_servicio
```
Dos tablas de hechos con grano distinto (reserva; reserva × servicio) y tres dimensiones. No hay dimensión fecha: el mes se materializa como columna (`start_month`, `created_month`) porque todas las consultas prioritarias agregan por mes y no hay calendario de festivos ni semanas fiscales.

## 3. Fase 3 · Granularidad, claves y reglas

| Elemento | ¿Qué representa exactamente? (grano) | Clave | Relaciones | Reglas |
|---|---|---|---|---|
| `dim_miembro` | Un miembro (identificador ficticio) | `member_id` | — | único; segmento ∈ {freelancer, startup, enterprise, student} |
| `dim_espacio` | Un espacio reservable, con su sede aplanada | `space_id` | — (la sede va dentro: `location_id`, `location_city`) | único; `capacity` > 0; cada `space_id` pertenece a una sola sede |
| `dim_servicio` | Un servicio del catálogo y su precio actual | `service_code` | — | único; `unit_price` ≥ 0 |
| `fact_reserva` | **Una reserva solicitada por un miembro** (una fila = un `reservation_id`) | `reservation_id` | FK `member_id` → `dim_miembro`; FK `space_id` → `dim_espacio` | inicio < fin; 1 ≤ `seats` ≤ `capacity`; estado y canal en dominio; `total_amount = base_amount + Σ líneas`; sin solapamiento en el mismo espacio (salvo canceladas) |
| `fact_reserva_servicio` | **Un servicio concreto dentro de una reserva** (una fila = reserva × servicio) | compuesta (`reservation_id`, `service_code`) | FK `reservation_id` → `fact_reserva`; FK `service_code` → `dim_servicio` | `quantity` entero > 0; un código no se repite dentro de la misma reserva; `line_amount = quantity × unit_price` |
| `stg_*` (solo en el pipeline) | Copia literal de los CSV, todo texto | — | — | Sin reglas: existen para poder validar antes de convertir tipos |

**Justificación de claves**
- *Identificadores naturales* (`reservation_id`, `member_id`, `space_id`, `service_code`): ya vienen asignados por la fuente, son estables y legibles; no hace falta clave sustituta con 18 filas ni con millones (los hash de unión de DuckDB sobre VARCHAR son suficientes a esta escala).
- *Clave compuesta en `fact_reserva_servicio`*: el par identifica la línea y, además, **impide por diseño** repetir el mismo servicio en una reserva (se acumula en `quantity`). Esto se valida con V15 porque Parquet no impone claves.
- *Parquet no tiene PK/FK/CHECK*: todas las claves y reglas son **contractuales** y se hacen cumplir en el pipeline (`02_validacion.sql`), no en el motor. Es un coste real de esta ruta.

**Representación de servicios y cantidades.** La fuente guarda `codigo=cantidad;codigo=cantidad` en una cadena. Se **desanida** a una fila por (reserva, servicio) con `quantity`. Así Q8 es un `SUM` simple, un servicio nuevo es una fila en el catálogo (sin tocar el esquema) y se respeta la primera forma normal.

**Campos originales frente a derivados**

| Campo | Tipo | Origen / fórmula | Motivo de materializarlo |
|---|---|---|---|
| `reservation_id`, `member_id`, `space_id`, `start_at`, `end_at`, `created_at`, `seats`, `status`, `channel`, `base_amount`, `total_amount` | original | Fuente | — |
| `quantity` | original | Parseo de `service_items` | — |
| `unit_price` (en `fact_reserva_servicio`) | original-congelado | Precio del catálogo al cargar | Para que un cambio futuro de tarifa no reescriba el histórico (ver riesgo en D2) |
| `duration_hours` | derivado | `(end_at − start_at) / 60` en horas | Se lee en Q5; evita recalcular por fila |
| `seat_hours` | derivado | `duration_hours × seats` | Métrica horas-plaza de Q5 |
| `line_amount` | derivado | `quantity × unit_price` | Q6/Q8 |
| `services_amount` | derivado | Σ `line_amount` de la reserva | Permite separar ingresos de espacio y de servicios en Q6 y verificar V10 |
| `start_month`, `created_month` | derivado | `date_trunc('month', …)` | Eje temporal de Q5/Q6/Q7 |
| `location_city`, `space_type`, `member_segment` en la fuente de reservas | **redundante** | Copia de maestros | **No se llevan a `fact_reserva`**; se validan contra el maestro (V12) y se leen de la dimensión |

## 4. Fase 4 · Normalización, duplicación y anidamiento

| Dato o relación | Decisión | Motivo | Riesgo | Cómo se mantiene la consistencia |
|---|---|---|---|---|
| **D1** Servicios de una reserva | **Separar** (tabla puente `fact_reserva_servicio`) | Q8 agrega por servicio; una cadena `a=1;b=2` obligaría a parsear en cada consulta | Un join extra para ver una reserva completa; **medido**: Q8 es entre 15 y 45 veces más lenta que Q6 y Q7 a 2 M de reservas (§ validacion.md) | `V07/V08/V15` antes de cargar; `services_amount` se calcula desde las líneas |
| **D2** Precio unitario | **Duplicar** (`unit_price` copiado en la línea) | Fija el precio vigente al reservar; Q6 no cambia si cambia el catálogo | La fuente no trae histórico de precios: se asume que el precio de catálogo coincide con el cobrado | `V10` lo contrasta: los 17 totales reales cuadran con el catálogo actual |
| **D3** Ciudad y tipo de espacio en la reserva | **Referenciar** (quitar de la tabla de hechos; vive en `dim_espacio`) | Es un atributo del espacio, no de la reserva; evita contradicciones | Join con una dimensión de 9 filas en cada consulta (coste despreciable) | `V12` compara la copia de la fuente con el maestro |
| **D4** Segmento del miembro | **Referenciar** (`dim_miembro`) | Misma razón | Si un miembro cambia de segmento, el histórico se re-atribuye al segmento actual (no hay SCD tipo 2) | `V12`; si el negocio lo exige se añade `segment_at_booking` al hecho |
| **D5** Importes `base_amount` / `total_amount` | **Conservar originales** y añadir `services_amount` derivado | El total original es el dato contable; el derivado sirve para auditarlo | Dos fuentes de verdad para el total | `V10`: `total = base + Σ líneas` (tolerancia 0,005) y conciliación en `run_all.py` |
| **D6** Sede | **Aplanar** en `dim_espacio` (no hay `dim_sede`) | Solo tiene 2 atributos (`location_id`, `location_city`) y ninguna consulta pide más | Si una sede gana atributos (dirección, zona horaria), habría que extraerla | `V12`; extraer `dim_sede` es un cambio aditivo (§ decision_record, evolución) |
| **D7** Mes | **Materializar** `start_month` / `created_month` | Todas las consultas agrupan por mes; ordenar por `start_at` ayuda a podar row-groups | Dos columnas que pueden divergir de la fecha | Se derivan en la carga con una única expresión |
| **D8** Impuestos | **No añadir** | La fuente no los contiene; inventar un tipo de IVA por país (ES 21 %, PT 23 %) sería una suposición sin base | Ingresos sin impuestos; no comparable con contabilidad | Documentado en validacion.md; añadirlos sería una columna derivada con fórmula explícita |
| **D9** Reservas anidadas dentro de miembro/espacio | **No anidar** | Parquet es columnar y plano; anidar rompe la agregación por pocas columnas | — | — |
