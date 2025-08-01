from langchain_core.tools import tool
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
from typing import List

@tool
def add_to_label(email_ids: List[str], label_name: str) -> str:
    """
    Add emails to a specific Gmail label
    
    Args:
        email_ids: List of email IDs to add to the label
        label_name: Name of the label to add emails to
    
    Returns:
        Success or error message
    """
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    
    # Get credentials
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        return "Gmail not authenticated. Run gmail_authenticate first."
    
    try:
        # Build the Gmail service
        service = build("gmail", "v1", credentials=creds)
        
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
                "messageListVisibility": "show"
            }
            created_label = service.users().labels().create(
                userId="me", 
                body=label_object
            ).execute()
            label_id = created_label["id"]
        
        # Add emails to the label
        for email_id in email_ids:
            service.users().messages().modify(
                userId="me",
                id=email_id,
                body={"addLabelIds": [label_id]}
            ).execute()
        
        return f"Successfully added {len(email_ids)} email(s) to label '{label_name}'"
        
    except HttpError as error:
        return f"An error occurred: {error}"