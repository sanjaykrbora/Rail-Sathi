import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth_helper import is_logged_in


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "databases" / "railway.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_css():

    css_path = BASE_DIR / "css" / "style.css"

    if css_path.exists():

        with open(css_path, "r", encoding="utf-8") as file:

            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )


def app():

    load_css()

    connection = get_connection()

    coaches = pd.read_sql_query(
        "SELECT * FROM coaches",
        connection
    )

    employees = pd.read_sql_query(
        "SELECT * FROM employees",
        connection
    )

    machines = pd.read_sql_query(
        "SELECT * FROM machines",
        connection
    )

    shops = pd.read_sql_query(
        "SELECT * FROM shops",
        connection
    )

    maintenance = pd.read_sql_query(
        "SELECT * FROM maintenance",
        connection
    )

    st.title("Rail Sathi AI")
    st.caption("Automated Task Assistant & AI Chat")
    st.divider()

    st.markdown("### 📋 Quick Automated Reports")
    st.write("Click a section below to automatically fetch the required reports:")
    
    if "menu_state" not in st.session_state:
        st.session_state.menu_state = "main"

    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🚆 Coaches", use_container_width=True):
        st.session_state.menu_state = "coaches"
    if c2.button("👨‍🔧 Employees", use_container_width=True):
        st.session_state.menu_state = "employees"
    if c3.button("⚙️ Machines", use_container_width=True):
        st.session_state.menu_state = "machines"
    if c4.button("🔧 Maintenance", use_container_width=True):
        st.session_state.menu_state = "maintenance"
        
    if st.session_state.menu_state == "coaches":
        st.dataframe(coaches, use_container_width=True, height=200)
    elif st.session_state.menu_state == "employees":
        st.dataframe(employees, use_container_width=True, height=200)
    elif st.session_state.menu_state == "machines":
        st.dataframe(machines, use_container_width=True, height=200)
    elif st.session_state.menu_state == "maintenance":
        st.dataframe(maintenance, use_container_width=True, height=200)

    st.divider()
    
    st.markdown("### 💬 Ask Rail Sathi AI")
    st.write("Click a question below to ask instantly, or type your own:")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    query = None
    
    # Interactive question buttons
    q1, q2, q3 = st.columns(3)
    if q1.button("How many coaches are currently undergoing POH?", use_container_width=True):
        query = "How many coaches are currently undergoing POH?"
    if q2.button("Which employees work in the Wheel Shop?", use_container_width=True):
        query = "Which employees work in the Wheel Shop?"
    if q3.button("Give me a summary of critical machine status.", use_container_width=True):
        query = "Give me a summary of critical machine status."

    # Display chat history
    for sender, message in st.session_state.chat_history:
        role = "user" if sender == "You" else "assistant"
        with st.chat_message(role):
            st.markdown(message)

    chat_input_val = st.chat_input("Ask Rail Sathi AI about the workshop...")
    if chat_input_val:
        query = chat_input_val

    if query:
        # Display user message
        st.session_state.chat_history.append(("You", query))
        with st.chat_message("user"):
            st.markdown(query)

        # Show typing indicator while generating response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing workshop data..."):
                try:
                    from utils.ai_helper import ai_response
                    response = ai_response(query)
                except Exception as e:
                    response = f"⚠️ Could not connect to AI service. Ensure AI keys are configured. Error: {e}"
                
            st.markdown(response)
        
        st.session_state.chat_history.append(("Rail Sathi AI", response))

    st.divider()
    st.caption("Rail Sathi AI • Proprietary Custom AI Model")

    connection.close()
