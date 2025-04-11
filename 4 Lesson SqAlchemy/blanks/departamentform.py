from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, EmailField, SubmitField
from wtforms.validators import DataRequired


class DepartamentForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    chief = SelectField('Шеф', coerce=int, validators=[DataRequired()])
    members = SelectMultipleField('Участники', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Добавить')
