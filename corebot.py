import re
from action_process import *
from text_preprocesssing import pad_sequences
import numpy as np
import pickle as pkl
import json
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from lstm_func import *

intents = json.load(open('chatbot\\test_siemese_network\\intents.json'))
saved_embeddings  = pkl.load(open('embeddings.pkl','rb'))
saved_parameters  = pkl.load(open('parameters.pkl','rb'))
saved_id_word  = pkl.load(open('id_word.pkl','rb'))
saved_word_id  = pkl.load(open('word_id.pkl','rb'))
saved_id_label  = pkl.load(open('id_label.pkl','rb'))
saved_label_id  = pkl.load(open('label_id.pkl','rb'))
ignore_latters = ['?','!','.',',']
stop_word = set(stopwords.words('english'))



def hotEncodeMessage(message):
    stemmer = SnowballStemmer('english')
    messageEncoded = []

    words = word_tokenize(message)
    words = [stemmer.stem(word) for word in words if word not in ignore_latters if word not in stop_word ]
    words = [word for word in words if word in saved_word_id.keys()]
    words = pad_sequences(11,words)
    print(words)
    #hot encode
    for i in range(len(words)):
        hotEncodedWord = np.zeros((1, len(saved_id_word)))
        word_index = saved_word_id[words[i]]
        hotEncodedWord[0,word_index] = 1.0
        messageEncoded.append(hotEncodedWord)

    return messageEncoded

def findPrediction(predictions_accuracy):
    labelIndex = 0
    closest_labelIndex = []
    max = 0

    for i in range(len(predictions_accuracy)) :
        for j in range(len(predictions_accuracy[0][0])):
            if predictions_accuracy[i][0][j] > max : 
                max = predictions_accuracy[i][0][j]
                index = j
                labelIndex = index

    if max <= 75 :
        for i in range(len(predictions_accuracy)) :
            for j in range(len(predictions_accuracy[0][0])):
                if predictions_accuracy[i][0][j] > (max-10) and j != labelIndex : 
                    index = j
                    closest_labelIndex.append(index)

    return labelIndex,closest_labelIndex

def lookOnSpecificTag(tag_name):
    response = ""
    desc = ""
    context = ""
    action = ""
    permission = ""
    for intent in intents['intents']:
        if intent['tag'] == tag_name :
            response = intent['responses']
            desc = intent['desc']
            permission = intent['permission']
            action = intent['action']
            context = intent['context']
    return response, desc, permission, action,context

def predict_classes(message):
    predict = []
    predicted_label = ""

    hotEncodedMessage = hotEncodeMessage(message)

    a0 = np.zeros([1,256],dtype=np.float32)
    c0 = np.zeros([1,256],dtype=np.float32)

    if hotEncodedMessage[0][0][0] == 1.0 : return None
    for i in range(len(hotEncodedMessage)) :
        if hotEncodedMessage[i][0][0] != 1.0 :
            embedding = get_embeddings(hotEncodedMessage[i], saved_embeddings)
            #lstm cell
            lstm_activations, ct, at = lstm_cell(embedding,a0,c0,saved_parameters)
            ot = output_cell(at,saved_parameters)
            a0 = at
            c0 = ct
        else :
            predict.append(ot)
            break
            
    predict = np.multiply(np.round(predict,2),100)

    #print(np.asarray(predict).shape)
    for i in range(len(predict[0][0])):
        print(saved_id_label[i], " : ", predict[0][0][i], "% confidence")


    #predict highest prediction
    predict_index_label,closest_index_labels = findPrediction(predict)
    print(predict_index_label)
    print(closest_index_labels)
    predicted_label = []
    predicted_label.append(saved_id_label[predict_index_label])

    if len(closest_index_labels) != 0 :
        for i in range(len(closest_index_labels)):
            predicted_label.append(saved_id_label[closest_index_labels[i]])

    return predicted_label

