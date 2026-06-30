import hashlib
from databases.database import db

workshop_info = (
    "N.F. Railway Mechanical Workshop",
    "Northeast Frontier Railway",
    "Dibrugarh, Assam",
    1115,
    16,
    68,
    55
)

db.execute(
    """
    INSERT OR IGNORE INTO workshop_info (
        workshop_name,
        railway_zone,
        location,
        total_employees,
        total_shops,
        monthly_poh_target,
        monthly_ioh_target
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    workshop_info
)

db.execute(
    """
    INSERT OR IGNORE INTO users (
        username,
        password,
        full_name,
        role
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        "admin",
        hashlib.sha256("admin123".encode()).hexdigest(),
        "Workshop Administrator",
        "Admin"
    )
)

shops = [
    ("Machine Shop", "R. Sharma", 104, 18, 42, 95.0),
    ("Wheel Shop", "P. Das", 86, 12, 38, 93.0),
    ("Welding Shop", "A. Singh", 82, 15, 35, 91.0),
    ("Corrosion Shop", "M. Roy", 64, 9, 24, 90.0),
    ("ISO Cell", "S. Kumar", 18, 3, 12, 98.0),
    ("Paint Shop", "B. Gogoi", 70, 8, 29, 92.0),
    ("Bogie Shop", "R. Dutta", 78, 11, 31, 94.0),
    ("Brake Shop", "A. Paul", 66, 10, 28, 92.0),
    ("Fitting Shop", "K. Nath", 74, 13, 34, 91.0),
    ("Electrical Shop", "S. Ahmed", 69, 10, 30, 94.0),
    ("Air Conditioning Shop", "J. Das", 48, 6, 18, 95.0),
    ("Battery Section", "D. Roy", 25, 4, 10, 96.0),
    ("Inspection Section", "R. Bora", 42, 6, 21, 97.0),
    ("Testing Section", "P. Kalita", 38, 5, 18, 95.0),
    ("Store Section", "T. Hazarika", 51, 7, 25, 93.0),
    ("Coach Assembly", "N. Saikia", 124, 20, 48, 94.0)
]

db.execute_many(
    """
    INSERT OR IGNORE INTO shops (
        shop_name,
        head_of_shop,
        total_staff,
        active_jobs,
        completed_jobs,
        efficiency
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    shops
)

coaches = [
    ("NF001245", "Sleeper", "POH", "Machine Shop", "In Progress", "2026-06-01", "2026-06-25", 35),
    ("NF001246", "AC 3 Tier", "POH", "Wheel Shop", "In Progress", "2026-06-02", "2026-06-24", 48),
    ("NF001247", "General", "IOH", "Welding Shop", "In Progress", "2026-06-03", "2026-06-18", 72),
    ("NF001248", "Chair Car", "POH", "Corrosion Shop", "In Progress", "2026-06-05", "2026-06-26", 64),
    ("NF001249", "Sleeper", "IOH", "Testing Section", "Inspection", "2026-06-07", "2026-06-19", 91)
]

db.execute_many(
    """
    INSERT OR IGNORE INTO coaches (
        coach_number,
        coach_type,
        overhaul_type,
        current_shop,
        status,
        arrival_date,
        expected_dispatch,
        progress
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    coaches
)

machines = [
    ("CNC Lathe", "MC001", "Machine Shop", "Running", "2026-05-15", "2026-08-15",98),
    ("Hydraulic Press", "MC002", "Machine Shop", "Running", "2026-05-18", "2026-08-18",95),
    ("Wheel Lathe", "WL001", "Wheel Shop", "Running", "2026-04-20", "2026-07-20",97),
    ("MIG Welding Machine", "WM001", "Welding Shop", "Maintenance", "2026-05-12", "2026-08-12",100),
    ("Paint Booth", "PT001", "Paint Shop", "Running", "2026-05-25", "2026-08-25",70)
]

db.execute_many(
    """
    INSERT OR IGNORE INTO machines (
        machine_name,
        machine_id,
        shop_name,
        machine_status,
        last_service_date,
        next_service_date,
        health_score
    )
    VALUES (?, ?, ?, ?, ?, ?,?)
    """,
    machines
)

print("Sample data inserted successfully.")