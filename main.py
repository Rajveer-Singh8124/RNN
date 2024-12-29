import numpy as np
import streamlit as st
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import load_model

word_index = imdb.get_word_index()
reverse_word_index = {value:key for key,value in word_index.items()}

model = load_model("model.h5")

def decode_review(encoded_review):
    return " ".join([reverse_word_index.get(i-3,"?") for i in encoded_review])

def preprocess_text(text):
    words = text.lower().split()
    encoded_review = [word_index.get(word,2)+3 for word in words]
    padded_review = sequence.pad_sequences([encoded_review],maxlen=500)
    return padded_review

def predict_sentiment(review):
    preprocessed_input = preprocess_text(review)
    prediction = model.predict(preprocessed_input)
    sentiment = "Positive" if prediction[0][0] >0.8 else "Negative"
    return sentiment,prediction[0][0]

st.title("Movie Review Sentiment Analysis")
st.write("Enter a movie review to classify it as positive or negative")

user_input = st.text_area("Movie Review")

if st.button("Classify"):
    sentiment,pred_prob = predict_sentiment(user_input)
    
    st.write(f"Sentiment: {sentiment}")
    st.write(f"Prediction Score: {pred_prob:.2f}")

else:
    st.write("Please enter a movie review")
    