from agent.graph import graph as agent_app
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict

app = FastAPI()

class AgentRequest(BaseModel):
    messages: List[Dict[str, str]]

    # Email address for the current user
    user_email: str
    # Cached OAuth token information
    token_info: Optional[str]
    preferences: dict[str, bool]
    

@app.post("/label")
async def label(request: AgentRequest):
    user_email = request.user_email
    token_info = request.token_info
    preferences = request.preferences
    
    state = {
        "messages": request.messages,
        "user_email": user_email,
        "token_info": token_info,
        "preferences": preferences,
    }

    _ = await agent_app.ainvoke(state)