# UD1 · Modelado documental y consulta analítica (P2)

**Integrante:** Francisco Javier Porta Borge

## 1. Finalidad y alcance

El sistema registra pedidos y sus líneas para **recuperar un pedido completo**, **analizar ventas por canal y mes** y **calcular el margen por producto (SKU)**. Quedan fuera pagos, devoluciones y stock.

## 2. Modelo documental

### Ejemplo abreviado (un documento = un pedido)

```json
{
  "order_id": 1,
  "customer_id": 2807,
  "fecha": "2024-06-01",
  "canal": "web",
  "lineas": [
    { "sku": "SKU0083", "qty": 2, "price": 5.93, "cost": 3.38 },
    { "sku": "SKU0018", "qty": 2, "price": 7.29, "cost": 5.55 }
  ]
}
```

- **Granularidad:** cada documento es **un pedido**; cada elemento de `lineas` es **una línea** (un producto en ese pedido).
- **Claves:** `order_id` identifica el pedido; `customer_id` referencia al cliente; `sku` referencia al producto. No hay catálogos, así que son referencias no verificables.
- **Tipologías:** identificadores (enteros/texto), fecha, categórico (`canal`), cantidades enteras, importes decimales y un array anidado de objetos.

### Dos ventajas

1. **Recuperación del pedido completo en una sola lectura.** Las líneas viajan anidadas con la cabecera; no hacen falta joins ni varias consultas para atender a un cliente.
2. **Cabecera sin duplicar.** Cliente, fecha y canal aparecen una vez por pedido, y un pedido es una unidad coherente (se escribe y se lee entero). Además el esquema es flexible si se añaden campos a las líneas.

### Una limitación

**Las agregaciones transversales son incómodas e ineficientes**: calcular ventas por canal y mes o margen por SKU obliga a “desanidar” (`UNNEST`/`explode`) las líneas de todos los pedidos. Por eso se mantiene también una vista plana (fila por línea) para análisis. Además, al duplicar datos entre las dos vistas hay que mantenerlas coherentes: si cambia una cabecera, hay que actualizar la vista plana.

## 3. Formato analítico: Parquet y DuckDB

**Qué conservaría en Parquet:** la vista plana, una fila por línea, con `order_id, customer_id, fecha, canal, sku, qty, price, cost`. Son exactamente las columnas que usan las consultas de ventas, margen y evolución temporal. El Parquet es regenerable desde el CSV/NDJSON, por lo que no se entrega.

**Por qué:** es **columnar**, así que una consulta como “suma de `qty*price` por canal” lee solo las columnas necesarias y no el documento entero. Guarda el esquema y los tipos (fecha, decimal, entero), y comprime bien porque columnas como `canal` o `sku` tienen muchos valores repetidos.

**Por qué DuckDB permite explorarlo sin servidor:** es una base de datos **embebida y en proceso** (como SQLite, pero orientada a análisis). Se ejecuta como librería o desde la línea de comandos y consulta directamente ficheros con `read_csv`/`read_parquet`. No hay que instalar, configurar ni mantener un servicio.

### Comparación JSON/documental vs Parquet/analítico

| Aspecto | NDJSON / documental | Parquet / analítico |
|---|---|---|
| Unidad | Un pedido con líneas anidadas | Una fila por línea (cabecera duplicada) |
| Mejor para | Leer/escribir un pedido completo | Agregar muchas líneas (canal, mes, SKU) |
| Cabecera | Una vez por pedido | Repetida en cada línea |
| Lectura | Registro entero | Solo las columnas necesarias |
| Riesgo | Agregaciones costosas | Desincronización si cambia la cabecera |

**Conclusión:** no compiten; sirven a consultas distintas. El documento atiende el acceso operativo (pedido completo) y el Parquet el analítico. Ojo: **NDJSON es solo un formato de fichero, no una base de datos documental**; para tener índices, consultas por clave, etc. haría falta un motor (p. ej. MongoDB).

## 4. Decisiones de diseño (resumen del taller)

| Dato o relación | Decisión | Motivo | Riesgo |
|---|---|---|---|
| Líneas de un pedido | **Anidar** (en el documento) | Se leen siempre con el pedido y su número es pequeño | Listas que crezcan sin límite; agregar exige desanidar |
| Cliente del pedido | **Referenciar** (`customer_id`) | Un cliente tiene muchos pedidos; no se copian sus datos | Sin catálogo no se puede verificar que exista |
| Producto de la línea | **Referenciar** (`sku`) | Un producto aparece en muchas líneas | Igual: sin catálogo de productos |
| Cabecera en el CSV | **Duplicar** en cada línea | Facilita agregar sin joins | Inconsistencias si cambia la cabecera |
| Precio y coste de la línea | **Copiar** el valor de la compra | Es el precio histórico, no el de catálogo | Confundirlo con el precio actual |

### Reglas de calidad (de diseño, no aplicadas automáticamente por P2)

| Campo / regla | Qué se comprueba | Si no se cumple |
|---|---|---|
| `order_id` | No nulo; cada pedido con ≥1 línea; cabecera idéntica en todas sus líneas | Marcar el pedido como sospechoso en una tabla de incidencias; no borrar |
| `canal` | Valor en {tienda, web, app} | Conservar el valor original y añadir columna `canal_valido = false` |
| `qty` | Entero > 0 | Marcar la línea y excluirla de las métricas, conservándola |
| `price`, `cost` | Numéricos ≥ 0; avisar si `cost > price` (margen negativo) | Marcar; revisar con negocio antes de corregir |
| `fecha` / `ts` | Fecha válida y no futura | Guardar el original y una versión normalizada aparte |
| Cabecera | Un único `customer_id`, `fecha` y `canal` por `order_id` | Marcar el pedido; la vista plana se regenera desde el documento |

La sección 2 de `p2_duckdb.sql` implementa estos controles como consultas que **solo informan**.

### Formato y organización física (razonado, no implementado en P2)

- **Indexar `order_id`** en una base documental haría la recuperación de un pedido proporcional a una búsqueda por clave, no a un recorrido completo. Cuesta espacio y algo de escritura.
- **Particionar por fecha** en un volumen grande permitiría leer solo los meses consultados y archivar los antiguos. A cambio, aparecen muchos ficheros pequeños y las consultas sin filtro de fecha leen todas las particiones.
- **Conservación:** los datos temporales (por ejemplo, ficheros intermedios o logs de carga) tendrían una caducidad definida; los pedidos se conservarían según la normativa aplicable.

## 5. Limitaciones

1. **Falta de clave de línea.** P2 no incluye `line_number`. La clave deseable sería `(order_id, line_number)`. Tampoco sirve `(order_id, sku)`, porque un pedido puede repetir un SKU en dos líneas. Sin clave de línea no se pueden identificar ni deduplicar líneas de forma segura.
2. **Ausencia de catálogos.** No hay catálogo de clientes ni de productos, así que no se puede comprobar que `customer_id` o `sku` existan.
3. **Datos sintéticos.** Representan compras simuladas; no hay estacionalidad ni comportamiento real de clientes.
4. **Sin medidas de rendimiento.** Las consultas se han probado solo para comprobar que son correctas. No se afirma nada sobre tiempos ni escalabilidad.
