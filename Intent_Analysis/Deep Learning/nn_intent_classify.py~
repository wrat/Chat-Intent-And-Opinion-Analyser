from nltk.stem.lancaster import LancasterStemmer
from textblob import TextBlob
import numpy as np
import tflearn
import tensorflow as tf
import random
ERROR_THRESHOLD = 0.25
import pickle
stemmer = LancasterStemmer()

data = pickle.load( open( "/home/abhishek/Facebook_data/CIO/Intent_Analysis/Deep Learning/training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

def clean_up_sentence(sentence):
    sentence_words = TextBlob(sentence.lower()).words
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def w2v(embed,sentence):

	words = TextBlob(sentence.lower()).words
    	vec = np.zeros(embed.W.shape[1])
	nwords = 0.
	for idx, term in enumerate(words):
		if term in embed.vocab:
	    		vec = vec + embed.W[embed.vocab[term], :]
			nwords += 1.
	vec = np.divide(vec,nwords)
	return vec
def load_model():

	# Build neural network
	net = tflearn.input_data(shape=[None, len(train_x[0])])
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
	net = tflearn.regression(net)
	# Define model and setup tensorboard
	model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
	return model

def classify_bow(sentence,model):
    results = model.predict([bow(sentence, words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list

def classify_w2v(sentence,model,embed):
	results = model.predict([w2v(embed,sentence)])[0]
	results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
	results.sort(key=lambda x: x[1], reverse=True)
	return_list = []
	for r in results:
		return_list.append((classes[r[0]], r[1]))
    	return return_list
