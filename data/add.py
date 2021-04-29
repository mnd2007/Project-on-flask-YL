from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    text = TextAreaField("Введите сообщение", validators=[DataRequired()])
    submit = SubmitField('Написать')
