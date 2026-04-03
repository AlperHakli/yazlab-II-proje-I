from pymongo import AsyncMongoClient
from beanie import init_beanie
from services.auth_service.app.pydantic_models import UserModel
from services.auth_service.config import settings


async def init_db():
    try:

        client = AsyncMongoClient(settings.AUTH_MONGODB_URL)


        db = client["auth_db"]


        await init_beanie(
            database=db,
            document_models=[UserModel]
        )
        print(f"Native pymongo async ile {db.name} başarıyla bağlandı ")

    except Exception as e:
        print(f" Hata Mongodb bağlantısı başarısız {str(e)} ")
        raise e


