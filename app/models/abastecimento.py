from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.database import Base

class AbastecimentoModel(Base):
    __tablename__ = "abastecimentos"

    id = Column(Integer, primary_key=True, index=True)
    id_posto = Column(Integer, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    tipo_combustivel = Column(String, nullable=False)
    preco_por_litro = Column(Float, nullable=False)
    volume_abastecido = Column(Float, nullable=False)
    cpf_motorista = Column(String(14), nullable=False)
    
    dado_improprio = Column(Boolean, default=False)