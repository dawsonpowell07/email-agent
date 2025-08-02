from langchain_core.tools import tool
from typing import Optional
from utils.auth import get_credentials, set_current_user, get_current_user
from utils.logging import get_logger

logger = get_logger(__name__)


@tool
def gmail_authenticate(user_email: Optional[str] = None) -> str:
    """Authenticate with Gmail for the specified user."""
    if user_email is None:
        user_email = get_current_user()
    if not user_email:
        logger.error("User email not specified.")
        return "Error: user email not specified"

    logger.info(f"Authenticating with Gmail for user: {user_email}")
    set_current_user(user_email)
    get_credentials(user_email)
    logger.info(f"Gmail authentication successful for {user_email}")
    return f"Gmail authentication successful for {user_email}"
