import httpx

from dispatcher.app.logic import verify_token, forward_request, get_service_url
from dispatcher.app.dispatcher_services import book_service_proxy, borrow_service_proxy
from fastapi import FastAPI, Depends, HTTPException

# app ana dispatcher (proxy de denir)

app = FastAPI()

app.get("/books/{rest_of_path}")


@app.get("/books/{rest_of_path:path}")
async def book_proxy_endpoint(
        rest_of_path: str,
        user: dict = Depends(verify_token),
        base_url: dict = Depends(get_service_url("/books"))
):
    return await (book_service_proxy.forward
                  (base_url,
                   rest_of_path,
                   user))


@app.get("/borrow/{rest_of_path:path}")
async def borrow_proxy_endpoint(
        rest_of_path: str,
        user: dict = Depends(verify_token),
        base_url: dict = Depends(get_service_url("/borrow"))
):
    return await (borrow_service_proxy.forward
                  (base_url,
                   rest_of_path,
                   user))
