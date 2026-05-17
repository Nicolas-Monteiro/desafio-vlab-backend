from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.abastecimento import (
    AbastecimentoCreate,
    AbastecimentoResponse,
    TipoCombustivel,
)
from app.services.abastecimento_service import AbastecimentoService

router = APIRouter(prefix="/api/v1/abastecimentos", tags=["Abastecimentos"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def receber_abastecimento(
    payload: AbastecimentoCreate, db: AsyncSession = Depends(get_db)
):
    try:
        result = await AbastecimentoService.process_ingestion(payload, db)
        return result

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/", response_model=list[AbastecimentoResponse], status_code=status.HTTP_200_OK
)
async def listar_abastecimentos(
    page: int = Query(1, ge=1, description="Número da página (mínimo 1)"),
    size: int = Query(
        10, ge=1, le=100, description="Quantidade de registros por página"
    ),
    tipo_combustivel: Optional[TipoCombustivel] = Query(
        None, description="Filtrar por tipo de combustível"
    ),
    data: Optional[date] = Query(
        None, description="Filtrar por data específica (AAAA-MM-DD)"
    ),
    db: AsyncSession = Depends(get_db),
):

    return await AbastecimentoService.listar_com_filtros(
        db=db, page=page, size=size, tipo_combustivel=tipo_combustivel, data_filtro=data
    )
