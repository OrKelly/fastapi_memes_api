from fastapi import status

from app.base_exceptions import BaseMemeException, BaseUnauthorizedExceptions


class UserAlreadyExistsException(BaseMemeException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь уже существует'


class IncorrectLoginOrPasswordException(BaseUnauthorizedExceptions):
    detail = 'Неверный логин или пароль'


class ExpiredTokenException(BaseUnauthorizedExceptions):
    detail = 'Токен истек'


class TokenAbsentException(BaseUnauthorizedExceptions):
    detail = 'Токен отсутствует'


class IncorrectTokenFormatException(BaseUnauthorizedExceptions):
    detail = 'Неккоректный формат токена'


class UserIsNotPresentException(BaseUnauthorizedExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Пользователь не найден/отсутствует'
