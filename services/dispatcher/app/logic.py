from typing import Optional
from fastapi import Header, HTTPException, status
from services.dispatcher import config
from services.dispatcher.app.redis_client import redis_manager
from jwt import encode , decode
from datetime import datetime , timedelta
from zoneinfo import ZoneInfo
from services.dispatcher.config import settings


def get_service_url(service_name: str):
    def _returner():
        return config.settings.SERVICES.get(service_name)

    return _returner


async def verify_token(token: Optional[str] = Header(None)):
    """
    Redis üzerinden token kontrolü yapan ana fonksiyon
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yetkisiz erişim: Token bulunamadı"
        )
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token içinde kullanıcı bilgisi yok")

        is_active = await redis_manager.checkToken(token)

        if not is_active:
            raise HTTPException(status_code=401, detail="Oturum sonlanmış")


        # id döndürülür
        return {"id": user_id, "role": "user"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token correction error: {str(e)}")




