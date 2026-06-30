import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
st.title("Analytics Loaded")
st.write("Hello Shobhraj")
st.title("Analytics Test")
st.write("Page Loaded Successfully")



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
    st.success("App Function Started")

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

    workshop = pd.read_sql_query(
        "SELECT * FROM workshop_info",
        connection
    )

    workshop = workshop.iloc[0]

    st.title("📈 Analytics Dashboard")

    st.caption(
        "Real-time analytics for N.F. Railway Mechanical Workshop, Dibrugarh."
    )

    st.divider()

    total_coaches = len(coaches)
    total_employees = len(employees)
    total_machines = len(machines)
    total_shops = len(shops)

    avg_efficiency = round(
        shops["efficiency"].mean(),
        2
    )

    avg_machine_health = round(
        machines["health_score"].mean(),
        2
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Workshop Shops",
        total_shops
    )

    col2.metric(
        "Employees",
        total_employees
    )

    col3.metric(
        "Machines",
        total_machines
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Coaches",
        total_coaches
    )

    col5.metric(
        "Avg Shop Efficiency",
        f"{avg_efficiency}%"
    )

    col6.metric(
        "Avg Machine Health",
        f"{avg_machine_health}%"
    )

    st.divider()
    st.subheader("📊 Workshop Performance Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        efficiency_chart = px.bar(
            shops,
            x="shop_name",
            y="efficiency",
            color="efficiency",
            text="efficiency",
            title="Shop Efficiency (%)",
            color_continuous_scale="Blues"
        )

        efficiency_chart.update_layout(
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False,
            xaxis_title="Workshop Shops",
            yaxis_title="Efficiency (%)"
        )

        st.plotly_chart(
            efficiency_chart,
            use_container_width=True
        )

    with chart_col2:

        machine_chart = px.bar(
            machines,
            x="machine_name",
            y="health_score",
            color="health_score",
            text="health_score",
            title="Machine Health Score",
            color_continuous_scale="Greens"
        )

        machine_chart.update_layout(
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False,
            xaxis_title="Machines",
            yaxis_title="Health Score (%)"
        )

        st.plotly_chart(
            machine_chart,
            use_container_width=True
        )

    st.divider()

    analytics_col1, analytics_col2 = st.columns(2)

    with analytics_col1:

        overhaul_data = (
            coaches["overhaul_type"]
            .value_counts()
            .reset_index()
        )

        overhaul_data.columns = [
            "Overhaul",
            "Coaches"
        ]

        overhaul_chart = px.pie(
            overhaul_data,
            names="Overhaul",
            values="Coaches",
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

    with analytics_col2:

        employee_chart = (
            employees["shop_name"]
            .value_counts()
            .reset_index()
        )

        employee_chart.columns = [
            "Workshop Shop",
            "Employees"
        ]

        employee_graph = px.bar(
            employee_chart,
            x="Workshop Shop",
            y="Employees",
            color="Employees",
            text="Employees",
            title="Employee Distribution by Shop",
            color_continuous_scale="Oranges"
        )

        employee_graph.update_layout(
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            employee_graph,
            use_container_width=True
        )

    st.divider()

    st.subheader("🚆 Coach Progress Analysis")

    progress_chart = px.histogram(
        coaches,
        x="progress",
        nbins=10,
        color_discrete_sequence=["#1565C0"],
        title="Coach Progress Distribution"
    )

    progress_chart.update_layout(
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Progress (%)",
        yaxis_title="Number of Coaches"
    )

    st.plotly_chart(
        progress_chart,
        use_container_width=True
    )

    st.divider()
    st.subheader("🏆 Executive Performance Summary")

    best_shop = shops.sort_values(
        by="efficiency",
        ascending=False
    ).iloc[0]

    best_machine = machines.sort_values(
        by="health_score",
        ascending=False
    ).iloc[0]

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        st.success(
            f"""
🏆 Best Performing Shop

Shop Name : {best_shop['shop_name']}

Efficiency : {best_shop['efficiency']}%

Completed Jobs : {best_shop['completed_jobs']}
"""
        )

    with summary_col2:

        st.success(
            f"""
⚙ Best Machine

Machine ID : {best_machine['machine_id']}

Machine : {best_machine['machine_name']}

Health Score : {best_machine['health_score']}%
"""
        )

    st.divider()

    st.subheader("🚨 Executive Alerts")

    delayed_coaches = coaches[
        coaches["progress"] < 50
    ]

    maintenance_due = machines[
        machines["machine_status"] == "Maintenance"
    ]

    low_efficiency = shops[
        shops["efficiency"] < 80
    ]

    alert_col1, alert_col2, alert_col3 = st.columns(3)

    alert_col1.metric(
        "Delayed Coaches",
        len(delayed_coaches)
    )

    alert_col2.metric(
        "Machines Under Maintenance",
        len(maintenance_due)
    )

    alert_col3.metric(
        "Low Efficiency Shops",
        len(low_efficiency)
    )

    st.divider()

    st.subheader("📋 Workshop Summary")

    total_active_jobs = int(
        shops["active_jobs"].sum()
    )

    total_completed_jobs = int(
        shops["completed_jobs"].sum()
    )

    completion_rate = round(
        (
            total_completed_jobs /
            (total_active_jobs + total_completed_jobs)
        ) * 100,
        2
    ) if (total_active_jobs + total_completed_jobs) > 0 else 0

    info1, info2, info3 = st.columns(3)

    info1.metric(
        "Active Jobs",
        total_active_jobs
    )

    info2.metric(
        "Completed Jobs",
        total_completed_jobs
    )

    info3.metric(
        "Completion Rate",
        f"{completion_rate}%"
    )

    st.divider()

    st.subheader("🤖 Executive Insights")

    insights = []

    if avg_efficiency >= 90:
        insights.append(
            "✅ Overall workshop efficiency is excellent."
        )
    else:
        insights.append(
            "⚠ Improve efficiency in low-performing shops."
        )

    if avg_machine_health >= 85:
        insights.append(
            "✅ Machine health across the workshop is good."
        )
    else:
        insights.append(
            "⚠ Schedule preventive maintenance for machines with lower health scores."
        )

    if len(delayed_coaches) > 0:
        insights.append(
            f"⚠ {len(delayed_coaches)} coaches are delayed and require immediate attention."
        )
    else:
        insights.append(
            "✅ No delayed coaches detected."
        )

    if len(low_efficiency) > 0:
        insights.append(
            f"⚠ {len(low_efficiency)} workshop shops have efficiency below 80%."
        )

    for insight in insights:
        st.info(insight)

    st.divider()

    st.caption(
        "Rail Sathi • Executive Analytics Dashboard | N.F. Railway Mechanical Workshop, Dibrugarh"
    )

    connection.close()
    
    
app()