import httpx
import pytest_asyncio
from httpx import AsyncClient

from main import app


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        yield ac
