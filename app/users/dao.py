from app.dao.base_dao import BaseDAO
from app.users.models import User


class UsersDAO(BaseDAO):
    model = User
