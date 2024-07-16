import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('login, password, status_code', [
    ('new_user', 'test', 200),
    ('test_user', 'test', 200),
    ('example', 'string', 409)
])
async def test_users_register(login, password, status_code, ac: AsyncClient):
    response = await ac.post('api/v1/auth/register', json={
        'login': login,
        'password': password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize('login, password, status_code', [
    ('test', 'string', 200),
    ('example', 'string', 200),
    ('test', 'wrong_pass', 401),
    ('wrong_example', 'string', 401),
])
async def test_user_auth(login, password, status_code, ac: AsyncClient):
    response = await ac.post('api/v1/auth/login', json={
        'login': login,
        'password': password
    })

    assert response.status_code == status_code

