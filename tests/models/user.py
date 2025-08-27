from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class UserName(BaseModel):
    username: str


class User(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    username: str
    currency: str = "RUB"
    firstname: str
    surname: str
    currency: str
    photo: str | None = None
    photo_small: str | None = None
    full_name: str