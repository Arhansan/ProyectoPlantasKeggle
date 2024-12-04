import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.preprocessing import image_dataset_from_directory  # Importar la función para cargar el dataset

# Ruta a tu directorio de imágenes (usar string raw o dobles backslashes)
data_dir = r"C:\Users\52834\AppData\Local\Programs\Python\Python310\ProyectoPlantas\fotosplantas"

# Parámetros del dataset
batch_size = 32
img_size = (224, 224)

# Crear el conjunto de datos de entrenamiento
train_dataset = image_dataset_from_directory(
    data_dir,
    validation_split=0.2,   # Separar el 20% para validación
    subset="training",      # Subconjunto de entrenamiento
    seed=123,               # Semilla para mezclar los datos aleatoriamente
    image_size=img_size,    # Tamaño de las imágenes (redimensionarlas a 224x224)
    batch_size=batch_size   # Número de imágenes por batch
)

# Crear el conjunto de datos de validación
validation_dataset = image_dataset_from_directory(
    data_dir,
    validation_split=0.2,   # Separar el 20% para validación
    subset="validation",    # Subconjunto de validación
    seed=123,               # Semilla para mezclar los datos aleatoriamente
    image_size=img_size,    # Tamaño de las imágenes (redimensionarlas a 224x224)
    batch_size=batch_size   # Número de imágenes por batch
)

# Normalizar los valores de los píxeles (entre 0 y 1)
normalization_layer = tf.keras.layers.Rescaling(1./255)

# Aplicar la normalización al conjunto de entrenamiento
normalized_train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y))

# Aplicar la normalización al conjunto de validación
normalized_validation_dataset = validation_dataset.map(lambda x, y: (normalization_layer(x), y))

# Verifica las clases del dataset
class_names = train_dataset.class_names
print("Clases encontradas:", class_names)

# Definir el modelo CNN
model = Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(class_names), activation='softmax')
])

# Compilar el modelo
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])

# Entrenar el modelo
history = model.fit(
    normalized_train_dataset,
    validation_data=normalized_validation_dataset,
    epochs=10
)

# Graficar la precisión del modelo
import matplotlib.pyplot as plt

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

epochs_range = range(10)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Entrenamiento')
plt.plot(epochs_range, val_acc, label='Validación')
plt.legend(loc='lower right')
plt.title('Precisión del Entrenamiento y Validación')

# Graficar la pérdida del modelo
loss = history.history['loss']
val_loss = history.history['val_loss']

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Entrenamiento')
plt.plot(epochs_range, val_loss, label='Validación')
plt.legend(loc='upper right')
plt.title('Pérdida del Entrenamiento y Validación')
plt.show()

# Guardar el modelo en formato .h5
model.save(r'C:\Users\52834\AppData\Local\Programs\Python\Python310\ProyectoPlantas\mi_modelo.h5')
