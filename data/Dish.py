import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Dish(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'dishes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photo = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    short_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    full_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    cart = orm.relation("Cart", back_populates='dish')


    def __repr__(self):
        return f'<Dish> {self.id} {self.name}\n {self.short_description}'
