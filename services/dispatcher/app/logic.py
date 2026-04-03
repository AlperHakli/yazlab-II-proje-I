from typing import Optional
from fastapi import Header, HTTPException, status
from services.dispatcher import config
from services.dispatcher.app.redis_client import redis_manager



def get_service_url(service_name: str):
    def _returner():
        return config.settings.SERVICES.get(service_name)

    return _returner


async def verify_token(authorization: Optional[str] = Header(None)):
    """
    Redis üzerinden token kontrolü yapan ana fonksiyon
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yetkisiz erişim: Token bulunamadı"
        )

    token = authorization.split(" ")[1]

    # gerçek redis kontrolü
    user_id = await redis_manager.getUserID(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yetkisiz erişim: Geçersiz veya süresi dolmuş token"
        )

    #id döndürülür
    return {"id": user_id, "role": "admin"}


