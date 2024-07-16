from fastapi import APIRouter, Response

from app.users.auth import (authenticate_user, create_access_token,
                            get_password_hash)
from app.users.auth.exceptions import (IncorrectLoginOrPasswordException,
                                       UserAlreadyExistsException)
from app.users.dao import UsersDAO
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix='/auth',
    tags=['Auth & Users'],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(login=user_data.login)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(login=user_data.login, password=hashed_password)
    return {'response': 'Вы успешно зарегистрированы'}


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.login, user_data.password)
    if not user:
        raise IncorrectLoginOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('meme_access_token', access_token, httponly=True)
    return {'access_token': access_token}


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('meme_access_token')
