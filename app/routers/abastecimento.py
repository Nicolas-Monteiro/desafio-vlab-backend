from fastapi import APIRouter
from app.schemas.abastecimento import AbastecimentoCreate

router = APIRouter(
    prefix="/api/v1/abastecimentos",
    tags=["Abastecimentos"]
)

@router.post("/", status_code=201)
def receber_abastecimento(payload: AbastecimentoCreate):

    dados_recebidos = payload.model_dump()
    
    print("Sucesso! Os dados que passaram pela validação foram:")
    print(dados_recebidos)

    return {
        "mensagem": "Abastecimento validado com sucesso (ainda não salvo)",
        "dados": dados_recebidos
    }