"""Tools for recording job applications to Google Sheets."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, List, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_core.tools import tool

from agent.utils.auth import get_credentials, get_current_user
from agent.utils.logging import get_logger

logger = get_logger(__name__)


@tool
def add_job_apps_to_spreadsheet(
    job_infos: List[Dict[str, str]], user_email: Optional[str] = None
) -> str:
    """Add multiple job application entries to a Google Sheet.

    Args:
        job_infos: A list of dictionaries, where each dictionary contains
            details about an application. Expected keys are ``company``,
            ``role``, and ``date``.
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
        logger.info(
            "Appending %d job applications to spreadsheet for user: %s",
            len(job_infos),
            user_email,
        )
        creds = get_credentials(user_email)
        service = build("sheets", "v4", credentials=creds)

        rows_to_append = []
        now = datetime.now().strftime("%Y-%m-%d")
        for job_info in job_infos:
            rows_to_append.append(
                [
                    job_info.get("company", ""),
                    job_info.get("role", ""),
                    job_info.get("date", now),
                ]
            )

        body = {"values": rows_to_append}
        range_name = f"'{sheet_name}'!A:C"
        logger.debug(f"Using range: {range_name}")

        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body,
        ).execute()

        logger.info("Successfully appended all job applications to sheet.")
        return f"{len(job_infos)} job applications added to spreadsheet."

    except HttpError as error:
        logger.error("An error occurred: %s", error)
        return f"An error occurred: {error}"
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        return f"An unexpected error occurred: {e}"
