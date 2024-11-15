import time
import os
from sentimentbot import load_data, train_model, analyze_user_input
from baymax import handle_conversation, speak
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report
from gtts import gTTS 

CSV_FILE_PATH = 'C:/Users/User/Documents/City/Hackathon/tweets.csv'

# Function to convert text to speech and overwrite the old MP3
def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")  # This will overwrite the previous output.mp3 file
    os.system("start output.mp3")  # Plays the audio (Windows)

def main():
    print("Loading data and training sentiment analysis model...")
    
    # Load data and train the sentiment analysis model
    X, y = load_data(CSV_FILE_PATH)  # Load the data
    model = train_model(X, y)  # Train sentiment analysis model
    
    print("\nSentiment analysis model trained successfully!")
    
    # Now, print only accuracy and avoid printing detailed classification report
    print("\nModel training completed. Accuracy:")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    y_pred = model.predict(X_test)
    accuracy_report = classification_report(y_test, y_pred, output_dict=True)  # Output as a dictionary
    accuracy = accuracy_report['accuracy']
    print(f"Accuracy: {accuracy:.2f}")
    
    # BayMax's introduction message (converted to speech)
    speak("Hello, I am BaeMax. Your personal healthcare assistant. Type 'exit' to quit.")
    
    context = ""
    while True:
        user_input = input("You: ")
        
        # Exit condition
        if user_input.lower() == "exit":
            print("Goodbye!")
            speak("Goodbye!")
            break
        
        # Analyze sentiment of user input
        sentiment, probability = analyze_user_input(user_input, model)
        
        print("\nSentiment Analysis:")
        print(f"Sentiment: {sentiment}")
        print(f"Probability: {probability[0]:.2f}\n")  # Format probability correctly
        
        # Handle conversation with BayMax
        response, context = handle_conversation(user_input, context)
        
        # Print and speak BayMax's response
        print(f"BaeMax: {response}")
        speak(response)  # Convert BayMax's response to speech

if __name__ == "__main__":
    main()











