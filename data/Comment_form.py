from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comment = StringField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
