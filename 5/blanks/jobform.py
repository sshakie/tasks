from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *


class JobForm(FlaskForm):
    team_leader = SelectField('id лидера', validators=[DataRequired()])
    job = StringField('Работа', validators=[DataRequired()])
    work_size = IntegerField('Длительность', validators=[DataRequired()])
    collaborators = SelectMultipleField('Сотрудники', validators=[DataRequired()])
    end_date = DateTimeField('Дедлайн')
    is_finished = BooleanField('Закончена')
    submit = SubmitField('Добавить')
