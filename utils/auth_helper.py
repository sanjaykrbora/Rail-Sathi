import hashlib

import bcrypt
import streamlit as st

from utils.database_helper import execute_query, fetch_query


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def _verify_password(password, stored_password):

    if not stored_password:
        return False

    #bcrypt headers look like this
    if stored_password.startswith("$2"):
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password.encode("utf-8")
            )
        except ValueError:
            return False

    legacy_hash = hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

    return stored_password == legacy_hash


def _maybe_upgrade_password(username, password, stored_password):

    if stored_password and not stored_password.startswith("$2"):
        new_hash = hash_password(password)
        execute_query(
            """
            UPDATE users
            SET password=?
            WHERE username=?
            """,
            (new_hash, username)
        )


def authenticate(username, password):

    user = fetch_query(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    if user.empty:

        return False

    user = user.iloc[0]

    if not _verify_password(password, user["password"]):

        return False

    _maybe_upgrade_password(
        username=user["username"],
        password=password,
        stored_password=user["password"]
    )

    st.session_state.logged_in = True
    st.session_state.username = user["username"]
    st.session_state.role = user["role"]
    st.session_state.name = user["full_name"]

    return True


def logout():

    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.name = None


def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )


def current_user():

    return st.session_state.get(
        "username",
        ""
    )


def current_name():

    return st.session_state.get(
        "name",
        ""
    )


def current_role():

    return st.session_state.get(
        "role",
        ""
    )


def is_admin():

    return current_role() == "Admin"


def is_manager():

    return current_role() == "Manager"


def is_supervisor():

    return current_role() == "Supervisor"


def is_staff():

    return current_role() == "Staff"


def has_permission(roles):

    return current_role() in roles


def create_session(user):

    st.session_state.logged_in = True
    st.session_state.username = user["username"]
    st.session_state.role = user["role"]
    st.session_state.name = user["full_name"]


def clear_session():

    keys = [
        "logged_in",
        "username",
        "role",
        "name"
    ]

    for key in keys:

        if key in st.session_state:

            del st.session_state[key]