import datetime
import sqlalchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from wtforms import PasswordField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    confirm_email = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    code = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='standard')
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='/static/img/profile/start_profile.png')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    Cart = orm.relation("Cart", back_populates='user')
    comment = orm.relation("Comment", back_populates='user')
    Discount = orm.relation("Discount", back_populates='user')

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.surname} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class ChangeProfile(FlaskForm):
    email = EmailField('Почта')
    password = PasswordField('Старый пароль')
    new_password = PasswordField('Новый пароль')
    name = StringField('Имя')
    surname = StringField('Фамилия')
    submit = SubmitField('Войти')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, old_password, password):
        return check_password_hash(password, old_password)
