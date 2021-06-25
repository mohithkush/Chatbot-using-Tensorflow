import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import pickle
import numpy as np
from training import model
import json
import random

with open('Yourowndata.json') as json_data:
    intents = json.load(json_data)
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model.load('./model.tflearn')

def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words, show_details = True):
  sentence_words = clean_up_sentence(sentence)
  bag = [0] * len(words)
  for s in sentence_words:
    for i, word in enumerate(words):
      if word == s:
        bag[i] = 1
        if show_details:
          print("found in bag : %s" % word)
  return (np.array(bag))


def predict_class(sentence):
  p = bag_of_words(sentence, words, show_details= False)
  res = model.predict(np.array([p]))[0]
  ERROR_THRESHOLD = 0.25
  results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
  results.sort(key = lambda x : x[1], reverse = True)
  return_list = []
  for r in results:
    return_list.append({"intent" : classes[r[0]], "probability" : str(r[1])})
  return return_list

def get_response(intenst_list, intents_json):
    tag = intenst_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


while True:
  message = input('User : ')
  ints = predict_class(message)
  res = get_response(ints, intents)
  print('chatbot : ',res)