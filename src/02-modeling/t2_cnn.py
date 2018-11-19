"""
Author: Alex Hamilton - https://github.com/alexhamiltonRN
Created: 2018-11-18
Description: CNN training using t2 images from ProstateX challenge. 
"""

import keras
from keras import layers
from keras import models

import numpy as np
from pathlib import Path

# Loading the data
t2_samples = np.load('/home/alexander/Documents/DataProjects/Data/MBI/ProstateX/generated/train/numpy/t2/X_train.npy')
t2_labels = np.load('/home/alexander/Documents/DataProjects/Data/MBI/ProstateX/generated/train/numpy/t2/Y_train.npy')

# Convert image samples to float32
t2_samples_flt32 = np.array(t2_samples, dtype=np.float32, copy = True)

# Reshape image samples to include single channel
x_train = t2_samples_flt32.reshape((620,32,32,1))

y_train = t2_labels

# MODEL SPECIFICATION
model = models.Sequential()

model.add(layers.Conv2D(32, kernel_size=(3,3), padding = 'same', activation='relu', input_shape=(32,32,1))) 
model.add(layers.Conv2D(32, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Dropout(0.25))

model.add(layers.Conv2D(64, (3,3), padding = 'same', activation='relu'))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Dropout(0.25))

model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dropout(0.5))

model.add(layers.Dense(1, activation='sigmoid'))
model.summary()

# COMPILATION

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# FIT
model.fit(x_train, y_train, epochs=10, validation_split=0.25, batch_size=32, shuffle=True)

#TODO: Implement csv logger - see KERAS documentation