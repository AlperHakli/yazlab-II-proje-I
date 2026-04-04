from contextlib import asynccontextmanager
from typing import Optional
from fastapi import (
    FastAPI,
    Depends,
    Request,
    Body # Body'yi ekledik
)

from services.dispatcher.app.redis_client import redis_manager
from services.dispatcher.app.logic import (
    verify_token,
    get_service_url
)
from services.dispatcher.app.dispatcher_services import (
    book_service_proxy,
    borrow_service_proxy,
    auth_service_proxy
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    yield
    await redis_manager.close()

app = FastAPI(lifespan=lifespan)

# books endpointi

# Dispatcher main.py

async def common_proxy_logic(request: Request, rest_of_path: str, body_content: Optional[dict], user: dict, proxy_service, base_url: str):
    """Tekrardan kaçınmak için ortak proxy mantığı"""
    raw_body = await request.body()
    return await proxy_service.forward(
        base_url=base_url,
        rest_of_path=rest_of_path,
        method=request.method, #request den gelen metod
        body=raw_body,
        headers=dict(request.headers),
        user=user
    )

# Auth servisleri
@app.post("/auth/{rest_of_path:path}", tags=["Auth"])
async def auth_post(request: Request, rest_of_path: str, body: Optional[dict] = Body(None), base_url=Depends(get_service_url("/auth"))):
    return await common_proxy_logic(request, rest_of_path, body, None, auth_service_proxy, base_url)

@app.get("/auth/{rest_of_path:path}", tags=["Auth"])
async def auth_get(request: Request, rest_of_path: str, base_url=Depends(get_service_url("/auth"))):
    return await common_proxy_logic(request, rest_of_path, None, None, auth_service_proxy, base_url)


# Book servisleri
@app.get("/books/{rest_of_path:path}", tags=["Books"])
async def get_books(request: Request, rest_of_path: str, user: dict = Depends(verify_token), base_url=Depends(get_service_url("/books"))):
    return await common_proxy_logic(request, rest_of_path, user, book_service_proxy, base_url)

@app.post("/books/{rest_of_path:path}", tags=["Books"])
async def post_books(request: Request, rest_of_path: str, body: Optional[dict] = Body(None), user: dict = Depends(verify_token), base_url=Depends(get_service_url("/books"))):
    return await common_proxy_logic(request, rest_of_path, user, book_service_proxy, base_url)

@app.put("/books/{rest_of_path:path}", tags=["Books"])
async def put_books(request: Request, rest_of_path: str, body: Optional[dict] = Body(None), user: dict = Depends(verify_token), base_url=Depends(get_service_url("/books"))):
    return await common_proxy_logic(request, rest_of_path, user, book_service_proxy, base_url)

@app.delete("/books/{rest_of_path:path}", tags=["Books"])
async def delete_books(request: Request, rest_of_path: str, user: dict = Depends(verify_token), base_url=Depends(get_service_url("/books"))):
    return await common_proxy_logic(request, rest_of_path, user, book_service_proxy, base_url)

# Borrow servisleri

@app.get("/borrow/{rest_of_path:path}", tags=["Borrow"])
async def get_borrow(request: Request, rest_of_path: str, user: dict = Depends(verify_token), base_url=Depends(get_service_url("/borrow"))):
    return await common_proxy_logic(request, rest_of_path, user, borrow_service_proxy, base_url)

@app.post("/borrow/{rest_of_path:path}", tags=["Borrow"])
async def post_borrow(request: Request, rest_of_path: str, body: Optional[dict] = Body(None), user: dict = Depends(verify_token), base_url=Depends(get_service_url("/borrow"))):
    return await common_proxy_logic(request, rest_of_path, user, borrow_service_proxy, base_url)

@app.put("/borrow/{rest_of_path:path}", tags=["Borrow"])
async def put_borrow(request: Request, rest_of_path: str, body: Optional[dict] = Body(None), user: dict = Depends(verify_token), base_url=Depends(get_service_url("/borrow"))):
    return await common_proxy_logic(request, rest_of_path, user, borrow_service_proxy, base_url)

@app.delete("/borrow/{rest_of_path:path}", tags=["Borrow"])
async def delete_borrow(request: Request, rest_of_path: str, user: dict = Depends(verify_token), base_url=Depends(get_service_url("/borrow"))):
    return await common_proxy_logic(request, rest_of_path, user, borrow_service_proxy, base_url)


