from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class WriteForm(FlaskForm):
    text = TextAreaField("Введите сообщение", validators=[DataRequired()])
    submit = SubmitField('Отправить')
