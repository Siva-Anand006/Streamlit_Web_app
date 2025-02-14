import streamlit as st
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

nltk.download('stopwords')

# Load the dataset
data = pd.read_csv(r'spam.csv')
data = data.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1)
data.rename(columns={'v1': 'label', 'v2': 'text'}, inplace=True)
data.drop_duplicates(inplace=True)
data['label'] = data['label'].map({'ham': 0, 'spam': 1})

# Text cleaning function
def process_text(text):
    text_no_punctuation = [char for char in text if char not in string.punctuation]
    text_no_punctuation = ''.join(text_no_punctuation)
    separator = ' '
    return separator.join([word for word in text_no_punctuation.split() if word.lower() not in stopwords.words('english')])

# Apply text cleaning
data['text'] = data['text'].apply(process_text)

# Prepare features and labels
X = data['text']
y = data['label']

# Convert text data to feature vectors
vectorizer = CountVectorizer()
X_features = vectorizer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_features, y, test_size=0.2, random_state=42)

# Build the Naive Bayes model
nb_model = MultinomialNB().fit(X_train, y_train)

# Function to make predictions
def classify_message(input_text):
    labels = ['Not Spam', 'Spam']
    input_features = vectorizer.transform(input_text).toarray()
    prediction = nb_model.predict(input_features)
    predicted_label = int(''.join([str(i) for i in prediction]))
    return f'This message is classified as: {labels[predicted_label]}'

# Streamlit interface
st.title('Spam Message Classifier')
st.image('img.jpg')
user_input = st.text_input('Enter your message:')
submit_button = st.button('Classify')

if submit_button:
    result = classify_message([user_input])
    st.text(result)
