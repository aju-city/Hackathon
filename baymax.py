from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os
from gtts import gTTS

# Function to handle conversation with BayMax (Healthcare Assistant)
def handle_conversation(user_input, context):
    # Define the prompt template
    template = """
        Write a concise response to the user
        Your name is "baemax"
        You are a healthcare assitant that reports back to the doctor/ nurse.
        You are in City hospital
        Here is the conversation history: {context}
        Patientinput: {patientinput}
        Answer:
    """
    
    model = OllamaLLM(model="llama3")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    # Generate the response based on user input
    result = chain.invoke({"context": context, "patientinput": user_input})
    
    # Update the context with the latest interaction
    context += f"\nUser: {user_input}\nAI: {result}"
    
    return result, context

# Function to speak the text using gTTS
def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    os.system("start output.mp3")  # Plays the audio on Windows

# Main function to run BayMax
def run_baymax():
    context = ""
    print("Hello, I am BaeMax. Your personal healthcare assistant. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        result, context = handle_conversation(user_input, context)
        speak(result)  # Speak the response from BayMax
        print(f"BaeMax: {result}")

