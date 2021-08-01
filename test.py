from corebot import *
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

words = []
labels = []
documents = []
ignore_latters = ['?','!','.',',']
stemmer = StemmerFactory().create_stemmer()
stop_word = set(stopwords.words('indonesian'))
maxlength_sentence = 11
ignore_word_on_stopword = ['tidak','saya','anda']
stop_word_new = [word for word in stop_word if word not in ignore_word_on_stopword]

sentence = "Minta tolong dong, aplikasi diperusahaan saya sepertinya butuh perbaikan !"

tokenize_sent = nltk.word_tokenize(sentence)

result = [stemmer.stem(word) for word in tokenize_sent if word not in ignore_latters ]
result = [word for word in result if word not in stop_word_new]
#result = pad_sequences(11,result)

#print(stop_word)
#print(predict_classes("rincian tentang tidak produknya ini"))

print(result)

#print([stemmer.stem(word) for word in nltk.word_tokenize("setidak-tidaknya setidaknya tidak tidaklah") if word not in ignore_latters])
