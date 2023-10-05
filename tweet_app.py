import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import pickle
import sklearn

 
#load the trained model
model = tf.keras.models.load_model('airline_tweet_project/Airline_Sentiment_Analysis_Project/simplernn_model.h5')

#load the encoder
enc_path = 'airline_tweet_project/Airline_Sentiment_Analysis_Project/enc.pkl'
with open(enc_path, 'rb') as file:
    encoder = pickle.load(file)



#pipeline for preprocessing
def input_preprocessing(text):
    #tokenize the text
    token = tk.texts_to_sequences([text])

    #pad the tokens to have consistent length of 28.
    token = pad_sequences(token, maxlen=28)
    return token[0]

#create app Title
st.title("Tweet Classification App")

#Welcome user
st.write('Welcome to our Airline Sentiment Analysis Application. Kindly give us the texts you need us to analyze')

#create user input interface
user_input = st.text_area(f"Enter Text Here", " ")
#st.write(user_input)

#create a button for prediction
button = st.button(f"Predict Sentiment")

if button and user_input is not None:
    #first preprocess text
    prep_text = input_preprocessing(user_input)

    prep_text = np.array(prep_text)  # Assuming prep_text is a list or array of text sequences
    prep_text = prep_text.reshape(-1, 28)

    #make prediction
    pred = model.predict(prep_text)


    #get the sentiment label
    sentiment = encoder.inverse_transform(pred)


    st.write(f'The Sentiment of the given text is: {sentiment}')


