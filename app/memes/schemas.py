from datetime import datetime
from typing import Union

from pydantic import BaseModel


class SMemes(BaseModel):
    id: int
    created_at: datetime
    url: str
    desc: Union[str, None]
    author: int

    class Config:
        orm_mode = True
        from_attributes = True
