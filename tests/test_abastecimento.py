import pytest
from pydantic import ValidationError

from app.schemas.abastecimento import AbastecimentoCreate

CPF_VALIDO = "12345678907"


@pytest.mark.asyncio
async def test_criar_abastecimento_cpf_invalido_matematicamente(client):
    payload = {
        "id_posto": 1,
        "data_hora": "2026-05-16T22:00:00",
        "tipo_combustivel": "GASOLINA",
        "preco_por_litro": 5.89,
        "volume_abastecido": 40.0,
        "cpf_motorista": "12345678911",
    }
    headers = {"X-API-Key": "vlab-token-secreto-2026"}
    response = await client.post(
        "/api/v1/abastecimentos/", json=payload, headers=headers
    )

    assert response.status_code == 422
    assert "CPF inválido" in response.text


@pytest.mark.asyncio
async def test_criar_abastecimento_cpf_sequencia_repetida(client):
    payload = {
        "id_posto": 1,
        "data_hora": "2026-05-16T22:00:00",
        "tipo_combustivel": "ETANOL",
        "preco_por_litro": 4.19,
        "volume_abastecido": 20.0,
        "cpf_motorista": "11111111111",
    }
    headers = {"X-API-Key": "vlab-token-secreto-2026"}
    response = await client.post(
        "/api/v1/abastecimentos/", json=payload, headers=headers
    )

    assert response.status_code == 422
    assert "CPF inválido" in response.text


@pytest.mark.asyncio
async def test_criar_abastecimento_valores_negativos(client):
    payload = {
        "id_posto": 1,
        "data_hora": "2026-05-16T22:00:00",
        "tipo_combustivel": "DIESEL",
        "preco_por_litro": -1.0,
        "volume_abastecido": 0.0,
        "cpf_motorista": CPF_VALIDO,
    }
    headers = {"X-API-Key": "vlab-token-secreto-2026"}
    response = await client.post(
        "/api/v1/abastecimentos/", json=payload, headers=headers
    )

    assert response.status_code == 422


def test_schema_aceita_cpf_formatado_e_limpa_caracteres():
    schema = AbastecimentoCreate(
        id_posto=1,
        data_hora="2026-05-16T22:00:00",
        tipo_combustivel="GASOLINA",
        preco_por_litro=5.50,
        volume_abastecido=10.0,
        cpf_motorista="123.456.789-09",
    )
    assert schema.cpf_motorista == "12345678909"


def test_schema_rejeita_cpf_com_tamanho_errado():
    with pytest.raises(ValidationError):
        AbastecimentoCreate(
            id_posto=1,
            data_hora="2026-05-16T22:00:00",
            tipo_combustivel="GASOLINA",
            preco_por_litro=5.50,
            volume_abastecido=10.0,
            cpf_motorista="123456",
        )


@pytest.mark.asyncio
async def test_criar_abastecimento_sem_token_falha(client):
    payload = {
        "id_posto": 1,
        "data_hora": "2026-05-16T22:00:00",
        "tipo_combustivel": "GASOLINA",
        "preco_por_litro": 5.89,
        "volume_abastecido": 40.0,
        "cpf_motorista": "12345678909",
    }

    response = await client.post("/api/v1/abastecimentos/", json=payload)

    assert response.status_code == 401
