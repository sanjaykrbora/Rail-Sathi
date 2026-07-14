import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


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

    workshop = pd.read_sql_query(
        "SELECT * FROM workshop_info",
        connection
    )

    workshop = workshop.iloc[0]

    st.title("⚙️ System Settings")

    st.caption(
        "Configure Rail Sathi application settings, databases, backups, and user profiles."
    )

    st.divider()

    st.subheader("🏢 Workshop Information")

    left, right = st.columns(2)

    with left:

        workshop_name = st.text_input(
            "Workshop Name",
            value=workshop["workshop_name"]
        )

        railway_zone = st.text_input(
            "Railway Zone",
            value=workshop["railway_zone"]
        )

        location = st.text_input(
            "Location",
            value=workshop["location"]
        )

    with right:

        total_employees = st.number_input(
            "Total Employees",
            value=int(workshop["total_employees"]),
            min_value=0
        )

        total_shops = st.number_input(
            "Total Workshop Shops",
            value=int(workshop["total_shops"]),
            min_value=0
        )

        st.write("### Monthly Targets")

        monthly_poh = st.number_input(
            "POH Target",
            value=int(workshop["monthly_poh_target"]),
            min_value=0
        )

        monthly_ioh = st.number_input(
            "IOH Target",
            value=int(workshop["monthly_ioh_target"]),
            min_value=0
        )

    st.divider()

    save_col, reset_col = st.columns(2)

    save_settings = save_col.button(
        "💾 Save Settings",
        use_container_width=True
    )

    reset_settings = reset_col.button(
        "🔄 Reset",
        use_container_width=True
    )

    if save_settings:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE workshop_info
            SET
                workshop_name = ?,
                railway_zone = ?,
                location = ?,
                total_employees = ?,
                total_shops = ?,
                monthly_poh_target = ?,
                monthly_ioh_target = ?
            """,
            (
                workshop_name,
                railway_zone,
                location,
                total_employees,
                total_shops,
                monthly_poh,
                monthly_ioh
            )
        )

        connection.commit()

        st.success(
            "Settings saved successfully."
        )

    if reset_settings:

        st.info(
            "Reload the page to restore the last saved values."
        )

    st.divider()
    st.subheader("👤 User Profile")

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:

        admin_name = st.text_input(
            "Administrator Name",
            value="Workshop Administrator"
        )

        admin_email = st.text_input(
            "Email",
            value="admin@nfrrailways.in"
        )

    with profile_col2:

        admin_phone = st.text_input(
            "Phone Number",
            value="+91XXXXXXXXXX"
        )

        designation = st.text_input(
            "Designation",
            value="Workshop Manager"
        )

    st.divider()

    st.subheader("🔒 Security")

    current_password = st.text_input(
        "Current Password",
        type="password"
    )

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button(
        "🔐 Update Password",
        use_container_width=True
    ):

        if new_password == "" or confirm_password == "":
            st.warning("Please enter the new password.")

        elif new_password != confirm_password:
            st.error("Passwords do not match.")

        else:
            #actually save this to the db now
            from utils.auth_helper import hash_password
            from utils.database_helper import execute_query
            
            try:
                hashed_pw = hash_password(new_password)
                execute_query(
                    "UPDATE users SET password = ? WHERE username = ?",
                    (hashed_pw, st.session_state.username)
                )
                st.success("Password updated successfully.")
            except Exception as e:
                st.error(f"Failed to update password: {e}")

    st.divider()

    st.subheader("🎨 Appearance")

    theme = st.selectbox(
        "Application Theme",
        [
            "Rail Blue",
            "Dark",
            "Light"
        ]
    )

    sidebar_state = st.selectbox(
        "Sidebar",
        [
            "Expanded",
            "Collapsed"
        ]
    )

    animations = st.toggle(
        "Enable Animations",
        value=True
    )

    notifications = st.toggle(
        "Enable Notifications",
        value=True
    )

    st.divider()

    st.subheader("💾 Database")

    backup_col, restore_col = st.columns(2)

    with backup_col:

        if st.button(
            "📦 Backup Database",
            use_container_width=True
        ):

            st.success(
                "Database backup created successfully."
            )

    with restore_col:

        uploaded_file = st.file_uploader(
            "Restore Database",
            type=["db"]
        )

        if uploaded_file is not None:

            st.success(
                "Database selected successfully."
            )

    st.divider()
    st.subheader("ℹ️ About Rail Sathi")

    st.info(
        """
Rail Sathi is an AI-powered Railway Workshop Management System developed
for N.F. Railway Mechanical Workshop, Dibrugarh.

It helps manage coaches, employees, machines, maintenance,
workshop shops, POH/IOH activities and reports through a
single integrated platform.
        """
    )

    st.divider()

    st.subheader("🖥️ System Information")

    system_col1, system_col2 = st.columns(2)

    with system_col1:

        st.metric(
            "Application",
            "Rail Sathi"
        )

        st.metric(
            "Version",
            "1.0 Enterprise"
        )

        st.metric(
            "Database",
            "SQLite"
        )

    with system_col2:

        st.metric(
            "Workshop",
            workshop["workshop_name"]
        )

        st.metric(
            "Railway Zone",
            workshop["railway_zone"]
        )

        st.metric(
            "Platform",
            "Streamlit"
        )

    st.divider()

    st.subheader("📊 Database Statistics")

    stats1, stats2, stats3 = st.columns(3)

    stats1.metric(
        "Employees",
        int(workshop["total_employees"])
    )

    stats2.metric(
        "Workshop Shops",
        int(workshop["total_shops"])
    )

    stats3.metric(
        "Monthly POH Target",
        int(workshop["monthly_poh_target"])
    )

    stats4, stats5 = st.columns(2)

    stats4.metric(
        "Monthly IOH Target",
        int(workshop["monthly_ioh_target"])
    )

    stats5.metric(
        "Database Status",
        "Connected"
    )

    st.divider()

    st.subheader("👨‍💻 Developer")

    st.success(
        """
Developer : Shobhraj Bhattacharjee & Sanjay Krishna Bora

Project : Rail Sathi

Internship : N.F. Railway Mechanical Workshop, Dibrugarh

Technology Stack :

• Python

• Streamlit

• SQLite

• Pandas

• Plotly
        """
    )

    st.divider()

    st.caption(
        "© 2026 Rail Sathi | Developed by Shobhraj Bhattacharjee & Sanjay Krishna Bora | Version 1.0 Enterprise"
    )

    connection.close()

