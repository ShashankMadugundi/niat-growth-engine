
import gspread
import json
import streamlit as st
import os

from datetime import datetime, timezone
from config import (
    GOOGLE_SHEET_ID,
    GOOGLE_SERVICE_ACCOUNT_FILE
)


HEADERS = [
    "Timestamp",
    "Student Name",
    "Phone",
    "City",
    "Coaching Centre",
    "Exam",
    "Exam Status",
    "Technology Interest",
    "Primary Concern",
    "Parent Involvement",
    "Counselling Interest",
    "Lead Score",
    "Priority",
    "Primary Concern (AI)",
    "Admission Intent",
    "Recommended Action",
    "WhatsApp Message",
    "AI Reasoning",
    "Follow-up Status",
    "Parent Phone",
    "Consent to Contact"
]


def get_google_client():

    try:
        service_account_info = st.secrets.get(
            "gcp_service_account"
        )

        if service_account_info:
            return gspread.service_account_from_dict(
                dict(service_account_info)
            )

    except Exception:
        pass

    if os.path.exists(GOOGLE_SERVICE_ACCOUNT_FILE):
        return gspread.service_account(
            filename=GOOGLE_SERVICE_ACCOUNT_FILE
        )

    raise FileNotFoundError(
        "Google credentials not configured"
    )


def get_worksheet():

    client = get_google_client()
    spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

    try:
        worksheet = spreadsheet.worksheet("Leads")

    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title="Leads",
            rows=1000,
            cols=len(HEADERS)
        )

    existing_headers = worksheet.row_values(1)

    if not existing_headers:
        worksheet.update(
            range_name="A1:U1",
            values=[HEADERS]
        )

    elif existing_headers == HEADERS[:len(existing_headers)]:
        if len(existing_headers) < len(HEADERS):
            worksheet.update(
                range_name=f"A1:U1",
                values=[HEADERS]
            )

    elif existing_headers != HEADERS:
        raise ValueError(
            "Google Sheets headers do not match expected HEADERS. "
            "Please check row 1 manually."
        )

    return worksheet


def save_lead(student_data, ai_analysis):

    worksheet = get_worksheet()

    row = [
        datetime.now(timezone.utc).isoformat(),
        student_data.get("name", ""),
        student_data.get("phone", ""),
        student_data.get("city", ""),
        student_data.get("coaching_centre", ""),
        student_data.get("exam", ""),
        student_data.get("exam_status", ""),
        student_data.get("technology_interest", ""),
        student_data.get("primary_concern", ""),
        student_data.get("parent_involvement", ""),
        student_data.get("counselling_interest", ""),
        ai_analysis.get("lead_score", ""),
        ai_analysis.get("priority", ""),
        ai_analysis.get("primary_concern", ""),
        ai_analysis.get("admission_intent", ""),
        ai_analysis.get("recommended_action", ""),
        ai_analysis.get("whatsapp_message", ""),
        ai_analysis.get("reasoning", ""),
        "Pending",
        student_data.get("parent_phone", ""),
        student_data.get("consent", False),
    ]

    worksheet.append_row(
        row,
        value_input_option="RAW"
    )

    return True


def get_all_leads():

    worksheet = get_worksheet()

    all_values = worksheet.get_all_values()

    if not all_values:
        return []

    headers = all_values[0]

    valid_columns = [
        (index, header)
        for index, header in enumerate(headers)
        if header.strip()
    ]

    records = []

    for row in all_values[1:]:

        record = {
            header: row[index] if index < len(row) else ""
            for index, header in valid_columns
        }

        if any(str(value).strip() for value in record.values()):
            records.append(record)

    return records


def update_followup_status(phone, new_status):

    worksheet = get_worksheet()

    cell = worksheet.find(
        str(phone),
        in_column=3
    )

    if cell is None:
        raise ValueError("Student not found in CRM")

    headers = worksheet.row_values(1)

    status_column = headers.index("Follow-up Status") + 1

    worksheet.update_cell(
        cell.row,
        status_column,
        new_status
    )

    return True
