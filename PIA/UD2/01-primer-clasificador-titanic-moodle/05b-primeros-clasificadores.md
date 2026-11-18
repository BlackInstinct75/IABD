# Primeros clasificadores: de una referencia a la regresión logística

Esta guía acompaña a la práctica `01-primer-clasificador-titanic.ipynb`.
No hace falta memorizar las fórmulas antes de ejecutar y observar.

## ¿Qué queremos aprender?

En clasificación supervisada disponemos de ejemplos con características **X**
y una respuesta conocida **y**. En Titanic, `y = Survived` toma los valores 0
(no sobrevivió) y 1 (sobrevivió). Queremos construir una regla para predecir
la clase de otro pasajero, no demostrar qué causó el resultado.

Reservamos datos para comprobar cómo funciona fuera del entrenamiento. Como el
EDA previo utilizó todo Titanic, esta primera evaluación es demostrativa y no
plenamente independiente: algunas decisiones podrían estar influidas por ese EDA.

## 1. Empezar por una referencia: `DummyClassifier`

Una referencia contesta: «¿Qué conseguiríamos sin aprender de las características?».
Con `strategy="most_frequent"`, se identifica la clase más frecuente **en train**
y se predice siempre esa clase. Por ejemplo, si en entrenamiento predominan
los ceros, dirá 0 para todo pasajero.

Si seis de cada diez casos fueran ceros, esa estrategia podría acertar alrededor
del 60 % sin detectar a ningún superviviente. No existe un porcentaje fijo
garantizado: depende de los datos. Comparar con esta base evita llamar bueno
a un modelo solo porque tenga un porcentaje aparentemente alto.

## 2. Regresión logística: un primer clasificador

Aunque su nombre incluya «regresión», aquí se usa para **clasificar dos clases**.
El modelo combina las características preparadas con unos coeficientes aprendidos
y obtiene una puntuación. La función sigmoide convierte esa puntuación en un
valor entre 0 y 1, interpretable como probabilidad estimada de la clase positiva:

```text
puntuación = intercepto + coeficiente₁ × característica₁ + …
probabilidad estimada = 1 / (1 + exp(-puntuación))
```

En la decisión binaria habitual de `predict`, se compara con un umbral que
normalmente es 0,5. `predict_proba` devuelve estimaciones por clase; conviene
comprobar el orden en `classes_`. Una probabilidad estimada no es una certeza ni
está necesariamente bien calibrada. El umbral apropiado depende del problema y
de los costes de equivocarse.

Durante `fit`, el algoritmo ajusta los coeficientes con los ejemplos de
entrenamiento; no recibe las respuestas del conjunto de prueba. Es lineal en
la **puntuación** de las características preparadas: puede funcionar bien como
punto de partida, pero no representa automáticamente cualquier relación compleja.
La regularización ayuda a limitar coeficientes extremos; no elimina por sí sola
el sobreajuste ni garantiza causalidad o ausencia de sesgos.

## 3. ¿Por qué hay preparación en el pipeline?

- `SimpleImputer` aprende cómo sustituir los nulos a partir de entrenamiento.
- `OneHotEncoder` convierte categorías en columnas numéricas; una categoría nueva
  se gestiona según `handle_unknown`.
- `StandardScaler` aprende medias y desviaciones del entrenamiento para escalar
  columnas numéricas; no es una regla universal para todos los algoritmos.
- `Pipeline` agrupa preparación y modelo: con `fit(X_train, y_train)` ajusta
  todo en orden; `predict(X_test)` aplica lo aprendido sin volver a ajustarlo.

Así mantenemos el conjunto de prueba fuera del aprendizaje. Tampoco debemos
incluir `Survived` ni otra columna que copie su contenido entre las entradas.

## 4. Leer los resultados

La **exactitud** es la proporción de predicciones correctas. No cuenta toda
la historia, especialmente si una clase es mucho más frecuente.

| | Predice 0 | Predice 1 |
|---|---|---|
| **Real 0** | acierto: verdadero negativo | error: falso positivo |
| **Real 1** | error: falso negativo | acierto: verdadero positivo |

Preguntamos cuántos errores hay de cada tipo y qué significan en el problema.
En decisiones reales, los costes de ambos errores pueden diferir. No hay que
confundir rendimiento predictivo con justicia, causalidad o utilidad práctica.

## 5. Después: comparar configuraciones

Una vez comprendido el primer recorrido, se puede usar validación cruzada dentro
de entrenamiento para comparar hiperparámetros. `GridSearchCV` repite el ajuste
en varias particiones y selecciona una configuración; la puntuación de validación
no es la nota del test final. El test se reserva hasta terminar la selección.
Un `Pipeline` dentro de la búsqueda evita ajustar el preprocesado usando el pliegue
de validación. Ejemplo posterior: sección GridSearch del cuaderno
`02-bloque2-scikitlearn-modelos-basicos.ipynb`.

El capítulo «II. Aprendizaje supervisado», disponible en la documentación completa
de UD3, recoge otras técnicas; no se necesita para esta práctica ni forma parte
del ZIP autónomo. Se introducirán gradualmente después de este primer flujo.
