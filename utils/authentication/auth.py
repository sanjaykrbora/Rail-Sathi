import streamlit as st

from utils.auth_helper import (
    is_logged_in,
    current_name,
    current_role,
    logout
)


def require_login():

    if not is_logged_in():

        st.error("🔒 Please login to access Rail Sathi.")

        st.stop()


def require_role(roles):

    require_login()

    if current_role() not in roles:

        st.error(
            "⛔ You are not authorized to access this page."
        )

        st.stop()


def sidebar_user():

    if is_logged_in():

        st.sidebar.markdown("---")

        st.sidebar.success(
            f"👤 {current_name()}"
        )

        st.sidebar.info(
            f"Role : {current_role()}"
        )

        if st.sidebar.button(
            "🚪 Logout",
            use_container_width=True
        ):

            logout()

            st.rerun()


def admin_only():

    require_role(["Admin"])


def manager_only():

    require_role(
        [
            "Admin",
            "Manager"
        ]
    )


def supervisor_only():

    require_role(
        [
            "Admin",
            "Manager",
            "Supervisor"
        ]
    )


def staff_access():

    require_role(
        [
            "Admin",
            "Manager",
            "Supervisor",
            "Staff"
        ]
    )
