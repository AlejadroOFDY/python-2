# TP1 - Redes Neuronales Básicas con Keras

Este trabajo práctico introduce los conceptos básicos de redes neuronales utilizando Keras y el dataset Fashion MNIST.

## Objetivo

Construir un modelo de clasificación multiclase capaz de reconocer 10 tipos de prendas:

- Camiseta
- Pantalón
- Pulóver
- Vestido
- Abrigo
- Sandalia
- Camisa
- Zapatilla
- Bolso
- Botín

## Dataset

Se usa Fashion MNIST, un conjunto de imágenes en escala de grises de 28x28 píxeles.

- Entrenamiento: 60.000 imágenes
- Prueba: 10.000 imágenes
- Cada imagen tiene tamaño 28x28
- Cada etiqueta corresponde a una de 10 clases

## Preparación de los datos

Antes de entrenar la red, los valores de los píxeles se normalizan al rango [0, 1] dividiendo por 255. Esto hace que el entrenamiento sea más estable y eficiente.

## Modelo propuesto

Se crea un modelo secuencial con:

- una capa de entrada según el tamaño de la imagen
- una capa Flatten para convertir la imagen 2D en una sola dimensión
- dos o más capas densas con activación ReLU
- una capa de salida con 10 neuronas y activación softmax

La activación softmax es necesaria porque se trata de un problema de clasificación multiclase.

## Compilación del modelo

El modelo se compila con:

- Optimizer: Adam
- Loss: Sparse Categorical Crossentropy
- Métrica: Accuracy

## Entrenamiento

Se entrena el modelo durante varias épocas usando el conjunto de entrenamiento. El objetivo es minimizar la pérdida y aumentar la precisión.

## Evaluación

Posteriormente, se evalúa el modelo con el conjunto de prueba para medir su rendimiento real.

Se observa:

- la pérdida del modelo
- la precisión (accuracy)

## Visualización de resultados

Se muestran imágenes del conjunto de prueba junto con:

- la etiqueta real
- la etiqueta predicha
- el porcentaje de confianza de la predicción

Esto permite interpretar visualmente si el modelo está realizando buenas clasificaciones.

## Ajuste del learning rate

Se prueba un learning rate distinto al valor por defecto de Adam para comparar si el rendimiento mejora o empeora. Esto ayuda a comprender cómo influyen los hiperparámetros en la optimización del modelo.

## TensorBoard

Como ejercicio extra, se usa TensorBoard para graficar la pérdida y la precisión a lo largo de las épocas. Esto permite visualizar cómo evoluciona el entrenamiento y detectar si el modelo deja de mejorar.

## Conclusión

Este TP introduce el flujo completo de un problema de clasificación con redes neuronales:

1. cargar y preparar datos
2. definir una red neuronal
3. compilarla
4. entrenarla
5. evaluarla
6. interpretar los resultados

Es una introducción práctica y clara al uso de Keras para deep learning.
