from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class TipoCombustivel(str, Enum):
    GASOLINA = "GASOLINA"
    ETANOL = "ETANOL"
    DIESEL = "DIESEL"

class AbastecimentoCreate(BaseModel):
    id_posto: int
    data_hora: datetime
    tipo_combustivel: TipoCombustivel
    preco_por_litro: float = Field(gt=0, description="Preço não pode ser negativo ou zero")
    volume_abastecido: float = Field(gt=0, description="Volume abastecido em litros")
    cpf_motorista: str = Field(min_length=11, max_length=14, description="CPF do motorista")