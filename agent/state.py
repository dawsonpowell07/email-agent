from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class State(TypedDict):
    """Graph state."""

    # Chat messages
    messages: Annotated[list, add_messages]
    # Email address for the current user
    user_email: str
    # Cached OAuth token information
    token_info: Optional[str]
