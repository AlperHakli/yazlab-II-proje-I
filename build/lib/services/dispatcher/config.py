from dotenv import load_dotenv
import os

#çevresel değişkenleri yüklemek için gerekli
load_dotenv()


class Settings():
    # todo önemli yerler çok fazla değişmezse mükemmel olur

    # çevresel değişkenler olarak gelen url ler
    #service url leri
    BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL")
    BORROW_SERVICE_URL = os.getenv("BORROW_SERVICE_URL")
    AUTH_SERCICE_URL = os.getenv("AUTH_SERVICE_URL")

    # dispatcher deki yetki korumalı endpointler
    PROTECTED_ENDPOINTS = ["/books", "/borrow"]

    # key olarak endpoint değer olarak url alan servis listesi
    SERVICES = {
        "/books": BOOK_SERVICE_URL,
        "/borrow": BORROW_SERVICE_URL,
        "/auth": AUTH_SERCICE_URL,
    }

    #redis url si ve portu
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDIS_HOST = os.getenv("redis_host", "localhost")


settings = Settings()
