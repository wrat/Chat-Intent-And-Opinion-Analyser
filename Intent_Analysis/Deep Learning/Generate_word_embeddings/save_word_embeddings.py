import numpy as np
from glove import Glove
import argparse
import codecs
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description=('Save Trained word vector into text '
		                                  'format for further use'))

	parser.add_argument('--model', '-m', action='store',
		        required=True,
		        help='The filename of the stored GloVe model.')

	parser.add_argument('--vector', '-vec', action='store',
		        required=True,
		        help='The filename of vector')
	parser.add_argument('--vocab', '-voc', action='store',
		        required=True,
		        help='The filename of vocab')

	args = parser.parse_args()

	# Load the GloVe model
	glove = Glove.load(args.model)
	vectors = codecs.open(args.vector,"w",encoding="utf-8")
	vocab = codecs.open(args.vocab,"w",encoding="utf-8")

	dictionary = glove.dictionary
	word_vectors = glove.word_vectors
	for each_word,vector in zip(dictionary,word_vectors):
		vocab.write(each_word+' '+str(dictionary[each_word])+'\n')
		vectors.write(each_word)
		vectors.write(' ')
		for each_attribute in vector:
			vectors.write(str(each_attribute)+' ')
		vectors.write('\n')


