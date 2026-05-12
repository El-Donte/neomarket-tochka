from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from sqlalchemy import text
from fastapi.staticfiles import StaticFiles
from .database import create_db_and_tables, engine
from app.api.v1 import auth, sku, products, invoices, upload
from app.core.config import settings
from app.api.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("app/static/uploads", exist_ok=True)
    try:
        await create_db_and_tables()
    except Exception as e:
        raise Exception(f"Не удалось создать таблицы {e}")

    yield
    await engine.dispose()

def get_application() ->FastAPI:


    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:8080", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    @app.get("/", include_in_schema=False)
    async def root():
        return {"message": "Service is running"}
    
    @app.get("/health", include_in_schema=False)
    async def health_check():
        try:
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
            return {"status": "ok", "db": "connected"}
        except Exception as e:
            raise HTTPException(status_code=503, detail=str(e))

    return app

app = get_application()