import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import pickle
from flask import Flask, request, render_template

 
#load the trained model
model = tf.keras.models.load_model('simplernn_model.h5')

#load the encoder
enc_path = 'enc.pkl'
with open(enc_path, 'rb') as file:
    encoder = pickle.load(file)

tokenizer_path = 'tokenizer.pkl'
with open(tokenizer_path, mode='rb') as tokenize:
    tk = pickle.load(tokenize)


#pipeline for preprocessing
def input_preprocessing(text):
    #tokenize the text
    token = tk.texts_to_sequences([text])

    #pad the tokens to have consistent length of 28.
    token = pad_sequences(token, maxlen=28)
    return token[0]

## Create the flask app by instantiating
app = Flask(__name__)

#give flask a way to route the app
#define which function should be executed for different URLs.
#  You can use the @app.route decorator to associate a function with a specific URL. 
@app.route(rule='/predict/', methods=['GET', 'POST'])
def index():
    """
    performs prediction
    """
    sentiment = ""
    #get the user input
    if request.method == 'POST':
        #keep track or hold the user input using the varible user_input
        user_input = request.form['input_from_user']
        #first preprocess text
        prep_text = input_preprocessing(user_input)

        prep_text = np.array(prep_text)  # Assuming prep_text is a list or array of text sequences
        prep_text = prep_text.reshape(-1, 28)

        #make prediction
        pred = model.predict(prep_text)


        #get the sentiment label
        sentiment = encoder.inverse_transform(pred)

        #return the sentiment using th erender template

    return render_template('index.html', sentiment = sentiment)
    #the above means that we will create an index.html form that will render our result.abs




if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=False)
    


