from agent.graph import graph as agent_app
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import traceback

app = FastAPI()

class AgentRequest(BaseModel):
    # Email address for the current user
    user_email: str
    # Cached OAuth token information
    token_info: Optional[str]
    

@app.post("/label")
async def label(request: AgentRequest):
    state = {
        "messages": [{"role": "user", "content": "classify my emails"}],
        "user_email": request.user_email,
        "token_info": request.token_info,
    }

    try:
        result = await agent_app.ainvoke(state)
        return result  # or filter response keys
    except Exception:
        print(traceback.format_exc())  # good for debugging
        raise HTTPException(status_code=500, detail="Agent processing failed")
