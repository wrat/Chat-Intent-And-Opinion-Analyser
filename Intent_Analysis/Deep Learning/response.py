import sys
sys.path.insert(0, '/home/abhishek/Facebook_data/CIO/Intent_Analysis/Naive Approach/')
from intent_entities import get_keyword

def inform_intent(sentence,intent):
	keyword = get_keyword(sentence)
	return keyword
