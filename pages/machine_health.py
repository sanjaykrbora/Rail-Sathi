import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
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

    machines = pd.read_sql_query(
        "SELECT * FROM machines",
        connection
    )

    st.title("💚 Machine Health Monitor")

    st.caption(
        "Real-time machine health monitoring and condition analysis."
    )

    st.divider()

    search_col, shop_col, health_col = st.columns(3)

    machine_search = search_col.text_input(
        "Search Machine ID"
    )

    shop_options = ["All"] + sorted(
        machines["shop_name"].dropna().unique().tolist()
    )

    selected_shop = shop_col.selectbox(
        "Workshop Shop",
        shop_options
    )

    health_filter = health_col.selectbox(
        "Health Status",
        [
            "All",
            "Excellent",
            "Good",
            "Average",
            "Critical"
        ]
    )

    filtered_data = machines.copy()

    if machine_search:

        filtered_data = filtered_data[
            filtered_data["machine_id"]
            .astype(str)
            .str.contains(
                machine_search,
                case=False,
                na=False
            )
        ]

    if selected_shop != "All":

        filtered_data = filtered_data[
            filtered_data["shop_name"] == selected_shop
        ]

    if health_filter != "All":

        if health_filter == "Excellent":

            filtered_data = filtered_data[
                filtered_data["health_score"] >= 90
            ]

        elif health_filter == "Good":

            filtered_data = filtered_data[
                (filtered_data["health_score"] >= 75) &
                (filtered_data["health_score"] < 90)
            ]

        elif health_filter == "Average":

            filtered_data = filtered_data[
                (filtered_data["health_score"] >= 50) &
                (filtered_data["health_score"] < 75)
            ]

        elif health_filter == "Critical":

            filtered_data = filtered_data[
                filtered_data["health_score"] < 50
            ]

    total = len(filtered_data)

    excellent = len(
        filtered_data[
            filtered_data["health_score"] >= 90
        ]
    )

    healthy = len(
        filtered_data[
            (filtered_data["health_score"] >= 75) &
            (filtered_data["health_score"] < 90)
        ]
    )

    critical = len(
        filtered_data[
            filtered_data["health_score"] < 50
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Machines",
        total
    )

    c2.metric(
        "Excellent",
        excellent
    )

    c3.metric(
        "Healthy",
        healthy
    )

    c4.metric(
        "Critical",
        critical
    )

    st.divider()
    st.subheader("💚 Machine Health Overview")

    display_data = filtered_data.copy()

    display_data = display_data.rename(
        columns={
            "machine_id": "Machine ID",
            "machine_name": "Machine Name",
            "shop_name": "Workshop Shop",
            "machine_status": "Machine Status",
            "health_score": "Health Score",
            "last_service_date": "Last Service",
            "next_service_date": "Next Service"
        }
    )

    st.dataframe(
        display_data[
            [
                "Machine ID",
                "Machine Name",
                "Workshop Shop",
                "Machine Status",
                "Health Score",
                "Last Service",
                "Next Service"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("⚙️ Machine Details")

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

            st.progress(
                float(machine["health_score"]) / 100
            )

            st.metric(
                "Machine Status",
                machine["machine_status"]
            )

        with right:

            st.markdown("### Machine Information")

            st.write(
                f"**Machine ID:** {machine['machine_id']}"
            )

            st.write(
                f"**Machine Name:** {machine['machine_name']}"
            )

            st.write(
                f"**Workshop Shop:** {machine['shop_name']}"
            )

            st.write(
                f"**Last Service Date:** {machine['last_service_date']}"
            )

            st.write(
                f"**Next Service Date:** {machine['next_service_date']}"
            )

            if machine["health_score"] >= 90:
                st.success("Machine condition is Excellent.")

            elif machine["health_score"] >= 75:
                st.info("Machine condition is Good.")

            elif machine["health_score"] >= 50:
                st.warning("Machine requires inspection.")

            else:
                st.error("Critical machine. Immediate maintenance required.")

    else:

        st.warning(
            "No machine records found."
        )

    st.divider()

    csv = display_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Machine Health Report",
        data=csv,
        file_name="machine_health_report.csv",
        mime="text/csv"
    )

    st.divider()
    st.subheader("📊 Machine Health Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        health_distribution = pd.DataFrame(
            {
                "Health Status": [
                    "Excellent",
                    "Good",
                    "Average",
                    "Critical"
                ],
                "Machines": [
                    len(filtered_data[filtered_data["health_score"] >= 90]),
                    len(filtered_data[
                        (filtered_data["health_score"] >= 75) &
                        (filtered_data["health_score"] < 90)
                    ]),
                    len(filtered_data[
                        (filtered_data["health_score"] >= 50) &
                        (filtered_data["health_score"] < 75)
                    ]),
                    len(filtered_data[
                        filtered_data["health_score"] < 50
                    ])
                ]
            }
        )

        health_chart = px.pie(
            health_distribution,
            names="Health Status",
            values="Machines",
            hole=0.45,
            title="Machine Health Distribution"
        )

        health_chart.update_layout(
            height=420
        )

        st.plotly_chart(
            health_chart,
            use_container_width=True
        )

    with chart_col2:

        shop_health = filtered_data.groupby(
            "shop_name",
            as_index=False
        )["health_score"].mean()

        health_bar = px.bar(
            shop_health,
            x="shop_name",
            y="health_score",
            color="health_score",
            text="health_score",
            color_continuous_scale="Greens",
            title="Average Health Score by Shop"
        )

        health_bar.update_layout(
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False,
            xaxis_title="Workshop Shop",
            yaxis_title="Average Health Score (%)"
        )

        st.plotly_chart(
            health_bar,
            use_container_width=True
        )

    st.divider()

    st.subheader("🚨 Critical Machines")

    critical_machines = filtered_data[
        filtered_data["health_score"] < 50
    ]

    if critical_machines.empty:

        st.success(
            "✅ No critical machines found."
        )

    else:

        st.dataframe(
            critical_machines[
                [
                    "machine_id",
                    "machine_name",
                    "shop_name",
                    "health_score",
                    "machine_status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("🏆 Top Healthy Machines")

    top_machines = filtered_data.sort_values(
        by="health_score",
        ascending=False
    ).head(5)

    st.dataframe(
        top_machines[
            [
                "machine_id",
                "machine_name",
                "shop_name",
                "health_score",
                "machine_status"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    average_health = round(
        filtered_data["health_score"].mean(),
        2
    )

    summary1, summary2, summary3 = st.columns(3)

    summary1.metric(
        "Average Health",
        f"{average_health}%"
    )

    summary2.metric(
        "Healthy Machines",
        len(
            filtered_data[
                filtered_data["health_score"] >= 75
            ]
        )
    )

    summary3.metric(
        "Critical Machines",
        len(critical_machines)
    )

    st.divider()

    st.caption(
        "Rail Sathi • Machine Health Monitoring Module"
    )

    connection.close()