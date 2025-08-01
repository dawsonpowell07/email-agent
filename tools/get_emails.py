from langchain_core.tools import tool
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import base64
import email
from typing import List, Dict, Any


# @tool
def get_emails(max_results: int = 50, query: str = "is:unread") -> List[Dict[str, Any]]:
    """
    Retrieve emails from Gmail

    Args:
        max_results: Maximum number of emails to retrieve (default: 50)
        query: Gmail search query (default: "is:unread" for unread emails)

    Returns:
        List of email data dictionaries
    """
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.labels",
        "https://www.googleapis.com/auth/gmail.modify",
    ]

    # Get credentials
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        return {"error": "Gmail not authenticated. Run gmail_authenticate first."}

    try:
        # Build the Gmail service
        service = build("gmail", "v1", credentials=creds)

        # Get messages
        results = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
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

            # Extract headers
            headers = msg["payload"]["headers"]
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "")
            date = next((h["value"] for h in headers if h["name"] == "Date"), "")

            # Extract body
            body = ""
            if "parts" in msg["payload"]:
                for part in msg["payload"]["parts"]:
                    if part["mimeType"] == "text/plain":
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode(
                            "utf-8"
                        )
                        break
            elif "body" in msg["payload"] and "data" in msg["payload"]["body"]:
                body = base64.urlsafe_b64decode(msg["payload"]["body"]["data"]).decode(
                    "utf-8"
                )

            email_data = {
                "id": message["id"],
                "subject": subject,
                "sender": sender,
                "date": date,
                "body": body,
                "snippet": msg.get("snippet", ""),
            }

            emails.append(email_data)

        return emails

    except HttpError as error:
        return {"error": f"An error occurred: {error}"}
