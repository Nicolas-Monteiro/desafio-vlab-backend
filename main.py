from fastapi import FastAPI

app = FastAPI(
    title="Gateway V-Lab - Abastecimentos",
    description="API de Entrada para o Data Lake de transportes.",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok", "versao": "1.0.0"}