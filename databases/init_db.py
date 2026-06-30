from databases.database import db


def create_tables():
    tables = [

        """
        CREATE TABLE IF NOT EXISTS workshop_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workshop_name TEXT,
            railway_zone TEXT,
            location TEXT,
            total_employees INTEGER,
            total_shops INTEGER,
            monthly_poh_target INTEGER,
            monthly_ioh_target INTEGER
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            full_name TEXT,
            role TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE,
            employee_name TEXT,
            designation TEXT,
            shop_name TEXT,
            phone TEXT,
            status TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS shops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_name TEXT UNIQUE,
            head_of_shop TEXT,
            total_staff INTEGER,
            active_jobs INTEGER,
            completed_jobs INTEGER,
            efficiency REAL
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS coaches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_number TEXT UNIQUE,
            coach_type TEXT,
            overhaul_type TEXT,
            current_shop TEXT,
            status TEXT,
            arrival_date TEXT,
            expected_dispatch TEXT,
            progress INTEGER
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_name TEXT,
            machine_id TEXT UNIQUE,
            shop_name TEXT,
            machine_status TEXT,
            last_service_date TEXT,
            next_service_date TEXT,
            health_score REAL
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT,
            machine_name TEXT,
            maintenance_type TEXT,
            maintenance_date TEXT,
            technician TEXT,
            remarks TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_number TEXT,
            inspector_name TEXT,
            inspection_date TEXT,
            inspection_status TEXT,
            remarks TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            message TEXT,
            created_at TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_name TEXT,
            generated_by TEXT,
            generated_on TEXT,
            report_type TEXT
        )
        """
    ]

    for table in tables:
        db.execute(table)

    print("Database initialized successfully.")


if __name__ == "__main__":
    create_tables()