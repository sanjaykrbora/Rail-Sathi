from pathlib import Path

APP_NAME = "Rail Sathi"
APP_VERSION = "1.0.0"

WORKSHOP_NAME = "N.F. Railway Mechanical Workshop"
WORKSHOP_LOCATION = "Dibrugarh, Assam"
RAILWAY_ZONE = "Northeast Frontier Railway"

TOTAL_EMPLOYEES = 1115
TOTAL_SHOPS = 16

MONTHLY_POH_TARGET = 68
MONTHLY_IOH_TARGET = 55

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "databases" / "railway.db"

DEFAULT_WORKSHOP_EFFICIENCY = 94
DEFAULT_PENDING_COACHES = 12

PRIMARY_COLOR = "#0B3D91"
SECONDARY_COLOR = "#1565C0"
SUCCESS_COLOR = "#2E7D32"
WARNING_COLOR = "#F9A825"
DANGER_COLOR = "#D32F2F"
BACKGROUND_COLOR = "#F5F7FA"

USER_ROLES = [
    "Admin",
    "Manager",
    "Supervisor",
    "Staff"
]

COACH_STATUS = [
    "Received",
    "Inspection",
    "Machine Shop",
    "Wheel Shop",
    "Welding Shop",
    "Corrosion Shop",
    "Painting",
    "Testing",
    "Ready for Dispatch",
    "Completed"
]

WORKSHOP_SHOPS = [
    "Machine Shop",
    "Wheel Shop",
    "Welding Shop",
    "Corrosion Shop",
    "ISO Cell",
    "Paint Shop",
    "Bogie Shop",
    "Brake Shop",
    "Fitting Shop",
    "Electrical Shop",
    "Air Conditioning Shop",
    "Battery Section",
    "Inspection Section",
    "Testing Section",
    "Store Section",
    "Coach Assembly"
]
