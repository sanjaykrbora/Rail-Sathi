import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "railway.db"


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

    st.title("🤖 Rail Sathi AI")

    st.caption(
        "AI Powered Railway Workshop Assistant"
    )

    st.divider()

    st.info(
        """
        Ask anything related to

        • Coach Status

        • POH / IOH Progress

        • Employee Details

        • Machine Health

        • Workshop Shops

        • Maintenance Records
        """
    )

    query = st.text_input(
        "Ask Rail Sathi AI"
    )

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Coaches",
        len(coaches)
    )

    col2.metric(
        "Employees",
        len(employees)
    )

    col3.metric(
        "Machines",
        len(machines)
    )

    col4.metric(
        "Workshop Shops",
        len(shops)
    )

    st.divider()
    if query:

        question = query.lower().strip()

        response = ""

        if "coach" in question:

            coach = coaches[
                coaches["coach_number"]
                .astype(str)
                .str.contains(
                    question,
                    case=False,
                    na=False
                )
            ]

            if not coach.empty:

                coach = coach.iloc[0]

                response = f"""
🚆 Coach Number : {coach['coach_number']}

Coach Type : {coach['coach_type']}

Overhaul : {coach['overhaul_type']}

Current Shop : {coach['current_shop']}

Status : {coach['status']}

Progress : {coach['progress']}%

Expected Dispatch : {coach['expected_dispatch']}
"""

            else:

                response = "No matching coach found."

        elif "employee" in question:

            employee = employees[
                employees["employee_name"]
                .astype(str)
                .str.contains(
                    question.replace("employee", "").strip(),
                    case=False,
                    na=False
                )
            ]

            if not employee.empty:

                employee = employee.iloc[0]

                response = f"""
👷 Employee : {employee['employee_name']}

Employee ID : {employee['employee_id']}

Designation : {employee['designation']}

Department : {employee['department']}

Workshop Shop : {employee['shop_name']}

Status : {employee['status']}
"""

            else:

                response = "Employee not found."

        elif "machine" in question:

            running = len(
                machines[
                    machines["machine_status"] == "Running"
                ]
            )

            maintenance_count = len(
                machines[
                    machines["machine_status"] == "Maintenance"
                ]
            )

            breakdown = len(
                machines[
                    machines["machine_status"] == "Breakdown"
                ]
            )

            response = f"""
⚙ Machine Summary

Running : {running}

Maintenance : {maintenance_count}

Breakdown : {breakdown}
"""

        elif "poh" in question:

            total = len(
                coaches[
                    coaches["overhaul_type"] == "POH"
                ]
            )

            completed = len(
                coaches[
                    (coaches["overhaul_type"] == "POH") &
                    (coaches["status"] == "Completed")
                ]
            )

            response = f"""
🚆 POH Report

Total POH Coaches : {total}

Completed : {completed}

Remaining : {total - completed}
"""

        elif "ioh" in question:

            total = len(
                coaches[
                    coaches["overhaul_type"] == "IOH"
                ]
            )

            completed = len(
                coaches[
                    (coaches["overhaul_type"] == "IOH") &
                    (coaches["status"] == "Completed")
                ]
            )

            response = f"""
🚆 IOH Report

Total IOH Coaches : {total}

Completed : {completed}

Remaining : {total - completed}
"""

        elif "shop" in question:

            response = f"""
🏭 Workshop Information

Total Shops : {len(shops)}

Total Employees : {len(employees)}

Active Jobs : {shops['active_jobs'].sum()}

Completed Jobs : {shops['completed_jobs'].sum()}
"""

        elif "maintenance" in question:

            response = f"""
🔧 Maintenance Summary

Total Records : {len(maintenance)}

Preventive : {
len(
maintenance[
maintenance["maintenance_type"]=="Preventive"
]
)
}

Corrective : {
len(
maintenance[
maintenance["maintenance_type"]=="Corrective"
]
)
}
"""

        else:

            response = """
Sorry!

I can currently answer questions related to

• Coaches

• POH

• IOH

• Employees

• Machines

• Workshop

• Maintenance
"""

        st.session_state.chat_history.append(
            ("You", query)
        )

        st.session_state.chat_history.append(
            ("Rail Sathi AI", response)
        )

    st.subheader("💬 Conversation")

    for sender, message in st.session_state.chat_history:

        if sender == "You":

            st.chat_message("user").write(message)

        else:

            st.chat_message("assistant").write(message)

    st.divider()
    if query:

        question = query.lower().strip()

        response = ""

        if "coach" in question:

            coach = coaches[
                coaches["coach_number"]
                .astype(str)
                .str.contains(
                    question,
                    case=False,
                    na=False
                )
            ]

            if not coach.empty:

                coach = coach.iloc[0]

                response = f"""
🚆 Coach Number : {coach['coach_number']}

Coach Type : {coach['coach_type']}

Overhaul : {coach['overhaul_type']}

Current Shop : {coach['current_shop']}

Status : {coach['status']}

Progress : {coach['progress']}%

Expected Dispatch : {coach['expected_dispatch']}
"""

            else:

                response = "No matching coach found."

        elif "employee" in question:

            employee = employees[
                employees["employee_name"]
                .astype(str)
                .str.contains(
                    question.replace("employee", "").strip(),
                    case=False,
                    na=False
                )
            ]

            if not employee.empty:

                employee = employee.iloc[0]

                response = f"""
👷 Employee : {employee['employee_name']}

Employee ID : {employee['employee_id']}

Designation : {employee['designation']}

Department : {employee['department']}

Workshop Shop : {employee['shop_name']}

Status : {employee['status']}
"""

            else:

                response = "Employee not found."

        elif "machine" in question:

            running = len(
                machines[
                    machines["machine_status"] == "Running"
                ]
            )

            maintenance_count = len(
                machines[
                    machines["machine_status"] == "Maintenance"
                ]
            )

            breakdown = len(
                machines[
                    machines["machine_status"] == "Breakdown"
                ]
            )

            response = f"""
⚙ Machine Summary

Running : {running}

Maintenance : {maintenance_count}

Breakdown : {breakdown}
"""

        elif "poh" in question:

            total = len(
                coaches[
                    coaches["overhaul_type"] == "POH"
                ]
            )

            completed = len(
                coaches[
                    (coaches["overhaul_type"] == "POH") &
                    (coaches["status"] == "Completed")
                ]
            )

            response = f"""
🚆 POH Report

Total POH Coaches : {total}

Completed : {completed}

Remaining : {total - completed}
"""

        elif "ioh" in question:

            total = len(
                coaches[
                    coaches["overhaul_type"] == "IOH"
                ]
            )

            completed = len(
                coaches[
                    (coaches["overhaul_type"] == "IOH") &
                    (coaches["status"] == "Completed")
                ]
            )

            response = f"""
🚆 IOH Report

Total IOH Coaches : {total}

Completed : {completed}

Remaining : {total - completed}
"""

        elif "shop" in question:

            response = f"""
🏭 Workshop Information

Total Shops : {len(shops)}

Total Employees : {len(employees)}

Active Jobs : {shops['active_jobs'].sum()}

Completed Jobs : {shops['completed_jobs'].sum()}
"""

        elif "maintenance" in question:

            response = f"""
🔧 Maintenance Summary

Total Records : {len(maintenance)}

Preventive : {
len(
maintenance[
maintenance["maintenance_type"]=="Preventive"
]
)
}

Corrective : {
len(
maintenance[
maintenance["maintenance_type"]=="Corrective"
]
)
}
"""

        else:

            response = """
Sorry!

I can currently answer questions related to

• Coaches

• POH

• IOH

• Employees

• Machines

• Workshop

• Maintenance
"""

        st.session_state.chat_history.append(
            ("You", query)
        )

        st.session_state.chat_history.append(
            ("Rail Sathi AI", response)
        )

    st.subheader("💬 Conversation")

    for sender, message in st.session_state.chat_history:

        if sender == "You":

            st.chat_message("user").write(message)

        else:

            st.chat_message("assistant").write(message)

    st.divider()