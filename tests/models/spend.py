from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Category(SQLModel, table=True):
    __tablename__ = "category"
    id: UUID = Field(primary_key=True)
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
