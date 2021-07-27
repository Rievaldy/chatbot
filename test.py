import re 
import numpy 
import pickle

import nltk
from helper_func import *
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

stemmer = SnowballStemmer('english')
stopword =  set(stopwords.words('english'))
sentence = "Help, I have trouble with my application. I need maintenance immedietly"
sentence = word_tokenize(sentence)
stemsentence = [stemmer.stem(word) for word in sentence ]

print(sentence)
print("stem=",stemsentence)