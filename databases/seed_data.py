import bcrypt
from databases.database import db


def seed_database():

    #wipe and reload workshop data so it doesnt double up
    existing = db.fetch_one("SELECT COUNT(*) FROM workshop_info")
    if existing and existing[0] == 0:
        db.execute(
            """
            INSERT INTO workshop_info (
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
            (
                "N.F. Railway Mechanical Workshop",
                "Northeast Frontier Railway",
                "Dibrugarh, Assam",
                1115,
                16,
                68,
                55
            )
        )

    #setup admin login
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
            bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            "Workshop Administrator",
            "Admin"
        )
    )

    #setup manager login
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
            "manager",
            bcrypt.hashpw("manager123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            "Workshop Manager",
            "Manager"
        )
    )

    #define shops
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

    #dump some fake employees
    employees = [
        ("EMP001", "Rajesh Sharma", "Supervisor", "Machine Shop", "Production", "+91-9000000001", "rajesh.sharma@nfrrailways.in", "2023-04-15", "Active"),
        ("EMP002", "Anita Das", "Technician", "Wheel Shop", "Mechanical", "+91-9000000002", "anita.das@nfrrailways.in", "2022-09-01", "Active"),
        ("EMP003", "Mohan Roy", "Engineer", "Welding Shop", "Engineering", "+91-9000000003", "mohan.roy@nfrrailways.in", "2021-07-21", "Active"),
        ("EMP004", "Suman Hazarika", "Technician", "Paint Shop", "Maintenance", "+91-9000000004", "suman.hazarika@nfrrailways.in", "2020-11-10", "On Leave"),
        ("EMP005", "Priya Kalita", "Staff", "Inspection Section", "Inspection", "+91-9000000005", "priya.kalita@nfrrailways.in", "2024-01-08", "Active"),
        ("EMP006", "Bikash Gogoi", "Engineer", "Bogie Shop", "Engineering", "+91-9000000006", "bikash.gogoi@nfrrailways.in", "2019-06-15", "Active"),
        ("EMP007", "Dipali Bora", "Staff", "Electrical Shop", "Electrical", "+91-9000000007", "dipali.bora@nfrrailways.in", "2022-03-20", "Active"),
        ("EMP008", "Rana Dutta", "Supervisor", "Fitting Shop", "Production", "+91-9000000008", "rana.dutta@nfrrailways.in", "2018-08-05", "Active"),
        ("EMP009", "Jyoti Ahmed", "Technician", "Brake Shop", "Mechanical", "+91-9000000009", "jyoti.ahmed@nfrrailways.in", "2023-11-12", "Active"),
        ("EMP010", "Kamal Nath", "Engineer", "Corrosion Shop", "Engineering", "+91-9000000010", "kamal.nath@nfrrailways.in", "2020-04-18", "Active"),
        ("EMP011", "Nilima Saikia", "Staff", "Air Conditioning Shop", "Maintenance", "+91-9000000011", "nilima.saikia@nfrrailways.in", "2021-09-22", "Active"),
        ("EMP012", "Tapan Paul", "Technician", "Battery Section", "Electrical", "+91-9000000012", "tapan.paul@nfrrailways.in", "2022-07-30", "Active"),
        ("EMP013", "Rituraj Borah", "Engineer", "Store Section", "Logistics", "+91-9000000013", "rituraj.borah@nfrrailways.in", "2019-02-14", "Active"),
        ("EMP014", "Samir Kumar", "Supervisor", "Coach Assembly", "Production", "+91-9000000014", "samir.kumar@nfrrailways.in", "2017-10-01", "Active"),
        ("EMP015", "Puja Singh", "Staff", "Testing Section", "Quality", "+91-9000000015", "puja.singh@nfrrailways.in", "2024-02-15", "Active"),
        ("EMP016", "Amit Baruah", "Technician", "Machine Shop", "Production", "+91-9000000016", "amit.baruah@nfrrailways.in", "2023-06-10", "Active"),
        ("EMP017", "Rimpi Devi", "Staff", "Wheel Shop", "Mechanical", "+91-9000000017", "rimpi.devi@nfrrailways.in", "2022-12-05", "On Leave"),
        ("EMP018", "Hiren Sarma", "Engineer", "Welding Shop", "Engineering", "+91-9000000018", "hiren.sarma@nfrrailways.in", "2020-08-25", "Active"),
        ("EMP019", "Bhaskar Talukdar", "Supervisor", "ISO Cell", "Quality", "+91-9000000019", "bhaskar.talukdar@nfrrailways.in", "2016-05-12", "Active"),
        ("EMP020", "Sangita Phukan", "Technician", "Inspection Section", "Inspection", "+91-9000000020", "sangita.phukan@nfrrailways.in", "2021-11-18", "Active"),
        ("EMP021", "Manish Tiwari", "Engineer", "Machine Shop", "Engineering", "+91-9000000021", "manish.tiwari@nfrrailways.in", "2020-03-10", "Active"),
        ("EMP022", "Kavita Reddy", "Technician", "Bogie Shop", "Mechanical", "+91-9000000022", "kavita.reddy@nfrrailways.in", "2018-07-22", "Active"),
        ("EMP023", "Prakash Jain", "Supervisor", "Electrical Shop", "Electrical", "+91-9000000023", "prakash.jain@nfrrailways.in", "2015-01-14", "Active"),
        ("EMP024", "Ravi Verma", "Technician", "Air Conditioning Shop", "Maintenance", "+91-9000000024", "ravi.verma@nfrrailways.in", "2021-06-05", "Active"),
        ("EMP025", "Sita Devi", "Staff", "Paint Shop", "Production", "+91-9000000025", "sita.devi@nfrrailways.in", "2019-11-30", "Active"),
        ("EMP026", "Vikram Singh", "Engineer", "Brake Shop", "Mechanical", "+91-9000000026", "vikram.singh@nfrrailways.in", "2017-09-18", "Active"),
        ("EMP027", "Alia Khan", "Technician", "Testing Section", "Quality", "+91-9000000027", "alia.khan@nfrrailways.in", "2023-04-12", "Active"),
        ("EMP028", "Sunil Chettri", "Supervisor", "Coach Assembly", "Production", "+91-9000000028", "sunil.chettri@nfrrailways.in", "2016-08-25", "Active"),
        ("EMP029", "Pooja Sharma", "Staff", "Store Section", "Logistics", "+91-9000000029", "pooja.sharma@nfrrailways.in", "2022-01-10", "On Leave"),
        ("EMP030", "Anil Kapoor", "Technician", "Fitting Shop", "Production", "+91-9000000030", "anil.kapoor@nfrrailways.in", "2020-12-01", "Active"),
    ]

    db.execute_many(
        """
        INSERT OR IGNORE INTO employees (
            employee_id,
            employee_name,
            designation,
            shop_name,
            department,
            phone,
            email,
            joining_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        employees
    )

    #add coaches
    coaches = [
        ("NF001245", "Sleeper", "POH", "Machine Shop", "In Progress", "2026-06-01", "2026-06-25", 35),
        ("NF001246", "AC 3 Tier", "POH", "Wheel Shop", "In Progress", "2026-06-02", "2026-06-24", 48),
        ("NF001247", "General", "IOH", "Welding Shop", "In Progress", "2026-06-03", "2026-06-18", 72),
        ("NF001248", "Chair Car", "POH", "Corrosion Shop", "In Progress", "2026-06-05", "2026-06-26", 64),
        ("NF001249", "Sleeper", "IOH", "Testing Section", "Inspection", "2026-06-07", "2026-06-19", 91),
        ("NF001250", "AC 2 Tier", "POH", "Bogie Shop", "In Progress", "2026-06-08", "2026-06-28", 55),
        ("NF001251", "General", "IOH", "Brake Shop", "In Progress", "2026-06-09", "2026-06-20", 80),
        ("NF001252", "Chair Car", "POH", "Fitting Shop", "In Progress", "2026-06-10", "2026-06-30", 25),
        ("NF001253", "Sleeper", "POH", "Electrical Shop", "In Progress", "2026-06-11", "2026-07-01", 42),
        ("NF001254", "AC 3 Tier", "IOH", "Coach Assembly", "Completed", "2026-05-15", "2026-06-15", 100),
        ("NF001255", "General", "POH", "Paint Shop", "In Progress", "2026-06-12", "2026-07-02", 38),
        ("NF001256", "Sleeper", "IOH", "Inspection Section", "Completed", "2026-05-20", "2026-06-10", 100),
        ("NF001257", "Chair Car", "POH", "Machine Shop", "In Progress", "2026-06-13", "2026-07-03", 20),
        ("NF001258", "AC 2 Tier", "IOH", "Wheel Shop", "In Progress", "2026-06-14", "2026-06-21", 60),
        ("NF001259", "General", "POH", "Welding Shop", "In Progress", "2026-06-15", "2026-07-05", 15),
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

    #add machines
    machines = [
        ("CNC Lathe",              "MC001", "Machine Shop",          "Running",     "2026-05-15", "2026-08-15", 98),
        ("Hydraulic Press",         "MC002", "Machine Shop",          "Running",     "2026-05-18", "2026-08-18", 95),
        ("Milling Machine",         "MC003", "Machine Shop",          "Maintenance", "2026-04-10", "2026-07-10", 62),
        ("Wheel Lathe",             "WL001", "Wheel Shop",            "Running",     "2026-04-20", "2026-07-20", 97),
        ("Axle Press",              "WL002", "Wheel Shop",            "Running",     "2026-05-01", "2026-08-01", 93),
        ("MIG Welding Machine",     "WM001", "Welding Shop",          "Maintenance", "2026-05-12", "2026-08-12", 74),
        ("TIG Welding Unit",        "WM002", "Welding Shop",          "Running",     "2026-05-22", "2026-08-22", 89),
        ("Shot Blasting Machine",   "CB001", "Corrosion Shop",        "Running",     "2026-05-08", "2026-08-08", 91),
        ("Paint Booth",             "PT001", "Paint Shop",            "Running",     "2026-05-25", "2026-08-25", 70),
        ("Bogie Lifting Jack",      "BG001", "Bogie Shop",            "Running",     "2026-04-15", "2026-07-15", 85),
        ("Air Compressor",          "AC001", "Air Conditioning Shop", "Breakdown",   "2026-03-20", "2026-06-20", 30),
        ("Testing Rig",             "TS001", "Testing Section",       "Running",     "2026-05-30", "2026-08-30", 96),
        ("Brake Testing Machine",   "BT001", "Brake Shop",            "Running",     "2026-05-10", "2026-08-10", 88),
        ("Battery Charger Unit",    "BC001", "Battery Section",       "Running",     "2026-04-25", "2026-07-25", 92),
        ("Overhead Crane",          "OC001", "Coach Assembly",        "Maintenance", "2026-04-05", "2026-07-05", 55),
        ("Surface Grinder",         "MC004", "Machine Shop",          "Running",     "2026-06-01", "2026-09-01", 90),
        ("Plasma Cutter",           "WM003", "Welding Shop",          "Running",     "2026-05-20", "2026-08-20", 88),
        ("Bearing Extractor",       "WL003", "Wheel Shop",            "Breakdown",   "2026-04-01", "2026-07-01", 40),
        ("Dynamic Balancing Mach.", "WL004", "Wheel Shop",            "Running",     "2026-05-15", "2026-08-15", 94),
        ("Ultrasonic Flaw Det.",    "TS002", "Testing Section",       "Running",     "2026-06-05", "2026-09-05", 99),
        ("Motorised Bogie Turnt.",  "BG002", "Bogie Shop",            "Running",     "2026-05-28", "2026-08-28", 92),
        ("Vacuum Impregnation Pt.", "ES001", "Electrical Shop",       "Running",     "2026-05-10", "2026-08-10", 87),
        ("Armature Winding Mach.",  "ES002", "Electrical Shop",       "Maintenance", "2026-04-15", "2026-07-15", 65),
        ("Refrigerant Recovery",    "AC002", "Air Conditioning Shop", "Running",     "2026-05-25", "2026-08-25", 96),
        ("Pneumatic Torque Wrench", "FS001", "Fitting Shop",          "Running",     "2026-06-10", "2026-09-10", 91),
        ("Radial Drilling Machine", "MC005", "Machine Shop",          "Running",     "2026-05-15", "2026-08-15", 94),
        ("Shaper Machine",          "MC006", "Machine Shop",          "Running",     "2026-04-10", "2026-07-10", 88),
        ("Journal Turning Lathe",   "WL005", "Wheel Shop",            "Running",     "2026-06-01", "2026-09-01", 96),
        ("Wheel Press",             "WL006", "Wheel Shop",            "Maintenance", "2026-03-25", "2026-06-25", 65),
        ("Submerged Arc Welder",    "WM004", "Welding Shop",          "Running",     "2026-05-05", "2026-08-05", 92),
        ("Spot Welding Machine",    "WM005", "Welding Shop",          "Running",     "2026-05-12", "2026-08-12", 89),
        ("Sand Blasting Machine",   "CB002", "Corrosion Shop",        "Running",     "2026-04-18", "2026-07-18", 85),
        ("Anti-Corrosive Sprayer",  "CB003", "Corrosion Shop",        "Running",     "2026-05-20", "2026-08-20", 91),
        ("Document Scanner",        "IS001", "ISO Cell",              "Running",     "2026-01-10", "2027-01-10", 99),
        ("Quality Audit Kiosk",     "IS002", "ISO Cell",              "Running",     "2026-02-15", "2027-02-15", 98),
        ("Airless Spray Gun",       "PT002", "Paint Shop",            "Running",     "2026-05-25", "2026-08-25", 93),
        ("Baking Oven",             "PT003", "Paint Shop",            "Running",     "2026-04-30", "2026-07-30", 87),
        ("Bogie Washing Plant",     "BG003", "Bogie Shop",            "Maintenance", "2026-04-05", "2026-07-05", 55),
        ("Spring Testing Machine",  "BG004", "Bogie Shop",            "Running",     "2026-05-15", "2026-08-15", 90),
        ("Air Brake Test Rig",      "BT002", "Brake Shop",            "Running",     "2026-06-02", "2026-09-02", 95),
        ("Cylinder Boring Machine", "BT003", "Brake Shop",            "Running",     "2026-05-11", "2026-08-11", 89),
        ("Hydraulic Pipe Bender",   "FS002", "Fitting Shop",          "Running",     "2026-04-20", "2026-07-20", 91),
        ("Bench Grinder",           "FS003", "Fitting Shop",          "Running",     "2026-05-01", "2026-08-01", 96),
        ("Stator Winding Machine",  "ES003", "Electrical Shop",       "Running",     "2026-05-18", "2026-08-18", 88),
        ("Insulation Tester",       "ES004", "Electrical Shop",       "Running",     "2026-06-05", "2026-09-05", 97),
        ("Vacuum Pump",             "AC003", "Air Conditioning Shop", "Running",     "2026-05-22", "2026-08-22", 92),
        ("Leak Detector",           "AC004", "Air Conditioning Shop", "Running",     "2026-06-08", "2026-09-08", 95),
        ("Battery Discharge Tester", "BC002","Battery Section",       "Running",     "2026-05-14", "2026-08-14", 91),
        ("Electrolyte Fill Mach.",  "BC003", "Battery Section",       "Maintenance", "2026-03-30", "2026-06-30", 60),
        ("Magnetic Particle Test",  "IN001", "Inspection Section",    "Running",     "2026-05-05", "2026-08-05", 98),
        ("Digital Calipers Set",    "IN002", "Inspection Section",    "Running",     "2026-01-15", "2027-01-15", 99),
        ("Universal Testing Mach.", "TS003", "Testing Section",       "Running",     "2026-04-12", "2026-07-12", 94),
        ("Hardness Tester",         "TS004", "Testing Section",       "Running",     "2026-05-20", "2026-08-20", 96),
        ("Forklift 5-Ton",          "ST001", "Store Section",         "Running",     "2026-05-10", "2026-08-10", 85),
        ("Automated Storage Rack",  "ST002", "Store Section",         "Running",     "2026-06-01", "2026-09-01", 97),
        ("Traverser",               "OC002", "Coach Assembly",        "Running",     "2026-04-25", "2026-07-25", 88),
        ("Scissor Lift",            "OC003", "Coach Assembly",        "Running",     "2026-05-28", "2026-08-28", 92),
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
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        machines
    )

    #add maintenance logs
    maintenance_count = db.fetch_one("SELECT COUNT(*) FROM maintenance")
    if not maintenance_count or maintenance_count[0] == 0:
        maintenance_records = [
            ("MC001", "CNC Lathe",           "Preventive", "2026-05-15", "Rajesh Sharma",    "Routine oil change and calibration"),
            ("WL001", "Wheel Lathe",         "Preventive", "2026-04-20", "Anita Das",         "Bearing inspection and lubrication"),
            ("WM001", "MIG Welding Machine", "Corrective", "2026-05-12", "Mohan Roy",         "Wire feed motor replaced"),
            ("MC002", "Hydraulic Press",     "Preventive", "2026-05-18", "Rana Dutta",        "Hydraulic fluid changed"),
            ("PT001", "Paint Booth",         "Corrective", "2026-04-30", "Suman Hazarika",    "Exhaust fan repaired"),
            ("AC001", "Air Compressor",      "Corrective", "2026-03-20", "Bikash Gogoi",      "Compressor valve replaced - breakdown"),
            ("BG001", "Bogie Lifting Jack",  "Preventive", "2026-04-15", "Kamal Nath",        "Annual servicing completed"),
            ("OC001", "Overhead Crane",      "Corrective", "2026-04-05", "Samir Kumar",       "Wire rope inspection and replacement"),
            ("WL002", "Axle Press",          "Preventive", "2026-05-01", "Jyoti Ahmed",       "Seal replacement and alignment check"),
            ("CB001", "Shot Blasting Machine","Preventive","2026-05-08", "Dipali Bora",       "Nozzle and filter cleaning"),
            ("BT001", "Brake Testing Machine","Preventive","2026-05-10", "Tapan Paul",        "Pressure gauge calibration"),
            ("BC001", "Battery Charger Unit","Preventive", "2026-04-25", "Nilima Saikia",     "Terminal cleaning and inspection"),
            ("TS001", "Testing Rig",         "Preventive", "2026-05-30", "Puja Singh",        "Software update and calibration"),
            ("MC003", "Milling Machine",     "Corrective", "2026-04-10", "Amit Baruah",       "Spindle motor overhaul"),
            ("WM002", "TIG Welding Unit",    "Preventive", "2026-05-22", "Hiren Sarma",       "Torch cleaning and gas line check"),
        ]

        db.execute_many(
            """
            INSERT INTO maintenance (
                machine_id,
                machine_name,
                maintenance_type,
                maintenance_date,
                technician,
                remarks
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            maintenance_records
        )

    #add inspections
    inspection_count = db.fetch_one("SELECT COUNT(*) FROM inspections")
    if not inspection_count or inspection_count[0] == 0:
        inspections = [
            ("NF001254", "R. Bora",            "2026-06-15", "Passed",  "All components checked, ready for dispatch"),
            ("NF001256", "P. Kalita",          "2026-06-10", "Passed",  "IOH completed, all brakes functional"),
            ("NF001247", "Sangita Phukan",      "2026-06-16", "Pending", "Welding inspection in progress"),
            ("NF001249", "R. Bora",            "2026-06-18", "Passed",  "Final inspection completed"),
            ("NF001251", "Bhaskar Talukdar",    "2026-06-18", "Pending", "Brake system check ongoing"),
        ]

        db.execute_many(
            """
            INSERT INTO inspections (
                coach_number,
                inspector_name,
                inspection_date,
                inspection_status,
                remarks
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            inspections
        )


if __name__ == "__main__":
    seed_database()