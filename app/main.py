from fastapi import FastAPI, HTTPException
from app.api.routes import router
import time

#БД
from contextlib import asynccontextmanager
from .database import create_db_and_tables, engine
from . import models
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
    except Exception as e:
        raise Exception(f"Не удалось создать таблицы {e}")
    
    yield
    engine.dispose()  #Закрываем соединения с БД



app = FastAPI(
    title="MarketPlace by Procrastination",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Service is running"}

@app.get("/health")
def health_check():
    try:
        engine.connect().execute(text("SELECT 1"))
        return {"db": "ok"}
    except Exception as e:
        raise HTTPException(503, f"DB error: {e}")