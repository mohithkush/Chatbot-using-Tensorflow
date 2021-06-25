import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
import tflearn

lemmatizer = WordNetLemmatizer()

#Load your own data in JSON Format
intents = json.loads(open('Yourowndata.json').read())

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

words = [lemmatizer.lemmatize(word) for word in words   if word not in ignore_letters]

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

train_x = list(training[:, 0])
train_y = list(training[:, 1])
#print('Inputs are Ready')

net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

model.fit(train_x, train_y, n_epoch=300, batch_size=5, show_metric=['accuracy'])
model.save('model.tflearn')