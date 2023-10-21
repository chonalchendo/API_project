import pytest
from app.models.adidas_model import Sports
from httpx import AsyncClient


async def test_sports(client_test: AsyncClient):
    response = await client_test.get("api/v1/sports/")
    assert response.status_code == 200
    msg = response.json()
    assert isinstance(msg, list)
