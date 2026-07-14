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

    maintenance = pd.read_sql_query(
        "SELECT * FROM maintenance",
        connection
    )

    st.title("🔧 Maintenance Management")

    st.caption(
        "Track machine maintenance records, technicians and service history."
    )

    st.divider()

    search_col, type_col, tech_col = st.columns(3)

    machine_search = search_col.text_input(
        "Search Machine ID"
    )

    maintenance_types = ["All"] + sorted(
        maintenance["maintenance_type"].dropna().unique().tolist()
    )

    maintenance_filter = type_col.selectbox(
        "Maintenance Type",
        maintenance_types
    )

    technician_list = ["All"] + sorted(
        maintenance["technician"].dropna().unique().tolist()
    )

    technician_filter = tech_col.selectbox(
        "Technician",
        technician_list
    )

    filtered_data = maintenance.copy()

    if machine_search:

        filtered_data = filtered_data[
            filtered_data["machine_id"]
            .str.contains(
                machine_search,
                case=False,
                na=False
            )
        ]

    if maintenance_filter != "All":

        filtered_data = filtered_data[
            filtered_data["maintenance_type"] == maintenance_filter
        ]

    if technician_filter != "All":

        filtered_data = filtered_data[
            filtered_data["technician"] == technician_filter
        ]

    st.divider()

    from utils.auth_helper import current_role
    if current_role() in ["Admin", "Manager"]:
        with st.expander("➕ Log Maintenance Record"):
            with st.form("add_maintenance_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                new_mach_id = col1.text_input("Machine ID")
                new_type = col2.selectbox("Maintenance Type", ["Preventive", "Corrective", "Predictive"])
                
                col3, col4 = st.columns(2)
                new_date = col3.date_input("Maintenance Date")
                new_tech = col4.text_input("Technician Name")
                
                new_status = st.selectbox("Status", ["Completed", "In Progress", "Pending"])
                new_notes = st.text_area("Maintenance Notes")
                
                submitted = st.form_submit_button("Save Record")
                
                if submitted:
                    if not new_mach_id or not new_tech:
                        st.error("Machine ID and Technician Name are required.")
                    else:
                        try:
                            from utils.database_helper import execute_query
                            import uuid
                            record_id = str(uuid.uuid4())[:8]
                            execute_query(
                                """
                                INSERT INTO maintenance (record_id, machine_id, maintenance_type, maintenance_date, technician_name, status, notes)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                """,
                                (record_id, new_mach_id, new_type, str(new_date), new_tech, new_status, new_notes)
                            )
                            st.success("Maintenance record added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to add record: {e}")

    st.divider()

    total_records = len(filtered_data)

    preventive = len(
        filtered_data[
            filtered_data["maintenance_type"] == "Preventive"
        ]
    )

    corrective = len(
        filtered_data[
            filtered_data["maintenance_type"] == "Corrective"
        ]
    )

    technicians = filtered_data["technician"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Maintenance Records",
        total_records
    )

    col2.metric(
        "Preventive",
        preventive
    )

    col3.metric(
        "Corrective",
        corrective
    )

    col4.metric(
        "Technicians",
        technicians
    )

    st.divider()
    st.subheader("🔧 Maintenance Records")

    display_data = filtered_data.copy()

    display_data = display_data.rename(
        columns={
            "machine_id": "Machine ID",
            "machine_name": "Machine Name",
            "maintenance_type": "Maintenance Type",
            "maintenance_date": "Maintenance Date",
            "technician": "Technician",
            "remarks": "Remarks"
        }
    )

    st.dataframe(
        display_data[
            [
                "Machine ID",
                "Machine Name",
                "Maintenance Type",
                "Maintenance Date",
                "Technician",
                "Remarks"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🛠 Maintenance Details")

    maintenance_ids = filtered_data["id"].tolist()

    if maintenance_ids:

        selected_record = st.selectbox(
            "Select Maintenance Record",
            maintenance_ids
        )

        record = filtered_data[
            filtered_data["id"] == selected_record
        ].iloc[0]

        left, right = st.columns([1, 2])

        with left:

            st.metric(
                "Machine ID",
                record["machine_id"]
            )

            st.metric(
                "Maintenance Type",
                record["maintenance_type"]
            )

            st.metric(
                "Technician",
                record["technician"]
            )

        with right:

            st.markdown("### Maintenance Information")

            st.write(
                f"**Machine Name:** {record['machine_name']}"
            )

            st.write(
                f"**Maintenance Date:** {record['maintenance_date']}"
            )

            st.write(
                f"**Maintenance Type:** {record['maintenance_type']}"
            )

            st.write(
                f"**Technician:** {record['technician']}"
            )

            st.write(
                f"**Remarks:** {record['remarks']}"
            )

    else:

        st.warning(
            "No maintenance records available."
        )

    st.divider()

    csv = display_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Maintenance Report",
        data=csv,
        file_name="maintenance_report.csv",
        mime="text/csv"
    )

    st.divider()
    st.subheader("📊 Maintenance Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        maintenance_chart_data = (
            filtered_data["maintenance_type"]
            .value_counts()
            .reset_index()
        )

        maintenance_chart_data.columns = [
            "Maintenance Type",
            "Count"
        ]

        maintenance_chart = px.pie(
            maintenance_chart_data,
            names="Maintenance Type",
            values="Count",
            hole=0.45,
            title="Maintenance Type Distribution"
        )

        maintenance_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            maintenance_chart,
            use_container_width=True
        )

    with chart_col2:

        technician_chart_data = (
            filtered_data["technician"]
            .value_counts()
            .reset_index()
        )

        technician_chart_data.columns = [
            "Technician",
            "Jobs"
        ]

        technician_chart = px.bar(
            technician_chart_data,
            x="Technician",
            y="Jobs",
            color="Jobs",
            text="Jobs",
            color_continuous_scale="Blues",
            title="Technician-wise Maintenance"
        )

        technician_chart.update_layout(
            height=420,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            technician_chart,
            use_container_width=True
        )

    st.divider()

    st.subheader("📅 Recent Maintenance")

    recent_records = filtered_data.sort_values(
        by="maintenance_date",
        ascending=False
    ).head(10)

    st.dataframe(
        recent_records[
            [
                "machine_id",
                "machine_name",
                "maintenance_type",
                "maintenance_date",
                "technician",
                "remarks"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("📌 Maintenance Summary")

    summary1, summary2, summary3 = st.columns(3)

    summary1.metric(
        "Total Records",
        len(filtered_data)
    )

    summary2.metric(
        "Maintenance Types",
        filtered_data["maintenance_type"].nunique()
    )

    summary3.metric(
        "Technicians",
        filtered_data["technician"].nunique()
    )

    st.divider()

    st.caption(
        "Rail Sathi • Maintenance Management Module"
    )

    connection.close()

