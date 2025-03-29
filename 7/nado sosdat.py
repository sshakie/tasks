from data.db_session import *
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


global_init('db/mars_explorer.db')
db_sess = create_session()
db_sess = db_sess.query(User).all()

print([i for i in db_sess if i.id == 1])