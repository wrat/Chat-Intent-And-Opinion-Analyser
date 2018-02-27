from Clean_chat_data import clean_chat

def read_data(source_file):
	data = open(source_file,"r")
	clean_data = open('clean_chat.txt','w')
	for chat in data:
		clean_text = clean_chat(chat)
		clean_data.write(clean_text+'\n')
