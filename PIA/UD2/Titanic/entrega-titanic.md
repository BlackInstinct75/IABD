# Entrega — Sesión Titanic

**Cuaderno:** [04_sesion_titanic.ipynb](04_sesion_titanic.ipynb).  
**Tarea Moodle:** «Sesión Titanic — Seaborn, Plotly y EDA».  
**Valoración:** hecho/no hecho y checklist; no es una prueba ni se corrige gráfico a gráfico.

Trabaja en pareja, pero **cada estudiante entrega su propio cuaderno**.

## Antes de empezar

Descarga el cuaderno, esta ficha y `titanic.csv` desde los recursos de la sesión. Si trabajas con archivos sueltos, coloca **el CSV junto al cuaderno**. Si has descargado el repositorio completo, puedes conservar las carpetas de UD2. Abre Jupyter con `pixi run --environment ud2 jupyter lab` y selecciona el intérprete/kernel de ese entorno; abrir Jupyter desde otro Python puede producir imports diferentes.

**Base de la sesión:** apartados 0–3 (Seaborn, Plotly y EDA), ticket y registro. **Ampliación guiada:** apartado 4 de preparación para ML, solo si el profesor lo activa y da tiempo. Que un apartado siga pendiente no convierte una incidencia en un examen suspenso.

## Qué se entrega

Un único ZIP:

```text
apellido_nombre_titanic/
├── 04_sesion_titanic.ipynb
└── titanic_interactivo.html
```

## Checklist

- [ ] El cuaderno se ejecuta de principio a fin sin errores.
- [ ] Los tres gráficos de Seaborn tienen título, ejes y unidades.
- [ ] La interpretación distingue recuento de tasa.
- [ ] El HTML de Plotly se abre en el navegador y responde a hover, leyenda y zoom.
- [ ] La tabla de supervivencia por clase y sexo es 3×2.
- [ ] Hay tres conclusiones y una limitación del dataset.
- [ ] Si se ha trabajado ML: `X_train_prep` tiene 712 filas, `X_test_prep` 179, las mismas columnas y no hay NaN en ninguna de las dos matrices.
- [ ] Si se ha trabajado ML: el preprocesador se ajusta **solo con train**; el test solo se transforma. No se incluyen ni `Survived` ni `Survived_label` en X.
- [ ] No se ha entrenado ningún modelo en esta sesión.
- [ ] Ticket, registro de ayuda y apartados pendientes están completos.

## Reglas

- No hace falta descargar Titanic: usa el CSV local.
- Si el HTML supera el límite de Moodle, avisa al profesor; no cambies a CDN sin indicarlo ni lo sustituyas por una captura.
- Si no terminas, sube lo hecho y registra lo pendiente; puedes completarlo después.
- Ejecuta en orden los apartados trabajados. Si uno no se ha iniciado, no ejecutes su checkpoint como si estuviera resuelto: anota «pendiente». Los checkpoints ayudan a detectar errores básicos; no sustituyen la interpretación ni califican el acierto.
