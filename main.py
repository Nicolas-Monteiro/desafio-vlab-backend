from fastapi import FastAPI
from app.routers import abastecimento

app = FastAPI(
    title="Gateway V-Lab - Abastecimentos",
    description="API de Entrada para o Data Lake de transportes.",
    version="1.0.0",
)

app.include_router(abastecimento.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "versao": "1.0.0"}