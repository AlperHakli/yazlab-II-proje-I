from pymongo import AsyncMongoClient
from beanie import init_beanie
from services.book_service.config import settings
from services.book_service.app.models import AllBooks



async def init_book_db():
    client = AsyncMongoClient(host=settings.BOOK_MONGODB_URL)

    db = client.get_default_database()

    await init_beanie(
        database=db,
        document_models=[AllBooks]
    )