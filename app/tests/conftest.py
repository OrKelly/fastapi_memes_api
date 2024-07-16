import asyncio
import json
from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.core.config import settings
from app.core.db import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.memes.models import Meme
from app.users.models import User


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'app/tests/mock_{model}.json', encoding='UTF-8') as file:
            return json.load(file)

    users = open_mock_json('users')
    memes = open_mock_json('memes')
    print(users)
    print(memes)

    async with async_session_maker() as session:
        add_users = insert(User).values(users)
        add_memes = insert(Meme).values(memes)

        await session.execute(add_users)
        await session.execute(add_memes)

        await session.commit()


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        await ac.post('api/v1/auth/login', json={
            'login': 'test',
            'password': 'string'
        })
        assert ac.cookies["meme_access_token"]
        yield ac


@pytest.fixture(scope='function')
async def session():
    async with async_session_maker() as session:
        yield session
