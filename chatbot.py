import json
import re
import numpy as np
import random
import matplotlib.pyplot as plt  #for visualization
import nltk
import pickle as pkl

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from chatbotapi.data_model.db_func.db_brand_func import *
from chatbotapi.data_model.db_func.db_service_func import *
from lstm_func import *
from text_preprocesssing import *

intents = json.load(open('chatbot\\test_siemese_network\\intents.json'))
words = []
labels = []
documents = []
maxlength_sentence = 11

documents,labels,words = splitdata(intents)


words = sorted(set(words))
#words = [stemmer.stem(word) for word in words if word not in ignore_latters if word not in stop_word]

labels = sorted(set(labels))
vocab_size_word = len(words)
vocab_size_label = len(labels)

word_id = dict()
id_word = dict()

label_id = dict()
id_label = dict()

for i in range(vocab_size_word):
    id_word[i] = words[i]
    word_id[words[i]] = i


for i in range(vocab_size_label):
    id_label[i] = labels[i]
    label_id[labels[i]] = i

def translate_data(batch_data) :
    for data in batch_data :
        for sentence in data :
            for word in sentence:
                for i in range(len(word)):
                    if word[i] == 1.0 :
                        print(id_word[i])

batch_size = 5
x_data= []
y_data=[]
y_sample=[]
print(len(y_sample))

random.shuffle(documents)
print(documents)

for i in range(len(documents) - batch_size+1):
    start = i*batch_size
    end = start+batch_size


    batch_data = documents[start:end]

    if(len(batch_data)!=batch_size):
        break
    

    sentence_encoded = []
    #convert each word of each sentence of batch data into one hot encoding
    for j in range(maxlength_sentence) :
        template_word_encoded = np.zeros([batch_size,vocab_size_word])
        for k in range(batch_size):
            word = batch_data[k][0][j]
            index_word = word_id[word]
            template_word_encoded[k,index_word] = 1.0
        sentence_encoded.append(template_word_encoded)
    x_data.append(sentence_encoded)

    #convert each label of each sentence of batch data into one hot encoding
    template_label_encoded = np.zeros([batch_size,vocab_size_label])
    for j in range(batch_size) :
        label = batch_data[j][1]
        index_label = label_id[label]
        y_sample.append(index_label)
        template_label_encoded[j,index_label] = 1.0
    y_data.append(template_label_encoded)
    


print(np.asarray(y_data).shape)
#number of input units or embedding size
input_units = 100

#number of hidden neurons
hidden_units = 256

#number of output units i.e vocab size
output_units = vocab_size_word

#learning rate
learning_rate = 0.005

#beta1 for V parameters used in Adam Optimizer
beta1 = 0.90

#beta2 for S parameters used in Adam Optimizer
beta2 = 0.99


data_size = len(x_data)
print(batch_size)
embeddings,parameters,J,P,A = train(x_data,vocab_size_word,y_data,vocab_size_label,input_units,256,50)

#Let's Plot some graphs
avg_loss = list()
avg_acc = list()
avg_perp = list()
i = 0

while(i<len(J)):
    avg_loss.append(np.mean(J[i:i+data_size]))
    avg_acc.append(np.mean(A[i:i+data_size]))
    avg_perp.append(np.mean(P[i:i+data_size]))
    i += data_size

pkl.dump(word_id, open('word_id.pkl', 'wb'))
pkl.dump(id_word, open('id_word.pkl', 'wb'))
pkl.dump(label_id, open('label_id.pkl', 'wb'))
pkl.dump(id_label, open('id_label.pkl', 'wb'))
pkl.dump(embeddings, open('embeddings.pkl', 'wb'))
pkl.dump(parameters, open('parameters.pkl', 'wb'))


plt.plot(list(range(len(avg_loss))),avg_loss)
plt.xlabel("x")
plt.ylabel("Loss (Avg of 1 epochs)")
plt.title("Loss Graph")
plt.show()

plt.plot(list(range(len(avg_perp))),avg_perp)
plt.xlabel("x")
plt.ylabel("Perplexity (Avg of 30 batches)")
plt.title("Perplexity Graph")
plt.show()

plt.plot(list(range(len(avg_acc))),avg_acc)
plt.xlabel("x")
plt.ylabel("Accuracy (Avg of 30 batches)")
plt.title("Accuracy Graph")
plt.show()   