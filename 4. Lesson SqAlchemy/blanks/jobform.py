from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SelectMultipleField, DateTimeField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = SelectField('id лидера', coerce=int, validators=[DataRequired()])
    job = StringField('Работа', validators=[DataRequired()])
    work_size = IntegerField('Длительность', validators=[DataRequired()])
    collaborators = SelectMultipleField('Сотрудники', validators=[DataRequired()])
    end_date = DateTimeField('Дедлайн')
    is_finished = BooleanField('Закончена')
    submit = SubmitField('Добавить')
