from langchain_core.tools import tool
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
from typing import List, Dict


@tool
def add_to_label(label_emails: Dict[str, List[str]]) -> str:
    """
    Add emails to multiple Gmail labels
    
    Args:
        label_emails: Dictionary where keys are label names and values is a set of email IDs
        {
            "label_emails" {
                "PERSONAL": ["email_id1", "email_id2", "email_id3"],
                "WORK": ["email_id4", "email_id5", "email_id6"],
                "SCHOOL": ["email_id7", "email_id8", "email_id9"],
                "PROMOTIONAL": ["email_id10", "email_id11", "email_id12"]
                }
        }
    
    Returns:
        Success or error message
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
        return "Gmail not authenticated. Run gmail_authenticate first."

    try:
        # Build the Gmail service
        service = build("gmail", "v1", credentials=creds)

        results = []

        # Process each label and its emails
        for label_name, email_ids in label_emails.items():
            # Get or create the label
            labels = service.users().labels().list(userId="me").execute()
            label_id = None

            # Check if label exists
            for label in labels.get("labels", []):
                if label["name"] == label_name:
                    label_id = label["id"]
                    break

            # Create label if it doesn't exist
            if not label_id:
                label_object = {
                    "name": label_name,
                    "labelListVisibility": "labelShow",
                    "messageListVisibility": "show",
                }
                created_label = (
                    service.users()
                    .labels()
                    .create(userId="me", body=label_object)
                    .execute()
                )
                label_id = created_label["id"]

            # Add emails to the label
            for email_id in email_ids:
                service.users().messages().modify(
                    userId="me", id=email_id, body={"addLabelIds": [label_id]}
                ).execute()

            results.append(f"Added {len(email_ids)} email(s) to label '{label_name}'")

        return "; ".join(results)

    except HttpError as error:
        return f"An error occurred: {error}"
