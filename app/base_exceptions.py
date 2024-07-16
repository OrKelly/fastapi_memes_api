from abc import ABC

from fastapi import HTTPException, status


class BaseMemeException(HTTPException, ABC):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class BaseUnauthorizedExceptions(BaseMemeException):
    status_code = status.HTTP_401_UNAUTHORIZED


class BaseNotFoundExceptions(BaseMemeException):
    status_code = status.HTTP_404_NOT_FOUND


class BaseValidationExceptions(BaseMemeException):
    status_code = status.HTTP_400_BAD_REQUEST


class BaseForbiddenExceptions(BaseMemeException):
    status_code = status.HTTP_403_FORBIDDEN
