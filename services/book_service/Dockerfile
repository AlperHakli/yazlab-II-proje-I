
FROM python:3.12-slim

WORKDIR /app


COPY services/book_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 8001

CMD ["uvicorn", "services.book_service.app.main:app", "--host", "0.0.0.0", "--port", "8001"]