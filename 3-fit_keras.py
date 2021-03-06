from __future__ import print_function
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file
from keras.regularizers import l2, activity_l2
from keras.utils.np_utils import to_categorical

import numpy as np
import pandas as pd
import random
import sys
import itertools


# ETL code to lines -----------------------------------------------------------
np.random.seed(1234)
train_frac = 0.7

hands = pd.DataFrame.from_csv('data/2yrs.csv')
hands = np.array(hands, dtype = int)
X = hands[:,1:]
y = hands[:,0]
y_binary = to_categorical(y)

train_rows = np.random.uniform(0, 1, len(X))

train_X = X[train_rows <= train_frac]
train_y = y_binary[train_rows <= train_frac]

test_X = X[train_rows > train_frac]
test_y = y_binary[train_rows > train_frac]

# Standardize
test_X = (test_X - np.mean(test_X, axis=0)) / np.std(test_X, axis=0)
train_X = (train_X - np.mean(train_X, axis=0)) / np.std(train_X, axis=0)

# Build model -----------------------------------------------------------------
model = Sequential()
model.add(Dense(216, input_shape=(51,)))
model.add(Activation('tanh'))
model.add(Dropout(0.05))
model.add(Dense(216))
model.add(Activation('tanh'))
model.add(Dropout(0.05))
model.add(Dense(128))
model.add(Activation('tanh'))
model.add(Dropout(0.05))
model.add(Dense(34))
model.add(Activation('softmax'))

# model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
sgd = keras.optimizers.SGD(lr=0.005, momentum=0.005)
# rmsprop = keras.optimizers.rmsprop(lr = 0.005)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

model.fit(train_X, train_y,
          batch_size=196,
          nb_epoch=500,
          validation_split = 0.25)

model.evaluate(test_X, test_y)
# ~2.4875 old data
# ~2.449   196/196. 0.005/0.005

p = model.predict(test_X)

# Save the model --------------------------------------------------------------
json_string = model.to_json()
open('models/keras_architecture.json', 'w').write(json_string)
model.save_weights('models/keras_weights.h5')

# elsewhere...
# model = model_from_json(open('my_model_architecture.json').read())
# model.load_weights('my_model_weights.h5')


# A good model.
# model = Sequential()
# model.add(Dense(196, input_shape=(51,)))
# model.add(Activation('tanh'))
# model.add(Dropout(0.05))
# model.add(Dense(196))
# model.add(Activation('tanh'))
# model.add(Dropout(0.05))
# model.add(Activation('tanh'))
# model.add(Dense(34))
# model.add(Activation('softmax'))
# sgd = keras.optimizers.SGD(lr=0.005, momentum=0.005)
# model.compile(loss='categorical_crossentropy', optimizer=sgd)
