import app.models

from fastapi import FastAPI
from sqlalchemy import text

from app.database.connection import engine
from app.routers.customers import router as customers_router
from app.routers.orders import router as orders_router
from app.routers.products import router as products_router


app = FastAPI(
    title="NovaRetail ERP API",
    description="Source API for the Enterprise Sales Lakehouse project.",
    version="1.0.0",
)


app.include_router(customers_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "NovaRetail ERP API is running",
        "documentation": "/docs",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected",
    }