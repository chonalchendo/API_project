import pytest
from app.app import app
from asgi_lifespan import LifespanManager
from httpx import AsyncClient


@pytest.fixture
async def client_test():
    async with LifespanManager(app):
        async with AsyncClient(
            app=app, base_url="http://127.0.0.1:8000", follow_redirects=True
        ) as ac:
            yield ac
