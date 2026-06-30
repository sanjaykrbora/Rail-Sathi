import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "databases"/ "railway.db"
print(DB_PATH)
print(DB_PATH.exists())

def get_connection():

    return sqlite3.connect(DB_PATH)


def close_connection(connection):

    if connection:

        connection.close()


def fetch_table(table_name):

    connection = get_connection()

    dataframe = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        connection
    )

    connection.close()

    return dataframe


def execute_query(query, parameters=()):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        query,
        parameters
    )

    connection.commit()

    connection.close()


def fetch_query(query, parameters=()):

    connection = get_connection()

    dataframe = pd.read_sql_query(
        query,
        connection,
        params=parameters
    )

    connection.close()

    return dataframe


def insert_record(table_name, data):

    columns = ", ".join(data.keys())

    placeholders = ", ".join(
        ["?"] * len(data)
    )

    query = f"""
    INSERT INTO {table_name}
    ({columns})
    VALUES
    ({placeholders})
    """

    execute_query(
        query,
        tuple(data.values())
    )


def update_record(
    table_name,
    data,
    where_clause,
    where_values
):

    fields = ", ".join(
        [
            f"{column}=?"
            for column in data.keys()
        ]
    )

    query = f"""
    UPDATE {table_name}
    SET {fields}
    WHERE {where_clause}
    """

    values = list(data.values())

    values.extend(where_values)

    execute_query(
        query,
        tuple(values)
    )


def delete_record(
    table_name,
    where_clause,
    where_values
):

    query = f"""
    DELETE FROM {table_name}
    WHERE {where_clause}
    """

    execute_query(
        query,
        tuple(where_values)
    )


def count_records(table_name):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total


def table_exists(table_name):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name=?
        """,
        (table_name,)
    )

    exists = cursor.fetchone() is not None

    connection.close()

    return exists


def database_statistics():

    return {
        "coaches": count_records("coaches"),
        "employees": count_records("employees"),
        "machines": count_records("machines"),
        "maintenance": count_records("maintenance"),
        "shops": count_records("shops")
    }