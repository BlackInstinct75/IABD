# UD1 · Modelado documental y consulta analítica

**Autor:** Francisco Javier Porta Borge

## 1. Decisiones de modelado

| Decisión | Elección | Justificación |
|---|---|---|
| Entidad | **Pedido** (`order`) | Es la unidad lógica de negocio. Sus líneas (`items`) son subelementos que no tienen sentido fuera del pedido. |
| Clave | `order_id` | Identifica cada pedido. Al aplanar se repite en cada línea para poder reagruparlas. `customer_id` es clave foránea hacia el cliente. |
| Campos conservados | `order_id`, `customer_id`, fecha, `canal`, `sku`, `qty`, `price`, `cost` | Son los datos de origen; con ellos se puede recalcular todo. |
| Campos calculados | `importe = qty*price`, `margen_u = price-cost`, `margen = qty*(price-cost)` | Se **guardan** en el formato analítico: Parquet es columnar y comprime bien, así que el coste de almacenar 3 columnas más es mínimo y las consultas de agregación evitan recalcular. En el JSON **no** se guardan: se pueden derivar y duplicarlos arriesga incoherencias si cambia `price` o `qty`. |
| Modelo de salida | JSON (documental) para recuperar el pedido completo; plano + Parquet para análisis agregado | Depende de **cómo se va a leer** el dato (ver §4). |

## 2. Estructura del documento JSON

Ejemplo abreviado (`data/orders.ndjson`, un documento por línea):

```json
{
  "order_id": 1,
  "customer_id": 2807,
  "ts": "2024-06-01T00:00:00T12:00:00",
  "canal": "web",
  "items": [
    {"sku": "SKU0083", "qty": 1, "price": 20.48, "cost": 11.66},
    {"sku": "SKU0018", "qty": 4, "price": 7.03,  "cost": 5.35}
  ]
}
```

**Tipologías:** es un dato **semiestructurado**. Los campos de primer nivel son
escalares (enteros, cadenas, marca temporal) y `items` es un **array de objetos
anidados** de longitud variable (1 a 4).

> **Incidencia detectada en el generador:** `ts` se construye como
> `d.isoformat() + "T12:00:00"`, pero `d.isoformat()` ya incluye la hora, por lo
> que sale `2024-06-01T00:00:00T12:00:00`, que no es una fecha ISO válida. En
> DuckDB se lee como `VARCHAR`. El CSV plano usa `fecha` (`date().isoformat()`)
> y no tiene el problema. La corrección sería `d.date().isoformat() + "T12:00:00"`.

### Dos ventajas del modelo documental

1. **El pedido se recupera completo en una lectura.** Cabecera y líneas viajan
   juntas, sin `JOIN` entre tablas. Ideal para mostrar o editar un pedido concreto.
2. **Esquema flexible y reflejo natural de la realidad.** Las líneas son un
   array dentro del pedido; se pueden añadir campos nuevos a unas líneas sin
   migrar todo el conjunto.

### Una limitación

**Las agregaciones transversales son más costosas.** Para el margen por producto
hay que desanidar (`$unwind` en MongoDB, `UNNEST` en DuckDB) y leer todo el
documento aunque solo se necesiten `sku`, `qty`, `price` y `cost`. Además, el
modelo no impone tipos ni coherencia (por ejemplo, el `ts` mal formado pasa sin
error) y los datos del cliente o producto repetidos en los documentos podrían
quedar desactualizados.

## 3. Consultas DuckDB (`p2_duckdb.sql`)

Resultados con la semilla fijada (`random.seed(13); np.random.seed(13)`):
9 057 pedidos y 22 579 líneas, del 2024-06-01 al 2024-07-30.

- **Coherencia:** el margen total es 198 454,36 tanto leyendo el JSON con
  `UNNEST` como desde la tabla plana, lo que confirma que el aplanado no pierde
  información.
- **Q1 margen por producto:** el top lo encabeza `SKU0067` (2 478,17 €), seguido
  de `SKU0051` y `SKU0069`. Los márgenes porcentuales son parecidos (~35 %) porque
  el coste es entre el 50 % y el 80 % del precio de forma aleatoria; las
  diferencias vienen sobre todo del volumen.
- **Q2 evolución de pedidos:** junio 4 591 pedidos y julio 4 466. Se usa
  `COUNT(DISTINCT order_id)` porque contar filas contaría líneas, no pedidos.
  También se incluye la vista semanal.
- **Q3 consulta adicional (ticket medio y margen por canal):** el canal es la
  dimensión de negocio principal del conjunto de datos. Se agrega primero por
  pedido para no mezclar líneas con pedidos. Resultado: los tres canales son muy
  similares (ticket ~62-63 €, margen ~35 %), coherente con que los datos son
  sintéticos y el canal se elige al azar.
- **Q4 clientes recurrentes:** la consulta de la plantilla (>5 pedidos desde
  julio) casi no devuelve filas, porque la media es de ~3 pedidos por cliente.
  Se muestra la distribución y los clientes con 7 o más pedidos.

## 4. JSON/documental frente a Parquet/analítico

| Aspecto | JSON documental | Parquet analítico |
|---|---|---|
| Unidad | Pedido completo con líneas anidadas | Línea de pedido (fila plana) |
| Lectura típica | "Dame el pedido 1234" | "Margen por producto en todo el periodo" |
| Almacenamiento | Por filas, texto, sin compresión eficiente | Columnar, binario, comprimido, tipado |
| Esquema | Flexible, no validado | Explícito, con tipos |
| Redundancia | Baja (cabecera una sola vez) | Alta (`order_id`, `customer_id`, `canal` se repiten por línea) |
| Escritura/edición | Cómoda (se actualiza un documento) | Pensado para escribir una vez y leer mucho |

**Qué conservaría en Parquet:** las columnas de origen (`order_id`, `customer_id`,
`fecha`, `canal`, `sku`, `qty`, `price`, `cost`) y las calculadas (`importe`,
`margen_u`, `margen`). Las analíticas leen pocas columnas, y al ser columnar
Parquet solo lee las que se piden, comprime bien los valores repetidos
(`canal`, `sku`) y conserva los tipos. No guardaría el array `items` anidado:
el aplanado lo vuelve innecesario.

**Por qué DuckDB no necesita servidor:** es un motor analítico **embebido** (en
proceso), como SQLite pero columnar. Se ejecuta desde la CLI, Python o un
notebook y consulta directamente ficheros (`read_csv`, `read_json`, Parquet) sin
instalar, configurar ni mantener un servicio, ni importar los datos antes. Para
este volumen y este tipo de preguntas es más sencillo que desplegar MongoDB.

**Conclusión:** no hay un modelo mejor en abstracto. Si el acceso principal es
recuperar o editar pedidos completos, conviene el **documental**; si se trata de
agregar, filtrar y agrupar sobre muchos pedidos, conviene el **plano en
Parquet**. En este caso las preguntas pedidas son analíticas, por lo que el
formato plano con DuckDB es la mejor opción.
