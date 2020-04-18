import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'comment'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    dish_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("dishes.id"))
    dish = orm.relation('Dish')
    service_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("services.id"))
    services = orm.relation('Services')

    def __repr__(self):
        return f'<Comment> {self.id}'
