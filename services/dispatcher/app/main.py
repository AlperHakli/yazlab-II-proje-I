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

@app.api_route("/books/{rest_of_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def book_proxy_endpoint(
        request: Request,
        rest_of_path: str,
        body_content: Optional[dict] = Body(None), # Swagger'da kutucuk açar
        user: dict = Depends(verify_token),
        base_url: str = Depends(get_service_url("/books")),
):
    # Swagger'dan gelen veya gelmeyen tüm body'yi ham (bytes) olarak okur
    raw_body = await request.body()

    return await book_service_proxy.forward(
        base_url=base_url,
        rest_of_path=rest_of_path,
        method=request.method,
        body=raw_body,
        headers=dict(request.headers),
        user=user
    )

# borrow endpointi
@app.api_route("/borrow/{rest_of_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def borrow_proxy_endpoint(
        request: Request,
        rest_of_path: str,
        body_content: Optional[dict] = Body(None), # Swagger'da kutucuk açar
        user: dict = Depends(verify_token),
        base_url: str = Depends(get_service_url("/borrow"))
):
    raw_body = await request.body()

    return await borrow_service_proxy.forward(
        base_url=base_url,
        rest_of_path=rest_of_path,
        method=request.method,
        body=raw_body,
        headers=dict(request.headers),
        user=user
    )

# auth endpointi
@app.api_route("/auth/{rest_of_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_proxy_endpoint(
        request: Request,
        rest_of_path: str,
        body_content: Optional[dict] = Body(None), # Login/Signup bilgilerini buradan girebilirsin
        user: Optional[dict] = None, # Auth için token zorunlu değil
        base_url: str = Depends(get_service_url("/auth"))
):
    raw_body = await request.body()

    return await auth_service_proxy.forward(
        base_url=base_url,
        rest_of_path=rest_of_path,
        method=request.method,
        body=raw_body,
        headers=dict(request.headers),
        user=user
    )