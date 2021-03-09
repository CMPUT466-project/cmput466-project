import numpy as np
import string
import os

from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
from keras.utils import np_utils


sep = os.path.sep
current = os.getcwd()
version ="4"
seq_length = 19
categories = [str(i+version) for i in ["business", "entertainment", "politics", "sport","tech"]]
path_list = [str(current + sep 
                         + "without_stop_word_usable_data" 
                         + sep 
                         + category
                         + sep) for category in categories]
use = 0
trainX_path = path_list[use] + "trainingX.txt"
trainY_path = path_list[use] + "trainingY.txt"
testX_path = path_list[use] + "testX.txt"
testY_path = path_list[use] + "testY.txt"
word_set_path = path_list[use] + "word_set.txt"

trainX_list = []
trainY_list = []
testX_list = []
testY_list = []
word_set = []

# A dictionary for all appeared words in our dataset. 
# Key is word, value is the unique index in the dict.
char_to_int_dict = {} 
# A dictionary for all appeared words in our dataset. 
# Key is the unique index in the dict, value is word.
int_to_char_dict = {}

# Read in word set data.
with open(word_set_path) as obj:
    word_set = sorted(obj.read().splitlines())
    char_to_int_dict = dict((word, index) for index, word in enumerate(word_set))
    int_to_char_dict = dict((index, word) for index, word in enumerate(word_set))

with open(trainX_path) as obj:
    lines = obj.read().splitlines()
    for row in lines:
        words_in_row = row.split(' ')
        trainX_list.append([char_to_int_dict[word] for word in words_in_row])

with open(trainY_path) as obj2:
    trainY_list = [char_to_int_dict[i] for i in obj2.read().splitlines()]

with open(testY_path) as obj2:
    testY_list = [char_to_int_dict[i] for i in obj2.read().splitlines()]

with open(testX_path) as obj:
    lines = obj.read().splitlines()
    for row in lines:
        words_in_row = row.split(' ')
        testX_list.append([char_to_int_dict[word] for word in words_in_row])


number_of_training_data = len(trainX_list)


X = np.reshape(trainX_list, (number_of_training_data, seq_length, 1))
X = X / float(len(word_set))
#y = np.reshape(trainY_list, (len(trainY_list),1))
y = np_utils.to_categorical(trainY_list,num_classes=len(word_set))
print(X.shape)#(99943, 6, 1)  (5840, 29, 1)
#print(y.shape)#(99943, 11862) (5840, 6006)
model = Sequential()
model.add(LSTM(512, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(512))
model.add(Dropout(0.2))

model.add(Dense(y.shape[1], activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
file_path = "cache_weights.hdf5"
checkpoint = ModelCheckpoint(file_path, 
                             monitor='loss', 
                             verbose=1,
                             save_best_only=True,
                             mode='min')
callbacks_list = [checkpoint]

testX = np.reshape(testX_list, (len(testX_list),seq_length,1))
testY = np_utils.to_categorical(testY_list,num_classes=len(word_set))
print("testX shape",testX.shape)
print("testY shape",testY.shape)
model.fit(X,y, epochs=500, batch_size=64, callbacks=callbacks_list)
model.evaluate(testX, y = testY, batch_size=64, verbose=1)
