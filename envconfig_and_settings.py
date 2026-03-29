from dotenv import load_dotenv
import os

#çevresel değişkenleri yüklemek için gerekli
load_dotenv()
class Settings():
    # todo önemli yerler çok fazla değişmezse mükemmel olur

    # çevresel değişkenler olarak gelen url ler
    BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL")
    BORROW_SERVICE_URL = os.getenv("BORROW_SERVICE_URL")
    AUTH_SERCICE_URL = os.getenv("AUTH_SERVICE_URL")

    # dispatcher deki yetki korumalı endpointler
    PROTECTED_ENDPOINTS = ["/books", "/borrow"]

    # tüm servislerin listesi
    ALL_SERVICES = [BOOK_SERVICE_URL , BORROW_SERVICE_URL]

    # key olarak endpoint değer olarak url alan servis listesi
    SERVICES = {
        "/books": BOOK_SERVICE_URL ,
        "/borrow": BORROW_SERVICE_URL,
    }