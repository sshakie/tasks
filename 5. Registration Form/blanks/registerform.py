from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Работа', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адрес проживания', validators=[DataRequired()])
    submit = SubmitField('Создать')
