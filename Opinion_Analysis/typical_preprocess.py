from stop_words import get_stop_words
from nltk.stem.wordnet import WordNetLemmatizer
from textblob import TextBlob
from Spell_checking import azure_Spell_checker
from nltk.stem.porter import PorterStemmer

def preprocess(chat_string):

	chat_string = chat_string.lower()
	#Spell-checker
	chat_string = azure_Spell_checker(chat_string)

	#Split Chat string into words
	blob = TextBlob(chat_string)
        chat_words = blob.words # here tokens are words of document

	#Remove Stop_words
	en_stop = get_stop_words('en')
	stopped_tokens = [i for i in chat_words if not i in en_stop]
	chat_words = stopped_tokens

	# Lemmatize token
	lemmatizer = WordNetLemmatizer()      
	leammatized_tokens = [lemmatizer.lemmatize(i) for i in chat_words]
	chat_words = leammatized_tokens

	#Stemming token
	porter_stemmer = PorterStemmer()
	stemmed_tokens = [porter_stemmer.stem(i) for i in chat_words]
	chat_words = stemmed_tokens


	return chat_words,chat_string
