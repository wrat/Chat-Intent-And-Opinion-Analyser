from typical_preprocess import preprocess
import shelve
import numpy as np
from stop_words import get_stop_words
import pandas as pd
en_stop = get_stop_words('en')
import shelve

def get_opinion(lexicon,Slang_lexicon,chat_string):
	chat_words,new_string = preprocess(chat_string)
	lexicon_sentiment_map = dict()
	slang_sentiment_map = dict()
	#Find all windows of original string
	words = chat_string.split(' ')
	sub_strings = list()
	for window in range(len(words)):
		index = 0
		while(index <= len(words)):
			string = ' '.join(words[index:index+window])
			if(string not in sub_strings and string != ''):
				sub_strings.append(string)
			index += 1
	#Original String
	sub_strings.append(' '.join(words))

	#In lexicon
	for each_word in chat_words:
		if(lexicon.has_key(str(each_word))):
			lexicon_sentiment_map[str(each_word)] = lexicon[str(each_word)]

	#Slang Lexicon
	for each_string in sub_strings:
		if(Slang_lexicon.has_key(str(each_string))):
			if(each_string not in en_stop):
				slang_sentiment_map[each_string] = Slang_lexicon[str(each_string)]

	#Opinion Calculated as average of sentiment each tokens
	#First Select Tokens which contribute sentiment
	final_sentiment = list()
	to_remove_word = list()
	to_remove_slang = list()
	for each_slang in slang_sentiment_map:
		flag = 0
		for each_word in lexicon_sentiment_map:
			if(each_word in each_slang and flag != 1):
				final_sentiment.append(slang_sentiment_map[each_slang])
				to_remove_slang.append(each_slang)
				to_remove_word.append(each_word)

			elif(each_word in each_slang):
				to_remove_word.append(each_word)

	for each_value in lexicon_sentiment_map:
		if(each_value not in to_remove_word):
			final_sentiment.append(lexicon_sentiment_map[each_value])

	for each_value in slang_sentiment_map:
		if(each_value not in to_remove_slang):
			final_sentiment.append(slang_sentiment_map[each_value])

	if(len(final_sentiment)):
		string_sentiment = sum(final_sentiment)/len(final_sentiment)
		return string_sentiment,new_string
	else:
		return 0,new_string
def Split_Opinion(data):

	columns = ["sentence","sentiment"]	
	lexicon = shelve.open("/home/abhishek/Facebook_data/Opinion_Analysis/Lexicon/lexicon.db")
	Slang_lexicon = shelve.open("/home/abhishek/Facebook_data/Opinion_Analysis/Lexicon/Slang_lexicon.db")
	count = 0
	tagging = list()
	id_sentence = list()

	for index,each_line in enumerate(data):
		each_line = each_line.replace('\n','')
		sentiment,new_string = get_opinion(lexicon,Slang_lexicon,each_line)
		tagging.append([new_string,sentiment])
		id_sentence.append(index+1)
	tagged_data = pd.DataFrame(data = tagging, columns=columns)
	tagged_data['sen_Id'] = id_sentence
	tagged_data = tagged_data[['sen_Id','sentence','sentiment']]
	tagged_data.to_csv("data.csv", index=False)

data = open("/home/abhishek/Facebook_data/Chat Data/Clean_Chat.txt","r")
Split_Opinion(data)
