from __future__ import print_function
import argparse
import pprint
import gensim
from read_data import read_data
from glove import Glove
from glove import Corpus

def build_model():

    # Set up command line parameters.
    parser = argparse.ArgumentParser(description='Fit a GloVe model.')

    parser.add_argument('--create', '-c', action='store',
                        default=None,
                        help=('The filename of the corpus to pre-process. '
                              'The pre-processed corpus will be saved '
                              'and will be ready for training.'))
    parser.add_argument('--train', '-t', action='store',
                        default=0,
                        help=('Train the GloVe model with this number of epochs.'
                              'If not supplied, '
                              'We\'ll attempt to load a trained model'))

    parser.add_argument('--parallelism', '-p', action='store',
                        default=1,
                        help=('Number of parallel threads to use for training'))

    parser.add_argument('--query', '-q', action='store',
                        default='',
                        help='Get closes words to this word.')
    args = parser.parse_args()

    if args.create:
        # Build the corpus dictionary and the cooccurrence matrix.

        print('Pre-processing corpus')
        data = read_data(args.create)
        corpus_model = Corpus()
        corpus_model.fit(data, window=10)
        corpus_model.save('corpus.model')

        print('Dict size: %s' % len(corpus_model.dictionary))
        print('Collocations: %s' % corpus_model.matrix.nnz)

    if args.train:

        # Train the GloVe model and save it to disk.
        if not args.create:
            # Try to load a corpus from disk.
            print('Reading corpus statistics')
            corpus_model = Corpus.load('corpus.model')

            print('Dict size: %s' % len(corpus_model.dictionary))
            print('Collocations: %s' % corpus_model.matrix.nnz)

        print('Training the GloVe model')

        glove = Glove(no_components=50, learning_rate=0.05)
        glove.fit(corpus_model.matrix, epochs=int(args.train),
                  no_threads=args.parallelism, verbose=True)
        glove.add_dictionary(corpus_model.dictionary)
        glove.save('glove.model')

    if args.query:
        # Finally, query the model for most similar words.
        if not args.train:
            print('Loading pre-trained GloVe model')
            glove = Glove.load('glove.model')

        print('Querying for %s' % args.query)
        pprint.pprint(glove.most_similar(args.query, number=10))
build_model()
