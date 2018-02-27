from stop_words import get_stop_words
from nltk.stem.wordnet import WordNetLemmatizer
from textblob import TextBlob
from Spell_checking import azure_Spell_checker
import shelve

def replace_slang_word(chat_words):

	slang_db = shelve.open("slang-meaning.db")
	#Replace each slang word with it's actual word
	new_chat_words = list()
	for each_word in chat_words:
		if(slang_db.has_key(str(each_word))):
			new_chat_words.append(slang_db[str(each_word)])
		else:
			new_chat_words.append(each_word)

	chat_string =  ' '.join(new_chat_words)
	blob = TextBlob(chat_string)
	return blob.words

def preprocess(chat_string,slang_replace = None):

	#Spell-checker
	chat_string = azure_Spell_checker(chat_string)

	#Split Chat string into words
	blob = TextBlob(chat_string)
        chat_words = blob.words # here tokens are words of document

	#Replace Slang words
	if(slang_replace):
		chat_words = replace_slang_word(chat_words)

	#Remove Stop_words
	en_stop = get_stop_words('en')
	stopped_tokens = [i for i in chat_words if not i in en_stop]
	chat_words = stopped_tokens

	lemmatizer = WordNetLemmatizer()      
	# Lemmatize token
	leammatized_tokens = [lemmatizer.lemmatize(i) for i in chat_words]
	chat_words = leammatized_tokens
	return chat_words
