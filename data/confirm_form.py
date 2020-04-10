from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class ConfirmForm(FlaskForm):
    code = StringField('Код с почты', validators=[DataRequired()])
    submit = SubmitField('Войти')
