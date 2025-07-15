from datetime import datetime, timezone
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from typing import Optional


class Category(SQLModel, table=True):
    __tablename__ = "category"
    id: str = Field(primary_key=True)
    name: str
    username: str
    archived: bool

    spends: list["Spend"] = Relationship(back_populates="category")


class Spend(SQLModel, table=True):
    __tablename__ = "spend"
    id: str = Field(primary_key=True)
    spend_date: datetime
    currency: str
    amount: float
    description: str
    username: str
    category_id: str = Field(foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="spends")


class SpendCreate(SQLModel):
    id: str
    spendDate: datetime
    currency: str
    amount: float
    description: str
    username: str
    category: Category

    @field_validator("spendDate")
    @classmethod
    def normalize_spend_date(cls, v: datetime) -> datetime:
        # Приводим к UTC
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        else:
            v = v.astimezone(timezone.utc)

        # Округляем до минут
        return v.replace(second=0, microsecond=0)
