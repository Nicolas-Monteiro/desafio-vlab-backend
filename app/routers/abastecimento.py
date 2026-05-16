from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.schemas.abastecimento import AbastecimentoCreate
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.abastecimento_service import AbastecimentoService

router = APIRouter(
    prefix="/api/v1/abastecimentos",
    tags=["Abastecimentos"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,)
async def receber_abastecimento(payload: AbastecimentoCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await AbastecimentoService.process_ingestion(payload, db)
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )