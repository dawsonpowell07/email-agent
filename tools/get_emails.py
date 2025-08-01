from langchain_core.tools import tool
from typing import List, Dict, Any, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.auth import get_credentials, get_current_user
from utils.logging import get_logger

logger = get_logger(__name__)


@tool
def get_emails(
    query: str = "is:unread", user_email: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve emails from Gmail."""
    if user_email is None:
        user_email = get_current_user()
    if not user_email:
        logger.error("User email not specified.")
        return {"error": "User email not specified. Run gmail_authenticate first."}

    try:
        logger.info(f"Retrieving emails for user: {user_email} with query: {query}")
        creds = get_credentials(user_email)
        service = build("gmail", "v1", credentials=creds)
        results = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=20)
            .execute()
        )
        messages = results.get("messages", [])
        emails = []
        for message in messages:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=message["id"], format="full")
                .execute()
            )
            headers = msg["payload"]["headers"]
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "")
            email_data = {
                "id": message["id"],
                "subject": subject,
                "sender": sender,
                "snippet": msg.get("snippet", ""),
            }
            emails.append(email_data)
        logger.info(
            f"Successfully retrieved {len(emails)} emails for user: {user_email}"
        )
        return emails
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        return {"error": f"An error occurred: {error}"}
