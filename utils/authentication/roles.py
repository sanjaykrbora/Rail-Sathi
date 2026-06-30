from enum import Enum


class Role(Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    SUPERVISOR = "Supervisor"
    STAFF = "Staff"


ROLE_PERMISSIONS = {

    Role.ADMIN: [
        "dashboard",
        "analytics",
        "coach_tracking",
        "employees",
        "machines",
        "machine_health",
        "workshop_shops",
        "maintenance",
        "poh_ioh",
        "reports",
        "ai_assistant",
        "settings",
        "notifications",
        "users"
    ],

    Role.MANAGER: [
        "dashboard",
        "analytics",
        "coach_tracking",
        "employees",
        "machines",
        "machine_health",
        "workshop_shops",
        "maintenance",
        "poh_ioh",
        "reports",
        "ai_assistant",
        "notifications"
    ],

    Role.SUPERVISOR: [
        "dashboard",
        "coach_tracking",
        "employees",
        "machines",
        "machine_health",
        "maintenance",
        "poh_ioh",
        "reports"
    ],

    Role.STAFF: [
        "dashboard",
        "coach_tracking",
        "machines"
    ]
}


def has_permission(role, page):

    try:
        role = Role(role)
    except Exception:
        return False

    return page in ROLE_PERMISSIONS.get(role, [])


def get_permissions(role):

    try:
        role = Role(role)
    except Exception:
        return []

    return ROLE_PERMISSIONS.get(role, [])


def all_roles():
    return [role.value for role in Role]


def is_admin(role):
    return role == Role.ADMIN.value


def is_manager(role):
    return role == Role.MANAGER.value


def is_supervisor(role):
    return role == Role.SUPERVISOR.value


def is_staff(role):
    return role == Role.STAFF.value