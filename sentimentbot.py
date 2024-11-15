import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, classification_report
import pickle
import database
import firebase_admin
from firebase_admin import credentials, firestore
from database import db

# Function to load data from the CSV file
def load_data(csv_path):
    df = pd.read_csv(csv_path)
      
    # Handle missing values by dropping rows with NaN values in the 'Tweet' column
    df = df.dropna(subset=['Tweet', 'Sentiment'])

    X = df['Tweet'] # Column names in csv file
    y = df['Sentiment']
    return X, y

# Function to train sentiment analysis model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a pipeline with TF-IDF and Logistic Regression
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(stop_words='english')),
        ('classifier', LogisticRegression())
    ])
    
    # Train the model
    model = pipeline.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    print(f"Classification report:\n{classification_report(y_test, y_pred)}")
    
    # Return trained model
    return model

# Function to analyze sentiment of user input
def analyze_user_input(user_input, model):
    sentiment = model.predict([user_input])[0]
    # Here, we don't use probability for simplicity; you can enhance it
    probability = model.predict_proba([user_input])[0]
    
    sentiment_label = 'Positive' if sentiment == 'Positive' else 'Negative'
    mood_monitoring = database.get_mood_monitoring('user_12345')
    moodCounter = mood_monitoring[0]["mood_data"][sentiment_label.lower()] + 1
    new_mood_data = mood_monitoring[0]["mood_data"]
    new_mood_data[sentiment_label.lower()] = moodCounter
    database.update_mood_monitoring('user_12345', new_mood_data)

    if mood_monitoring[0]["mood_data"]['negative'] >= 3:
        print("Contacting Staff...")

    return sentiment_label, probability

# Save trained model to a file
def save_model(model, filename="sentiment_model.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(model, f)

# Load trained model from a file
def load_model(filename="sentiment_model.pkl"):
    with open(filename, 'rb') as f:
        return pickle.load(f)


# 'C:/Users/User/Documents/City/Hackathon/tweets.csv' ---> Filepath
