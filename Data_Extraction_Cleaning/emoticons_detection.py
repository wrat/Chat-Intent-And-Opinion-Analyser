import re
import emo

def emoticons(string):
    __entities = []
    pattern = u'(' + u'|'.join(k for k in emo.EMOTICONS) + u')'
    __entities = []
    matches = re.finditer(r"%s"%pattern,str(string),re.IGNORECASE)
    prev_word = ''
    for et in matches:
	if(et.group().strip() == "oo"):
		continue

        index = et.start() - 1
	if(string[index] == ' '):
            index = index - 1
        while(index >= 0 and string[index] != ' '):
            prev_word += string[index]
            index -= 1
	prev_word = re.sub(pattern='(\W+)|(\d+)|(\s+)',repl='',string=prev_word)
        __entities.append({'value': et.group().strip(),
        'prev_word' : prev_word[::-1]
        })

    for each_entity in __entities:
	string = string.replace(each_entity['value'],'')
    return __entities,string
