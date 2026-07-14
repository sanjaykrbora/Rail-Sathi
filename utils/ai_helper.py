import pandas as pd
from utils.database_helper import fetch_table
import re

def get_database_context():
    pass

def ai_response(question):
    question = question.lower()
    
    try:
        coaches = fetch_table("coaches")
        employees = fetch_table("employees")
        machines = fetch_table("machines")
        shops = fetch_table("shops")
        maintenance = fetch_table("maintenance")
        workshop = fetch_table("workshop_info")

        # Intent: Coaches in POH
        if "coaches" in question and "poh" in question:
            poh_coaches = coaches[coaches['status'].str.contains('POH', case=False, na=False)]
            return f"👋 **Hello!** Based on the current workshop records, there are exactly **{len(poh_coaches)} coaches** undergoing POH (Periodic Overhaul) right now."

        # Intent: Employees in a specific shop
        if "employees" in question and "shop" in question:
            # try to extract shop name
            for shop_name in shops['shop_name'].dropna().unique():
                if shop_name.lower() in question:
                    shop_emps = employees[employees['shop_name'].str.lower() == shop_name.lower()]
                    names = ", ".join(shop_emps['employee_name'].tolist()[:10])
                    count = len(shop_emps)
                    return f"**Sure thing!** There are **{count} employees** currently assigned to the {shop_name}. \n\nHere are a few of them: {names}."
            
            return f"I couldn't find that specific shop, but we have **{int(workshop.iloc[0]['total_employees'])} total employees** working across all workshop shops."

        # Intent: Critical machines
        if "critical" in question and "machine" in question:
            critical_machines = machines[machines['status'].str.contains('Critical', case=False, na=False)]
            if len(critical_machines) == 0:
                return "🎉 **Good news!** I just checked the database and there are currently *no machines* in critical status."
            
            names = ", ".join(critical_machines['machine_name'].tolist())
            return f"⚠️ **Attention needed:** I found **{len(critical_machines)} critical machines** requiring immediate repair. \n\nThese machines are: {names}."
            
        # Intent: How many coaches
        if "how many coaches" in question or "total coaches" in question:
            return f"🚂 **Let's see...** There are a total of **{len(coaches)} coaches** currently registered in the workshop database!"

        # Fallback / Generic search
        if "maintenance" in question:
            pending = maintenance[maintenance['status'] == 'Pending']
            return f"🔧 We currently have **{len(pending)} pending maintenance tasks** logged in the system. \n\nLet me know if you need to look at specific machines!"

        return "🤖 **Hello! I am the Rail Sathi Custom AI.** \n\nI have successfully connected to the workshop database, but I need you to be slightly more specific. Try asking me about **coaches in POH**, **employees in a shop**, or **critical machines**!"

    except Exception as error:
        return f"❌ Custom AI Engine Error: {error}"
