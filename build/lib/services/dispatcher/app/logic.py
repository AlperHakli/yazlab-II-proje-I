from typing import Optional
import envconfig_and_settings
import httpx
from fastapi import Header, Depends, HTTPException, status
import envconfig_and_settings
from services.dispatcher.app.redis_client import redis_manager

#auth katmanı


def get_service_url(service_name: str):
    def _returner():
        return envconfig_and_settings.Settings.SERVICES.get(service_name)

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

    # GERÇEK REDIS KONTROLÜ
    user_id = await redis_manager.getUserID(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yetkisiz erişim: Geçersiz veya süresi dolmuş token"
        )

    # Burası önemli: ID'yi dönüyoruz ki Dispatcher bunu kullanabilsin
    return {"id": user_id, "role": "admin"}  # Role bilgisini de ileride Redis'e ekleyebilirsin


