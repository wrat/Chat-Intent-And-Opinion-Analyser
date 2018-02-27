from flask import Flask, render_template, request
from flask import jsonify
import sys
sys.path.insert(0, '/home/abhishek/Facebook_data/CIO/Intent_Analysis/Deep Learning/')
from naive_intent import get_result
from load_embeddings import Embedding
app = Flask(__name__,static_url_path="/static")
from nn_intent_classify import classify_w2v,load_model
from response import *
####Load Pretrained Embeddings
vocab_file = "/home/abhishek/Facebook_data/CIO/Pre_trained_Embeddings/glove_vector/twitter_vocab.txt"
vectors_file = "/home/abhishek/Facebook_data/CIO/Pre_trained_Embeddings/glove_vector/twitter_vector.txt"
embed = Embedding(vocab_file,vectors_file)

model = load_model()
model.load('./model.tflearn')
#############
# Routing
#
@app.route('/message', methods=['POST'])
def reply():
    msg = request.form['msg']
    res = classify_w2v(msg,model,embed)[0][0]
    if(res == 'inform'):
        temp = inform_intent(msg,res)
	return jsonify({'text':temp})
    else:
    	return jsonify({'text':res})
	
@app.route("/")
def index(): 
    return render_template("index.html")

#############
# start app
if (__name__ == "__main__"): 
    app.run(port = 5000)
