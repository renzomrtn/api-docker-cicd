# main.py
from fastapi import FastAPI
from .database import Base, engine
from .routers import items, orders, categories

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce API",
    version="1.0.0",
    description="API for managing an e-commerce platform",
)

app.include_router(items.router)
app.include_router(orders.router)
app.include_router(categories.router)

# root
@app.get("/")
def root():
    return {
        "message": "Welcome to E-commerce API",
        "docs": "/docs",
        "endpoints / print all": {
            "get items": "/items",
            "get orders": " /orders",
            "get categories": "/categories"
        }
    }
