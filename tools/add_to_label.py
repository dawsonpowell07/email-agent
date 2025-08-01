from langchain_core.tools import tool
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.auth import get_credentials, get_current_user


@tool
def add_to_label(label_emails: Dict[str, List[str]], user_email: Optional[str] = None) -> str:
    """Add emails to multiple Gmail labels."""
    if user_email is None:
        user_email = get_current_user()
    if not user_email:
        return "Gmail not authenticated. Run gmail_authenticate first."

    try:
        creds = get_credentials(user_email)
        service = build("gmail", "v1", credentials=creds)
        results = []
        for label_name, email_ids in label_emails.items():
            labels = service.users().labels().list(userId="me").execute()
            label_id = None
            for label in labels.get("labels", []):
                if label["name"] == label_name:
                    label_id = label["id"]
                    break
            if not label_id:
                label_object = {
                    "name": label_name,
                    "labelListVisibility": "labelShow",
                    "messageListVisibility": "show",
                }
                created_label = (
                    service.users().labels().create(userId="me", body=label_object).execute()
                )
                label_id = created_label["id"]
            for email_id in email_ids:
                service.users().messages().modify(
                    userId="me", id=email_id, body={"addLabelIds": [label_id]}
                ).execute()
            results.append(f"Added {len(email_ids)} email(s) to label '{label_name}'")
        return "; ".join(results)
    except HttpError as error:
        return f"An error occurred: {error}"
