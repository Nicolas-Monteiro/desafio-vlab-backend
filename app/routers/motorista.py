from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.abastecimento import AbastecimentoResponse
from app.services.abastecimento_service import AbastecimentoService

router = APIRouter(prefix="/api/v1/motoristas", tags=["Motoristas"])


@router.get(
    "/{cpf}/historico",
    response_model=list[AbastecimentoResponse],
    status_code=status.HTTP_200_OK,
)
async def historico_motorista(
    cpf: str = Path(..., description="CPF do motorista (com ou sem formatação)"),
    db: AsyncSession = Depends(get_db),
):
    return await AbastecimentoService.buscar_por_motorista(db=db, cpf=cpf)
