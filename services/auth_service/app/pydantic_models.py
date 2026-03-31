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
    userID: str = Field(unique= True)
    username: str = Field(unique= True)
    password: str
    full_name: str

    class Settings():
        name ="users"