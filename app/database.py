import os
from sqlmodel import create_engine, SQLModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def create_db_and_tables():
    """Создать все таблицы при старте"""
    from sqlmodel import SQLModel
    from app.models.product import Product
    from app.models.category import Category
    from app.models.sku import SKU
    from app.models.invoice import Stock
    from app.models.seller import Seller
    from app.models.sku import CharacteristicValue
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()