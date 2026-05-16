import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.abastecimento import AbastecimentoModel
from app.schemas.abastecimento import AbastecimentoCreate

MEDIAS_PADRAO = {
    "GASOLINA": 5.50,
    "ETANOL": 3.80,
    "DIESEL": 6.00
}

class AbastecimentoService:
    @staticmethod
    async def process_ingestion(payload: AbastecimentoCreate, db: AsyncSession) -> dict:
        redis = aioredis.from_url("redis://cache:6379", decode_responses=True)
        
        try:
            tipo_combustivel = payload.tipo_combustivel.upper()
            chave_cache = f"avg_price:{tipo_combustivel}"
            media_historica = await redis.get(chave_cache)
            
            if media_historica is None:
                media_historica = MEDIAS_PADRAO.get(tipo_combustivel, 5.00)
                await redis.set(chave_cache, media_historica)
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
            await redis.close()