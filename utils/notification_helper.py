from datetime import datetime

from utils.database_helper import fetch_table


def generate_notifications():

    notifications = []

    coaches = fetch_table("coaches")
    machines = fetch_table("machines")
    shops = fetch_table("shops")
    maintenance = fetch_table("maintenance")

    # Delayed Coaches
    delayed = coaches[coaches["progress"] < 50]

    for _, coach in delayed.iterrows():

        notifications.append(
            {
                "type": "warning",
                "title": "Delayed Coach",
                "message": (
                    f"Coach {coach['coach_number']} "
                    f"is only {coach['progress']}% completed."
                )
            }
        )

    # Machine Health
    critical = machines[machines["health_score"] < 50]

    for _, machine in critical.iterrows():

        notifications.append(
            {
                "type": "error",
                "title": "Critical Machine",
                "message": (
                    f"{machine['machine_name']} "
                    f"health is {machine['health_score']}%."
                )
            }
        )

    # Machines Under Maintenance
    maintenance_machines = machines[
        machines["machine_status"] == "Maintenance"
    ]

    for _, machine in maintenance_machines.iterrows():

        notifications.append(
            {
                "type": "info",
                "title": "Machine Maintenance",
                "message": (
                    f"{machine['machine_name']} "
                    "is currently under maintenance."
                )
            }
        )

    # Low Efficiency Shops
    low_efficiency = shops[shops["efficiency"] < 80]

    for _, shop in low_efficiency.iterrows():

        notifications.append(
            {
                "type": "warning",
                "title": "Low Shop Efficiency",
                "message": (
                    f"{shop['shop_name']} "
                    f"efficiency is {shop['efficiency']}%."
                )
            }
        )

    # Maintenance Records
    for _, record in maintenance.iterrows():

        notifications.append(
            {
                "type": "info",
                "title": "Maintenance Record",
                "message": (
                    f"{record['machine_name']} serviced on "
                    f"{record['maintenance_date']}."
                )
            }
        )

    return notifications


def today_summary():

    coaches = fetch_table("coaches")
    employees = fetch_table("employees")
    machines = fetch_table("machines")
    shops = fetch_table("shops")

    return {
        "date": datetime.now().strftime("%d-%m-%Y"),
        "coaches": len(coaches),
        "employees": len(employees),
        "machines": len(machines),
        "shops": len(shops),
        "running_machines": len(
            machines[
                machines["machine_status"] == "Running"
            ]
        ),
        "completed_coaches": len(
            coaches[
                coaches["status"] == "Completed"
            ]
        )
    }


def unread_count():

    return len(generate_notifications())


def has_alerts():

    return unread_count() > 0


def high_priority_alerts():

    alerts = []

    machines = fetch_table("machines")
    coaches = fetch_table("coaches")

    critical = machines[
        machines["health_score"] < 40
    ]

    delayed = coaches[
        coaches["progress"] < 30
    ]

    for _, machine in critical.iterrows():

        alerts.append(
            f"🚨 Critical Machine : {machine['machine_name']}"
        )

    for _, coach in delayed.iterrows():

        alerts.append(
            f"🚨 Coach {coach['coach_number']} requires immediate attention."
        )

    return alerts


def dashboard_message():

    total = unread_count()

    if total == 0:

        return "✅ No notifications."

    return f"🔔 {total} notifications available."
