from utils.auth import set_current_user, get_credentials
from state import State
from utils.logging import get_logger

logger = get_logger(__name__)


def load_auth(state: State) -> dict:
    """Load credentials for the user specified in state."""
    user_email = state["user_email"]
    logger.info(f"Loading auth for user: {user_email}")
    set_current_user(user_email)
    creds = get_credentials(user_email)
    logger.info(f"Successfully loaded auth for user: {user_email}")
    return {"token_info": creds.to_json()}
