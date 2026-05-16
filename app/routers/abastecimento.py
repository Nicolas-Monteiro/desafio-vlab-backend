from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.schemas.abastecimento import AbastecimentoCreate
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/api/v1/abastecimentos",
    tags=["Abastecimentos"]
)

@router.post("/", status_code=201)
async def receber_abastecimento(payload: AbastecimentoCreate, db: AsyncSession = Depends(get_db)):
    try:
        dados_recebidos = payload.model_dump()
        
        print("Sucesso! Os dados que passaram pela validação foram:")
        print(dados_recebidos)

        return {
            "mensagem": "Abastecimento validado com sucesso (ainda não salvo)",
            "dados": dados_recebidos
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )