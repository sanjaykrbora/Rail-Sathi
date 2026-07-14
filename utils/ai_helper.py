import pandas as pd
from utils.database_helper import fetch_table
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Define our training data (phrases mapping to specific intents)
TRAINING_DATA = {
    "greeting": [
        "hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"
    ],
    "help": [
        "what can you do", "help me", "how do I use this", "what are your features", "help", "what do you do", "tasks"
    ],
    "identity": [
        "who are you", "what is your name", "what are you", "who built you", "tell me about yourself", "are you ai"
    ],
    "workshop_info": [
        "where is this workshop", "tell me about the workshop", "workshop details", "railway workshop location", "what workshop is this"
    ],
    "count_employees": [
        "how many employees are working", "how many employees work here", "total staff", "employee count", 
        "number of workers", "how many people", "total employees", "employees working", "staff count", "worker count"
    ],
    "list_employees": [
        "show employees", "list employees", "who works here", "display staff", "employee list", "give me the employees", "view employees"
    ],
    "shop_employees": [
        "who works in the shop", "employees in the wheel shop", 
        "give me employees for a shop", "which employees work in the shop", "staff in the shop"
    ],
    "count_coaches": [
        "how many coaches", "total coaches", "number of coaches", 
        "coach count", "how many trains"
    ],
    "list_coaches": [
        "show coaches", "list coaches", "display coaches", "view coaches", "coach list"
    ],
    "poh_coaches": [
        "coaches in poh", "how many coaches are undergoing poh", 
        "periodic overhaul count", "coaches under poh", "poh coaches", "show poh"
    ],
    "count_machines": [
        "how many machines", "total machines", "number of machines", "machine count"
    ],
    "list_machines": [
        "show machines", "list machines", "display machines", "view machines", "machine list"
    ],
    "critical_machines": [
        "critical machines", "machines in critical status", 
        "broken machines", "machines needing immediate attention", "summary of critical machine status", "critical status", "show critical"
    ],
    "count_shops": [
        "how many shops", "number of shops", "total workshops", "shop count"
    ],
    "list_shops": [
        "show shops", "list shops", "display shops", "view shops", "shop list", "what shops are there"
    ],
    "pending_maintenance": [
        "pending maintenance", "maintenance tasks", 
        "maintenance logged", "pending repairs", "how many pending maintenance tasks are there", "show maintenance"
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
    if best_score < 0.15:
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
        
        # Smart routing: if they asked for shop employees but didn't specify a shop, route to list_employees
        if intent == "shop_employees":
            shop_name = extract_shop_name(question, shops)
            if not shop_name:
                intent = "list_employees"
        
        if intent == "greeting":
            return "👋 **Hello there!** I am the Rail Sathi AI Assistant. How can I help you with the workshop today?"
            
        elif intent == "identity":
            return "🤖 **I am Rail Sathi AI**, a custom Machine Learning model built exclusively for the N.F. Railway Mechanical Workshop, Dibrugarh. I don't rely on Gemini or external APIs—I run completely locally!"
            
        elif intent == "help":
            return "**I can help you with many basic tasks!** Try asking me things like:\n- *How many employees are working?*\n- *Show employees*\n- *List shops*\n- *Critical machines*\n- *Pending maintenance*"
            
        elif intent == "workshop_info":
            name = workshop['workshop_name'].iloc[0] if not workshop.empty else "N.F. Railway Mechanical Workshop"
            location = workshop['location'].iloc[0] if not workshop.empty else "Dibrugarh"
            established = workshop['established_year'].iloc[0] if not workshop.empty else "N/A"
            return f"🏭 **Workshop Details:** This is the **{name}** located in **{location}**. It was established in {established}."
        
        elif intent == "count_shops":
            return f"🏭 We have exactly **{len(shops)} distinct shops** operating within the workshop."
            
        elif intent == "list_shops":
            shop_list = ", ".join(shops['shop_name'].tolist())
            return f"🏭 **Here are all our shops:**\n{shop_list}"
            
        elif intent == "count_machines":
            return f"⚙️ There are **{len(machines)} machines** registered and monitored in our database."

        elif intent == "list_machines":
            names = ", ".join(machines['machine_name'].tolist()[:15])
            return f"⚙️ **Here is a sample of {min(15, len(machines))} machines in the database:**\n{names}...\n\n(There are {len(machines)} in total)"

        elif intent == "count_employees":
            return f"👨‍🔧 There are exactly **{len(employees)} employees** currently working in the workshop."
            
        elif intent == "list_employees":
            emp_list = [f"{row['employee_name']} ({row['employee_id']})" for _, row in employees.head(15).iterrows()]
            names = ", ".join(emp_list)
            return f"👨‍🔧 **Here is a sample of {min(15, len(employees))} employees working here:**\n{names}...\n\n(There are {len(employees)} total employees)"
            
        elif intent == "shop_employees":
            shop_name = extract_shop_name(question, shops)
            shop_emps = employees[employees['shop_name'].str.lower() == shop_name.lower()]
            emp_list = [f"{row['employee_name']} ({row['employee_id']})" for _, row in shop_emps.head(15).iterrows()]
            names = ", ".join(emp_list)
            count = len(shop_emps)
            return f"**Sure thing!** There are **{count} employees** currently assigned to the {shop_name}. \n\nHere are some of them: {names}."
                
        elif intent == "count_coaches":
            return f"🚂 We have a total of **{len(coaches)} coaches** registered in the database."
            
        elif intent == "list_coaches":
            ids = ", ".join(coaches['coach_id'].astype(str).tolist()[:15])
            return f"🚂 **Here is a sample of {min(15, len(coaches))} coaches:**\n{ids}...\n\n(There are {len(coaches)} total coaches)"
            
        elif intent == "poh_coaches":
            poh_coaches = coaches[coaches['status'].str.contains('POH', case=False, na=False)]
            return f"👋 **Hello!** Based on the current workshop records, there are exactly **{len(poh_coaches)} coaches** undergoing POH (Periodic Overhaul) right now."
            
        elif intent == "critical_machines":
            critical_machines = machines[machines['status'].str.contains('Critical', case=False, na=False)]
            if len(critical_machines) == 0:
                return "🎉 **Good news!** I just checked the database and there are currently *no machines* in critical status."
            names = ", ".join(critical_machines['machine_name'].tolist())
            return f"⚠️ **Attention needed:** I found **{len(critical_machines)} critical machines** requiring immediate repair. \n\nThese machines are: {names}."
                
        elif intent == "pending_maintenance":
            pending = maintenance[maintenance['status'] == 'Pending']
            return f"🔧 We currently have **{len(pending)} pending maintenance tasks** logged in the system."
            
        else:
            return "🤖 **I didn't quite catch that.** \n\nI am the Rail Sathi Custom Local AI. You can ask me basic questions like **'show employees'**, **'what are your features'**, or **'critical machines'**!"

    except Exception as error:
        return f"❌ Custom AI Engine Error: {error}"
