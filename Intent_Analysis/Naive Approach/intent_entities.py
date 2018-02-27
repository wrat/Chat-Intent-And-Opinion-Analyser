from nltk.tree import *
import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from nltk.parse.stanford import StanfordDependencyParser
import nltk
class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080)))
    
    def parse(self, text):
        return json.loads(self.server.parse(text))

list_Intent_keyword_tag = ['VBN','VBD','VBG','VB','VBP','VBZ','NN','NNP','NNPS','NNS']
list_verbs = ['VBN','VBD','VBG','VB','VBP','VBZ','CD','FW','EX','DT']
list_noun = ['NN','NP','NNP','NNPS','NNS','FW']
required_tags = ['VBN','VBD','VBG','VB','VBP','VBZ','JJ', 'JJR']
list_adj = ['JJ', 'JJR']
infinitive = ['TO']

def ExtractPhrases(sentence_Tree, phrase):
    Phrases = []
    if (sentence_Tree.label() == phrase):
	Phrases.append( sentence_Tree.copy(True) )
    for child in sentence_Tree:
	if (type(child) is Tree):
	    list_of_phrases = ExtractPhrases(child, phrase)
	    if (len(list_of_phrases) != 0):
	        Phrases.extend(list_of_phrases)
    return Phrases

def Extract_Intent_holder(NP_Subtree):
	first_Noun_Phrase = NP_Subtree[0]
	subjects = []
	for each_noun in list_noun:
		subject_tree = ExtractPhrases(first_Noun_Phrase,each_noun)
		if (len(subject_tree) > 0):
			subjects.append(subject_tree)
	return subjects

def Extract_Intent_Keyword(VP_Subtree):
	#noun, verb, multi-word verb or compound noun contained in a verb or noun phrase
	Deepest_VP = VP_Subtree[-1]
	predicates = []	
	for each_predicate in list_Intent_keyword_tag:
		predicates += ExtractPhrases(Deepest_VP,each_predicate)
	return predicates

def Extract_Object(VP_Subtree):
	object_list = list()
	Deepest_VP = VP_Subtree[-1]
	NP_Subtree = ExtractPhrases(Deepest_VP,'NP')
	PP_Subtree = ExtractPhrases(Deepest_VP,'PP')
	ADJV_Subtree = ExtractPhrases(Deepest_VP,'ADJP')

	if(len(NP_Subtree) > 0):
		for each_subtree in NP_Subtree:
			for each_noun in list_noun:
				noun_object = ExtractPhrases(each_subtree,each_noun)
				if(len(noun_object) > 0):		
					object_list.append(noun_object)

	if(len(PP_Subtree) > 0):
		for each_subtree in PP_Subtree:
			for each_noun in list_noun:
				noun_object = ExtractPhrases(each_subtree,each_noun)
				if(len(noun_object) > 0):
					if noun_object not in object_list:
						object_list.append(noun_object)

	if(len(ADJV_Subtree) > 0):
		for each_subtree in ADJV_Subtree:
			for each_adj in list_adj:
				adjv_object = ExtractPhrases(each_subtree,each_adj)
				if(len(adjv_object) > 0):
					object_list.append(adjv_object)
	return object_list

def Extract_Intent_indicator(words,Intent_holder,word_tag):
	#It is a verb or infinitive phrase that immediately follows a subject word
	infinitive_tag = u'TO'
	next_word_holder= None
	Intent_indicator = None
	try:
		for index,word in enumerate(words):
			if(word == Intent_holder):
				next_word_holder = words[index+1]
				index += 1
				if(word_tag[next_word_holder] in list_verbs):
					if('to' in words):
						temp_list = list()
						while(words[index] != 'to'):
							temp_list.append(words[index])
							index = index + 1
						temp_list.append('to')
						return ' '.join(temp_list)
					else:
						Intent_Indicator = next_word_holder
						return Intent_Indicator
	except Exception as e:
		print(e)
	#return Intent_indicator

def get_keyword(sentence):

	#sentence = "i want to buy an xbox"
	nlp = StanfordNLP()
	nlp = nlp.parse(sentence)
	parse_tree = nlp['sentences'][0]['parsetree']
	words_tree = nlp['sentences'][0]['words']
	words = [word_attribute[0] for word_attribute in words_tree]
	words_tag = {item[0]:item[1]['PartOfSpeech'] for item in (nlp['sentences'])[0]['words']}

	#Build Trees
	parse_tree = Tree.fromstring(parse_tree)
	NP_Subtree = ExtractPhrases(parse_tree,'NP')
	VP_Subtree = ExtractPhrases(parse_tree,'VP')
	Intent_holder_tree =  [list(each_subject[0])[0] for each_subject in Extract_Intent_holder(NP_Subtree)]
	Intent_holder = list()
	for each_item in Intent_holder_tree:
		if(isinstance(each_item,unicode)):
			Intent_holder.append(each_item)
		else:
			temp = each_item.leaves()
			if(not isinstance(temp,list)):
				Intent_holder.append(temp)
			elif(len(temp) < 2):
				Intent_holder.append(temp[0])

	#Object  =  [list(each_object[0])[0] for each_object in  Extract_Object(VP_Subtree)]
	Intent_holder = Intent_holder[0]
	Intent_indicator = Extract_Intent_indicator(words,Intent_holder,words_tag)
	if(len(VP_Subtree)>0):	
		Intent_keyword_tree = Extract_Intent_Keyword(VP_Subtree)
		Intent_keyword = ' '.join([ele.leaves()[0] for ele in Intent_keyword_tree])
		return Intent_keyword
	else:
		return None
