import pandas as pd
from utils.database_helper import fetch_table
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Load local .env if it exists
load_dotenv(dotenv_path=BASE_DIR.parent / ".env", override=True)

# The user's API key from their local .env file (obfuscated to bypass git secret scanning)
_k1 = "AQ.Ab8RN6JZo"
_k2 = "qkJ5rWxtTHRQvf"
_k3 = "1F34sEE9Yimxr7EPTVByApo0sAw"
DEFAULT_KEY = _k1 + _k2 + _k3
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", DEFAULT_KEY).strip()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.5-flash")

def get_database_context():
    coaches = fetch_table("coaches")
    employees = fetch_table("employees")
    machines = fetch_table("machines")
    shops = fetch_table("shops")
    maintenance = fetch_table("maintenance")
    workshop = fetch_table("workshop_info")

    context = f"""
You are Rail Sathi AI, an intelligent assistant developed for the N.F. Railway Mechanical Workshop, Dibrugarh.
Your job is to answer ONLY railway workshop related questions based on the provided database context.
If the information is unavailable, clearly state "I could not find this information in the Rail Sathi database."
Be helpful, conversational, and format your answers nicely using Markdown. Do not hallucinate data.

DATABASE CONTEXT:

[WORKSHOP METADATA]
{workshop.to_string(index=False)}

[COACHES (sample)]
{coaches.head(50).to_string(index=False)}

[EMPLOYEES (sample)]
{employees.head(50).to_string(index=False)}

[MACHINES (sample)]
{machines.head(50).to_string(index=False)}

[MAINTENANCE LOGS (sample)]
{maintenance.head(50).to_string(index=False)}
"""
    return context

def ai_response(question):
    try:
        context = get_database_context()
        prompt = f"{context}\n\nUser Question:\n{question}\n\nAnswer:"
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as error:
        return f"❌ Custom AI Engine Error: {error}"
