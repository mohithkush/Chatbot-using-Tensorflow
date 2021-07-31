import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from tensorflow.keras.optimizers import SGD


lemmatizer = WordNetLemmatizer()

intents = json.loads(open('dataset.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?','!',',','.']
for intent in intents['intents']:
    for pattern in intent['patterns']:
        Word_list = nltk.word_tokenize(pattern)
        words.extend(Word_list)
        documents.append((Word_list ,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
words = [lemmatizer.lemmatize(word) for word in words  if word not in ignore_letters]

words = sorted(set(words))

classes = sorted(set(classes))


pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        if word in word_patterns:
            bag.append(1)
        else:
            bag.append(0)
            
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1

    training.append([bag, output_row])


random.shuffle(training)
training = np.array(training)

train_x  = list(training[ :,0])
train_y = list(training[: , 1])


print("Input is ready")

model = Sequential()
model.add(Dense(128, input_shape = (len(train_x[0]),),activation = 'relu'))
model.add(Dropout(0.5))
model.add((Dense(64, activation='relu')))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation= 'softmax'))

sgd = SGD(learning_rate=0.01, decay = 1e-06, momentum = 0.9, nesterov = True)
model.compile(loss = 'categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs = 300, batch_size = 5, validation_data = (train_x, train_y))
model.save('chatmodel.h5')

print('Model is trained')

from matplotlib import pyplot as plt
N = 300

plt.style.use("classic")
plt.figure()
plt.plot(np.arange(0, N), hist.history["loss"], label = "train_loss")
plt.plot(np.arange(0, N), hist.history["val_loss"], label = "val_loss")
plt.plot(np.arange(0, N), hist.history["accuracy"], label = "train_acc")
plt.plot(np.arange(0, N), hist.history["val_accuracy"], label = "val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Loss/Accuracy")
plt.legend(loc = "upper right")
plt.show()