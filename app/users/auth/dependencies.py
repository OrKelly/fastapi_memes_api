from datetime import datetime

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.core.config import settings
from app.users.dao import UsersDAO

from .exceptions import (ExpiredTokenException, IncorrectTokenFormatException,
                         TokenAbsentException, UserIsNotPresentException)


def get_token(request: Request):
    token = request.cookies.get('meme_access_token')
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORYTHM)
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get('exp')
    if not (expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise ExpiredTokenException
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user
