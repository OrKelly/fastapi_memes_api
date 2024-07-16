from app.base_exceptions import BaseForbiddenExceptions, BaseNotFoundExceptions


class MemeNotFound(BaseNotFoundExceptions):
    detail = 'Мем с таким айди не найден'


class NotMemeAuthorException(BaseForbiddenExceptions):
    detail = 'Для изменения/удаления мема нужно быть его автором'
