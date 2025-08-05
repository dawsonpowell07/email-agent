from pydantic import BaseModel
from typing import Optional


class AgentRequest(BaseModel):
    """Request payload for agent endpoints."""

    user_email: str
    token_info: Optional[str]
