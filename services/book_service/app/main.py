from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Service is running, but logic is empty yet."}