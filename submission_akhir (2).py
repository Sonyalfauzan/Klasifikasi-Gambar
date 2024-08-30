# -*- coding: utf-8 -*-
"""Submission Akhir.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RWLOUUDpqmiGVBfOwzr8olSLAZGdpoD7

# Proyek Klasifikasi Gambar: Melanoma Skin Cancer
- **Nama:** Sony Alfauzan
- **Email:** sonyalfauzan46@gmail.com
- **ID Dicoding:** sonyalfauzan

https://www.kaggle.com/datasets/hasnainjaved/melanoma-skin-cancer-dataset-of-10000-images

## Import Semua Packages/Library yang Digunakan
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

"""### Data Loading"""

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Path to the dataset directory in your Google Drive
dataset_dir = '/content/drive/MyDrive/Proyek Klasifikasi Gambar/melanoma_cancer_dataset'

"""Data augmentation"""

datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = datagen.flow_from_directory(
    '/content/drive/MyDrive/Proyek Klasifikasi Gambar/melanoma_cancer_dataset', # Replace with the actual path to your dataset
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    '/content/drive/MyDrive/Proyek Klasifikasi Gambar/melanoma_cancer_dataset', # Replace with the actual path to your dataset
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

"""Build CNN model"""

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # Ubah jumlah neuron output menjadi 1 dan aktivasi menjadi 'sigmoid'

"""Compile model"""

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

"""Train model"""

history = model.fit(train_generator, epochs=10, validation_data=validation_generator)

"""Plot accuracy and loss"""

import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.legend()
plt.show()

"""Save model in different formats"""

# Simpan model dalam format SavedModel
model.save('/content/drive/MyDrive/Proyek Klasifikasi Gambar/my_model.h5')

# Simpan model dalam format TF-Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open('/content/drive/MyDrive/Proyek Klasifikasi Gambar/my_model.tflite', 'wb') as f:
    f.write(tflite_model)

# Simpan model dalam format TFJS
!pip install tensorflowjs
import tensorflowjs as tfjs
tfjs.converters.save_keras_model(model, '/content/drive/MyDrive/Proyek Klasifikasi Gambar/tfjs_model')

!pip freeze>requirements.txt