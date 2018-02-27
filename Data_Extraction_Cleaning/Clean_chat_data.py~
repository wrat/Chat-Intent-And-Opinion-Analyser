from textblob import TextBlob
import string
import itertools
import re
from collections import Counter
from emoticons_detection import emoticons

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

def word_prob(word): 
	return dictionary[word] / total

def words(text): 
	return re.findall('[a-z]+', text.lower())

dictionary = Counter(words(open('big.txt').read()))
max_word_length = max(map(len, dictionary))
total = float(sum(dictionary.values()))

def viterbi_segment(text):
    probs, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = max((probs[j] * word_prob(text[j:i]), j)
                        for j in range(max(0, i - max_word_length), i))
        probs.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words, probs[-1]

def clean_chat(chat_string):

	#Decoding data
	chat_string = chat_string.decode("utf8").encode('ascii','ignore')
	chat_words = chat_string.split()

	#Removing Appostophes
	reformed = [APPOSTOPHES[word] if word in APPOSTOPHES else word for word in chat_words]
	chat_string = " ".join(reformed)

	##Split Attached Words
	#chat_words = chat_string.split(' ')
	#chat_string = list()
	#for each_word in chat_words:
		 #chat_string.append(' '.join(viterbi_segment(each_word)[0]))		
	#chat_string = ' '.join(chat_string)

	#Standardizing words
	chat_string = ''.join(''.join(s)[:2] for _, s in itertools.groupby(chat_string))

	#Removing Special Character But not emoticons we need to preserve it for getting actual sentiment
	emoticons_list,chat_string = emoticons(chat_string)
	chat_string = re.sub(pattern='(\W+)|(\d+)|(\s+)',repl=' ',string=chat_string)

	#Place emoticon at right place
	for each_emoticon in emoticons_list:
		prev_word = each_emoticon['prev_word']
		emoticon = each_emoticon['value']
		if prev_word:
			chat_string  = chat_string.split(prev_word)
			if(len(chat_string) > 1):
				chat_string = chat_string[0] + ' ' + prev_word + ' ' + emoticon + ' ' + chat_string[1]
			else:
				chat_string = chat_string[0] + ' ' + prev_word + ' ' + emoticon
	return chat_string
