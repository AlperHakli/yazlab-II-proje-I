from beanie import Document
from pydantic import Field , BaseModel
import datetime

class AllBorrows(Document):
    borrowID: str = Field(json_schema_extra={"unique" : False})
    userID: str
    bookID: str
    userName: str
    bookName: str

    class Settings:
        name ="borrows"


class BorrowBook(BaseModel):
    userID: str
    bookID: str
    userName: str
    bookName: str
    end: datetime.datetime

class BringBook(BaseModel):
    userID:str
    bookID:str
    username:str
    bookName:str
    borrowID: str




