from pydantic import BaseModel , Field
from beanie import Document

# Giriş yapma request modeli
class LoginRequest(BaseModel):
    username: str = Field(description="Kullanıcı ismi")
    password: str = Field(description="Şifre")

# Kayıt olma request modeli
class SignUpRequest(BaseModel):
    username: str = Field(description="Kullanıcı ismi")
    password: str = Field(description="Şifre")
    fullname: str = Field(description="Kullanıcı tam ismi")

# Kullanıcıların tutulduğu nosql koleksiyonu
class UserModel(Document):
    userID: str = Field(json_schema_extra={"unique": True})
    username: str = Field(json_schema_extra={"unique": True})
    password: str
    fullname: str

    class Settings:
        name ="users"