import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Services(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'services'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photo = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    short_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    full_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    cart = orm.relation("Cart", back_populates='services')
    comment = orm.relation("Comment", back_populates='services')

    def __repr__(self):
        return f'<Services> {self.id} {self.name}\n{self.short_description}\n{self.price}'
