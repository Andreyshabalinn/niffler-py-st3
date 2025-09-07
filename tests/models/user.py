from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date


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


class Friendship(SQLModel, table=True):
    requester_id: str = Field(primary_key=True, foreign_key="user.id")
    addressee_id: str = Field(primary_key=True, foreign_key="user.id")
    status: str
    created_date: date