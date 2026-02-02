from fastapi import FastAPI

from app.admin import setup_admin
from app.routes.stock import router as stock_router
from app.routes.chat import router as chat_router

app = FastAPI(title="Stock Management Assistant - POC")

setup_admin(app)

app.include_router(stock_router)
app.include_router(chat_router)


@app.get("/")
def health_check():
    return {"status": "ok"}
