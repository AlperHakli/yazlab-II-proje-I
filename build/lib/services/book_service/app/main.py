import traceback

from fastapi import FastAPI
from services.book_service.app.database import init_book_db
from contextlib import asynccontextmanager
from services.book_service.app.logic import decreasebookcount , increasebookcount , addbook , deletebook
from services.book_service.app.models import BorrowOrBringBook , AddBook , DeleteBook
@asynccontextmanager
async def lifespan(app:FastAPI):

    try:

        #Veritabanını başlatır
        await init_book_db()

        yield

        pass

    except Exception as e:
        print("\n" + "=" * 50)
        print("Kritik başlangıç hatası book service")
        print(f"Hata Türü: {type(e).__name__}")
        print(f"Hata Mesajı: {str(e)}")
        traceback.print_exc()
        print("=" * 50 + "\n")
        raise e




app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Book service is running"}
@app.patch("/borrow_book")
async def borrow_a_book(request: BorrowOrBringBook):
    return await decreasebookcount(request=request)

@app.patch("/bring_book")
async def bring_a_book(request: BorrowOrBringBook):
    return await increasebookcount(request=request)

@app.post("/add_book")
async def add_book(request: AddBook):
    return await addbook(request=request)

@app.delete("/delete_book")
async def delete_book(request: DeleteBook):
    return await deletebook(request=request)





