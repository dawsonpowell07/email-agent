from utils.auth import set_current_user, get_credentials
from state import State


def load_auth(state: State) -> dict:
    """Load credentials for the user specified in state."""
    user_email = state["user_email"]
    set_current_user(user_email)
    creds = get_credentials(user_email)
    return {"token_info": creds.to_json()}
