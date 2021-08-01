import re
import nltk

from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

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
    stemmer = StemmerFactory().create_stemmer()
    stop_word = set(stopwords.words('indonesian'))
    maxlength_sentence = 11
    max = 0

    for intent in intents['intents'] :
        for pattern in intent['patterns'] :       
            word_list = nltk.word_tokenize(pattern)
            word_list = [stemmer.stem(word) for word in word_list if word not in ignore_latters if word not in stop_word]
            if len(word_list) > 0 :
                word_list = pad_sequences(maxlength_sentence,word_list)
                max = len(word_list) if len(word_list) > max else max
                words.extend(word_list)
                documents.append((word_list, intent['tag']))
            if intent['tag'] not in labels :
                labels.append(intent['tag'])
    print("Panjang Karakter maximum  =" , max)

    return documents,labels,words
