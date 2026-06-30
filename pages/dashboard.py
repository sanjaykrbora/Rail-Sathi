import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "railway.db"


def load_css():
    css_file = BASE_DIR / "css" / "style.css"

    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as file:
            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )


def get_connection():
    return sqlite3.connect(DB_PATH)


def app():

    load_css()

    connection = get_connection()

    workshop = pd.read_sql_query(
        "SELECT * FROM workshop_info",
        connection
    )

    shops = pd.read_sql_query(
        "SELECT * FROM shops",
        connection
    )

    coaches = pd.read_sql_query(
        "SELECT * FROM coaches",
        connection
    )

    machines = pd.read_sql_query(
        "SELECT * FROM machines",
        connection
    )

    workshop = workshop.iloc[0]

    st.markdown(
        f"""
        <div class="header">
            <h1>🚆 Rail Sathi</h1>
            <p>{workshop['workshop_name']}</p>
            <h5>{workshop['railway_zone']} • {workshop['location']}</h5>
        </div>
        """,
        unsafe_allow_html=True
    )

    employee_col, shop_col, poh_col, ioh_col = st.columns(4)

    employee_col.metric(
        "Employees",
        workshop["total_employees"]
    )

    shop_col.metric(
        "Workshop Shops",
        workshop["total_shops"]
    )

    poh_col.metric(
        "Monthly POH",
        workshop["monthly_poh_target"]
    )

    ioh_col.metric(
        "Monthly IOH",
        workshop["monthly_ioh_target"]
    )

    st.divider()

    st.subheader("Workshop Analytics")
    analytics_col, status_col = st.columns(2)

    with analytics_col:

        shop_chart = px.bar(
            shops,
            x="shop_name",
            y="efficiency",
            color="efficiency",
            text="efficiency",
            title="Shop Efficiency (%)",
            color_continuous_scale="Blues"
        )

        shop_chart.update_layout(
            height=430,
            xaxis_title="Workshop Shops",
            yaxis_title="Efficiency (%)",
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            shop_chart,
            use_container_width=True
        )

    with status_col:

        coach_status = (
            coaches["status"]
            .value_counts()
            .reset_index()
        )

        coach_status.columns = [
            "Status",
            "Total"
        ]

        status_chart = px.pie(
            coach_status,
            names="Status",
            values="Total",
            hole=0.45,
            title="Coach Status"
        )

        status_chart.update_layout(
            height=430,
            showlegend=True
        )

        st.plotly_chart(
            status_chart,
            use_container_width=True
        )

    st.divider()

    machine_col, overhaul_col = st.columns(2)

    with machine_col:

        machine_data = (
            machines["machine_status"]
            .value_counts()
            .reset_index()
        )

        machine_data.columns = [
            "Status",
            "Machines"
        ]

        machine_chart = px.bar(
            machine_data,
            x="Status",
            y="Machines",
            color="Status",
            text="Machines",
            title="Machine Status"
        )

        machine_chart.update_layout(
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            machine_chart,
            use_container_width=True
        )

    with overhaul_col:

        overhaul_data = (
            coaches["overhaul_type"]
            .value_counts()
            .reset_index()
        )

        overhaul_data.columns = [
            "Overhaul",
            "Total Coaches"
        ]

        overhaul_chart = px.pie(
            overhaul_data,
            names="Overhaul",
            values="Total Coaches",
            hole=0.45,
            title="POH vs IOH Distribution"
        )

        overhaul_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            overhaul_chart,
            use_container_width=True
        )

    st.divider()

    st.subheader("Workshop Performance")

    performance_table = shops[
        [
            "shop_name",
            "total_staff",
            "active_jobs",
            "completed_jobs",
            "efficiency"
        ]
    ]

    st.dataframe(
        performance_table,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Coach Progress")

    coach_table = coaches[
        [
            "coach_number",
            "coach_type",
            "overhaul_type",
            "current_shop",
            "status",
            "progress"
        ]
    ]

    st.dataframe(
        coach_table,
        use_container_width=True,
        hide_index=True
    )

    connection.close()
    st.divider()

    st.subheader("📌 Workshop Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        running_machines = len(
            machines[machines["machine_status"] == "Running"]
        )

        maintenance_machines = len(
            machines[machines["machine_status"] == "Maintenance"]
        )

        completed_coaches = len(
            coaches[coaches["status"] == "Completed"]
        )

        st.info(
            f"""
            🚆 Total Coaches : {len(coaches)}

            ✅ Completed Coaches : {completed_coaches}

            ⚙️ Running Machines : {running_machines}

            🔧 Machines Under Maintenance : {maintenance_machines}
            """
        )

    with summary_col2:

        active_jobs = shops["active_jobs"].sum()
        completed_jobs = shops["completed_jobs"].sum()

        avg_efficiency = round(
            shops["efficiency"].mean(),
            2
        )

        st.success(
            f"""
            📋 Active Jobs : {active_jobs}

            ✔️ Completed Jobs : {completed_jobs}

            📈 Average Workshop Efficiency : {avg_efficiency}%
            """
        )

    st.divider()

    st.subheader("🏭 Shop Wise Active Jobs")

    active_job_chart = px.bar(
        shops,
        x="shop_name",
        y="active_jobs",
        color="active_jobs",
        text="active_jobs",
        color_continuous_scale="Turbo"
    )

    active_job_chart.update_layout(
        xaxis_title="Workshop Shops",
        yaxis_title="Active Jobs",
        height=450,
        plot_bgcolor="white",
        paper_bgcolor="white",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        active_job_chart,
        use_container_width=True
    )

    st.divider()

    st.subheader("📈 Workshop Statistics")

    stat_col1, stat_col2, stat_col3 = st.columns(3)

    stat_col1.metric(
        "Running Machines",
        running_machines
    )

    stat_col2.metric(
        "Completed Coaches",
        completed_coaches
    )

    stat_col3.metric(
        "Workshop Efficiency",
        f"{avg_efficiency}%"
    )

    st.divider()

    st.subheader("🚆 Recent Coaches")

    recent_coaches = coaches.sort_values(
        by="arrival_date",
        ascending=False
    ).head(10)

    st.dataframe(
        recent_coaches,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.caption(
        "Rail Sathi v1.0 • N.F. Railway Mechanical Workshop, Dibrugarh"
    )

    connection.close()
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

    st.title("🚆 Coach Tracking")

    st.caption(
        "Monitor coach movement, overhaul progress and workshop status."
    )

    st.divider()

    search_col, type_col, status_col = st.columns(3)

    coach_search = search_col.text_input(
        "Search Coach Number"
    )

    overhaul_filter = type_col.selectbox(
        "Overhaul Type",
        ["All", "POH", "IOH"]
    )

    status_filter = status_col.selectbox(
        "Coach Status",
        [
            "All",
            "Received",
            "Inspection",
            "Machine Shop",
            "Wheel Shop",
            "Welding Shop",
            "Corrosion Shop",
            "Painting",
            "Testing",
            "Ready for Dispatch",
            "Completed"
        ]
    )

    filtered_data = coaches.copy()

    if coach_search:
        filtered_data = filtered_data[
            filtered_data["coach_number"]
            .str.contains(
                coach_search,
                case=False
            )
        ]

    if overhaul_filter != "All":
        filtered_data = filtered_data[
            filtered_data["overhaul_type"] == overhaul_filter
        ]

    if status_filter != "All":
        filtered_data = filtered_data[
            filtered_data["status"] == status_filter
        ]

    st.divider()

    total_coaches = len(filtered_data)

    poh_count = len(
        filtered_data[
            filtered_data["overhaul_type"] == "POH"
        ]
    )

    ioh_count = len(
        filtered_data[
            filtered_data["overhaul_type"] == "IOH"
        ]
    )

    completed_count = len(
        filtered_data[
            filtered_data["status"] == "Completed"
        ]
    )

    card1, card2, card3, card4 = st.columns(4)

    card1.metric(
        "Total Coaches",
        total_coaches
    )

    card2.metric(
        "POH Coaches",
        poh_count
    )

    card3.metric(
        "IOH Coaches",
        ioh_count
    )

    card4.metric(
        "Completed",
        completed_count
    )

    st.divider()
    st.subheader("Coach Status")

    display_data = filtered_data.copy()

    display_data["Progress"] = (
        display_data["progress"].astype(str) + "%"
    )

    display_data = display_data.rename(
        columns={
            "coach_number": "Coach Number",
            "coach_type": "Coach Type",
            "overhaul_type": "Overhaul",
            "current_shop": "Current Shop",
            "status": "Status",
            "arrival_date": "Arrival Date",
            "expected_dispatch": "Expected Dispatch"
        }
    )

    st.dataframe(
        display_data[
            [
                "Coach Number",
                "Coach Type",
                "Overhaul",
                "Current Shop",
                "Status",
                "Progress",
                "Arrival Date",
                "Expected Dispatch"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Coach Progress")

    selected_coach = st.selectbox(
        "Select Coach",
        filtered_data["coach_number"]
    )

    coach = filtered_data[
        filtered_data["coach_number"] == selected_coach
    ].iloc[0]

    left, right = st.columns([1, 2])

    with left:

        st.metric(
            "Progress",
            f"{coach['progress']}%"
        )

        st.progress(
            int(coach["progress"]) / 100
        )

        st.metric(
            "Current Shop",
            coach["current_shop"]
        )

        st.metric(
            "Status",
            coach["status"]
        )

    with right:

        st.markdown("### Coach Information")

        st.write(
            f"**Coach Number:** {coach['coach_number']}"
        )

        st.write(
            f"**Coach Type:** {coach['coach_type']}"
        )

        st.write(
            f"**Overhaul Type:** {coach['overhaul_type']}"
        )

        st.write(
            f"**Arrival Date:** {coach['arrival_date']}"
        )

        st.write(
            f"**Expected Dispatch:** {coach['expected_dispatch']}"
        )

    st.divider()

    csv = display_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Coach Report",
        data=csv,
        file_name="coach_tracking_report.csv",
        mime="text/csv"
    )

    st.divider()
    st.subheader("📊 Coach Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        shop_distribution = (
            filtered_data["current_shop"]
            .value_counts()
            .reset_index()
        )

        shop_distribution.columns = [
            "Shop",
            "Coaches"
        ]

        import plotly.express as px

        shop_chart = px.bar(
            shop_distribution,
            x="Shop",
            y="Coaches",
            color="Coaches",
            text="Coaches",
            color_continuous_scale="Blues",
            title="Shop-wise Coach Distribution"
        )

        shop_chart.update_layout(
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            shop_chart,
            use_container_width=True
        )

    with chart_col2:

        overhaul_chart = (
            filtered_data["overhaul_type"]
            .value_counts()
            .reset_index()
        )

        overhaul_chart.columns = [
            "Overhaul",
            "Total"
        ]

        pie_chart = px.pie(
            overhaul_chart,
            names="Overhaul",
            values="Total",
            hole=0.45,
            title="POH vs IOH Distribution"
        )

        pie_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            pie_chart,
            use_container_width=True
        )

    st.divider()

    st.subheader("⚠ Delayed Coaches")

    delayed = filtered_data[
        filtered_data["progress"] < 50
    ]

    if delayed.empty:

        st.success(
            "No delayed coaches found."
        )

    else:

        st.dataframe(
            delayed[
                [
                    "coach_number",
                    "coach_type",
                    "current_shop",
                    "progress",
                    "expected_dispatch"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("📌 Quick Summary")

    summary1, summary2, summary3 = st.columns(3)

    summary1.metric(
        "Average Progress",
        f"{round(filtered_data['progress'].mean(),1)}%"
    )

    summary2.metric(
        "Highest Progress",
        f"{filtered_data['progress'].max()}%"
    )

    summary3.metric(
        "Lowest Progress",
        f"{filtered_data['progress'].min()}%"
    )

    st.divider()

    st.caption(
        "Rail Sathi • Smart Railway Workshop Management System"
    )

    connection.close()