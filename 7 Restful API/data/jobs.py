from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
import sqlalchemy, datetime


class Job(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    job = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    leader = sqlalchemy.orm.relationship('User')
