from services.auth_service.app.pydantic_models import LoginRequest, SignUpRequest
from fastapi import HTTPException, status
from services.auth_service.app.redis_client import redis_manager
from services.auth_service.app.pydantic_models import UserModel
import uuid


async def login_logic(request: LoginRequest):
    """
    Giriş yapma kısmının arkaplan kodu
    :param request: gelen veri (username ve şifre)
    """
    user = await UserModel.find_one(UserModel.username == request.username, UserModel.password == request.password)

    if user:
        access_token = str(uuid.uuid4())

        await redis_manager.setToken(access_token, user_id=user.userID)

        return {
            "access_token": access_token,  # Şimdilik statik
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

    new_user = UserModel(
        username=request.username,
        password=request.password,
        full_name=request.fullname
    )

    await new_user.insert()

    return {"message": "Kayıt başarılı", "user_id": str(new_user.id)}
