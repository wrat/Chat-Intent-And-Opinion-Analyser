import shelve
import codecs
class lexicon():
	def __init__(self,lexicon_location,pos=None,neg=None,Emoticon=None,Slang=None):
		self.lexicon_database = None
		self.positive_words = list()
		self.negative_words = list()
		self.Emoticon = list()
		self.slangSD = list()
		self.positive_file = None
		self.negative_file = None
		self.Emoticon_file = None
		self.slangSD_file = None

		if(lexicon_location):
			self.lexicon_database = shelve.open(lexicon_location)
		if(pos):
			self.positive_file = open(pos,"r")
			for each_line in self.positive_file:
				each_line = each_line.replace('\n',"")
				self.positive_words.append((each_line,1))
		if(neg):
			self.negative_file = open(neg,"r")
			for each_line in self.negative_file:
				each_line = each_line.replace('\n',"")
				self.negative_words.append((each_line,-1))

		if(Emoticon):
			self.Emoticon_file = open(Emoticon,"r")
			for each_line in self.Emoticon_file:
				each_line = each_line.replace('\n',"")
				temp = each_line.split()
				if(len(temp) > 2):
					self.Emoticon.append(('	'.join(temp[:-1]),int(temp[-1])))
				else:
					self.Emoticon.append((temp[0],int(temp[1])))

		if(Slang):
			self.slangSD_file = open(Slang,"r")
			for each_line in self.slangSD_file:
				each_line = each_line.replace('\n',"")
				temp = each_line.split('\t')
				self.slangSD.append((' '.join(temp[:-1]),int(temp[-1])))

	def insert_lexicon(self,item_tuples):
		if(len(item_tuples) > 0):
			for entity,sentiment in item_tuples:
				self.lexicon_database[entity] = sentiment
