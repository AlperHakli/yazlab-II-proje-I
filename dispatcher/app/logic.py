from typing import Optional
import envconfig_and_settings
import httpx
from fastapi import Header , Depends , HTTPException , status
import envconfig_and_settings
#auth katmanı

MOCK_USERS_DB = {
    "gecerli_token_123": {"id": "1", "name": "alper", "role": "admin"},
    "baska_bir_token": {"id": "2", "name": "ayşe", "role": "user"}
}

# Bu fonksiyonu bir kere yazıyorsun
def get_service_url(service_key: str):
    def _returner():
        return envconfig_and_settings.Settings.SERVICES.get(service_key)
    return _returner

async def verify_token(authorization : Optional[str] = Header(None)):
    """
    kullanıcı token kontrolü yapan fonksiyon
    """

    if not authorization or not authorization.startswith("Bearer"):
        #TEST A tetiklenir
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED , detail= "Yetkisiz erişim")

    #örnek token: Bearer abc123
    token = authorization.split(" ")[1]
    #henüz veritabanı yok şuan test olsun diye böyle yaptım mock users db gerçekte postresql den falan gelicek
    user = MOCK_USERS_DB[token]

    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED , detail="Yetkisiz erişim: eksik veya yanlış auth token")

    return user




async def forward_request(target_url:str,user:dict):
    """
    dispatcher in ana fonksiyonu amaç mikroservise yönlendirme(routing) yapmaktır
    :return ilgili mikroservisden gelen üzerine user id de eklenmiş data
    """
    try:
        #burada Dispatcher mikroservis karşısında client gibi davranır yani mikroservise istek atar
        # logic şöyledir
        # USER -> DISPATCHER
        # DISPATCHER (Routing)-> MICROSERVICE
        # MICROSERVICE (Zenginleştirilmiş (id eklenmiş) cevabı yollar) -> DISPATCHER
        # DISPATCHER -> USER
        async with httpx.AsyncClient() as client:
            headers = {"X_User_ID" : str(user["id"])}
            response = await client.get(target_url , headers = headers)

            #Dispatcher in dönen veriye ekstra bir user_id eklemesini sağlar
            data = response.json()
            if isinstance(data , dict):
                data["id"] = user["id"]

            return data
    except HTTPException as e:
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE , detail= f"microservise is unavailable right now detail: {e}")

