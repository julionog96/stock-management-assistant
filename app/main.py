from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routes.stock import router as stock_router

app = FastAPI(title="Stock Management Assistant - POC")


# Criação de lifespace para criação do banco de dados
# Considerando que é uma POC, o banco de dados será criado na inicialização 
# da aplicação


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app.include_router(stock_router)


@app.get("/")
def health_check():
    return {"status": "ok"}
