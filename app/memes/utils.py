from app.memes.dao import MemeDAO
from app.memes.exceptions import MemeNotFound, NotMemeAuthorException


async def verify_is_meme_author(user, meme_id):
    """Функция проверяет и верифицирует автора мема"""
    meme = await MemeDAO.find_one_or_none(id=meme_id)
    if not meme:
        raise MemeNotFound
    if not meme.author == user.id:
        raise NotMemeAuthorException
