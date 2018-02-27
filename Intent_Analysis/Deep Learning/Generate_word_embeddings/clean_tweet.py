import HTMLParser
from textblob import TextBlob
from stop_words import get_stop_words
from nltk.stem.wordnet import WordNetLemmatizer
import string
import itertools
import re

APPOSTOPHES = {"'s":"is","aren't" :"are not","can't":"cannot", "couldn't"	: "could not", "didn't":"did not", "doesn't" : "does not" ,
"don't":"do not","hadn't" :"had not","hasn't" : "has not","haven't":"have not","he'd"	: "he would","he'll"	: "he will",
"he's"	: "he is","I'd"   : "I would","I'll"  : "I will","I'm"	: "I am","I've"  : "I have","isn't"	: "is not",
"it's"	: "it is","let's"	: "let us","mightn't" : "might not","mustn't" :  "must not","shan't"  :"shall not",
"she'd"	 : "she would","she'll" : "she will","she's" : "she is","shouldn't" : "should not","that's"    : "that is",
"there's"   : "there is","they'd"    : "they would","they'll"   : "they will","they're"	:   "they are",
"they've"	:  "they have","we'd"	: "we would","we're" : "we are","we've" : "we have","weren't" : "were not",
"what'll" : "what will","what're" : "what are","what's"  : "what is","what've"	: "what have","where's" : "where is",
"who'd"   : "who would","who'll"  : "who will","who's"  : "who is","who've" : "who have","won't"	:"will not",
"wouldn't"  : "would not","you'd"	: "you would","you'll" : "you will","you're" : "you are","you've" : "you have"}

def clean_tweet(original_tweet,stop_words = None , lemmatize = None):

	#Escaping HTML characters
	html_parser = HTMLParser.HTMLParser()
	tweet = html_parser.unescape(original_tweet)

	#Decoding data
	tweet = tweet.decode('unicode_escape').encode('ascii','ignore')


	tweet_words = tweet.split()
	#Removing Appostophes
	reformed = [APPOSTOPHES[word] if word in APPOSTOPHES else word for word in tweet_words]	
	tweet = " ".join(reformed)

	#Split Attached Words
	#tweet = " ".join(re.findall('[A-Z][^A-Z]*',tweet))

	#Standardizing words
	tweet = ''.join(''.join(s)[:2] for _, s in itertools.groupby(tweet))

	#Removing url from tweet
	tweet = re.sub(r"http\S+", "", tweet)

	tweet = re.sub(pattern='(\W+)|(\d+)|(\s+)',repl=' ',string=tweet)

	blob = TextBlob(tweet)
        tweet = blob.words # here tokens are words of document

	# remove stop words from tokens
	if(stop_words):		
		# create English stop words list
		en_stop = get_stop_words('en')
		stopped_tokens = [i for i in tweet if not i in en_stop]
		tweet = stopped_tokens

	if(lemmatize):
        	# Create WordNet_Lemmatizer of class WordNetLemmatizer
        	lemmatizer = WordNetLemmatizer()      
        	# Lemmatize token
		leammatized_tokens = [lemmatizer.lemmatize(i) for i in tweet]
		tweet = leammatized_tokens
	return tweet
