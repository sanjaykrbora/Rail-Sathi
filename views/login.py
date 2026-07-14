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

                st.session_state.remember_me = remember

                #spinny loading thing
                st.markdown(f"""
                <div id="login-loader" style="
                    position:fixed; inset:0; z-index:999999;
                    background:linear-gradient(135deg,#0d47a1,#1565c0);
                    display:flex; flex-direction:column;
                    align-items:center; justify-content:center;
                    gap:24px;
                ">
                    <div style="
                        width:56px; height:56px; border-radius:50%;
                        border:5px solid rgba(255,255,255,0.2);
                        border-top-color:#ffffff;
                        animation:spin 0.8s linear infinite;
                    "></div>
                    <div style="color:white; font-size:1.25rem; font-weight:600; letter-spacing:1px;">
                        Welcome, {st.session_state.name}
                    </div>
                    <div style="color:rgba(255,255,255,0.7); font-size:0.85rem;">
                        Loading your workspace...
                    </div>
                    <style>
                        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
                    </style>
                </div>
                """, unsafe_allow_html=True)

                import time
                time.sleep(1.2)
                st.rerun()

            else:

                st.error(
                    "❌ Invalid Username or Password."
                )

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
Username : manager

Password : manager123

Role : Manager
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
        "© 2026 Rail Sathi | Developed by Shobhraj Bhattacharjee & Sanjay Krishna Bora"
    )
