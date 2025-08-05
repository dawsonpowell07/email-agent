from agent.graph import graph as agent_app
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict

app = FastAPI()

class AgentRequest(BaseModel):
    # Email address for the current user
    user_email: str
    # Cached OAuth token information
    token_info: Optional[str]
    

@app.post("/label")
async def label(request: AgentRequest):
    user_email = request.user_email
    token_info = request.token_info
    
    state = {
        "messages": [{"role": "user", "content": "classify my emails"}],
        "user_email": user_email,
        "token_info": token_info,
    }

    _ = await agent_app.ainvoke(state)