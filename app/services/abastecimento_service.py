from datetime import date
import json
import os
from typing import Optional

from sqlalchemy import Date, cast, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.abastecimento import AbastecimentoModel
from app.schemas.abastecimento import AbastecimentoCreate, TipoCombustivel
import redis.asyncio as aioredis
MEDIAS_PADRAO = {
    "GASOLINA": 5.50,
    "ETANOL": 3.80,
    "DIESEL": 6.00
}
REDIS_URL = os.getenv("REDIS_URL", "redis://cache:6379")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

class AbastecimentoService:
    @staticmethod
    async def process_ingestion(payload: AbastecimentoCreate, db: AsyncSession) -> dict:

        
        try:
            tipo_combustivel = payload.tipo_combustivel.upper()
            chave_cache = f"avg_price:{tipo_combustivel}"
            media_historica = await redis_client.get(chave_cache)
            
            if media_historica is None:
                media_historica = MEDIAS_PADRAO.get(tipo_combustivel, 5.00)
                await redis_client.set(chave_cache, media_historica)
            else:
                media_historica = float(media_historica)

            limite = media_historica * 1.25
            e_anomalia = payload.preco_por_litro > limite

            data_hora_limpa = payload.data_hora.replace(tzinfo=None)

            db_abastecimento = AbastecimentoModel(
                id_posto=payload.id_posto,
                data_hora=data_hora_limpa,
                tipo_combustivel=tipo_combustivel,
                preco_por_litro=payload.preco_por_litro,
                volume_abastecido=payload.volume_abastecido,
                cpf_motorista=payload.cpf_motorista,
                dado_improprio=e_anomalia  
            )

            db.add(db_abastecimento)
            await db.flush()
            await db.commit()
            await db.refresh(db_abastecimento)

            return {
                "status": "success",
                "data": {
                    "id": db_abastecimento.id,
                    "improper_data": db_abastecimento.dado_improprio,
                    "historical_average_used": media_historica
                }
            }
            
        finally:
            await redis_client.close()
    
    @staticmethod
    async def listar_com_filtros(
        db: AsyncSession,
        page: int,
        size: int,
        tipo_combustivel: Optional[TipoCombustivel],
        data_filtro: Optional[date]
    ) -> list[dict]:

        cache_key = f"abastecimentos:page:{page}:size:{size}:tipo:{tipo_combustivel}:data:{data_filtro}"
        
        try:
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Erro Redis (Leitura): {e}")

        query = select(AbastecimentoModel).order_by(AbastecimentoModel.data_hora.desc())
        
        if tipo_combustivel:
            query = query.where(AbastecimentoModel.tipo_combustivel == tipo_combustivel)
            
        if data_filtro:

            query = query.where(cast(AbastecimentoModel.data_hora, Date) == data_filtro)

        offset = (page - 1) * size
        query = query.offset(offset).limit(size)
        
        result = await db.execute(query)
        abastecimentos = result.scalars().all()

        serialized_data = [
            {
                "id": a.id,
                "id_posto": a.id_posto,
                "data_hora": a.data_hora.isoformat(),
                "tipo_combustivel": a.tipo_combustivel,
                "preco_por_litro": float(a.preco_por_litro),
                "volume_abastecido": float(a.volume_abastecido),
                "cpf_motorista": a.cpf_motorista,
                "dado_improprio": a.dado_improprio
            }
            for a in abastecimentos
        ]

        try:
            await redis_client.setex(cache_key, 60, json.dumps(serialized_data))
        except Exception as e:
            print(f"Erro Redis (Escrita): {e}")

        return serialized_data

    @staticmethod
    async def buscar_por_motorista(db: AsyncSession, cpf: str) -> list[dict]:
        cpf_limpo = "".join(filter(str.isdigit, cpf))
        
        cache_key = f"motorista:{cpf_limpo}:historico"
        
        try:
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Erro Redis (Motorista): {e}")

        query = select(AbastecimentoModel).where(AbastecimentoModel.cpf_motorista == cpf_limpo).order_by(AbastecimentoModel.data_hora.desc())
        result = await db.execute(query)
        abastecimentos = result.scalars().all()

        serialized_data = [
            {
                "id": a.id,
                "id_posto": a.id_posto,
                "data_hora": a.data_hora.isoformat(),
                "tipo_combustivel": a.tipo_combustivel,
                "preco_por_litro": float(a.preco_por_litro),
                "volume_abastecido": float(a.volume_abastecido),
                "cpf_motorista": a.cpf_motorista,
                "dado_improprio": a.dado_improprio
            }
            for a in abastecimentos
        ]

        try:
            await redis_client.setex(cache_key, 60, json.dumps(serialized_data))
        except Exception as e:
            print(f"Erro Redis (Escrita Motorista): {e}")

        return serialized_data