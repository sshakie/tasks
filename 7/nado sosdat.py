# from data.db_session import SqlAlchemyBase
# import sqlalchemy
# import datetime
# 
# 
# class Departaments(SqlAlchemyBase):
#     __tablename__ = 'departaments'
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
#     title = sqlalchemy.Column(sqlalchemy.String)
#     chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
#     members = sqlalchemy.Column(sqlalchemy.String)
#     email = sqlalchemy.Column(sqlalchemy.String, unique=True)
#     created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)


global_init(input())
db_sess = create_session()

department = db_sess.query(Departments).filter(Departments.id == 1).first()
a = list(map(int, department.members.split(',')))

for ii in a:
    for i in db_sess.query(User).filter(User.id == ii).all():
        if sum(i.work_size for i in db_sess.query(Jobs).filter(Jobs.collaborators.like(f'%{i.id}%')).all()) > 25:
            print(f'{i.surname} {i.name}')
