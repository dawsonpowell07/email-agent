from agent.graph import graph as agent_app
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import traceback
from starlette.middleware.sessions import SessionMiddleware
import os
from fastapi.templating import Jinja2Templates
from backend.api.auth import auth, users
from backend.db.session import Base, engine

app = FastAPI()
app.include_router(auth.router, prefix="/api/authentication", tags=["auth"])
app.include_router(users.router, prefix="/api/authentication", tags=["users"])
app.add_middleware(
    SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "default_secret_key")
)

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="backend/static/")


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


@app.get("/")
async def login(request: Request):
    """
    :param request: An instance of the `Request` class, representing the incoming HTTP request.
    :return: A TemplateResponse object rendering the "login.html" template with the given request context.
    """
    return templates.TemplateResponse("pages/login/login.html", {"request": request})


@app.get("/welcome")
async def welcome(request: Request):
    """
    :param request: The incoming HTTP request containing session data.
    :return: A TemplateResponse object that renders the welcome page with the user's name or 'Guest' if not found.
    """
    name = request.session.get("user_name", "Guest")
    context = {"request": request, "name": name}
    return templates.TemplateResponse("pages/welcome/welcome.html", context)
