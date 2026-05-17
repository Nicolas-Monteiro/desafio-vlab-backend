import os

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

API_KEY_NAME = "X-API-Key"

SECRET_API_KEY = os.getenv("API_KEY", "vlab-token-secreto-2026")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def validar_api_key(api_key: str = Security(api_key_header)):
    if api_key == SECRET_API_KEY:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acesso negado. API Key inválida ou ausente.",
    )
