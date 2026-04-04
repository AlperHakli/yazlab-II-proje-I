from services.auth_service.app.pydantic_models import LoginRequest, SignUpRequest
from fastapi import HTTPException, status
from services.auth_service.app.redis_client import redis_manager
from services.auth_service.app.pydantic_models import UserModel
from services.auth_service.config import settings
from datetime import datetime , timedelta
from zoneinfo import ZoneInfo
from jwt import encode
import uuid



async def create_access_token(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(ZoneInfo("Europe/Istanbul")) + timedelta(hours=1)
    }
    return encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def login_logic(request: LoginRequest):
    """
    Giriş yapma kısmının arkaplan kodu
    :param request: gelen veri (userName ve şifre)
    """
    user = await UserModel.find_one(UserModel.username == request.username, UserModel.password == request.password)

    if user:

        str_user_id = str(user.userID)

        access_token = await create_access_token(user_id=str_user_id)


        await redis_manager.setToken(access_token, user_id=str_user_id)



        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre geçersiz"
        )


async def signup_logic(request: SignUpRequest):
    """
    Veritabanına yeni bir kullanıcı eklenir
    """

    existing_user = await UserModel.find_one(UserModel.username == request.username)

    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Böyle bir kullanıcı mevcuttur")

    user_id = str(uuid.uuid4())

    new_user = UserModel(
        userID= user_id,
        username=request.username,
        password=request.password,
        fullname=request.fullname
    )

    await new_user.insert()

    return {"message": "Kayıt başarılı", "userID": str(new_user.userID)}
