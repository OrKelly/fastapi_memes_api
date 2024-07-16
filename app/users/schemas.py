from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    login: str
    password: str
