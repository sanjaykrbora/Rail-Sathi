import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "databases" / "railway.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_css():
    css_file = BASE_DIR / "css" / "style.css"
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def status_badge(status):
    colors = {
        "Completed":  ("#d4edda", "#155724"),
        "In Progress": ("#fff3cd", "#856404"),
        "Pending":    ("#f8d7da", "#721c24"),
        "Running":    ("#d4edda", "#155724"),
        "Maintenance": ("#fff3cd", "#856404"),
        "Idle":       ("#e2e3e5", "#383d41"),
    }
    bg, fg = colors.get(status, ("#e2e3e5", "#383d41"))
    return (
        f'<span style="background:{bg};color:{fg};padding:3px 10px;'
        f'border-radius:12px;font-size:0.78rem;font-weight:600;">{status}</span>'
    )


def app():
    load_css()

    conn = get_connection()
    workshop_df = pd.read_sql_query("SELECT * FROM workshop_info", conn)
    shops       = pd.read_sql_query("SELECT * FROM shops", conn)
    coaches     = pd.read_sql_query("SELECT * FROM coaches", conn)
    machines    = pd.read_sql_query("SELECT * FROM machines", conn)
    employees_df = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()

    ws = workshop_df.iloc[0]

    #crunch top numbers
    total_coaches       = len(coaches)
    completed_coaches   = len(coaches[coaches["status"] == "Completed"])
    in_progress_coaches = len(coaches[coaches["status"] == "In Progress"])
    running_machines    = len(machines[machines["machine_status"] == "Running"])
    maint_machines      = len(machines[machines["machine_status"] == "Maintenance"])
    active_jobs         = int(shops["active_jobs"].sum())
    completed_jobs      = int(shops["completed_jobs"].sum())
    avg_efficiency      = round(shops["efficiency"].mean(), 1)
    total_employees     = int(ws["total_employees"])

    now_str = datetime.now().strftime("%d %b %Y, %I:%M %p")

    #show hero banner
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%);
            border-radius: 16px;
            padding: 32px 36px;
            margin-bottom: 24px;
            color: white;
            box-shadow: 0 4px 20px rgba(13,71,161,0.4);
        ">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                <div>
                    <div style="font-size:0.82rem; letter-spacing:2px; text-transform:uppercase;
                                opacity:0.8; margin-bottom:6px;">
                        🚆 Rail Sathi &nbsp;•&nbsp; Executive Dashboard
                    </div>
                    <h1 style="margin:0; font-size:2rem; font-weight:700; color:white;">
                        {ws['workshop_name']}
                    </h1>
                    <p style="margin:6px 0 0; opacity:0.85; font-size:0.95rem;">
                        {ws['railway_zone']} &nbsp;|&nbsp; {ws['location']}
                    </p>
                </div>
                <div style="text-align:right; opacity:0.85; font-size:0.82rem; margin-top:4px;">
                    <div>🕐 {now_str}</div>
                    <div style="margin-top:6px;">
                        <span style="background:rgba(255,255,255,0.2); padding:4px 12px;
                                     border-radius:20px; font-size:0.78rem;">
                            🟢 System Online
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    #draw 4 stat boxes
    c1, c2, c3, c4 = st.columns(4)

    card_style = (
        "border-radius:12px; padding:20px 22px; color:white; "
        "box-shadow:0 2px 12px rgba(0,0,0,0.15); margin-bottom:4px;"
    )

    c1.markdown(
        f'<div style="background:linear-gradient(135deg,#1565c0,#1e88e5);{card_style}">'
        f'<div style="font-size:0.78rem;opacity:0.85;letter-spacing:1px;">TOTAL EMPLOYEES</div>'
        f'<div style="font-size:2.2rem;font-weight:700;margin:4px 0;">{total_employees}</div>'
        f'<div style="font-size:0.8rem;opacity:0.8;">👷 Across all shops</div>'
        f'</div>', unsafe_allow_html=True
    )

    c2.markdown(
        f'<div style="background:linear-gradient(135deg,#2e7d32,#43a047);{card_style}">'
        f'<div style="font-size:0.78rem;opacity:0.85;letter-spacing:1px;">COACHES IN WORKSHOP</div>'
        f'<div style="font-size:2.2rem;font-weight:700;margin:4px 0;">{total_coaches}</div>'
        f'<div style="font-size:0.8rem;opacity:0.8;">✅ {completed_coaches} Completed &nbsp;|&nbsp; 🔄 {in_progress_coaches} In Progress</div>'
        f'</div>', unsafe_allow_html=True
    )

    c3.markdown(
        f'<div style="background:linear-gradient(135deg,#6a1b9a,#8e24aa);{card_style}">'
        f'<div style="font-size:0.78rem;opacity:0.85;letter-spacing:1px;">ACTIVE JOBS</div>'
        f'<div style="font-size:2.2rem;font-weight:700;margin:4px 0;">{active_jobs}</div>'
        f'<div style="font-size:0.8rem;opacity:0.8;">✔️ {completed_jobs} Completed</div>'
        f'</div>', unsafe_allow_html=True
    )

    c4.markdown(
        f'<div style="background:linear-gradient(135deg,#e65100,#f57c00);{card_style}">'
        f'<div style="font-size:0.78rem;opacity:0.85;letter-spacing:1px;">AVG EFFICIENCY</div>'
        f'<div style="font-size:2.2rem;font-weight:700;margin:4px 0;">{avg_efficiency}%</div>'
        f'<div style="font-size:0.8rem;opacity:0.8;">⚙️ {running_machines} Machines Running</div>'
        f'</div>', unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    #display targets
    st.markdown("#### 🎯 Monthly Targets")
    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Monthly POH Target", ws["monthly_poh_target"])
    t2.metric("Monthly IOH Target", ws["monthly_ioh_target"])
    t3.metric("Workshop Shops",     ws["total_shops"])
    t4.metric("Machines Under Maintenance", maint_machines,
              delta=f"-{maint_machines}" if maint_machines > 0 else "0",
              delta_color="inverse")

    st.divider()

    #draw performance table
    left_col, right_col = st.columns([3, 2], gap="medium")

    with left_col:
        st.markdown("#### 🏭 Shop-wise Performance")
        perf = shops[["shop_name", "total_staff", "active_jobs",
                       "completed_jobs", "efficiency"]].copy()
        perf.columns = ["Shop", "Staff", "Active Jobs", "Completed Jobs", "Efficiency (%)"]
        st.dataframe(perf, use_container_width=True, hide_index=True)

    with right_col:
        st.markdown("#### ⚙️ Machine Status")
        mach_counts = (
            machines["machine_status"]
            .value_counts()
            .reset_index()
        )
        mach_counts.columns = ["Status", "Count"]
        fig_mach = px.pie(
            mach_counts,
            names="Status",
            values="Count",
            hole=0.55,
            color="Status",
            color_discrete_map={
                "Running":     "#43a047",
                "Maintenance": "#f57c00",
                "Idle":        "#90a4ae",
            },
        )
        fig_mach.update_layout(
            height=280,
            margin=dict(t=20, b=10, l=10, r=10),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.25),
        )
        fig_mach.update_traces(textinfo="label+percent")
        st.plotly_chart(fig_mach, use_container_width=True)

    st.divider()

    #show coach progress
    st.markdown("#### 🚆 Coach Progress — Live Tracker")

    coach_display = coaches[[
        "coach_number", "coach_type", "overhaul_type",
        "current_shop", "status", "progress", "arrival_date"
    ]].sort_values("progress", ascending=False).reset_index(drop=True)

    #make html table
    rows_html = ""
    for _, row in coach_display.iterrows():
        pct   = int(row["progress"])
        bar_color = "#43a047" if pct >= 75 else ("#f57c00" if pct >= 40 else "#e53935")
        badge = status_badge(str(row["status"]))
        rows_html += f"""<tr style="border-bottom:1px solid #eee;">
            <td style="padding:10px 8px;font-weight:600;">{row['coach_number']}</td>
            <td style="padding:10px 8px;">{row['coach_type']}</td>
            <td style="padding:10px 8px;">{row['overhaul_type']}</td>
            <td style="padding:10px 8px;">{row['current_shop']}</td>
            <td style="padding:10px 8px;">{badge}</td>
            <td style="padding:10px 8px; min-width:140px;">
                <div style="background:var(--progress-track,#e0e0e0);border-radius:6px;height:10px;width:100%;">
                    <div style="background:{bar_color};width:{pct}%;height:10px;border-radius:6px;"></div>
                </div>
                <span style="font-size:0.75rem;opacity:0.7;">{pct}%</span>
            </td>
            <td style="padding:10px 8px;font-size:0.82rem;opacity:0.65;">{row['arrival_date']}</td>
        </tr>"""

    st.markdown(
        f"""
        <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
            <thead>
                <tr style="background:var(--table-head-bg,#f0f4f8);text-align:left;border-bottom:2px solid rgba(128,128,128,0.2);">
                    <th style="padding:10px 8px;opacity:0.75;font-weight:600;letter-spacing:.4px;font-size:0.80rem;text-transform:uppercase;">Coach No.</th>
                    <th style="padding:10px 8px;opacity:0.75;font-weight:600;letter-spacing:.4px;font-size:0.80rem;text-transform:uppercase;">Type</th>
                    <th style="padding:10px 8px;opacity:0.75;font-weight:600;letter-spacing:.4px;font-size:0.80rem;text-transform:uppercase;">Overhaul</th>
                    <th style="padding:10px 8px;opacity:0.75;font-weight:600;letter-spacing:.4px;font-size:0.80rem;text-transform:uppercase;">Current Shop</th>
                    <th style="padding:10px 8px;opacity:0.75;font-weight:600;letter-spacing:.4px;font-size:0.80rem;text-transform:uppercase;">Status</th>
                    <th style="padding:10px 8px;opacity:0.75;font-weight:600;letter-spacing:.4px;font-size:0.80rem;text-transform:uppercase;">Progress</th>
                    <th style="padding:10px 8px;opacity:0.75;font-weight:600;letter-spacing:.4px;font-size:0.80rem;text-transform:uppercase;">Arrival</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    #list recent arrivals
    st.markdown("#### 🕐 Recent Arrivals")
    recent = coaches.sort_values("arrival_date", ascending=False).head(5)[[
        "coach_number", "coach_type", "overhaul_type",
        "current_shop", "status", "arrival_date"
    ]]
    recent.columns = ["Coach No.", "Type", "Overhaul", "Current Shop", "Status", "Arrival Date"]
    st.dataframe(recent, use_container_width=True, hide_index=True)

    st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.78rem;margin-top:24px;'>"
        "Rail Sathi v1.0 &nbsp;•&nbsp; N.F. Railway Mechanical Workshop, Dibrugarh &nbsp;•&nbsp; "
        "Developed by Shobhraj Bhattacharjee &amp; Sanjay Krishna Bora"
        "</div>",
        unsafe_allow_html=True,
    )