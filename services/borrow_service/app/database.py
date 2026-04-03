from pymongo import AsyncMongoClient
from beanie import init_beanie
from services.borrow_service.config import settings
from services.borrow_service.app.models import AllBorrows

async def init_borrow_database():
    client = AsyncMongoClient(host=settings.BORROW_MONGODB_URL)

    db = client.get_default_database()


    await init_beanie(
        database=db,
        document_models=[AllBorrows]
    )