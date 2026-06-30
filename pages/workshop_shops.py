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

    shops = pd.read_sql_query(
        "SELECT * FROM shops",
        connection
    )

    st.title("🏭 Workshop Shops")

    st.caption(
        "Monitor all workshop shops, staff strength and overall performance."
    )

    st.divider()

    search_col, efficiency_col = st.columns(2)

    shop_search = search_col.text_input(
        "Search Shop"
    )

    efficiency_filter = efficiency_col.selectbox(
        "Minimum Efficiency",
        [
            "All",
            "70%",
            "80%",
            "90%",
            "95%"
        ]
    )

    filtered_data = shops.copy()

    if shop_search:

        filtered_data = filtered_data[
            filtered_data["shop_name"]
            .str.contains(
                shop_search,
                case=False,
                na=False
            )
        ]

    if efficiency_filter != "All":

        minimum_efficiency = int(
            efficiency_filter.replace("%", "")
        )

        filtered_data = filtered_data[
            filtered_data["efficiency"] >= minimum_efficiency
        ]

    st.divider()

    total_shops = len(filtered_data)

    total_staff = int(
        filtered_data["total_staff"].sum()
    )

    active_jobs = int(
        filtered_data["active_jobs"].sum()
    )

    completed_jobs = int(
        filtered_data["completed_jobs"].sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Workshop Shops",
        total_shops
    )

    col2.metric(
        "Total Staff",
        total_staff
    )

    col3.metric(
        "Active Jobs",
        active_jobs
    )

    col4.metric(
        "Completed Jobs",
        completed_jobs
    )

    st.divider()
    st.subheader("🏭 Workshop Shop Details")

    display_data = filtered_data.copy()

    display_data = display_data.rename(
        columns={
            "shop_name": "Shop Name",
            "head_of_shop": "Head of Shop",
            "total_staff": "Total Staff",
            "active_jobs": "Active Jobs",
            "completed_jobs": "Completed Jobs",
            "efficiency": "Efficiency (%)"
        }
    )

    st.dataframe(
        display_data[
            [
                "Shop Name",
                "Head of Shop",
                "Total Staff",
                "Active Jobs",
                "Completed Jobs",
                "Efficiency (%)"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🔍 Shop Information")

    shop_list = filtered_data["shop_name"].tolist()

    if shop_list:

        selected_shop = st.selectbox(
            "Select Workshop Shop",
            shop_list
        )

        shop = filtered_data[
            filtered_data["shop_name"] == selected_shop
        ].iloc[0]

        left, right = st.columns([1, 2])

        with left:

            st.metric(
                "Efficiency",
                f"{shop['efficiency']}%"
            )

            st.metric(
                "Total Staff",
                int(shop["total_staff"])
            )

            st.metric(
                "Active Jobs",
                int(shop["active_jobs"])
            )

        with right:

            st.markdown("### Shop Information")

            st.write(
                f"**Shop Name:** {shop['shop_name']}"
            )

            st.write(
                f"**Head of Shop:** {shop['head_of_shop']}"
            )

            st.write(
                f"**Completed Jobs:** {shop['completed_jobs']}"
            )

            st.write(
                f"**Efficiency:** {shop['efficiency']}%"
            )

            completion_rate = 0

            total_jobs = (
                shop["active_jobs"] +
                shop["completed_jobs"]
            )

            if total_jobs > 0:

                completion_rate = (
                    shop["completed_jobs"] /
                    total_jobs
                )

            st.write("### Job Completion")

            st.progress(completion_rate)

            st.caption(
                f"{completion_rate * 100:.1f}% Jobs Completed"
            )

    else:

        st.warning(
            "No workshop shop found."
        )

    st.divider()

    csv = display_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Workshop Report",
        data=csv,
        file_name="workshop_shops_report.csv",
        mime="text/csv"
    )

    st.divider()
    st.subheader("📊 Workshop Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        efficiency_chart = px.bar(
            filtered_data,
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

        jobs_data = pd.DataFrame({
            "Category": ["Active Jobs", "Completed Jobs"],
            "Count": [
                filtered_data["active_jobs"].sum(),
                filtered_data["completed_jobs"].sum()
            ]
        })

        jobs_chart = px.pie(
            jobs_data,
            names="Category",
            values="Count",
            hole=0.45,
            title="Active vs Completed Jobs"
        )

        jobs_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            jobs_chart,
            use_container_width=True
        )

    st.divider()

    st.subheader("👨‍🏭 Staff Distribution")

    staff_chart = px.bar(
        filtered_data,
        x="shop_name",
        y="total_staff",
        color="total_staff",
        text="total_staff",
        color_continuous_scale="Greens",
        title="Staff Strength by Workshop Shop"
    )

    staff_chart.update_layout(
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
        coloraxis_showscale=False,
        xaxis_title="Workshop Shops",
        yaxis_title="Number of Employees"
    )

    st.plotly_chart(
        staff_chart,
        use_container_width=True
    )

    st.divider()

    st.subheader("🏆 Best Performing Shop")

    best_shop = filtered_data.sort_values(
        by="efficiency",
        ascending=False
    ).iloc[0]

    best_col1, best_col2, best_col3 = st.columns(3)

    best_col1.metric(
        "Best Shop",
        best_shop["shop_name"]
    )

    best_col2.metric(
        "Efficiency",
        f"{best_shop['efficiency']}%"
    )

    best_col3.metric(
        "Head of Shop",
        best_shop["head_of_shop"]
    )

    st.divider()

    st.caption(
        "Rail Sathi • Workshop Shop Management Module"
    )

    connection.close()