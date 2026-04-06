from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="MarketPlace by Procrastination",
    version="0.1.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Service is running"}