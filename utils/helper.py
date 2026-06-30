from datetime import datetime


def format_date(date):

    if not date:
        return "-"

    try:
        return datetime.strptime(
            str(date),
            "%Y-%m-%d"
        ).strftime("%d-%m-%Y")

    except Exception:
        return str(date)


def progress_status(progress):

    progress = float(progress)

    if progress >= 90:
        return "Completed"

    if progress >= 70:
        return "Near Completion"

    if progress >= 40:
        return "In Progress"

    return "Delayed"


def health_status(score):

    score = float(score)

    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Good"

    if score >= 50:
        return "Average"

    return "Critical"


def efficiency_status(score):

    score = float(score)

    if score >= 90:
        return "Excellent"

    if score >= 80:
        return "Good"

    if score >= 70:
        return "Average"

    return "Poor"


def calculate_completion(active_jobs, completed_jobs):

    total = active_jobs + completed_jobs

    if total == 0:
        return 0

    return round(
        (completed_jobs / total) * 100,
        2
    )


def calculate_average(series):

    if len(series) == 0:
        return 0

    return round(
        series.mean(),
        2
    )


def percentage(value, total):

    if total == 0:
        return 0

    return round(
        (value / total) * 100,
        2
    )


def coach_delay(progress):

    progress = float(progress)

    if progress < 50:
        return True

    return False


def machine_due(score):

    score = float(score)

    if score < 50:
        return True

    return False


def welcome_message():

    hour = datetime.now().hour

    if hour < 12:
        return "Good Morning"

    if hour < 17:
        return "Good Afternoon"

    return "Good Evening"


def workshop_status(efficiency):

    efficiency = float(efficiency)

    if efficiency >= 90:
        return "Excellent"

    if efficiency >= 80:
        return "Good"

    if efficiency >= 70:
        return "Average"

    return "Needs Improvement"


def format_number(number):

    return f"{number:,}"


def capitalize(text):

    return str(text).title()


def database_status():

    return "Connected"


def app_version():

    return "Rail Sathi Enterprise v1.0"