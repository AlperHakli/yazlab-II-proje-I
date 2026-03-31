from contextlib import asynccontextmanager
from services.dispatcher.app.redis_client import redis_manager
from services.dispatcher.app.logic import (
    verify_token,
    get_service_url
)

from services.dispatcher.app.dispatcher_services import (
    book_service_proxy,
    borrow_service_proxy ,
    auth_service_proxy
)

from fastapi import (
    FastAPI,
    Depends,
    Request

)




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Uygulama başlarken bağlantıyı kur
    await redis_manager.connect()
    yield
    # Uygulama kapanırken bağlantıyı kes
    await redis_manager.close()

app = FastAPI(lifespan=lifespan)


@app.get("/books/{rest_of_path:path}")
async def book_proxy_endpoint(
        request: Request,
        rest_of_path: str,
        user: dict = Depends(verify_token),
        base_url: dict = Depends(get_service_url("/books")),

):
    #gelen tüm body i okur
    body = await request.body()


    return await book_service_proxy.forward(
        base_url=base_url, # base url
        rest_of_path=rest_of_path,
        method=request.method,
        body=body,
        headers=dict(request.headers),
        user=user
    )



@app.get("/borrow/{rest_of_path:path}")
async def borrow_proxy_endpoint(
        request: Request,
        rest_of_path: str,
        user: dict = Depends(verify_token),
        base_url: dict = Depends(get_service_url("/borrow"))
):
    #gelen tüm body i okur
    body = await request.body()


    return await borrow_service_proxy.forward(
        base_url=base_url, # base url
        rest_of_path=rest_of_path,
        method=request.method,
        body=body,
        headers=dict(request.headers),
        user=user
    )

@app.post("/auth/{rest_of_path:path}")
async def auth_proxy_endpoint(
        request: Request,
        rest_of_path: str,
        user: None = None,
        base_url: dict = Depends(get_service_url("/auth"))
):
    # gelen tüm body i okur
    body = await request.body()

    return await auth_service_proxy.forward(
        base_url=base_url,  # base url
        rest_of_path=rest_of_path,
        method=request.method,
        body=body,
        headers=dict(request.headers),
        user=user
    )
