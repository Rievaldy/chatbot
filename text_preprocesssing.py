import re
import nltk

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from chatbotapi.data_model.db_func.db_brand_func import *

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

def pad_sequences(maxlength, phrase):
    phrase_for_padded = "--$$--"

    if len(phrase) < maxlength : 
            added_count = maxlength - len(phrase)
            phrase_dump = [phrase_for_padded] * added_count
            phrase.extend(phrase_dump)
    return phrase


def splitdata(intents) :
    words = []
    labels = []
    documents = []
    ignore_latters = ['?','!','.',',']
    stemmer = SnowballStemmer('english')
    stop_word = set(stopwords.words('english'))
    maxlength_sentence = 11

    for intent in intents['intents'] :
        for pattern in intent['patterns'] :       
            pattern = decontracted(pattern)
            word_list = nltk.word_tokenize(pattern)
            word_list = [stemmer.stem(word) for word in word_list if word not in ignore_latters if word not in stop_word]
            if len(word_list) > 0 :
                word_list = pad_sequences(maxlength_sentence,word_list)
                words.extend(word_list)
                documents.append((word_list, intent['tag']))
            if intent['tag'] not in labels :
                labels.append(intent['tag'])

    return documents,labels,words
