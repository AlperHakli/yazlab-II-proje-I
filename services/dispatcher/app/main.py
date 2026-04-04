from contextlib import asynccontextmanager
from services.dispatcher.app.dispatcher_services import DispatcherProxyService
from typing import Optional
from fastapi import (
    FastAPI,
    Depends,
    Request,
    Body
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
async def lifespan(
        app: FastAPI
        ):
    await redis_manager.connect()
    yield
    await redis_manager.close()


app = FastAPI(
    lifespan=lifespan
    )


# books endpointi



async def common_proxy_logic(
        request: Request,
        rest_of_path: str,
        proxy_service,
        base_url: str,
        modified_body: Optional[dict] = None,

):
    """tekrardan kaçınmak için ortak proxy mantığı
    :param request: bilgilerin girildiği ana request objesi içinde isteğin metodu headers gibi ifadeleri var
    :param rest_of_path: mikroservisin içindeki endpointi ifade eder dispatcher e endpoint ismi girilir ve ilgili mikroservisdeki aynı endpoint çalışır
    :param proxy_service: tüm endpointlerin kullandığı ortak servis
    :param base_url: ilgili mikroservisin url si
    :param modified_body: raw body nin içine userID eklenmiş hali (veriler güvenlik için body den gönderilir)

    """


    body_to_send = modified_body if modified_body is not None else await request.body()

    return await proxy_service.forward(
        base_url=base_url,
        rest_of_path=rest_of_path,
        method=request.method,
        body=body_to_send,
        headers=dict(
            request.headers
            ),
    )

# AUTH SERVİSLERİ


@app.post(
    "/auth/{rest_of_path:path}",
    tags=["Auth"]
)
async def auth_post(
    request: Request,
    rest_of_path: str,
    body: Optional[dict] = Body(None),

    base_url: str = Depends(get_service_url("/auth"))
):

    return await common_proxy_logic(
        request=request,
        rest_of_path=rest_of_path,
        proxy_service=auth_service_proxy,
        base_url=base_url,
        modified_body=body
    )


@app.get(
    "/auth/{rest_of_path:path}",
    tags=["Auth"]
)
async def auth_get(
    request: Request,
    rest_of_path: str,
    base_url: str = Depends(get_service_url("/auth"))
):

    return await common_proxy_logic(
        request=request,
        rest_of_path=rest_of_path,
        proxy_service=auth_service_proxy,
        base_url=base_url
    )
 # -------------- BOOK SERVİSLERİ --------------------

@app.get("/books/{rest_of_path:path}", tags=["Books"])
async def get_books(
    request: Request,
    rest_of_path: str,
    user: dict = Depends(verify_token),
    base_url=Depends(get_service_url("/books"))
):
    # Okul projesi için params kalsın dedin, ekliyoruz

    return await common_proxy_logic(
        request=request,
        rest_of_path=rest_of_path,
        proxy_service=book_service_proxy,
        base_url=base_url,
    )
@app.post(
    "/books/{rest_of_path:path}",
    tags=["Books"]
)
async def post_books(
        request: Request,
        rest_of_path: str,
        body: Optional[dict] = Body(
            None
            ),
        user: dict = Depends(
            verify_token
            ),
        base_url=Depends(
            get_service_url(
                "/books"
                )
            )
):

    if body is None: body = {}
    body["userID"] = user["id"]

    return await common_proxy_logic(
        request=request,
        rest_of_path=rest_of_path,
        proxy_service=book_service_proxy,
        base_url=base_url,
        modified_body=body
    )


@app.put(
    "/books/{rest_of_path:path}",
    tags=["Books"]
)
async def put_books(
        request: Request,
        rest_of_path: str,
        body: Optional[dict] = Body(
            None
            ),
        user: dict = Depends(
            verify_token
            ),
        base_url=Depends(
            get_service_url(
                "/books"
                )
            )
):
    if body is None: body = {}
    body["userID"] = user["id"]

    return await common_proxy_logic(
        request=request,
        rest_of_path=rest_of_path,
        proxy_service=book_service_proxy,
        base_url=base_url,
        modified_body=body
    )


@app.patch(
    "/books/{rest_of_path:path}",
    tags=["Books"]
)
async def patch_books(
        request: Request,
        rest_of_path: str,
        body: Optional[dict] = Body(
            None
            ),
        user: dict = Depends(
            verify_token
            ),
        base_url=Depends(
            get_service_url(
                "/books"
                )
            )
):

    if body is None:
        body = {}

    body["userID"] = user["id"]

    return await common_proxy_logic(
        request=request,
        rest_of_path=rest_of_path,
        proxy_service=book_service_proxy,
        base_url=base_url,
        modified_body=body
    )


@app.delete(
    "/books/{rest_of_path:path}",
    tags=["Books"]
)
async def delete_books(
        request: Request,
        rest_of_path: str,
        body: Optional[dict] = Body(
            None
            ),
        user: dict = Depends(
            verify_token
            ),
        base_url=Depends(
            get_service_url(
                "/books"
                )
            )
):
    if body is None:
        body = {}

    body["userID"] = user["id"]

    return await common_proxy_logic(
        request=request,
        rest_of_path=rest_of_path,
        proxy_service=book_service_proxy,
        base_url=base_url,
        modified_body=body
    )





# --------- BORROW SERVİSLERİ -------------

@app.post(
    "/borrow/{rest_of_path:path}",
    tags=["Borrow"]
)
async def post_borrow(
        request: Request,
        rest_of_path: str,
        body: Optional[dict] = Body(
            None
            ),
        user: dict = Depends(
            verify_token
            ),
        base_url=Depends(
            get_service_url(
                "/borrow"
                )
            )
):
    if body is None: body = {}
    body["userID"] = user["id"]

    return await common_proxy_logic(
        request=request,
        rest_of_path=rest_of_path,
        proxy_service=borrow_service_proxy,
        base_url=base_url,
        modified_body=body
    )


@app.put(
    "/borrow/{rest_of_path:path}",
    tags=["Borrow"]
)
async def put_borrow(
        request: Request,
        rest_of_path: str,
        body: Optional[dict] = Body(
            None
            ),
        user: dict = Depends(
            verify_token
            ),
        base_url=Depends(
            get_service_url(
                "/borrow"
                )
            )
):
    if body is None: body = {}
    body["userID"] = user["id"]

    return await common_proxy_logic(
        request=request,
        rest_of_path=rest_of_path,
        proxy_service=borrow_service_proxy,
        base_url=base_url,
        modified_body=body
    )


@app.get(
    "/borrow/{rest_of_path:path}",
    tags=["Borrow"]
)
async def get_borrow(
        request: Request,
        rest_of_path: str,
        user: dict = Depends(
            verify_token
            ),
        base_url=Depends(
            get_service_url(
                "/borrow"
                )
            )
):
    query_params = {"user_id": user["id"]}
    return await common_proxy_logic(
        request=request,
        rest_of_path=rest_of_path,
        proxy_service=borrow_service_proxy,
        base_url=base_url,
    )


@app.delete(
    "/borrow/{rest_of_path:path}",
    tags=["Borrow"]
)
async def delete_borrow(
        request: Request,
        rest_of_path: str,
        body: Optional[dict] = Body(
            None
            ),
        user: dict = Depends(
            verify_token
            ),
        base_url=Depends(
            get_service_url(
                "/borrow"
                )
            )
):

    if body is None:
        body = {}

    body["userID"] = user["id"]

    return await common_proxy_logic(
        request=request,
        rest_of_path=rest_of_path,
        proxy_service=borrow_service_proxy,
        base_url=base_url,
        modified_body=body
    )
