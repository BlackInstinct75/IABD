# DEPARTAMENTO DE INFORMÁTICA

**MÓDULO:** Sistemas de Aprendizaje Automático

## Trabajo de investigación: Análisis y estudio del estado y tendencias en herramientas de Aprendizaje Automático

**Alumno:** Francisco Javier Porta Borge
**Unidad Didáctica 2 (UD2)**
**Fecha:** Octubre de 2026

---

## Índice

1. [Introducción](#1-introducción)
2. [Principios de los sistemas de aprendizaje automático](#2-principios-de-los-sistemas-de-aprendizaje-automático)
3. [Tipos y usos de los sistemas de aprendizaje automático](#3-tipos-y-usos-de-los-sistemas-de-aprendizaje-automático)
   - 3.1. Tipos principales
   - 3.2. Diferencias entre los tipos en el contexto actual
4. [Estado actual y tendencias de las herramientas](#4-estado-actual-y-tendencias-de-las-herramientas)
   - 4.1. Técnicas y herramientas
   - 4.2. Asociación de técnicas y herramientas a cada tipo
   - 4.3. Tendencias
5. [Conclusiones](#5-conclusiones)
6. [Bibliografía y webgrafía](#6-bibliografía-y-webgrafía)

---

## 1. Introducción

El aprendizaje automático (*machine learning*, ML) es la rama de la inteligencia artificial que estudia cómo construir sistemas capaces de mejorar su rendimiento en una tarea a partir de la experiencia, es decir, de los datos, sin que cada comportamiento tenga que ser programado de forma explícita. Hoy está presente en buscadores, sistemas de recomendación, diagnóstico médico, detección de fraude, conducción asistida y asistentes conversacionales. Este trabajo resume sus principios, describe sus tipos y usos, repasa el estado actual de las herramientas y expone las tendencias que se observan a finales de 2026.

## 2. Principios de los sistemas de aprendizaje automático

Un sistema de aprendizaje automático se basa en la idea de que un modelo matemático puede ajustar sus parámetros a partir de ejemplos para generalizar a datos nuevos. Los principios fundamentales son los siguientes:

- **Datos como materia prima.** La calidad, cantidad y representatividad de los datos condicionan el resultado. Antes de entrenar es necesario recopilarlos, limpiarlos y transformarlos (ingeniería de características).
- **Modelo y función de pérdida.** El modelo (regresión lineal, árbol de decisión, red neuronal, etc.) produce predicciones, y una función de pérdida mide el error cometido respecto al objetivo deseado.
- **Optimización.** El entrenamiento consiste en minimizar la función de pérdida mediante algoritmos como el descenso del gradiente, ajustando los parámetros del modelo de forma iterativa.
- **Generalización.** El objetivo no es memorizar los datos de entrenamiento, sino rendir bien con datos nunca vistos. Por ello se separan los datos en conjuntos de entrenamiento, validación y prueba, y se vigilan el sobreajuste (*overfitting*) y el subajuste (*underfitting*), buscando el equilibrio entre sesgo y varianza.
- **Evaluación y ciclo de vida.** Se emplean métricas adecuadas a cada problema (exactitud, precisión, exhaustividad, F1, error cuadrático medio, etc.) y el modelo se despliega, se monitoriza y se reentrena cuando los datos cambian, lo que se conoce como ciclo de vida del modelo.

## 3. Tipos y usos de los sistemas de aprendizaje automático

### 3.1. Tipos principales

**Aprendizaje supervisado.** El modelo aprende a partir de datos etiquetados, es decir, pares entrada-salida conocidos. Se divide en clasificación (predecir una categoría, como detectar correo no deseado) y regresión (predecir un valor numérico, como el precio de una vivienda).

**Aprendizaje no supervisado.** Trabaja con datos sin etiquetar y busca estructura oculta: agrupamiento (*clustering*) de clientes, reducción de dimensionalidad o detección de anomalías.

**Aprendizaje semisupervisado y autosupervisado.** El primero combina pocos datos etiquetados con muchos sin etiquetar. El segundo genera sus propias etiquetas a partir de los datos (por ejemplo, predecir la siguiente palabra de un texto) y es la base del preentrenamiento de los grandes modelos de lenguaje y de visión actuales.

**Aprendizaje por refuerzo.** Un agente interactúa con un entorno y aprende una política que maximiza una recompensa acumulada mediante prueba y error. Se usa en robótica, videojuegos, optimización de recursos y en el ajuste de modelos de lenguaje a partir de retroalimentación humana.

### 3.2. Diferencias entre los tipos en el contexto actual

La tabla 1 resume las diferencias. En la práctica actual, los problemas de negocio con datos tabulares siguen resolviéndose sobre todo con aprendizaje supervisado clásico, mientras que el auge de la inteligencia artificial generativa ha situado el aprendizaje autosupervisado y el refuerzo en el centro de la investigación y de los productos más visibles.

| Tipo | Datos | Objetivo | Usos habituales |
|---|---|---|---|
| Supervisado | Etiquetados | Predecir una salida conocida | Diagnóstico, fraude, precios, reconocimiento de imágenes |
| No supervisado | Sin etiquetar | Descubrir estructura | Segmentación de clientes, anomalías, compresión |
| Semisupervisado / autosupervisado | Pocos etiquetados o etiquetas generadas | Aprovechar grandes volúmenes de datos | Modelos de lenguaje, visión, voz |
| Por refuerzo | Interacción con un entorno | Maximizar una recompensa | Robótica, juegos, control, alineación de modelos |

*Tabla 1. Comparativa de los tipos de aprendizaje automático. Elaboración propia.*

## 4. Estado actual y tendencias de las herramientas

### 4.1. Técnicas y herramientas

Entre las **técnicas** más empleadas se encuentran la regresión lineal y logística, los árboles de decisión y los métodos de conjunto (*random forest*, *gradient boosting*), las máquinas de vectores de soporte, *k-means* y PCA, las redes neuronales profundas (convolucionales, recurrentes y, sobre todo, *transformers*) y los algoritmos de refuerzo como Q-learning o PPO.

En cuanto a las **herramientas**, *scikit-learn* continúa siendo la referencia para el aprendizaje automático clásico y los modelos base sobre datos estructurados. Para aprendizaje profundo dominan *PyTorch* y *TensorFlow*, este último con *Keras*, que en su versión 3 es multiempleado sobre TensorFlow, PyTorch o JAX. *Hugging Face Transformers* se ha consolidado como el repositorio estándar de modelos preentrenados. Para datos tabulares se utilizan *XGBoost*, *LightGBM* y *CatBoost*, y para aceleración con GPU bibliotecas como NVIDIA cuML, con una API similar a la de scikit-learn. En refuerzo destacan *Gymnasium* y *Stable-Baselines3*.

Alrededor de los marcos de modelado ha crecido un ecosistema de **plataformas de AutoML y MLOps**: Google Vertex AI, Azure Machine Learning, Amazon SageMaker, H2O.ai y DataRobot en la nube y en el ámbito empresarial, y *MLflow*, *Kubeflow*, *DVC* o *Weights & Biases* para el seguimiento de experimentos, el versionado y el despliegue.

### 4.2. Asociación de técnicas y herramientas a cada tipo

| Tipo | Técnicas representativas | Herramientas |
|---|---|---|
| Supervisado | Regresión, árboles, *random forest*, boosting, SVM, redes neuronales | scikit-learn, XGBoost, LightGBM, CatBoost, Keras, PyTorch |
| No supervisado | K-means, clustering jerárquico, DBSCAN, PCA, autoencoders, Isolation Forest | scikit-learn, cuML, PyTorch, TensorFlow |
| Semisupervisado / autosupervisado | Preentrenamiento con *transformers*, aprendizaje contrastivo, ajuste fino | Hugging Face Transformers, PyTorch, JAX, TensorFlow |
| Por refuerzo | Q-learning, DQN, gradiente de política, PPO, RLHF | Gymnasium, Stable-Baselines3, Ray RLlib, PyTorch |
| Transversal (todos) | AutoML, seguimiento de experimentos, despliegue y monitorización | MLflow, Kubeflow, DVC, W&B, Vertex AI, Azure ML, SageMaker |

*Tabla 2. Técnicas y herramientas asociadas a cada tipo. Elaboración propia.*

### 4.3. Tendencias

Las fuentes consultadas coinciden en que PyTorch y TensorFlow siguen siendo estándares de la industria, pero los flujos de trabajo actuales priorizan la automatización, la reproducibilidad y la preparación para producción. Las tendencias más relevantes son:

- **MLOps como disciplina central.** Herramientas como MLflow se consideran casi imprescindibles para gestionar el ciclo de vida de los modelos, y el mercado de MLOps crece a gran velocidad, con atención creciente al control de costes (FinOps) y a los cumplimientos regulatorios como el Reglamento europeo de IA.
- **AutoML y automatización.** Plataformas como Vertex AI o DataRobot reducen el trabajo manual de selección de modelos y ajuste de hiperparámetros, democratizando el acceso al ML.
- **Modelos preentrenados e IA generativa.** En lugar de entrenar desde cero, es habitual reutilizar modelos de Hugging Face y adaptarlos mediante ajuste fino, junto con marcos como LangChain para construir aplicaciones y agentes.
- **Aceleración y portabilidad.** El uso de GPU en bibliotecas clásicas y los marcos multiempleado como Keras 3 reducen la dependencia de un único ecosistema.

## 5. Conclusiones

El aprendizaje automático se apoya en principios estables (datos, modelo, optimización y generalización) que se aplican a cuatro grandes familias de sistemas: supervisado, no supervisado, semi/autosupervisado y por refuerzo. Cada una responde a un tipo de problema distinto, y elegir bien depende de si se dispone de datos etiquetados y de cuál es el objetivo.

En el plano de las herramientas, scikit-learn sigue siendo imprescindible para el ML clásico, PyTorch y TensorFlow/Keras para el aprendizaje profundo, y Hugging Face para modelos preentrenados, mientras que MLOps y AutoML han pasado de ser un complemento a una parte esencial de cualquier proyecto real. Mi conclusión es que el valor ya no está solo en entrenar un buen modelo, sino en llevarlo a producción de forma reproducible, mantenible y responsable. Por eso conviene dominar tanto las bases teóricas como el ecosistema de herramientas que las rodea.

## 6. Bibliografía y webgrafía

- Atlantic.Net (2026). *8 of the Most Popular Machine Learning Tools in 2026*. https://www.atlantic.net/gpu-server-hosting/8-of-the-most-popular-machine-learning-tools/ (consultado el 29/10/2026).
- Codebasics (2026). *Top Data Science Tools in 2026 – What You Should Learn*. https://codebasics.io/blog/top-data-science-tools-in-2026-what-you-should-learn (consultado el 29/10/2026).
- DEV Community (2026). *Mastering Machine Learning in 2026: Frameworks, Models, and Trends*. https://dev.to/sahil_waykar/mastering-machine-learning-in-2026-frameworks-models-and-trends-4ici (consultado el 29/10/2026).
- Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow* (3.ª ed.). O'Reilly Media.
- Goodfellow, I., Bengio, Y. y Courville, A. (2016). *Deep Learning*. MIT Press.
- Hugging Face. *Documentación de Transformers*. https://huggingface.co/docs/transformers (consultado el 29/10/2026).
- KodeKloud (2026). *Top MLOps Tools in 2026*. https://kodekloud.com/blog/top-mlops-tools/ (consultado el 29/10/2026).
- MLflow. *Documentación oficial*. https://mlflow.org/docs/latest/ (consultado el 29/10/2026).
- PyTorch. *Documentación oficial*. https://pytorch.org/ (consultado el 29/10/2026).
- scikit-learn. *User Guide*. https://scikit-learn.org/stable/user_guide.html (consultado el 29/10/2026).
- Sutton, R. S. y Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2.ª ed.). MIT Press.
- TensorFlow y Keras. *Documentación oficial*. https://www.tensorflow.org/ y https://keras.io/ (consultado el 29/10/2026).
