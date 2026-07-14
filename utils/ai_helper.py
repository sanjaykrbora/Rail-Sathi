import os

import google.generativeai as genai
from dotenv import load_dotenv

from utils.database_helper import fetch_table

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR.parent / ".env", override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY").strip() if os.getenv("GEMINI_API_KEY") else None

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3.5-flash")


def get_database_context():

    coaches = fetch_table("coaches")
    employees = fetch_table("employees")
    machines = fetch_table("machines")
    shops = fetch_table("shops")
    maintenance = fetch_table("maintenance")

    context = f"""
You are Rail Sathi AI.

You are an AI assistant developed for
N.F. Railway Mechanical Workshop, Dibrugarh.

Your job is to answer ONLY railway workshop related questions.

DATABASE

========== COACHES ==========
{coaches.head(20).to_string(index=False)}

========== EMPLOYEES ==========
{employees.head(20).to_string(index=False)}

========== MACHINES ==========
{machines.head(20).to_string(index=False)}

========== WORKSHOP SHOPS ==========
{shops.head(20).to_string(index=False)}

========== MAINTENANCE ==========
{maintenance.head(20).to_string(index=False)}

Rules

1. Answer only using available data.

2. If information is unavailable,
say

"Record not found in Rail Sathi database."

3. Keep answers professional.

4. Give short and accurate answers.

5. Never generate fake railway information.

"""

    return context


def ai_response(question):

    try:

        if not GEMINI_API_KEY:
            return "AI Service API key is missing. Ensure the system is configured correctly."

        context = get_database_context()

        prompt = f"""
{context}

User Question

{question}

Answer:
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as error:

        return f"""
❌ AI Error

{error}

Please check

• Internet Connection

• AI Service Configuration

• Database
"""
