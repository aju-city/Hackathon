import firebase_admin
from firebase_admin import credentials, firestore
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="google")




# Initialize Firebase with the service account credentials
cred = credentials.Certificate(r"C:\Users\User\Documents\City\baymax_hackathon_keys.json")
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()


def create_user(user_id, name, email, date_of_birth):
    # Reference to the 'users' collection and the user's document
    user_ref = db.collection('users').document(user_id)
    
    # Set the user's data
    user_ref.set({
        'name': name,
        'email': email,
        'patient_id': user_id,
        'date_of_birth': date_of_birth,
        'last_accessed': firestore.SERVER_TIMESTAMP  # Timestamp for when the user last accessed
    })

def get_user(user_id):
    try:
        # Reference to the 'users' collection and user document
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            return user_doc.to_dict()  # Return user data as a dictionary
        else:
            return None  # Return None if user doesn't exist
        
    except Exception as e:
        # Catch any exceptions (including Firestore-related exceptions)
        print(f"Error retrieving conversations: {e}")
        return {}  # Return an empty dict in case of error
    
def update_user(user_id, updated_data):
    try:
        # Reference to the user's document
        user_ref = db.collection('users').document(user_id)
        
        # Update the user data
        user_ref.update(updated_data)
        print(f"User data for {user_id} has been updated.")
    
    except Exception as e:
        print(f"Error updating user: {e}")

def create_symptom_report(user_id, symptoms, solutions):
    # Reference to the 'symptoms' collection within the user's document
    symptoms_ref = db.collection('symptoms').document()
    
    # Set the symptom data
    symptoms_ref.set({
        'user_id': user_id,
        'symptoms': symptoms,
        'solutions': solutions,
        'timestamp': firestore.SERVER_TIMESTAMP  # Timestamp for the report
    })    

def get_symptom_report(user_id):
    try:
        # Reference to the 'symptoms' collection
        symptoms_ref = db.collection('symptoms').where('user_id', '==', user_id)
        symptoms_docs = symptoms_ref.stream()

        symptom_reports = []
        for doc in symptoms_docs:
            symptom_reports.append(doc.to_dict())  # Append the symptom report data

        return symptom_reports  # Return the list of symptom reports
    
    except Exception as e:
        # Catch any exceptions (including Firestore-related exceptions)
        print(f"Error retrieving conversations: {e}")
        return {}  # Return an empty dict in case of error
    
def update_symptom_report(user_id, new_symptom_data):
    try:
        # Query the 'symptoms' collection for the specific user_id
        symptoms_ref = db.collection('symptoms').where('user_id', '==', user_id)
        symptoms_docs = symptoms_ref.stream()

        updated = False
        for doc in symptoms_docs:
            doc_ref = db.collection('symptoms').document(doc.id)
            doc_ref.update(new_symptom_data)
            updated = True

        if updated:
            print(f"Symptom report for user {user_id} has been updated.")
        else:
            print(f"No symptom report found for user {user_id}.")
    
    except Exception as e:
        print(f"Error updating symptom report: {e}")

def create_dementia_query(user_id, query, response):
    # Reference to the 'dementia_queries' collection
    dementia_ref = db.collection('dementia_queries').document()
    
    # Set the dementia query data
    dementia_ref.set({
        'user_id': user_id,
        'query': query,
        'response': response,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

def get_dementia_query(user_id):
    try:
        # Reference to the 'dementia_queries' collection
        dementia_ref = db.collection('dementia_queries').where('user_id', '==', user_id)
        dementia_docs = dementia_ref.stream()

        dementia_queries = []
        for doc in dementia_docs:
            dementia_queries.append(doc.to_dict())  # Append dementia query data

        return dementia_queries  # Return the list of dementia queries
    
    except Exception as e:
        # Catch any exceptions (including Firestore-related exceptions)
        print(f"Error retrieving conversations: {e}")
        return {}  # Return an empty dict in case of error
    
def update_dementia_query(user_id, new_query_data):
    try:
        # Query the 'dementia_queries' collection for the specific user_id
        dementia_ref = db.collection('dementia_queries').where('user_id', '==', user_id)
        dementia_docs = dementia_ref.stream()

        updated = False
        for doc in dementia_docs:
            doc_ref = db.collection('dementia_queries').document(doc.id)
            doc_ref.update(new_query_data)
            updated = True

        if updated:
            print(f"Dementia query for user {user_id} has been updated.")
        else:
            print(f"No dementia query found for user {user_id}.")
    
    except Exception as e:
        print(f"Error updating dementia query: {e}")

    



def create_mood_monitoring(user_id, mood_data):
    # Reference to the 'mood_monitoring' collection
    mood_ref = db.collection('mood_monitoring').document()
    
    # Set the mood data
    mood_ref.set({
        'user_id': user_id,
        'mood_data': mood_data,  # e.g., { 'aggressive': 0, 'depressive': 1 }
        'timestamp': firestore.SERVER_TIMESTAMP
    })  

def get_mood_monitoring(user_id):
    try:
        # Reference to the 'mood_monitoring' collection
        mood_ref = db.collection('mood_monitoring').where('user_id', '==', user_id)
        mood_docs = mood_ref.stream()

        mood_data = []
        for doc in mood_docs:
            mood_data.append(doc.to_dict())  # Append mood data

        return mood_data  # Return the list of mood data
    
    except Exception as e:
        # Catch any exceptions (including Firestore-related exceptions)
        print(f"Error retrieving conversations: {e}")
        return {}  # Return an empty dict in case of error

def update_mood_monitoring(user_id, mood_data_update):
    try:
        # Query the 'mood_monitoring' collection for documents with the specified user_id
        mood_ref = db.collection('mood_monitoring').where('user_id', '==', user_id)
        mood_docs = mood_ref.stream()
        
        updated = False
        for doc in mood_docs:
            # Update the mood_data field in each document with the new data
            doc_ref = db.collection('mood_monitoring').document(doc.id)
            mood_data_update['timestamp'] = firestore.SERVER_TIMESTAMP
            doc_ref.update({'mood_data': mood_data_update})
            updated = True

        if updated:
            print(f"Mood monitoring data for user {user_id} has been updated.")
        else:
            print(f"No mood monitoring record found for user {user_id}.")
    
    except Exception as e:
        # Catch any exceptions
        print(f"Error updating mood monitoring: {e}")

## Example usage

def create_mental_health_conversation(user_id, conversation):
    # Reference to the 'mental_health_conversations' collection
    conversation_ref = db.collection('mental_health_conversations').document()
    
    # Set the conversation data
    conversation_ref.set({
        'user_id': user_id,
        'conversation': conversation,  # e.g., a list of chat messages
        'timestamp': firestore.SERVER_TIMESTAMP
    })    

def get_mental_health_conversation(user_id):
    try:
        # Reference to the 'mental_health_conversations' collection
        conversations_ref = db.collection('mental_health_conversations').where('user_id', '==', user_id)
        conversations_docs = conversations_ref.stream()

        conversations = []
        for doc in conversations_docs:
            conversations.append(doc.to_dict())  # Append conversation data

        return conversations  # Return the list of mental health conversations
    
    except Exception as e:
        # Catch any exceptions (including Firestore-related exceptions)
        print(f"Error retrieving conversations: {e}")
        return {}  # Return an empty dict in case of error
    

def update_mental_health_conversation(user_id, new_conversation_data):
    try:
        # Query the 'mental_health_conversations' collection for the specific user_id
        conversation_ref = db.collection('mental_health_conversations').where('user_id', '==', user_id)
        conversation_docs = conversation_ref.stream()

        updated = False
        for doc in conversation_docs:
            doc_ref = db.collection('mental_health_conversations').document(doc.id)
            # Add or update the 'timestamp' field
            new_conversation_data['timestamp'] = firestore.SERVER_TIMESTAMP
            doc_ref.update(new_conversation_data)
            updated = True

        if updated:
            print(f"Mental health conversation for user {user_id} has been updated.")
        else:
            print(f"No mental health conversation found for user {user_id}.")
    
    except Exception as e:
        print(f"Error updating mental health conversation: {e}")






'''
# 1. Create a new user
create_user('user_12345', 'John Doe', 'johndoe@example.com', '1990-01-01')

# 2. Create symptom reports for the user
create_symptom_report('user_12345', ['headache', 'fever'], ['take ibuprofen', 'drink water'])

# 3. Create dementia query logs
create_dementia_query('user_12345', 'Where am I?', 'You are in Room 101.')

# 4. Create mood monitoring data
create_mood_monitoring('user_12345', {'positive': 0, 'negative': 1})

# 5. Create a mental health conversation log
create_mental_health_conversation('user_12345', [{'role': 'user', 'message': 'I feel anxious'}, {'role': 'bot', 'message': 'It’s okay to feel that way!'}])
'''


# Example usage of the functions to retrieve data
user_data = get_user('user_12345')
symptoms_data = get_symptom_report('user_12345')
dementia_queries_data = get_dementia_query('user_12345')
mood_monitoring = get_mood_monitoring('user_12345')
conversation_data = get_mental_health_conversation('user_12345')

'''
print("User Data:", user_data)
print("Symptoms Data:", symptoms_data)
print("Dementia Queries Data:", dementia_queries_data)
print("Mood Data:", mood_monitoring)
print("Conversations Data:", conversation_data)
'''

'''# Example usage
new_conversation_data = {'conversation': [{'role': 'user', 'message': 'I feel anxious'}, {'role': 'bot', 'message': 'It’s okay to feel that way!'}]}
update_mental_health_conversation('user_12345', new_conversation_data)

#new_mood_data = {'negative': 2, 'positive': 0}
update_mood_monitoring('user_12345', new_mood_data)

# Example usage
new_query_data = {'response': 'You are in Room 202.'}
update_dementia_query('user_12345', new_query_data)

# Example usage 
new_symptom_data = {'symptoms': ['headache', 'nausea'], 'solutions': ['take pain reliever', 'drink water']}
update_symptom_report('user_12345', new_symptom_data)

# Example usage
update_user('user_12345', {'email': 'newemail@example.com', 'last_accessed': firestore.SERVER_TIMESTAMP})

'''



# C:/Users/User/Documents/City/Hackathon/baymax_hackathon_keys.json