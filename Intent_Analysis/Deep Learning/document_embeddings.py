from load_embeddings import Embedding
from textblob import TextBlob
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
vocab_file = "/home/abhishek/Facebook_data/CIO/Pre_trained_Embeddings/glove_vector/twitter_vocab.txt"
vectors_file = "/home/abhishek/Facebook_data/CIO/Pre_trained_Embeddings/glove_vector/twitter_vector.txt"
embed = Embedding(vocab_file,vectors_file)

#Why average versus sum
#To handle variable length sentences

def normal_averaging(documents,classes):

	features_vecs = list()
	output_empty = [0] * len(classes)
	train_y = list()

	for words,tag in documents:
	    	vec = np.zeros(embed.W.shape[1])
		nwords = 0.
		for idx, term in enumerate(words):
			if term in embed.vocab:
		    		vec = vec + embed.W[embed.vocab[term], :]
				nwords += 1.

		vec = np.divide(vec,nwords)
		features_vecs.append(vec)

		output_row = list(output_empty)
		output_row[classes.index(tag)] = 1
		train_y.append(output_row)

	return np.array(features_vecs),np.array(train_y)

def averaging_tf_idf_features(embed,documents):

	tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(documents)

        max_idf = max(tfidf.idf_)
        word2weight = defaultdict(
            lambda: max_idf, 
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return np.array([
                np.mean([embed.W[embed.vocab[w],:] * word2weight[w]
                         for w in words if w in embed.vocab] or
                        [np.zeros(embed.W.shape[1])], axis=0)
                for words,tag in documents
            ])

def document_embed(doc):
	blob = TextBlob(doc.lower())
        words.extend(blob.words) # here tokens are words of document
