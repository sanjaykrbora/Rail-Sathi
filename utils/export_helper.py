from utils.pdf_generator import generate_pdf
from utils.excel_export import export_excel


def export_report(
    title,
    dataframe,
    report_name,
    export_type
):

    export_type = export_type.lower()

    if export_type == "pdf":

        return generate_pdf(
            title,
            dataframe,
            f"{report_name}.pdf"
        )

    if export_type == "excel":

        return export_excel(
            title,
            dataframe,
            f"{report_name}.xlsx"
        )

    if export_type == "csv":

        filename = f"{report_name}.csv"

        dataframe.to_csv(
            filename,
            index=False
        )

        return filename

    raise ValueError(
        "Unsupported export format."
    )


def export_coach_report(
    dataframe,
    export_type="pdf"
):

    return export_report(
        "Coach Report",
        dataframe,
        "coach_report",
        export_type
    )


def export_employee_report(
    dataframe,
    export_type="pdf"
):

    return export_report(
        "Employee Report",
        dataframe,
        "employee_report",
        export_type
    )


def export_machine_report(
    dataframe,
    export_type="pdf"
):

    return export_report(
        "Machine Report",
        dataframe,
        "machine_report",
        export_type
    )


def export_maintenance_report(
    dataframe,
    export_type="pdf"
):

    return export_report(
        "Maintenance Report",
        dataframe,
        "maintenance_report",
        export_type
    )


def export_workshop_report(
    dataframe,
    export_type="pdf"
):

    return export_report(
        "Workshop Report",
        dataframe,
        "workshop_report",
        export_type
    )


def export_poh_ioh_report(
    dataframe,
    export_type="pdf"
):

    return export_report(
        "POH IOH Report",
        dataframe,
        "poh_ioh_report",
        export_type
    )


def export_analytics_report(
    dataframe,
    export_type="pdf"
):

    return export_report(
        "Analytics Report",
        dataframe,
        "analytics_report",
        export_type
    )