import traceback

from fastapi import FastAPI
from services.borrow_service.app.database import init_borrow_database
from services.borrow_service.app.logic import borrowbook , bringbook , getallborrows
from services.borrow_service.app.models import BringBook , BorrowBook , UserIDModel
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        #Veritabanını başlatır
        await init_borrow_database()

        yield

        pass

    except Exception as e:
        print("\n" + "=" * 50)
        print("Kritik başlangıç hatası borrow service")
        print(f"Hata Türü: {type(e).__name__}")
        print(f"Hata Mesajı: {str(e)}")
        traceback.print_exc()
        print("=" * 50 + "\n")
        raise e

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Borrow service is running ..."}

@app.post("/borrow_book")
async def borrow_book(request: BorrowBook):
    return await borrowbook(request=request)


@app.post("/bring_back_book")
async def bring_book(request: BringBook):
    return await bringbook(request=request)

@app.get("/all_borrows")
async def get_all_borrows(user_id: str):
    return await getallborrows(user_id=user_id)


