from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base

app = FastAPI(title="Stock Management Assistant - POC")

# Criação de lifespace para criação do banco de dados
# Considerando que é uma POC, o banco de dados será criado na inicialização da aplicação

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}
