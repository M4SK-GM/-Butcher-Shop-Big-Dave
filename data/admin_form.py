from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class Add_Dish_Form(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    short_description = StringField('Краткое описание', validators=[DataRequired()])
    full_description = StringField('Полное описание', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    photo = StringField('Фото')
    submit = SubmitField('Подтвердить')


class Add_Services(FlaskForm):
    name = StringField('Услуга', validators=[DataRequired()])
    short_description = StringField('Краткое описание', validators=[DataRequired()])
    full_description = StringField('Полное описание', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    photo = StringField('Фото')
    submit = SubmitField('Подтвердить')
