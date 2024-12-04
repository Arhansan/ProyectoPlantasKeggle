import tensorflow as tf

# Suponiendo que ya has entrenado tu modelo, lo cargas aquí
# Si ya has guardado tu modelo después del entrenamiento:
model = tf.keras.models.load_model('C:/Users/52834/AppData/Local/Programs/Python/Python310/ProyectoPlantas/mi_modelo.h5')

# Convertir el modelo a TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Guardar el modelo convertido
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

print("Modelo convertido y guardado como model.tflite")
