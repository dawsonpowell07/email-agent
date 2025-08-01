from typing import Dict, Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path

SCOPES = [
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.modify",
]

_current_user_email: Optional[str] = None
_credentials_cache: Dict[str, Credentials] = {}


def set_current_user(email: str) -> None:
    """Set the current user email for Gmail operations."""
    global _current_user_email
    _current_user_email = email


def get_current_user() -> Optional[str]:
    """Return the currently active user email."""
    return _current_user_email


def _load_credentials_from_file(email: str) -> Credentials:
    """Load credentials from the user's token file or start OAuth flow."""
    token_file = f"token_{email}.json"
    creds: Optional[Credentials] = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as f:
            f.write(creds.to_json())
    return creds


def get_credentials(email: Optional[str] = None) -> Credentials:
    """Return cached credentials for the given email, loading if necessary."""
    if email is None:
        email = _current_user_email
    if email is None:
        raise ValueError("User email not specified")

    creds = _credentials_cache.get(email)
    if not creds:
        creds = _load_credentials_from_file(email)
        _credentials_cache[email] = creds
    elif creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_file = f"token_{email}.json"
        with open(token_file, "w") as f:
            f.write(creds.to_json())

    return creds
