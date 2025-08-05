from agent.graph import graph as agent_app
from agent.nodes.summarizer import summarizer_agent
from fastapi import Depends, FastAPI, HTTPException
import traceback

from .auth import User, create_db_and_tables, get_current_user
from .schemas import AgentRequest

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    """Initialize application resources."""
    create_db_and_tables()


@app.post("/label")
async def label(request: AgentRequest, user: User = Depends(get_current_user)):
    state = {
        "messages": [{"role": "user", "content": "classify my emails"}],
        "user_email": user.email,
        "token_info": request.token_info,
    }

    try:
        result = await agent_app.ainvoke(state)
        return result  # or filter response keys
    except Exception:  # pragma: no cover - logged for debugging
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Agent processing failed")


@app.post("/summarize")
async def summarize(request: AgentRequest, user: User = Depends(get_current_user)):
    state = {
        "messages": [{"role": "user", "content": "summarize my emails"}],
        "user_email": user.email,
        "token_info": request.token_info,
    }

    try:
        result = await summarizer_agent.ainvoke(state)
        return result
    except Exception:  # pragma: no cover - logged for debugging
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Agent processing failed")
