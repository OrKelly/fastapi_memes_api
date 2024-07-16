from app.dao.base_dao import BaseDAO
from app.memes.models import Meme


class MemeDAO(BaseDAO):
    model = Meme
