from sqlalchemy import create_engine, Engine
from sqlmodel import Session, select
from tests.models.spend import Category, Spend
import allure


class SpendDb:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_categories(self, username: str):
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            allure.attach(
                f"username = {username}",
                name="Query Params",
                attachment_type=allure.attachment_type.TEXT,
            )
            result = session.exec(statement).all()
            allure.attach(
                str(result),
                name="Query Result",
                attachment_type=allure.attachment_type.TEXT,
            )
            return result

    def get_category_by_id(self, category_id):
        with Session(self.engine) as session:
            statement = select(Category).where(Category.id == category_id)
            allure.attach(
                f"category_id = {category_id}",
                name="Query Params",
                attachment_type=allure.attachment_type.TEXT,
            )
            result = session.exec(statement).first()
            allure.attach(
                str(result),
                name="Query Result",
                attachment_type=allure.attachment_type.TEXT,
            )
            return result

    def get_category_by_name(self, category_name):
        with Session(self.engine) as session:
            statement = select(Category).where(Category.name == category_name)
            allure.attach(
                f"category_name = {category_name}",
                name="Query Params",
                attachment_type=allure.attachment_type.TEXT,
            )
            result = session.exec(statement).first()
            allure.attach(
                str(result),
                name="Query Result",
                attachment_type=allure.attachment_type.TEXT,
            )
            return result

    def delete_category(self, category_id: int):
        with Session(self.engine) as session:
            category = session.get(Category, category_id)
            allure.attach(
                f"deleted category_id = {category_id}",
                name="Query Params",
                attachment_type=allure.attachment_type.TEXT,
            )
            session.delete(category)
            session.commit()

    def delete_category_by_name(self, category_name: str):
        with Session(self.engine) as session:
            statement = select(Category).where(Category.name == category_name)
            allure.attach(
                f"deleted category_name = {category_name}",
                name="Query Params",
                attachment_type=allure.attachment_type.TEXT,
            )
            category = session.exec(statement).first()

            if category:
                session.delete(category)
                session.commit()

    def get_spend_by_id(self, spend_id):
        with Session(self.engine) as session:
            statement = select(Spend).where(Spend.id == spend_id)
            allure.attach(
                f"deleted spend_id = {spend_id}",
                name="Query Params",
                attachment_type=allure.attachment_type.TEXT,
            )
            result = session.exec(statement).first()
            allure.attach(
                str(result),
                name="Query Result",
                attachment_type=allure.attachment_type.TEXT,
            )
            return result

    def delete_spend(self):
        with Session(self.engine) as session:
            spend = session.get(Spend, id)
            allure.attach(
                f"deleted spend = {spend}",
                name="Query Params",
                attachment_type=allure.attachment_type.TEXT,
            )
            session.delete(spend)
            session.commit()
