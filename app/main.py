from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Новый импорт
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.api.v1 import invoices, products, sellers
from .database import create_db_and_tables, engine
from app.api.v1.routes import router as base_router
from app.api.v1 import sku

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    engine.dispose()

app = FastAPI(
    title="MarketPlace by Procrastination",
    version="0.1.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router, include_in_schema=False)
app.include_router(sellers.router, prefix="/api/v1/sellers", include_in_schema=False)
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(sku.router, prefix="/api/v1/skus", tags=["SKU"])
app.include_router(invoices.invoices_router, prefix="/api/v1/invoices", tags=["Invoices"])

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Service is running"}

@app.get("/health", include_in_schema=False)
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))