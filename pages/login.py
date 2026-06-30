import streamlit as st
from pathlib import Path

from utils.auth_helper import authenticate


BASE_DIR = Path(__file__).resolve().parent.parent


def load_css():

    css_path = BASE_DIR / "css" / "style.css"

    if css_path.exists():

        with open(css_path, "r", encoding="utf-8") as file:

            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )


def app():

    st.set_page_config(
        page_title="Rail Sathi Login",
        page_icon="🚆",
        layout="wide"
    )

    load_css()

    left, right = st.columns([1.4, 1])

    with left:

        bg_path = BASE_DIR / "assets" / "railway_bg.jpg"

        if bg_path.exists():

            st.image(
                str(bg_path),
                use_container_width=True
            )

    with right:

        logo_path = BASE_DIR / "assets" / "logo.png"

        if logo_path.exists():

            st.image(
                str(logo_path),
                width=140
            )

        st.title("Rail Sathi")

        st.caption(
            "Smart Railway Workshop Management System"
        )

        st.divider()

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        remember = st.checkbox(
            "Remember Me"
        )

        login = st.button(
            "🔐 Login",
            use_container_width=True
        )

        st.caption(
            "Authorized users only."
        )

        st.divider()
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

    if login:

        if username.strip() == "" or password.strip() == "":

            st.warning(
                "Please enter both username and password."
            )

        else:

            success = authenticate(
                username,
                password
            )

            if success:

                st.success(
                    "Login Successful."
                )

                st.balloons()

                st.session_state.logged_in = True

                st.session_state.remember_me = remember

                st.session_state.username = username

                st.success(
                    f"Welcome {st.session_state.name}"
                )

                st.info(
                    f"Role : {st.session_state.role}"
                )

                st.divider()

                st.markdown(
                    "### Login Details"
                )

                info1, info2 = st.columns(2)

                info1.metric(
                    "Username",
                    st.session_state.username
                )

                info2.metric(
                    "Role",
                    st.session_state.role
                )

                st.success(
                    "Access Granted."
                )

                st.button(
                    "Continue to Dashboard",
                    use_container_width=True,
                    disabled=True
                )

            else:

                st.error(
                    "Invalid Username or Password."
                )

                st.stop()

    st.divider()
    st.subheader("🔑 Need Help?")

    with st.expander("Forgot Password"):

        st.write(
            """
            Please contact the system administrator to
            reset your password.

            Email : admin@nfrrailways.in
            """
        )

    st.divider()

    st.subheader("👤 Demo Credentials")

    demo_col1, demo_col2 = st.columns(2)

    with demo_col1:

        st.info(
            """
Username : admin

Password : admin123

Role : Admin
"""
        )

    with demo_col2:

        st.info(
            """
Username : supervisor

Password : supervisor123

Role : Supervisor
"""
        )

    st.divider()

    st.subheader("🔒 Security Notice")

    st.warning(
        """
• Authorized users only.

• Never share your password.

• Logout after completing your work.

• All activities are logged for security purposes.
"""
    )

    st.divider()

    if st.session_state.get("logged_in", False):

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            for key in [
                "logged_in",
                "username",
                "role",
                "name",
                "remember_me"
            ]:

                if key in st.session_state:

                    del st.session_state[key]

            st.success(
                "Logged out successfully."
            )

            st.rerun()

    st.divider()

    st.caption(
        "© 2026 Rail Sathi | Smart Railway Workshop Management System"
    )