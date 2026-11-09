# NexoWork · UD1 — Modelado completo (Perfil C analítico, DuckDB + Parquet)

**Integrante:** _Francisco Javier Porta Borge_ 
## Perfil y tecnología
- **Perfil principal:** C · analítico (consultas prioritarias Q5, Q6, Q7 y Q8).
- **Tecnología:** DuckDB 2.0.0 + ficheros Parquet (zstd), esquema en estrella.
- **No se usa como sistema transaccional** (ver `decision_record.md` §5.3).

## Requisitos y versiones
- Python ≥ 3.9 (probado con 3.12.3) y `duckdb==2.0.0`.
- Sin Docker, sin servidor, sin credenciales. Datos 100 % ficticios.
```bash
pip install -r requirements.txt
```

## Contenido
| Fichero | Fase |
|---|---|
| `decision_record.md` | 1 Requisitos/perfiles/consultas · 5 Comparación y decisión tecnológica |
| `modelo_conceptual.mmd` | 2 Diagrama Mermaid (explicación textual en `modelo_logico.md` §1) |
| `modelo_logico.md` | 2–4 Entidades, granularidad, claves, original vs derivado, normalización |
| `modelo_fisico/` | 6 Datos, SQL (`sql/`) y scripts (`scripts/`) |
| `validacion.md` | 7 Reglas, casos límite, resultados y medición |

## Orden de ejecución (desde la raíz del proyecto)
```bash
python modelo_fisico/scripts/run_all.py              # 1) valida → modelo → Parquet → Q5..Q8
python modelo_fisico/scripts/validar_casos_limite.py # 2) casos límite (debe acabar en RESULTADO: OK)
python modelo_fisico/scripts/generar_ampliacion.py   # 3) opcional: 2 M reservas sintéticas (~1 min)
python modelo_fisico/scripts/benchmark.py            # 4) opcional: tiempos Q5..Q8 (requiere 1 y 3)
```
`generar_ampliacion.py` acepta un tamaño: `... generar_ampliacion.py 500000`.

## Resultados esperados
1. `run_all.py`: `0 violaciones`, `Conciliación OK: 18 reservas, 17 líneas de servicio, total 2245.00 EUR` y las cuatro tablas de resultados. Genera `modelo_fisico/out/parquet/*.parquet` (5 ficheros) y `modelo_fisico/out/resultados/Q5..Q8.csv`.
2. `validar_casos_limite.py`: 0 violaciones en la fuente; 19 pares (regla, id) en fuente + inválidos; `No detectadas: ninguna`, `Falsos positivos: ninguno`, `RESULTADO: OK`.
3. `generar_ampliacion.py`: `fact_reserva=2,000,000  fact_reserva_servicio=2,703,253` en `modelo_fisico/out/scale/`.
4. `benchmark.py`: la tabla de `validacion.md` §6 (los milisegundos variarán según la máquina; el orden de magnitud y la lentitud relativa de Q8 deben mantenerse).

## Limitaciones conocidas
- El dataset real tiene 18 reservas: **demuestra el modelo, no su rendimiento**. Las conclusiones de escala se limitan a la ampliación sintética de 2 M filas, en 1 hilo.
- Parquet no impone claves ni restricciones: toda la integridad la aplica el pipeline (`02_validacion.sql`).
- V09 detecta solapamientos, no los impide; para impedirlos haría falta un sistema transaccional.
- Sin `cancelled_at` en la fuente: la tasa de cancelación se calcula por mes de **creación**.
- Sin impuestos; sin histórico de precios (se asume que el precio de catálogo es el cobrado, lo que V10 confirma para los 17 datos de partida).
- Q8 es costosa a gran escala por el join entre hechos (ver `validacion.md` §6).
- Las frecuencias, el crecimiento y los tiempos esperados de `decision_record.md` son **hipótesis de diseño**, no datos medidos de NexoWork.
