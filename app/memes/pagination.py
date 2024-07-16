from fastapi import Query
from pydantic import BaseModel

from app.core.base_schemas import PagedResponseSchema, T


def get_pagination_params(
        page: int = Query(1, gt=0, description='Страница'),
        per_page: int = Query(10, gt=0, description='Элементов на странице'),
):
    return {"page": page, "per_page": per_page}


def paginate(page_params, query, ResponseSchema: BaseModel) -> PagedResponseSchema[T]:
    """Функция делает пагинация для выборки из БД."""
    offset_min = page_params['per_page'] * page_params['page'] - page_params['per_page']
    offset_max = page_params['per_page'] * page_params['page']
    paginated_query = query[offset_min:offset_max]
    results = [ResponseSchema.from_orm(item) for item in paginated_query]
    return PagedResponseSchema(
        total=len(query),
        page=page_params['page'],
        items_on_page=len(paginated_query),
        results=results,
    )
