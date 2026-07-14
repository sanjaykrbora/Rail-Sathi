import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
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

    employees = pd.read_sql_query(
        "SELECT * FROM employees",
        connection
    )
    
    workshop = pd.read_sql_query(
        "SELECT * FROM workshop_info",
        connection
    ).iloc[0]

    st.title("👷 Employee Management")

    st.caption(
        "Manage employees of N.F. Railway Mechanical Workshop, Dibrugarh."
    )

    st.divider()

    search_col, shop_col, designation_col = st.columns(3)

    employee_search = search_col.text_input(
        "Search Employee"
    )

    shop_options = ["All"] + sorted(
        employees["shop_name"].dropna().unique().tolist()
    )

    shop_filter = shop_col.selectbox(
        "Workshop Shop",
        shop_options
    )

    designation_options = ["All"] + sorted(
        employees["designation"].dropna().unique().tolist()
    )

    designation_filter = designation_col.selectbox(
        "Designation",
        designation_options
    )

    filtered_data = employees.copy()

    if employee_search:

        filtered_data = filtered_data[
            filtered_data["employee_name"]
            .str.contains(
                employee_search,
                case=False,
                na=False
            )
        ]

    if shop_filter != "All":

        filtered_data = filtered_data[
            filtered_data["shop_name"] == shop_filter
        ]

    if designation_filter != "All":

        filtered_data = filtered_data[
            filtered_data["designation"] == designation_filter
        ]

    st.divider()

    from utils.auth_helper import current_role
    if current_role() in ["Admin", "Manager"]:
        with st.expander("➕ Add New Employee"):
            with st.form("add_employee_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                new_name = col1.text_input("Employee Name")
                new_emp_id = col2.text_input("Employee ID")
                
                col3, col4 = st.columns(2)
                new_designation = col3.selectbox("Designation", ["Technician", "Supervisor", "Engineer", "Manager", "Inspector"])
                new_shop = col4.selectbox("Workshop Shop", ["Wheel Shop", "Bogie Shop", "Paint Shop", "Machine Shop", "Fitting Shop"])
                
                col5, col6 = st.columns(2)
                new_dept = col5.text_input("Department", value="Mechanical")
                new_phone = col6.text_input("Phone Number")
                
                submitted = st.form_submit_button("Save Employee")
                
                if submitted:
                    if not new_name or not new_emp_id:
                        st.error("Name and Employee ID are required.")
                    else:
                        try:
                            from utils.database_helper import execute_query
                            from datetime import date
                            execute_query(
                                """
                                INSERT INTO employees (employee_id, employee_name, designation, department, shop_name, status, phone, email, joining_date)
                                VALUES (?, ?, ?, ?, ?, 'Active', ?, ?, ?)
                                """,
                                (new_emp_id, new_name, new_designation, new_dept, new_shop, new_phone, f"{new_emp_id.lower()}@nfrrailways.in", str(date.today()))
                            )
                            st.success("Employee added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to add employee: {e}")

    st.divider()

    total_employees = int(workshop["total_employees"])

    active_employees = len(
        filtered_data[
            filtered_data["status"] == "Active"
        ]
    )

    inactive_employees = len(
        filtered_data[
            filtered_data["status"] != "Active"
        ]
    )

    total_shops = filtered_data["shop_name"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Employees",
        total_employees
    )

    col2.metric(
        "Active",
        active_employees
    )

    col3.metric(
        "Inactive",
        inactive_employees
    )

    col4.metric(
        "Departments",
        total_shops
    )

    st.divider()
    st.subheader("👨‍💼 Employee Records")

    display_data = filtered_data.copy()

    display_data = display_data.rename(
        columns={
            "employee_id": "Employee ID",
            "employee_name": "Employee Name",
            "designation": "Designation",
            "shop_name": "Workshop Shop",
            "department": "Department",
            "phone": "Phone",
            "email": "Email",
            "joining_date": "Joining Date",
            "status": "Status"
        }
    )

    display_columns = [
        "Employee ID",
        "Employee Name",
        "Designation",
        "Workshop Shop",
        "Department",
        "Phone",
        "Email",
        "Joining Date",
        "Status"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in display_data.columns
    ]

    st.dataframe(
        display_data[available_columns],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("👤 Employee Details")

    employee_ids = filtered_data["employee_id"].tolist()

    if employee_ids:

        selected_employee = st.selectbox(
            "Select Employee",
            employee_ids
        )

        employee = filtered_data[
            filtered_data["employee_id"] == selected_employee
        ].iloc[0]

        left, right = st.columns(2)

        with left:

            st.metric(
                "Employee ID",
                employee["employee_id"]
            )

            st.metric(
                "Designation",
                employee["designation"]
            )

            st.metric(
                "Status",
                employee["status"]
            )

        with right:

            st.markdown("### Employee Information")

            st.write(
                f"**Name:** {employee['employee_name']}"
            )

            st.write(
                f"**Department:** {employee.get('department', 'N/A')}"
            )

            st.write(
                f"**Workshop Shop:** {employee['shop_name']}"
            )

            st.write(
                f"**Phone:** {employee['phone']}"
            )

            st.write(
                f"**Email:** {employee.get('email', 'N/A')}"
            )

            st.write(
                f"**Joining Date:** {employee.get('joining_date', 'N/A')}"
            )

    else:

        st.warning("No employee records found.")

    st.divider()

    csv = display_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Employee Report",
        data=csv,
        file_name="employee_report.csv",
        mime="text/csv"
    )

    st.divider()
    st.subheader("📊 Employee Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        designation_data = (
            filtered_data["designation"]
            .value_counts()
            .reset_index()
        )

        designation_data.columns = [
            "Designation",
            "Employees"
        ]

        designation_chart = px.bar(
            designation_data,
            x="Designation",
            y="Employees",
            color="Employees",
            text="Employees",
            color_continuous_scale="Blues",
            title="Designation-wise Employees"
        )

        designation_chart.update_layout(
            height=420,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            designation_chart,
            use_container_width=True
        )

    with chart_col2:

        shop_data = (
            filtered_data["shop_name"]
            .value_counts()
            .reset_index()
        )

        shop_data.columns = [
            "Workshop Shop",
            "Employees"
        ]

        shop_chart = px.pie(
            shop_data,
            names="Workshop Shop",
            values="Employees",
            hole=0.45,
            title="Shop-wise Employee Distribution"
        )

        shop_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            shop_chart,
            use_container_width=True
        )

    st.divider()

    st.subheader("📌 Employee Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    summary_col1.metric(
        "Total Employees",
        int(workshop["total_employees"])
    )

    summary_col2.metric(
        "Workshop Shops",
        filtered_data["shop_name"].nunique()
    )

    summary_col3.metric(
        "Designations",
        filtered_data["designation"].nunique()
    )

    st.divider()

    st.caption(
        "Rail Sathi • Employee Management Module"
    )

    connection.close()

