import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint
from nltk.tree import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
from nltk.parse.stanford import StanfordDependencyParser
import pandas as pd
import pickle
import unicodecsv as csv
import nltk
from stop_words import get_stop_words

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
en_stop = get_stop_words('en')

class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080)))
    
    def parse(self, text):
        return json.loads(self.server.parse(text))

def get_dict(words_tags,item1,item2):
	if((words_tags[item1] == 'NN') or (words_tags[item1] == 'NP')):
		return 1
	else:
		return 2
#Get Number of review
##num_reviews = len(clean_train_reviews)
nlp = StanfordNLP()

result = nlp.parse("the entry to the hotel did not give a very good impression.")
dependencies = ((result['sentences'])[0]['dependencies'])
print(dependencies)
					
typed_dependencies = []
location = ['jaipur']
"""
final_list = set()
final_tags = open('tags_jaipur.txt','w+')
for l in location:
	with open('/home/abhishek/Desktop/Review_analysis/itemsHotel_' + l + '.csv', 'rb') as dataFile:
		train = csv.reader(dataFile)
		for row in train:
			raw_sentences = tokenizer.tokenize(row[0].strip())
			for raw_sentence in raw_sentences:
				try:
					
					result = nlp.parse(raw_sentence)
					dependencies = ((result['sentences'])[0]['dependencies'])
					words_tag = {item[0]:item[1]['PartOfSpeech'] for item in (result['sentences'])[0]['words']}
					temp_dict = dict()
					print(dependencies)
					print('\n')
					print(raw_sentence)
					print("\n\n\n\n")
				#print(words_tag)
					for item in dependencies:
						if 'ROOT' not in item:		
							if ((words_tag[item[1]] == 'NN') or (words_tag[item[2]] == 'NN')):
								if(item[0] == 'nsubj' or item[0] == 'nsubjpass' or item[0] == 'amod'):
									if((item[1] not in en_stop) and (item[2] not in en_stop)):
										if(get_dict(words_tag,item[1],item[2]) == 1):
											if(item[1] in temp_dict.keys()):
												temp_dict[item[1]].append(item[2])
											else:
												temp_dict[item[1]] = [item[2]]
										else:
											if(item[2] in temp_dict.keys()):
												temp_dict[item[2]].append(item[1])
											else:
												temp_dict[item[2]] = [item[1]]
					#print(temp_dict)
				except Exception as e:
					print("somthing went wrong",e)
"""
