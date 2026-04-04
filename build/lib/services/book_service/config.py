from dotenv import load_dotenv
import os

load_dotenv()

class Settings():
    #Veritabanı url si
    BOOK_MONGODB_URL = os.getenv("BOOK_MONGODB_URL")


settings = Settings()

