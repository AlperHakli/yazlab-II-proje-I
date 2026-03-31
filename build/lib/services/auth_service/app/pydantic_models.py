from pydantic import BaseModel , Field

class LoginRequest(BaseModel):
    username: str = Field(description="Kullanıcı ismi")
    password: str = Field(description="Şifre")


class SignUpRequest(BaseModel):
    username: str = Field(description="Kullanıcı ismi")
    password: str = Field(description="Şifre")
    fullname: str = Field(description="Kullanıcı tam ismi")
