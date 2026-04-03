from beanie import Document
from pydantic import Field , BaseModel


class AllBooks(Document):
    book_id: str = Field(json_schema_extra={"unique":True}, description="kitap id si")
    book_name: str
    author: str
    quantity: int = Field(description="number of available books")

    class Setting:
        name="all_books"


class BorrowOrBringBook(BaseModel):
    userID: str
    bookID: str
    userName:str
    bookName:str

class AddBook(BaseModel):
    bookID: str
    bookName: str = Field(description="Name of book")
    author: str
    quantity: int = Field(default=0 , description="number of books")


class DeleteBook(BaseModel):
    bookID: str
    bookName: str






