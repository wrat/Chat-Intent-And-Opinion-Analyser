import gensim
import logging
import pprint

# Load Google's pre-trained Word2Vec model.
model = gensim.models.Word2Vec.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
index2word_set = set(model.index2word)
vectors = open('vector.txt','w')
vocab = open('vocab.txt','w')
for i,word in enumerate(index2word_set):
	vocab.write(word.encode('utf-8'))
	vocab.write(' ')
	vocab.write(str(i))
	vectors.write(word.encode('utf-8'))
	vectors.write(' ')
	for ele in model[word]:
		vectors.write(str(ele))
		vectors.write(' ')
	vectors.write('\n')
	vocab.write('\n')
# for logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# Load evaluation dataset of analogy task 
#model.accuracy('questions-words.txt')
# execute analogy task like king - man + woman = queen
#positive=['woman', 'king'], negative=['man']
#pprint.pprint(model.most_similar("room"))
