# Entrega — Comparativa cooperativa de motores Titanic

Enunciado: [actividad-comparativa-motores-titanic.md](actividad-comparativa-motores-titanic.md).

**Dos momentos de entrega**, con una sola subida por equipo en cada momento.
El profesor comunicará los códigos de equipo/grupo y los plazos. No se crea una
entrega individual duplicada ni se exige a cada estudiante hacer los tres motores.

## 1. Equipo experto: cuaderno y ficha de resultados

Una persona designada sube `experto_<motor>_<codigo>.zip`:

```text
experto_<motor>_<codigo>/
├── eda_titanic_<motor>.ipynb
└── ficha_experta.md
```

Usad `polars`, `duckdb` o `cudf` como motor. El cuaderno cuDF puede conservar el
nombre original `eda_titanic_cudf_colab.ipynb`. No adjuntéis entornos, instalaciones,
el CSV original ni los cuadernos de los otros equipos.

### Plantilla de `ficha_experta.md`

```markdown
# Equipo experto <codigo> — <motor>

## Integrantes y aportación
| Integrante | Qué ejecutó, modificó, comprobó o explicó |
|---|---|
| | |

## Entorno y archivo
- Versiones del motor/Python:
- SHA-256 del CSV:
- Estado: ejecutado / NO EJECUCIÓN DE CUDF / ERROR DE INSTALACIÓN / ERROR DE CARGA O EJECUCIÓN CUDF.
- Incidencias y qué probamos:

## Núcleo común
Copiad las cinco tablas del cuaderno: global, Sex, Pclass, Pclass × Sex y edad.
Después de las claves, todas llevan total, supervivientes y tasa.
Indicad si cada tabla fue ejecutada o es REFERENCIA PRECOMPUTADA.

## Nuestra pregunta propia
- Pregunta:
- Filtro y agrupación:
- Qué filas entran/salen y qué hacemos con valores ausentes:
- Qué significa el denominador:
- Dónde está el código en el cuaderno:
- Resultado obtenido (o PENDIENTE DE EJECUCIÓN):
- Interpretación y limitación:

## Ayuda utilizada
Documentación, otras personas o IA; para qué y qué comprobamos nosotros.
```

### Checklist experto

- [ ] El cuaderno conserva código y salidas reales de los apartados ejecutados.
- [ ] CSV original 891×12; nulos comprobados, sin limpiar ni imputar el original.
- [ ] Cinco tablas comparables con `total`, `supervivientes`, `tasa`.
- [ ] En edad se excluyen 177 ausentes: 113 menores y 601 adultos; no usar 714 como denominador de cada grupo.
- [ ] Pregunta propia con código del motor, evidencia y denominador explícito.
- [ ] Integrantes, aportaciones y ayuda registrados.
- [ ] Si no se ejecutó cuDF, estado/error y referencias claramente etiquetados; pregunta propia pendiente sin cifras inventadas.

## 2. Grupo mixto: informe y exposición

Una persona designada sube `mixto_<codigo>.zip`:

```text
mixto_<codigo>/
├── informe_comparativo.md
└── presentacion.pdf
```

- **Informe:** seguid la plantilla de diez puntos del enunciado. Incluid una
  tabla común comprobada con numerador/denominador/tasa, las discrepancias y cómo
  se resolvieron, una síntesis de las preguntas propias y el estado real de cuDF.
- **Presentación:** máximo cinco diapositivas, 5 minutos de exposición + 2 de
  preguntas. Intervienen todos; si hay cuatro integrantes, se reparte también
  la cuarta intervención. No se requiere otro informe individual.
- **Comparación honesta:** si cuDF no se ejecutó, podéis contrastar sus referencias
  y explicar el enfoque, pero no declarar paridad empírica de los tres motores.

### Checklist del grupo mixto

- [ ] Representados los tres enfoques, con incidencias/estados visibles.
- [ ] Tablas del núcleo común contrastadas; mismas claves, orden y significado.
- [ ] Preguntas propias separadas del núcleo: preguntas diferentes no exigen cifras iguales.
- [ ] Conclusión respaldada por cifras y una limitación que impide afirmar causalidad.
- [ ] Justificada la elección de herramienta; no hay benchmark ni motor ganador.
- [ ] Cada integrante puede explicar una consulta, un resultado o una limitación.

## 3. Criterio de seguimiento

Se revisan **trabajo realizado, evidencia, interpretación, claridad y aportación**,
con registro de completitud. No se establecen porcentajes nuevos ni se puntúan
los tiempos de ejecución o conseguir una GPU. Si falta algo, indicadlo y continuad
según el plazo que concrete el profesor.

Los documentos completados con integrantes se entregan en Moodle; no se suben
con identidades del alumnado al repositorio público.
