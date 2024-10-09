from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class Newspaper(BaseModel):
    id: int
    name: constr(max_length=255)
    email: EmailStr

    class Config:
        orm_mode = True
