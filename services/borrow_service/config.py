from dotenv import load_dotenv
import os


load_dotenv()

class Settings():

    #veritabanı url si
    BORROW_MONGODB_URL = os.getenv("BORROW_MONGODB_URL")

    #book servisi base url si
    BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL")


settings = Settings()