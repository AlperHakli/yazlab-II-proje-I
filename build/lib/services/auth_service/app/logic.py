from services.auth_service.app.pydantic_models import LoginRequest
from fastapi import HTTPException , status
from services.auth_service.app.redis_client import redis_manager
import uuid
async def login_logic(request: LoginRequest):
    """
    Giriş yapma kısmının arkaplan kodu
    :param request: gelen veri (username ve şifre)
    """

    if request.username == "admin"  and request.password == "admin123":

        access_token = str(uuid.uuid4())

        await redis_manager.setToken(access_token , user_id="1")


        return {
            "access_token": access_token,  # Şimdilik statik
            "token_type": "bearer"
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre geçersiz"
        )

async def signup_logic(request: LoginRequest):
    """
    Veritabanına yeni bir kullanıcı eklenir
    """