import pytest
from app.models.adidas_model import Brands
from httpx import AsyncClient


async def test_brands(client_test: AsyncClient):
    response = await client_test.get("/api/v1/brands/")
    assert response.status_code == 200
    msg = response.json()
    assert isinstance(msg, list)
