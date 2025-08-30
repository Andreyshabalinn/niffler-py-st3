from sqlalchemy import create_engine, Engine, event
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from collections.abc import Sequence
from tests.models.user import Friendship, User
from tests.utils.allure_helper import attach_sql


class UsersDb:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        event.listen(self.engine, "before_cursor_execute", attach_sql)

    def get_user(self, username: str) -> Sequence[User]:
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            return session.exec(statement).one()

    def get_friendship(self, user_uuid: str, user_to_uuid: str):
        with Session(self.engine) as session:
            statement = select(Friendship).where(Friendship.requester_id == user_uuid,
                                                 Friendship.addressee_id == user_to_uuid)
            try:
                return session.exec(statement).one()
            except NoResultFound:
                return None