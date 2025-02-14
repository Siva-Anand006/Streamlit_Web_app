# Spam Message Classifier

This is a simple machine learning-based web application that classifies text messages as spam or not spam using Streamlit, Naive Bayes classification, and text pre-processing techniques.

## Project Overview:
The Spam Message Classifier uses Natural Language Processing (NLP) and machine learning to classify text messages as spam or non-spam. It uses a dataset of messages, pre-processes the text to remove punctuation and stop words, and then trains a Naive Bayes classifier to predict whether a given message is spam. The application is built using **Streamlit** for the user interface, **Scikit-learn** for the model, and **NLTK** for text processing.

## Key Features:
- **Text Preprocessing**: The app removes punctuation, stop words, and normalizes the text to improve the model’s performance.
- **Naive Bayes Classifier**: Uses the Multinomial Naive Bayes algorithm to classify messages as either spam or not spam based on training data.
- **Streamlit Web Interface**: The user can input a message into the web interface, and the app will return whether the message is classified as "Spam" or "Not Spam".
- **Dataset**: The model is trained on a labeled dataset (`spam.csv`) containing both spam and non-spam (ham) messages.

## Requirements:
- Python 3.x
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- NLTK
- string (Python library)

## Installation:
1. Clone or download the repository to your local machine.
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
