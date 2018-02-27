from xml.dom import minidom
import os
from os import listdir
from os.path import isfile, join

def make_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def parse_sms_corpus(path,xml_file_name,directory):
    try:
        xml_tree = minidom.parse(path)
        sms_tag  = xml_tree.getElementsByTagName('smsCorpus')
        path_save = directory + '/chat_raw_data' + xml_file_name + '.txt'
        file = open(path_save,'w+')
        for sms in sms_tag:
            msg_tag   = sms.getElementsByTagName('message')
            for msg in msg_tag:
                text_tag  = msg.getElementsByTagName('text')
                for text in text_tag:
                    text_msg = text.firstChild.data
                    #text_msg = text_msg.encode('utf-8')
                    try:
                      file.write(text_msg+'\n')
                    except Exception as e:
                        print(e)
    except Exception as e:
        print(e)

def fetch_file_name(directory_name):
    mypath = directory_name
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

if __name__ == "__main__":
	list_file_name = fetch_file_name('SMS_corpus_file')
	directory = 'sms_corpus'
	for file_name in list_file_name:
	    path =  'SMS_corpus_file/' + file_name
	    parse_sms_corpus(path ,file_name, directory)
