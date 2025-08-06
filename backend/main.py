from agent.graph import graph as agent_app
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import traceback
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from pymongo import MongoClient
import logging
from fastapi.responses import JSONResponse
import datetime
from backend.db.users import (create_user, get_user_by_email, update_user)
from backend.db.models import UserUpdate, UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config(".env")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config("SECRET_KEY"))

MONGO_URI = config("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client[config("MONGO_DB_NAME")]
user_collection = db[config("MONGO_USER_COLLECTION")]


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


oauth = OAuth()

google = oauth.register(
    name="google",
    client_id=config("GOOGLE_CLIENT_ID"),
    client_secret=config("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@app.get("/login/{provider}")
async def login(request: Request, provider: str):
    if provider != "google":
        raise HTTPException(status_code=400, detail="Invalid provider")
    oauth_provider = oauth.create_client(provider)

    redirect_uri = config("REDIRECT_URL")

    return await oauth_provider.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback/{provider}")
async def callback(request: Request, provider: str):
    try:
        if provider != "google":
            raise HTTPException(status_code=400, detail="Invalid provider")

        oauth_provider = oauth.create_client(provider)

        token = await oauth_provider.authorize_access_token(request)

        # Defensive check
        if not token or "access_token" not in token:
            raise Exception("Token retrieval failed")

        user_info = token.get("userinfo")  # usually already included
        if not user_info:
            user_info = (await oauth_provider.get("userinfo")).json()

        # Save or update user in MongoDB
        existing_user = await get_user_by_email(user_info["email"])
        if not existing_user:
            now = datetime.datetime.now(datetime.timezone.utc)

            await create_user(UserCreate(
                email=user_info["email"],
                name=user_info.get("name"),
                provider=provider,
                provider_id=user_info["sub"],
                created_at=now,
                updated_at=now,
            ))
        else:
            await update_user(existing_user._id, UserUpdate(
                name=user_info.get("name"),
                updated_at=datetime.datetime.now(datetime.timezone.utc),
            ))

        return JSONResponse(
            {"message": "User authenticated successfully", "user_info": user_info}
        )

    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        return JSONResponse({"error": str(e)})
