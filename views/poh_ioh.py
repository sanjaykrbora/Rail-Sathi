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

    coaches = pd.read_sql_query(
        "SELECT * FROM coaches",
        connection
    )

    st.title("🚆 POH & IOH Management")

    st.caption(
        "Track Periodic Overhaul (POH) and Intermediate Overhaul (IOH) progress."
    )

    st.divider()

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    overhaul_filter = filter_col1.selectbox(
        "Overhaul Type",
        [
            "All",
            "POH",
            "IOH"
        ]
    )

    status_filter = filter_col2.selectbox(
        "Status",
        [
            "All"
        ] + sorted(
            coaches["status"].dropna().unique().tolist()
        )
    )

    search = filter_col3.text_input(
        "Coach Number"
    )

    filtered_data = coaches.copy()

    if overhaul_filter != "All":

        filtered_data = filtered_data[
            filtered_data["overhaul_type"] == overhaul_filter
        ]

    if status_filter != "All":

        filtered_data = filtered_data[
            filtered_data["status"] == status_filter
        ]

    if search:

        filtered_data = filtered_data[
            filtered_data["coach_number"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    total = len(filtered_data)

    poh = len(
        filtered_data[
            filtered_data["overhaul_type"] == "POH"
        ]
    )

    ioh = len(
        filtered_data[
            filtered_data["overhaul_type"] == "IOH"
        ]
    )

    completed = len(
        filtered_data[
            filtered_data["status"] == "Completed"
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Coaches",
        total
    )

    c2.metric(
        "POH",
        poh
    )

    c3.metric(
        "IOH",
        ioh
    )

    c4.metric(
        "Completed",
        completed
    )

    st.divider()
    st.subheader("🚆 POH / IOH Coach Details")

    display_data = filtered_data.copy()

    display_data = display_data.rename(
        columns={
            "coach_number": "Coach Number",
            "coach_type": "Coach Type",
            "overhaul_type": "Overhaul Type",
            "current_shop": "Current Shop",
            "status": "Status",
            "arrival_date": "Arrival Date",
            "expected_dispatch": "Expected Dispatch",
            "progress": "Progress (%)"
        }
    )

    st.dataframe(
        display_data[
            [
                "Coach Number",
                "Coach Type",
                "Overhaul Type",
                "Current Shop",
                "Status",
                "Progress (%)",
                "Arrival Date",
                "Expected Dispatch"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("📋 Coach Information")

    coach_numbers = filtered_data["coach_number"].tolist()

    if coach_numbers:

        selected_coach = st.selectbox(
            "Select Coach",
            coach_numbers
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
                float(coach["progress"]) / 100
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

            st.markdown("### Coach Details")

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

            st.write(
                f"**Current Shop:** {coach['current_shop']}"
            )

    else:

        st.warning(
            "No coach records found."
        )

    st.divider()

    csv = display_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download POH / IOH Report",
        data=csv,
        file_name="poh_ioh_report.csv",
        mime="text/csv"
    )

    st.divider()
    st.subheader("📊 POH / IOH Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        overhaul_summary = (
            filtered_data["overhaul_type"]
            .value_counts()
            .reset_index()
        )

        overhaul_summary.columns = [
            "Overhaul Type",
            "Coaches"
        ]

        overhaul_chart = px.pie(
            overhaul_summary,
            names="Overhaul Type",
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

    with chart_col2:

        shop_summary = (
            filtered_data["current_shop"]
            .value_counts()
            .reset_index()
        )

        shop_summary.columns = [
            "Workshop Shop",
            "Coaches"
        ]

        shop_chart = px.bar(
            shop_summary,
            x="Workshop Shop",
            y="Coaches",
            color="Coaches",
            text="Coaches",
            color_continuous_scale="Blues",
            title="Shop-wise Coach Distribution"
        )

        shop_chart.update_layout(
            height=420,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            shop_chart,
            use_container_width=True
        )

    st.divider()

    st.subheader("🎯 Monthly Target Progress")

    poh_target = 68
    ioh_target = 55

    poh_completed = len(
        filtered_data[
            filtered_data["overhaul_type"] == "POH"
        ]
    )

    ioh_completed = len(
        filtered_data[
            filtered_data["overhaul_type"] == "IOH"
        ]
    )

    target_col1, target_col2 = st.columns(2)

    with target_col1:

        st.write("### POH Target")

        st.progress(
            min(poh_completed / poh_target, 1.0)
        )

        st.caption(
            f"{poh_completed} / {poh_target} Coaches"
        )

    with target_col2:

        st.write("### IOH Target")

        st.progress(
            min(ioh_completed / ioh_target, 1.0)
        )

        st.caption(
            f"{ioh_completed} / {ioh_target} Coaches"
        )

    st.divider()

    st.subheader("⚠️ Delayed Coaches")

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

    st.subheader("📌 Summary")

    avg_progress = round(
        filtered_data["progress"].mean(),
        2
    )

    summary1, summary2, summary3 = st.columns(3)

    summary1.metric(
        "Average Progress",
        f"{avg_progress}%"
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
        "Rail Sathi • POH & IOH Management Module"
    )

    connection.close()

