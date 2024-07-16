import pytest
from httpx import AsyncClient


async def test_get_all_memes(ac: AsyncClient):
    response = await ac.get('api/v1/memes')

    assert response.status_code == 200


@pytest.mark.parametrize('meme_id, meme_desc, status_code', [
    (1, 'Милый кролик', 200),
    (2, 'Милый котенок', 200),
    (3, '', 404)
])
async def test_get_specified_meme(meme_id: int, meme_desc: str, status_code: int, ac: AsyncClient):
    response = await ac.get(f'api/v1/memes/{meme_id}', params={'meme_id': meme_id})
    print(response.json())
    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()['desc'] == meme_desc


@pytest.mark.parametrize('meme_id, status_code', [
    (1, 200),
    (2, 403)
])
async def test_delete_meme(meme_id:int, status_code: int, authenticated_ac: AsyncClient):
    response = await authenticated_ac.delete(f'api/v1/memes/delete_meme/{meme_id}',
                                             params={'meme_id': meme_id})
    assert response.status_code == status_code
