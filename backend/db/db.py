from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# Replace the placeholder with your Atlas connection string
uri = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = AsyncIOMotorClient(uri)


# Send a ping to confirm a successful connection
async def ping_server():
    try:
        await client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


def get_database():
    return client.get_database("email_agent")
