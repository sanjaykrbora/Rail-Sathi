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

    st.title("🚆 Coach Tracking")

    st.caption(
        "Track every coach from arrival to dispatch in the workshop."
    )

    st.divider()

    filter1, filter2, filter3, filter4 = st.columns(4)

    coach_search = filter1.text_input(
        "Coach Number"
    )

    overhaul_filter = filter2.selectbox(
        "Overhaul",
        [
            "All",
            "POH",
            "IOH"
        ]
    )

    status_filter = filter3.selectbox(
        "Status",
        ["All"] +
        sorted(
            coaches["status"].dropna().unique().tolist()
        )
    )

    shop_filter = filter4.selectbox(
        "Current Shop",
        ["All"] +
        sorted(
            coaches["current_shop"].dropna().unique().tolist()
        )
    )

    filtered_data = coaches.copy()

    if coach_search:

        filtered_data = filtered_data[
            filtered_data["coach_number"]
            .astype(str)
            .str.contains(
                coach_search,
                case=False,
                na=False
            )
        ]

    if overhaul_filter != "All":

        filtered_data = filtered_data[
            filtered_data["overhaul_type"] ==
            overhaul_filter
        ]

    if status_filter != "All":

        filtered_data = filtered_data[
            filtered_data["status"] ==
            status_filter
        ]

    if shop_filter != "All":

        filtered_data = filtered_data[
            filtered_data["current_shop"] ==
            shop_filter
        ]

    total = len(filtered_data)

    completed = len(
        filtered_data[
            filtered_data["status"] ==
            "Completed"
        ]
    )

    in_progress = len(
        filtered_data[
            filtered_data["status"] !=
            "Completed"
        ]
    )

    avg_progress = round(
        filtered_data["progress"].mean(),
        1
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "Total Coaches",
        total
    )

    kpi2.metric(
        "Completed",
        completed
    )

    kpi3.metric(
        "In Progress",
        in_progress
    )

    kpi4.metric(
        "Average Progress",
        f"{avg_progress}%"
    )

    st.divider()
    st.subheader("🚆 Coach Overview")

    display_data = filtered_data.copy()

    display_data = display_data.rename(
        columns={
            "coach_number": "Coach Number",
            "coach_type": "Coach Type",
            "overhaul_type": "Overhaul",
            "current_shop": "Current Shop",
            "status": "Status",
            "progress": "Progress (%)",
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

    coach_list = filtered_data["coach_number"].tolist()

    if coach_list:

        selected_coach = st.selectbox(
            "Select Coach",
            coach_list
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

            st.write(
                f"**Current Status:** {coach['status']}"
            )

            if coach["progress"] >= 90:

                st.success(
                    "Coach is almost ready for dispatch."
                )

            elif coach["progress"] >= 60:

                st.info(
                    "Coach overhaul is progressing normally."
                )

            elif coach["progress"] >= 30:

                st.warning(
                    "Coach requires continuous monitoring."
                )

            else:

                st.error(
                    "Coach is delayed and requires immediate attention."
                )

    else:

        st.warning(
            "No coach records found."
        )

    st.divider()

    csv = display_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Coach Report",
        data=csv,
        file_name="coach_tracking_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()
    st.subheader("📊 Coach Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        shop_data = (
            filtered_data["current_shop"]
            .value_counts()
            .reset_index()
        )

        shop_data.columns = [
            "Workshop Shop",
            "Coaches"
        ]

        shop_chart = px.bar(
            shop_data,
            x="Workshop Shop",
            y="Coaches",
            color="Coaches",
            text="Coaches",
            title="Shop-wise Coach Distribution",
            color_continuous_scale="Blues"
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

    with chart_col2:

        overhaul_data = (
            filtered_data["overhaul_type"]
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

    st.divider()

    st.subheader("🚨 Delayed Coaches")

    delayed = filtered_data[
        filtered_data["progress"] < 50
    ]

    if delayed.empty:

        st.success(
            "✅ No delayed coaches found."
        )

    else:

        st.dataframe(
            delayed[
                [
                    "coach_number",
                    "coach_type",
                    "current_shop",
                    "status",
                    "progress",
                    "expected_dispatch"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("🏆 Workshop Performance")

    performance = (
        filtered_data.groupby("current_shop")
        .agg(
            Average_Progress=("progress", "mean"),
            Coaches=("coach_number", "count")
        )
        .reset_index()
    )

    performance["Average_Progress"] = (
        performance["Average_Progress"]
        .round(2)
    )

    st.dataframe(
        performance.rename(
            columns={
                "current_shop": "Workshop Shop",
                "Average_Progress": "Average Progress (%)"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    if not performance.empty:

        best_shop = performance.sort_values(
            by="Average_Progress",
            ascending=False
        ).iloc[0]

        st.success(
            f"""
🏆 Best Performing Shop

Shop : {best_shop['current_shop']}

Average Progress : {best_shop['Average_Progress']}%

Total Coaches : {best_shop['Coaches']}
"""
        )

    st.divider()

    st.subheader("📌 Executive Summary")

    summary1, summary2, summary3 = st.columns(3)

    summary1.metric(
        "Average Progress",
        f"{filtered_data['progress'].mean():.1f}%"
    )

    summary2.metric(
        "Completed Coaches",
        len(
            filtered_data[
                filtered_data["status"] == "Completed"
            ]
        )
    )

    summary3.metric(
        "Delayed Coaches",
        len(delayed)
    )

    st.divider()

    st.caption(
        "Rail Sathi • Coach Tracking Module | N.F. Railway Mechanical Workshop, Dibrugarh"
    )

    connection.close()

