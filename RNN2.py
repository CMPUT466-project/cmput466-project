import numpy as np
import string
import os
import re
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Dropout, LSTM, Input, Embedding,GRU
from keras.models import Sequential
from keras.utils import np_utils
from keras.layers.normalization import BatchNormalization
from keras.layers import Activation
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
import time
from tensorflow.keras.preprocessing.sequence import pad_sequences


Train = True
cache_file_name = 'rnn_weights_20.h5'
sep = os.path.sep
current = os.getcwd()
path_with_stopwords = "/processed_datasets/proced_News_Articles"
path1 = current+path_with_stopwords+sep+"business"
maxlen = 20
sentences = []

all_files_with_stopwords = [str(path1+sep+relative) for relative in sorted(os.listdir(path1))]
for each_file_path in all_files_with_stopwords:
    with open(each_file_path) as obj:
        text = obj.read()
        processed = re.sub(r'[^\x00-\x7f]', r'', text).split("\n") # a list of lines
        for each_line in processed:
            
            split_line = [i for i in each_line.split(" ") if i]
            length = len(split_line)
            if length >= maxlen: 
                for each_word_index in range(length-maxlen+1):
                    seq = split_line[each_word_index:each_word_index+maxlen]
                    line = " ".join(seq)
                    sentences.append(line)           


tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
sequences = np.array(tokenizer.texts_to_sequences(sentences))
X, y = sequences[:, :-1], sequences[:, -1]

vocab_size = len(tokenizer.word_index) + 1


y = to_categorical(y, num_classes = vocab_size)
model = Sequential()


model.add(Embedding(vocab_size, 256))
model.add(LSTM(1024))
model.add(Dropout(0.2))
model.add(Dense(1024, activation='relu'))
model.add(Dense(vocab_size, activation='softmax'))

if os.path.isfile(current + sep + cache_file_name):
    model.load_weights(cache_file_name)

model.summary()
model.compile(loss = 'categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

if Train:
  checkpoint = ModelCheckpoint(cache_file_name, 
                             monitor='loss', 
                             verbose=1,
                             save_best_only=True,
                             mode='min')
  callbacks_list = [checkpoint]
  model.fit(X,y, batch_size=256, epochs=20, callbacks=callbacks_list)
  model.save_weights(cache_file_name)

seed_text = 'I am'


def generate_text(model, tokenizer, text_seq_len, seed_text, n_words):
  text = []
  word_distribution = []

  for _ in range(n_words):
    encoded = tokenizer.texts_to_sequences([seed_text])[0]
    encoded = pad_sequences([encoded], maxlen = text_seq_len, truncating='pre')

    temp = model.predict(encoded)

    y_predict = np.argmax(temp, axis=-1)
    word_list = []
    max_index = y_predict
    for x in range(text_seq_len):
      temp[0][max_index] = -1
      max_index = np.argmax(temp, axis=-1)
      word_list.append(max_index)

    predicted_word = ''
    temp = model.predict(encoded)

    for word, index in tokenizer.word_index.items():
      if index == y_predict:
        predicted_word = word
        break
    seed_text = seed_text + ' ' + predicted_word
    text.append(predicted_word)

    distribution = [(predicted_word, temp[0][y_predict][0])]
    for predicted in word_list:
      predicted_word = ''
      for word, index in tokenizer.word_index.items():
        if index == predicted:
          predicted_word = word
          break
      distribution.append((predicted_word, temp[0][predicted][0]))
    word_distribution.append(distribution)

  return ' '.join(text), word_distribution

text, distribution = generate_text(model, tokenizer, 6, seed_text, 20)

print(text)
for iteration in distribution:
  print("+++++++++++++++++")
  for word in iteration:
    print(word[0],":",word[1])