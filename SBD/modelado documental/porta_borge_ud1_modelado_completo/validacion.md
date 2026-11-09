# Validación y calidad — Fase 7

Todo lo que sigue se obtiene ejecutando los scripts (ver `README.md`). Los números son salidas reales del prototipo.

## 1. Reglas de calidad (`modelo_fisico/sql/02_validacion.sql`)

Cada regla devuelve una fila `(regla, reservation_id)` por violación. Resultado vacío = datos válidos. El pipeline (`run_all.py`) **se detiene** si hay alguna.

| Regla | Qué comprueba | Requisito del enunciado |
|---|---|---|
| V01 | `reservation_id` único y no nulo | Identificadores únicos |
| V02 | Fechas e importes interpretables (`try_cast` no nulo) | Soporte de las demás |
| V03 | `start_at < end_at` | Inicio anterior al fin |
| V04 | `status` ∈ {pending, confirmed, completed, cancelled} | Estado en dominio |
| V05 | `member_id` existe en `miembros_fuente` | Miembro existente |
| V06 | `space_id` existe en `espacios_fuente` | Espacio existente |
| V07 | Cada ítem de `service_items` tiene formato `codigo=cantidad` y el código existe en el catálogo | Servicio existente |
| V08 | `quantity` entero > 0 | Cantidades positivas |
| V09 | Sin solapamiento de horario en el mismo `space_id`, ignorando canceladas | Ausencia de solapes |
| V10 | `total_amount = base_amount + Σ(cantidad × precio)` (tolerancia 0,005) | Coherencia de importes |
| V11 | 1 ≤ `seats` ≤ `capacity` del espacio | Regla adicional |
| V12 | Ciudad, sede, tipo de espacio y segmento de la reserva coinciden con los maestros | Regla adicional (redundancia) |
| V13 | `created_at ≤ start_at` | Regla adicional |
| V14 | `channel` ∈ {web, app, partner, phone} | Regla adicional |
| V15 | Un mismo servicio no se repite dentro de una reserva | Protege la clave compuesta de la tabla puente |

**Decisión sobre impuestos:** la fuente no los contiene y **no se añaden** (D8). La fórmula validada es solo `total = base + servicios`.

## 2. Resultado sobre los datos de partida

```
python modelo_fisico/scripts/run_all.py
[1/4] Validación: 0 violaciones
[2/4] Parquet escrito en .../modelo_fisico/out/parquet
[3/4] Conciliación OK: 18 reservas, 17 líneas de servicio, total 2245.00 EUR
```
Conciliación: nº de reservas y de líneas del modelo igual al de la fuente; `Σ total_amount` de la fuente = del modelo = `Σ(base + servicios)`.
Comprobación cruzada manual: ingresos Q6 = 2051,50 EUR = 2245,00 − 193,50, donde 193,50 son los importes de las 2 reservas `pending` (R005, R013) y las 2 `cancelled` (R009, R016).

## 3. Casos límite creados por mí (`data/casos_limite/reservas_invalidas.csv`)

16 registros inválidos, cada uno diseñado para violar **una** regla. Se añaden a la fuente y se exige que el conjunto de violaciones detectadas sea **exactamente** el esperado (ni una de menos, ni una de más).

| Registro | Qué tiene de erróneo | Regla que lo detecta | Tratamiento propuesto en el sistema |
|---|---|---|---|
| `R001` (duplicado) | Mismo id que una reserva existente | V01 | Rechazar la carga; investigar origen duplicado |
| `INV02` | Fin (10:00) anterior a inicio (12:00) | V03 | Cuarentena + devolver al origen |
| `INV03` | Estado `archived` fuera de dominio | V04 | Rechazar; ampliar dominio solo si negocio lo aprueba |
| `INV04` | Miembro `M999` inexistente | V05 | Cuarentena hasta que exista en maestro |
| `INV05` | Espacio `NX-MAD-XX-99` inexistente | V06 | Cuarentena |
| `INV06` | Servicio `jacuzzi` no está en el catálogo | V07 | Cuarentena; alta previa en catálogo |
| `INV14` | Ítem mal formado `coffee2` (sin `=`) | V07 | Rechazar |
| `INV07` | Cantidad `0` | V08 | Rechazar (una línea con 0 no tiene sentido) |
| `INV08` | Solapa con R001 (misma sala, 11:00–14:00 vs 09:00–12:00) | V09 | En OLTP: impedir el alta; en este modelo: alertar |
| `INV09` | Total 40,00 ≠ 25,00 + 2 × 3,50 = 32,00 | V10 | Recalcular o devolver al origen |
| `INV10` | 25 plazas en sala de capacidad 20 | V11 | Rechazar |
| `INV11` | Espacio `NX-MAD-HD-01` marcado como ciudad Sevilla | V12 | Corregir con el maestro |
| `INV12` | Creada (10-dic) después del inicio (5-dic) | V13 | Cuarentena |
| `INV13` | Canal `fax` | V14 | Rechazar |
| `INV15` | Fecha imposible `2026-13-45T25:00` | V02 | Rechazar |
| `INV16` | `coffee=1;coffee=2` (servicio repetido) | V15 | Fusionar en `coffee=3` o rechazar |

```
python modelo_fisico/scripts/validar_casos_limite.py
Fuente original: 0 violaciones (esperado 0) -> OK
Fuente + casos límite: 19 violaciones distintas
...
No detectadas: ninguna
Falsos positivos: ninguno
RESULTADO: OK
```

**Hallazgo (no es un fallo de las reglas):** el duplicado `R001` produce además violaciones de V10 y V15 sobre `R001`. Es un efecto colateral lógico: con dos filas con el mismo id, sus servicios se cuentan dos veces. Está declarado en el script como esperado. Moraleja de diseño: **V01 debe ser la primera regla en ejecutarse y su fallo debe bloquear el resto**.

## 4. Alcance de la comprobación de solapes (V09)

V09 **detecta**, no **impide**. En el perfil analítico eso es suficiente (se audita el histórico); en un perfil operacional exigiría una restricción transaccional en el motor. Se tratan como no solapadas las reservas canceladas y las que solo se tocan en el borde (`11:00 fin` vs `11:00 inicio`), porque la comparación usa desigualdad estricta.

## 5. Resultados de las consultas prioritarias (datos de partida)

**Q5 · Horas por ciudad y mes (excluye canceladas)**

| Mes | Ciudad | Horas-reserva | Horas-plaza | Rank horas-reserva | Rank horas-plaza |
|---|---|---:|---:|:-:|:-:|
| 2026-10 | Lisboa | 16,0 | 16,0 | 1 | 1 |
| 2026-10 | Madrid | 11,0 | 15,0 | 2 | 2 |
| 2026-11 | Madrid | 41,0 | 339,0 | 1 | 1 |
| 2026-11 | Lisboa | 14,0 | 41,0 | 2 | 3 |
| 2026-11 | Sevilla | 10,0 | 94,0 | 3 | 2 |

Elegir la métrica **cambia el resultado**: en noviembre, Lisboa es 2.ª en horas-reserva y 3.ª en horas-plaza (Sevilla la supera por sus salas de formación con muchas plazas). Por eso se publican las dos.

**Q6 · Ingresos (confirmed + completed, sin impuestos)**: Madrid-training_room 606,00 · Madrid-meeting_room 418,00 · Sevilla-training_room 430,00 · Lisboa-meeting_room 373,00 · Sevilla-meeting_room 115,00 · Lisboa-hot_desk 77,50 · Madrid-hot_desk 32,00.

**Q7 · Cancelación por canal y mes de creación**: octubre: `app` 1/3 (33,3 %), `phone` 1/2 (50 %), `web` 0/4, `partner` 0/5; septiembre: 0 %.
⚠️ Con 1–5 reservas por celda, **estos porcentajes no son concluyentes**: sirven para demostrar el cálculo, no para decidir sobre canales.

**Q8 · Servicios (unidades en reservas no canceladas)**: catering 16 (3 reservas) · projector 6 (6) · coffee 3 (2; 6 contando las canceladas) · locker 2 · whiteboard 2. Por *reservas* distintas, el proyector es el más pedido; por *unidades*, el catering. Otra métrica, otro ganador.

## 6. Ampliación reproducible y medición

`generar_ampliacion.py` crea **2.000.000 de reservas y 2.703.253 líneas** (50.000 miembros, 90 espacios), sintéticas y deterministas (dos ejecuciones dan el mismo `Σ total_amount` = 310.855.212,50; ~7 % de canceladas). Los hechos pesan **32,4 MB + 6,9 MB** en Parquet/zstd.

Medición (`benchmark.py`): DuckDB 2.0.0, Python 3.12.3, **1 hilo / 1 CPU**, mediana de 5 ejecuciones tras 1 de calentamiento, lectura directa de Parquet:

| Consulta | Prototipo (18 reservas) | Ampliación (2 M reservas) |
|---|---:|---:|
| Q5 horas por ciudad/mes | 3,0 ms | 41,1 ms |
| Q6 ingresos ciudad × tipo | 2,3 ms | 63,0 ms |
| Q7 cancelación canal × mes | 1,7 ms | 21,4 ms |
| Q8 servicios más solicitados | 3,7 ms | **987,7 ms** |

**Lectura prudente de la evidencia**
- Q5–Q7 agregan 2 M de filas en decenas de milisegundos en una sola CPU, compatible con la hipótesis de 'consulta interactiva'.
- **Q8 es 15–45 veces más lenta** que las demás: es la única que hace un join entre las dos tablas de hechos y un `COUNT(DISTINCT)`. Es un coste del modelo normalizado (decisión D1), no del motor. Mitigación posible (no implementada ni medida): copiar `status` a `fact_reserva_servicio`.
- **Límites:** una sola máquina y un solo hilo; datos sintéticos de distribución uniforme (sin sesgo realista); sin medir carga concurrente ni tiempos de carga/escritura; **no se extrapola** más allá de 2 M de reservas. Los datos de la ampliación no cumplen V09 (no se evitaron solapes) y no sirven para validar reglas de negocio.
