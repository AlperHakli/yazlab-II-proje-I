from fastapi import status , HTTPException , Response
import httpx
from services.borrow_service.config import settings
from services.borrow_service.app.models import BorrowBook , AllBorrows , BringBook
import uuid
async def borrowbook(request: BorrowBook , fastapiresponse: Response):
    try:
        full_url = f"{settings.BOOK_SERVICE_URL}/borrow_book"

        async with httpx.AsyncClient() as client:
            response = await client.patch(
                full_url,
                json={
                    "userID": request.userID,
                    "bookID": request.bookID,
                    "userName": request.userName,
                    "bookName": request.bookName
                })

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code , detail="An error occur in borrowbook")


        borrowID = str(uuid.uuid4())

        newborrow = AllBorrows(

            borrowID=borrowID,
            userID=request.userID,
            bookID=request.bookID,
            userName=request.userName,
            bookName=request.bookName

        )

        await newborrow.insert()

        fastapiresponse.status_code = status.HTTP_201_CREATED


        return {
            "userID": request.userID,
            "bookID": request.bookID,
            "userName": request.userName,
            "bookName": request.bookName,
            "endsat": request.end,
            "detail": "User successfully borrow specified book"

        }
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Book Service is not available")
    except HTTPException: raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f"Warning critical error on borrowbook {e}")


async def bringbook(request: BringBook):
    try:
        full_url = f"{settings.BOOK_SERVICE_URL}/bring_book"


        async with httpx.AsyncClient() as client:
            response = await client.patch(
                full_url,
                json={
                    "userID": request.userID,
                    "bookID": request.bookID,
                    "userName": request.userName,
                    "bookName": request.bookName
                })

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code , detail="An error occur in bringbook")

        deleted_book = await AllBorrows.find_one(AllBorrows.borrowID == request.borrowID)

        if not deleted_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="There is no borrowed books that would bring back on bringbook")
        await deleted_book.delete()

        return {
            "userID": request.userID,
            "userName": request.userName,
            "bookName": request.bookName,
            "detail": "User successfully bring back specified book"

        }
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Book Service is not available")
    except HTTPException:
        raise
    except Exception as e:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Warning critical error on bringbook {e}")


async def getallborrows(user_id: str):
    try:
        all_borrows = AllBorrows.find_all(AllBorrows.userID == user_id)
        borrow_list = await all_borrows.to_list()
        if len(borrow_list)<=0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User with specified user id doesn't exist or doesn't borrowed a book")


        return {
            "data":borrow_list,
            "status":"all borrows successfully fetched"
        }
    except HTTPException: raise

    except Exception as e:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Warning critical error on getallborrows {e}")













