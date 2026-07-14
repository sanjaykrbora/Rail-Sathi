import pandas as pd
from utils.database_helper import fetch_table
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Define our training data (phrases mapping to specific intents)
TRAINING_DATA = {
    "count_employees": [
        "how many employees are working", "how many employees work here", "total staff", "employee count", 
        "number of workers", "how many people", "total employees", "employees working", "staff count", "worker count"
    ],
    "count_coaches": [
        "how many coaches", "total coaches", "number of coaches", 
        "coach count", "how many trains"
    ],
    "poh_coaches": [
        "coaches in poh", "how many coaches are undergoing poh", 
        "periodic overhaul count", "coaches under poh", "poh coaches"
    ],
    "critical_machines": [
        "critical machines", "machines in critical status", 
        "broken machines", "machines needing immediate attention", "summary of critical machine status", "critical status"
    ],
    "shop_employees": [
        "who works in the shop", "employees in the wheel shop", 
        "give me employees for a shop", "which employees work in the shop", "staff in the shop"
    ],
    "pending_maintenance": [
        "pending maintenance", "maintenance tasks", 
        "maintenance logged", "pending repairs", "how many pending maintenance tasks are there"
    ]
}

# Flatten the training data for the model
X_train = []
y_train = []
for intent, phrases in TRAINING_DATA.items():
    for phrase in phrases:
        X_train.append(phrase)
        y_train.append(intent)

# Train the local TF-IDF Vectorizer with stop words removed so common words don't skew the results
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
X_train_vectorized = vectorizer.fit_transform(X_train)

def predict_intent(question):
    # Vectorize the user's question
    question_vec = vectorizer.transform([question.lower()])
    
    # Calculate cosine similarity against all trained phrases
    similarities = cosine_similarity(question_vec, X_train_vectorized)[0]
    
    # Find the most similar phrase
    best_match_idx = np.argmax(similarities)
    best_score = similarities[best_match_idx]
    
    # If the confidence is too low, return a fallback intent
    if best_score < 0.2:
        return "unknown"
        
    return y_train[best_match_idx]

def extract_shop_name(question, shops_df):
    for shop_name in shops_df['shop_name'].dropna().unique():
        if shop_name.lower() in question.lower():
            return shop_name
    return None

def ai_response(question):
    try:
        coaches = fetch_table("coaches")
        employees = fetch_table("employees")
        machines = fetch_table("machines")
        shops = fetch_table("shops")
        maintenance = fetch_table("maintenance")
        workshop = fetch_table("workshop_info")

        # Predict the intent using our local ML model
        intent = predict_intent(question)
        
        if intent == "count_employees":
            return f"👨‍🔧 There are exactly **{len(employees)} employees** currently working in the workshop."
            
        elif intent == "count_coaches":
            return f"🚂 We have a total of **{len(coaches)} coaches** registered in the database."
            
        elif intent == "poh_coaches":
            poh_coaches = coaches[coaches['status'].str.contains('POH', case=False, na=False)]
            return f"👋 **Hello!** Based on the current workshop records, there are exactly **{len(poh_coaches)} coaches** undergoing POH (Periodic Overhaul) right now."
            
        elif intent == "critical_machines":
            critical_machines = machines[machines['status'].str.contains('Critical', case=False, na=False)]
            if len(critical_machines) == 0:
                return "🎉 **Good news!** I just checked the database and there are currently *no machines* in critical status."
            names = ", ".join(critical_machines['machine_name'].tolist())
            return f"⚠️ **Attention needed:** I found **{len(critical_machines)} critical machines** requiring immediate repair. \n\nThese machines are: {names}."
            
        elif intent == "shop_employees":
            shop_name = extract_shop_name(question, shops)
            if shop_name:
                shop_emps = employees[employees['shop_name'].str.lower() == shop_name.lower()]
                names = ", ".join(shop_emps['employee_name'].tolist()[:10])
                count = len(shop_emps)
                return f"**Sure thing!** There are **{count} employees** currently assigned to the {shop_name}. \n\nHere are a few of them: {names}."
            else:
                return "I couldn't identify a specific shop in your question, but try asking something like *'Which employees work in the Wheel Shop?'*"
                
        elif intent == "pending_maintenance":
            pending = maintenance[maintenance['status'] == 'Pending']
            return f"🔧 We currently have **{len(pending)} pending maintenance tasks** logged in the system."
            
        else:
            return "🤖 **Hello! I am the Rail Sathi Custom Local AI.** \n\nI have successfully analyzed your question using my local Machine Learning model, but I couldn't quite understand what you're looking for. Try asking me about **coaches**, **employees in a shop**, or **critical machines**!"

    except Exception as error:
        return f"❌ Custom AI Engine Error: {error}"
