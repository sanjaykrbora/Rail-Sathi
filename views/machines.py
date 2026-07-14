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

    machines = pd.read_sql_query(
        "SELECT * FROM machines",
        connection
    )

    st.title("⚙️ Machine Management")

    st.caption(
        "Monitor workshop machines, maintenance status and service schedule."
    )

    st.divider()

    search_col, shop_col, status_col = st.columns(3)

    machine_search = search_col.text_input(
        "Search Machine ID"
    )

    shop_options = ["All"] + sorted(
        machines["shop_name"].dropna().unique().tolist()
    )

    shop_filter = shop_col.selectbox(
        "Workshop Shop",
        shop_options
    )

    status_options = ["All"] + sorted(
        machines["machine_status"].dropna().unique().tolist()
    )

    status_filter = status_col.selectbox(
        "Machine Status",
        status_options
    )

    filtered_data = machines.copy()

    if machine_search:

        filtered_data = filtered_data[
            filtered_data["machine_id"]
            .str.contains(
                machine_search,
                case=False,
                na=False
            )
        ]

    if shop_filter != "All":

        filtered_data = filtered_data[
            filtered_data["shop_name"] == shop_filter
        ]

    if status_filter != "All":

        filtered_data = filtered_data[
            filtered_data["machine_status"] == status_filter
        ]

    st.divider()

    from utils.auth_helper import current_role
    if current_role() in ["Admin", "Manager"]:
        with st.expander("➕ Add New Machine"):
            with st.form("add_machine_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                new_mach_name = col1.text_input("Machine Name")
                new_mach_id = col2.text_input("Machine ID")
                
                col3, col4 = st.columns(2)
                new_type = col3.selectbox("Machine Type", ["CNC Lathe", "Hydraulic Press", "Milling Machine", "Welding Robot", "Drill Press"])
                new_shop = col4.selectbox("Workshop Shop", ["Wheel Shop", "Bogie Shop", "Paint Shop", "Machine Shop", "Fitting Shop"])
                
                col5, col6 = st.columns(2)
                new_status = col5.selectbox("Status", ["Running", "Maintenance", "Breakdown"])
                new_date = col6.date_input("Installation Date")
                
                submitted = st.form_submit_button("Save Machine")
                
                if submitted:
                    if not new_mach_name or not new_mach_id:
                        st.error("Name and Machine ID are required.")
                    else:
                        try:
                            from utils.database_helper import execute_query
                            from datetime import timedelta
                            next_maint = new_date + timedelta(days=90)
                            execute_query(
                                """
                                INSERT INTO machines (machine_id, machine_name, machine_type, shop_name, installation_date, last_maintenance, next_maintenance, machine_status)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                """,
                                (new_mach_id, new_mach_name, new_type, new_shop, str(new_date), str(new_date), str(next_maint), new_status)
                            )
                            st.success("Machine added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to add machine: {e}")

    st.divider()

    total_machines = len(filtered_data)

    running = len(
        filtered_data[
            filtered_data["machine_status"] == "Running"
        ]
    )

    maintenance = len(
        filtered_data[
            filtered_data["machine_status"] == "Maintenance"
        ]
    )

    breakdown = len(
        filtered_data[
            filtered_data["machine_status"] == "Breakdown"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Machines",
        total_machines
    )

    col2.metric(
        "Running",
        running
    )

    col3.metric(
        "Maintenance",
        maintenance
    )

    col4.metric(
        "Breakdown",
        breakdown
    )

    st.divider()
    st.subheader("⚙️ Machine Inventory")

    display_data = filtered_data.copy()

    display_data = display_data.rename(
        columns={
            "machine_id": "Machine ID",
            "machine_name": "Machine Name",
            "shop_name": "Workshop Shop",
            "machine_type": "Machine Type",
            "machine_status": "Status",
            "health_score": "Health Score",
            "last_service_date": "Last Service",
            "next_service_date": "Next Service"
        }
    )

    columns_to_display = [
        "Machine ID",
        "Machine Name",
        "Workshop Shop",
        "Machine Type",
        "Status",
        "Health Score",
        "Last Service",
        "Next Service"
    ]

    available_columns = [
        col for col in columns_to_display
        if col in display_data.columns
    ]

    st.dataframe(
        display_data[available_columns],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🔍 Machine Details")

    machine_ids = filtered_data["machine_id"].tolist()

    if machine_ids:

        selected_machine = st.selectbox(
            "Select Machine",
            machine_ids
        )

        machine = filtered_data[
            filtered_data["machine_id"] == selected_machine
        ].iloc[0]

        left, right = st.columns([1, 2])

        with left:

            st.metric(
                "Health Score",
                f"{machine['health_score']}%"
            )

            st.metric(
                "Status",
                machine["machine_status"]
            )

            st.metric(
                "Workshop",
                machine["shop_name"]
            )

        with right:

            st.markdown("### Machine Information")

            st.write(
                f"**Machine ID:** {machine['machine_id']}"
            )

            st.write(
                f"**Machine Name:** {machine['machine_name']}"
            )

            if "machine_type" in machine.index:
                st.write(
                    f"**Machine Type:** {machine['machine_type']}"
                )

            st.write(
                f"**Last Service:** {machine['last_service_date']}"
            )

            st.write(
                f"**Next Service:** {machine['next_service_date']}"
            )

    else:

        st.warning(
            "No machine records found."
        )

    st.divider()

    csv = display_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Machine Report",
        data=csv,
        file_name="machine_report.csv",
        mime="text/csv"
    )

    st.divider()
    st.subheader("📊 Machine Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        health_chart = px.histogram(
            filtered_data,
            x="health_score",
            nbins=10,
            title="Machine Health Score Distribution",
            color_discrete_sequence=["#1565C0"]
        )

        health_chart.update_layout(
            height=420,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Health Score (%)",
            yaxis_title="Machines"
        )

        st.plotly_chart(
            health_chart,
            use_container_width=True
        )

    with chart_col2:

        status_data = (
            filtered_data["machine_status"]
            .value_counts()
            .reset_index()
        )

        status_data.columns = [
            "Status",
            "Machines"
        ]

        status_chart = px.pie(
            status_data,
            names="Status",
            values="Machines",
            hole=0.45,
            title="Machine Status Distribution"
        )

        status_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            status_chart,
            use_container_width=True
        )

    st.divider()

    st.subheader("🔧 Machines Due For Service")

    due_service = filtered_data.sort_values(
        by="next_service_date"
    ).head(10)

    st.dataframe(
        due_service[
            [
                "machine_id",
                "machine_name",
                "shop_name",
                "machine_status",
                "health_score",
                "next_service_date"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("📌 Machine Summary")

    avg_health = round(
        filtered_data["health_score"].mean(),
        2
    )

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    summary_col1.metric(
        "Average Health",
        f"{avg_health}%"
    )

    summary_col2.metric(
        "Workshop Shops",
        filtered_data["shop_name"].nunique()
    )

    summary_col3.metric(
        "Machines",
        len(filtered_data)
    )

    st.divider()

    st.caption(
        "Rail Sathi • Machine Management Module"
    )

    connection.close()
    

