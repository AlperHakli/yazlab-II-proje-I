from services.book_service.app.models import BorrowOrBringBook , AllBooks , AddBook , DeleteBook
from fastapi import status , HTTPException , Response
import uuid

async def decreasebookcount(request: BorrowOrBringBook):
    try:
        book = await AllBooks.find_one(
            AllBooks.book_id == request.bookID,
            AllBooks.book_name == request.bookName,
            AllBooks.quantity>0
        ).update({"$inc": {AllBooks.quantity: -1}})

        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no available book with specified book name")

        return {
            "userID": request.userID,
            "userName": request.userName,
            "book_taken": request.bookName,
            "detail": "specified user took a book"
        }
    except HTTPException: raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f"Warning critical error on takeabook {e}")



async def increasebookcount(request: BorrowOrBringBook):
    try:
        book = await AllBooks.find_one(
            AllBooks.book_name == request.bookName,
            AllBooks.book_id == request.bookID

        ).update({"$inc": {AllBooks.quantity: 1}})

        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no book with specified book name")


        return {
            "userID": request.userID,
            "userName": request.userName,
            "book_bring": request.bookName,
            "detail": "specified user bring back a book"
        }

    except HTTPException: raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f"Warning critical error on bringabook {e}")


async def addbook(request: AddBook , fastapiresponse: Response):
    try:
        currentbook = await AllBooks.find_one(
            AllBooks.book_name == request.bookName,
            AllBooks.book_id == request.bookID

        )

        if currentbook:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="There is a book with specified book name")

        bookID = str(uuid.uuid4())

        new_book = AllBooks(
            book_id=bookID,
            book_name=request.bookName,
            author=request.author,
            quantity=request.quantity)

        await new_book.insert()
        fastapiresponse.status_code = status.HTTP_201_CREATED

        return {
            "book id": bookID,
            "book name": request.bookName,
            "detail": "New book added"
        }

    except HTTPException: raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Warning critical error on addbook {e}")


async def deletebook(request: DeleteBook):
    try:
        bookexists = await AllBooks.find_one(AllBooks.book_name == request.bookName,
                                             AllBooks.book_id == request.bookID)

        if not bookexists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="There is no book exists with specified book name")

        await bookexists.delete()

        return {
            "book id": request.bookID,
            "book name": request.bookName,
            "detail": "Book has been deleted"
        }

    except HTTPException: raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Warning critical error on deletebook {e}")




