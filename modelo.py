import tensorflow as tf
from tensorflow.keras import layers, models

# Definir el modelo CNN
model = models.Sequential([
    # Capa convolucional + capa de pooling
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    
    # Segunda capa convolucional + pooling
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    
    # Tercera capa convolucional + pooling
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),

    # Aplanar la salida para las capas densas
    layers.Flatten(),
    
    # Capa densa completamente conectada
    layers.Dense(128, activation='relu'),

    # Capa de salida (softmax para clasificación multiclase)
    layers.Dense(len(train_dataset.class_names), activation='softmax')
])

# Compilar el modelo
model.compile(optimizer='adam',               # Optimizador Adam
              loss='sparse_categorical_crossentropy',  # Pérdida para clasificación de etiquetas enteras
              metrics=['accuracy'])            # Métrica de precisión
# Entrenar el modelo
history = model.fit(
    normalized_train_dataset,     # Conjunto de entrenamiento
    validation_data=normalized_validation_dataset,  # Conjunto de validación
    epochs=10                     # Número de épocas
)
