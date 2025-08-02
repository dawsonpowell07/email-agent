"""Tools for recording job applications to Google Sheets."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_core.tools import tool

from utils.auth import get_credentials, get_current_user
from utils.logging import get_logger

logger = get_logger(__name__)


@tool
def add_job_app_to_spreadsheet(
    job_info: Dict[str, str], user_email: Optional[str] = None
) -> str:
    """Add a job application entry to a Google Sheet.

    Args:
        job_info: Dictionary containing details about the application. Expected keys
            are ``company`` and ``role``. ``email_id`` and ``date`` are optional.
        user_email: Email address whose credentials will be used. Defaults to the
            currently authenticated user.

    Returns:
        A message indicating success or failure.
    """

    if user_email is None:
        user_email = get_current_user()
    if not user_email:
        logger.error("Gmail not authenticated.")
        return "Gmail not authenticated. Run gmail_authenticate first."

    spreadsheet_id = os.getenv("JOB_SHEET_ID")
    sheet_name = os.getenv("JOB_SHEET_NAME", "Sheet1")
    if not spreadsheet_id:
        logger.error("JOB_SHEET_ID environment variable not set.")
        return "Spreadsheet ID not configured."

    try:
        logger.info("Appending job application to spreadsheet for user: %s", user_email)
        creds = get_credentials(user_email)
        service = build("sheets", "v4", credentials=creds)

        now = datetime.utcnow().isoformat()
        values = [
            [
                job_info.get("company", ""),
                job_info.get("role", ""),
                job_info.get("email_id", ""),
                job_info.get("date", now),
            ]
        ]
        body = {"values": values}
        range_name = f"{sheet_name}!A:D"
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body,
        ).execute()
        logger.info("Successfully appended job application to sheet.")
        return "Job application added to spreadsheet."
    except HttpError as error:
        logger.error("An error occurred: %s", error)
        return f"An error occurred: {error}"
