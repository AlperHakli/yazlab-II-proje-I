PROTECTED_ENDPOINTS = ["/books", "/borrow"]
BOOK_SERVICE_URL = "http://book-service:8001/api/v1"
BORROW_SERVICE_URL = "http://borrow-service:8000/api/v1"
ALL_SERVICES = [BOOK_SERVICE_URL , BORROW_SERVICE_URL]
ENDPOINTS_AND_URLS = [
    ("/books", "http://book-service:8001/api/v1"),
    ("/borrow", "http://borrow-service:8000/api/v1")
]

