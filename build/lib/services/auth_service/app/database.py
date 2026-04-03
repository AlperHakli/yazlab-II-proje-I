from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from services.auth_service.app.pydantic_models import UserModel
from services.dispatcher.config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)

    await init_beanie(database=client.auth_db , document_models=[UserModel])


