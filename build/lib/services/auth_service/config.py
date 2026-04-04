from dotenv import load_dotenv
import os

load_dotenv()
class Settings():
    #database url leri
    AUTH_MONGODB_URL = os.getenv("AUTH_MONGODB_URL")

    #redis url si ve portu
    REDIS_PORT = os.getenv("REDIS_PORT" , 6379)
    REDIS_HOST = os.getenv("REDIS_HOST" , "localhost")


settings = Settings()
