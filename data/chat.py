import sqlalchemy

from .db_session import SqlAlchemyBase


class Chats(SqlAlchemyBase):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_out = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name_to = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    message_to_user = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
