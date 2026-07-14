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
            return f"There are currently {len(poh_coaches)} coaches undergoing POH (Periodic Overhaul)."

        # Intent: Employees in a specific shop
        if "employees" in question and "shop" in question:
            # try to extract shop name
            for shop_name in shops['shop_name'].dropna().unique():
                if shop_name.lower() in question:
                    shop_emps = employees[employees['shop_name'].str.lower() == shop_name.lower()]
                    names = ", ".join(shop_emps['employee_name'].tolist()[:10])
                    count = len(shop_emps)
                    return f"There are {count} employees working in the {shop_name}. Some of them are: {names}."
            
            return f"We have {int(workshop.iloc[0]['total_employees'])} total employees across all shops."

        # Intent: Critical machines
        if "critical" in question and "machine" in question:
            critical_machines = machines[machines['status'].str.contains('Critical', case=False, na=False)]
            if len(critical_machines) == 0:
                return "Good news! There are currently no machines in critical status."
            
            names = ", ".join(critical_machines['machine_name'].tolist())
            return f"There are {len(critical_machines)} critical machines requiring immediate attention: {names}."
            
        # Intent: How many coaches
        if "how many coaches" in question or "total coaches" in question:
            return f"There are a total of {len(coaches)} coaches currently registered in the workshop database."

        # Fallback / Generic search
        if "maintenance" in question:
            pending = maintenance[maintenance['status'] == 'Pending']
            return f"There are {len(pending)} pending maintenance tasks currently logged in the system."

        return "I am the Rail Sathi Custom AI. I have analyzed the workshop database, but I need a more specific question about coaches, employees, machines, or maintenance to give you an exact answer."

    except Exception as error:
        return f"❌ Custom AI Engine Error: {error}"
