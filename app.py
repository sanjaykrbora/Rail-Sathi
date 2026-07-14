import streamlit as st
from pathlib import Path

from utils.authentication.auth import require_login, sidebar_user
from utils.authentication.roles import has_permission

from views import (
    dashboard,
    analytics,
    coach_tracking,
    employees,
    machines,
    machine_health,
    workshop_shops,
    maintenance,
    poh_ioh,
    reports,
    ai_assistant,
    settings,
    login
)

from utils.notification_helper import unread_count


BASE_DIR = Path(__file__).resolve().parent


st.set_page_config(
    page_title="Rail Sathi",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_css():

    css_path = BASE_DIR / "css" / "style.css"

    if css_path.exists():

        with open(css_path, "r", encoding="utf-8") as file:

            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )

load_css()


if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if not st.session_state.logged_in:

    login.app()

    st.stop()

require_login()
logo_path = BASE_DIR / "assets" / "logo.png"

with st.sidebar:

    if logo_path.exists():

        st.image(
            str(logo_path),
            width=120
        )

    st.markdown("## 🚆 Rail Sathi")

    st.caption(
        "Smart Railway Workshop Management System"
    )

    sidebar_user()

    st.divider()

    st.metric(
        "🔔 Notifications",
        unread_count()
    )

    st.divider()

    pages = {

        "🏠 Dashboard": "dashboard",

        "📈 Analytics": "analytics",

        "🚆 Coach Tracking": "coach_tracking",

        "👷 Employees": "employees",

        "⚙ Machines": "machines",

        "💚 Machine Health": "machine_health",

        "🏭 Workshop Shops": "workshop_shops",

        "🔧 Maintenance": "maintenance",

        "🚄 POH / IOH": "poh_ioh",

        "📄 Reports": "reports",

        "🤖 AI Assistant": "ai_assistant",

        "⚙ Settings": "settings"

    }

    available_pages = {}

    for page_name, page_key in pages.items():

        if has_permission(
            st.session_state.role,
            page_key
        ):

            available_pages[page_name] = page_key

    selected_page = st.radio(

        "Navigation",

        list(
            available_pages.keys()
        )

    )

    st.divider()

    st.caption(
        f"👤 {st.session_state.name}"
    )

    st.caption(
        f"Role : {st.session_state.role}"
    )
    #hook up the pages
try:

    page_key = available_pages[selected_page]

    if page_key == "dashboard":
        dashboard.app()

    elif page_key == "analytics":
        analytics.app()

    elif page_key == "coach_tracking":
        coach_tracking.app()

    elif page_key == "employees":
        employees.app()

    elif page_key == "machines":
        machines.app()

    elif page_key == "machine_health":
        machine_health.app()

    elif page_key == "workshop_shops":
        workshop_shops.app()

    elif page_key == "maintenance":
        maintenance.app()

    elif page_key == "poh_ioh":
        poh_ioh.app()

    elif page_key == "reports":
        reports.app()

    elif page_key == "ai_assistant":
        ai_assistant.app()

    elif page_key == "settings":
        settings.app()

    else:

        st.warning(
            "Selected page is not available."
        )

except Exception as error:

    st.error("⚠️ An unexpected error occurred.")

    with st.expander("View Error Details"):

        st.code(str(error))
        #show alerts on top
from datetime import datetime

from utils.notification_helper import (
    generate_notifications,
    high_priority_alerts,
    dashboard_message
)

with st.sidebar:

    st.divider()

    st.subheader("🚨 Alerts")

    alerts = high_priority_alerts()

    if alerts:

        for alert in alerts[:5]:

            st.error(alert)

    else:

        st.success("No Critical Alerts")

    st.divider()

    st.subheader("📢 Notifications")

    notifications = generate_notifications()

    if notifications:

        for notification in notifications[:5]:

            if notification["type"] == "error":

                st.error(notification["message"])

            elif notification["type"] == "warning":

                st.warning(notification["message"])

            else:

                st.info(notification["message"])

    else:

        st.success("No Notifications")

    st.divider()

    st.caption(dashboard_message())

    st.divider()

    st.subheader("📊 Quick Stats")

    st.metric(
        "Current User",
        st.session_state.name
    )

    st.metric(
        "Role",
        st.session_state.role
    )

    st.metric(
        "Notifications",
        unread_count()
    )

    st.metric(
        "Status",
        "Online"
    )

    st.divider()

    st.subheader("🕒 System")
    st.write("Online")
    #standard footer stuff
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:

    st.caption(
        "🚆 Rail Sathi Enterprise"
    )

with footer_col2:

    st.caption(
        "N.F. Railway Mechanical Workshop"
    )

with footer_col3:

    st.caption(
        "Version 1.0"
    )

st.caption(
    "© 2026 Rail Sathi | Developed by Shobhraj Bhattacharjee & Sanjay Krishna Bora"
)

#make logout work
if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True,
    key="sidebar_logout_btn"
):

    keys = [
        "logged_in",
        "username",
        "name",
        "role",
        "remember_me"
    ]

    for key in keys:

        if key in st.session_state:

            del st.session_state[key]

    st.success(
        "Logged out successfully."
    )

    st.rerun()