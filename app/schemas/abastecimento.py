from pydantic import BaseModel, ConfigDict, Field, field_validator
from enum import Enum
from datetime import datetime
import re

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
    
    @field_validator('cpf_motorista')
    @classmethod
    def validar_cpf_matematico(cls, v: str) -> str:
        cpf = re.sub(r'\D', '', v)

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            raise ValueError('CPF inválido')

        for i in range(9, 11):
            soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
            digito = ((soma * 10) % 11) % 10
            if digito != int(cpf[i]):
                raise ValueError('CPF inválido')

        return cpf
    

class AbastecimentoResponse(BaseModel):
    id: int
    id_posto: int
    data_hora: datetime 
    tipo_combustivel: TipoCombustivel  
    preco_por_litro: float
    volume_abastecido: float
    cpf_motorista: str
    dado_improprio: bool

model_config = ConfigDict(from_attributes=True)