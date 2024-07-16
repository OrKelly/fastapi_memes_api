from typing import Generic, List, TypeVar

from pydantic.v1.generics import GenericModel

T = TypeVar("T")


class PagedResponseSchema(GenericModel, Generic[T]):
    """Схема для пагигинированных респонсов"""

    total: int
    page: int
    items_on_page: int
    results: List[T]
